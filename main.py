from fastapi import FastAPI, HTTPException
import logging
from database import database
from pymongo import ASCENDING

app = FastAPI()
logging.basicConfig(level=logging.INFO)


def convert_objectid_to_str(doc):
    if isinstance(doc, list):
        return [convert_objectid_to_str(item) for item in doc]
    if isinstance(doc, dict):
        return {key: convert_objectid_to_str(value) for key, value in doc.items() if key != "_id"}
    return str(doc) if hasattr(doc, 'binary') else doc


async def fetch_and_convert(collection_name, query=None, sort=None, limit=1000):
    query = query or {}
    cursor = database[collection_name].find(query)
    if sort:
        cursor = cursor.sort(sort)
    items = await cursor.to_list(limit)
    return convert_objectid_to_str(items)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/fixtures/")
async def get_fixtures():
    return await fetch_and_convert("euro-24-fixture", sort=[("fixture.id", ASCENDING)])


@app.get("/standings/")
async def get_standings():
    return await fetch_and_convert("euro-24-standings")


@app.get("/matches")
async def get_match_by_id(id: int):
    logging.info(f"Searching for match with fixture.id: {id}")
    item = await database["euro-2024-matches"].find_one({"fixture.id": id})
    if item is None:
        logging.error(f"Match with fixture.id {id} not found")
        raise HTTPException(status_code=404, detail="Match not found")
    logging.info(f"Match found: {item}")
    return convert_objectid_to_str(item)
