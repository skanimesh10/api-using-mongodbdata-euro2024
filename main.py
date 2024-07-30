import uvicorn
from fastapi import FastAPI, HTTPException
import logging
from config import Settings
from database import database
from bson import ObjectId
from pymongo import ASCENDING

app = FastAPI()
logging.basicConfig(level=logging.INFO)
settings = Settings()


def convert_objectid_to_str(doc):
    """
    Recursively converts ObjectId instances in a document to strings.

    Args:
        doc (Union[dict, list, ObjectId]): The document to convert.

    Returns:
        Union[dict, list, str]: The document with ObjectId instances converted to strings.
    """
    if isinstance(doc, list):
        return [convert_objectid_to_str(item) for item in doc]
    if isinstance(doc, dict):
        return {key: convert_objectid_to_str(value) for key, value in doc.items() if key != "_id"}
    return str(doc) if isinstance(doc, ObjectId) else doc


async def fetch_and_convert(collection_name, query=None, sort=None, limit=1000):
    """
    Fetches documents from a MongoDB collection and converts ObjectId instances to strings.

    Args:
        collection_name (str): The name of the MongoDB collection.
        query (dict, optional): The query to filter documents. Defaults to None.
        sort (list of tuple, optional): The sort order for the documents. Defaults to None.
        limit (int, optional): The maximum number of documents to fetch. Defaults to 1000.

    Returns:
        list: The list of documents with ObjectId instances converted to strings.
    """
    query = query or {}
    cursor = database[collection_name].find(query)
    if sort:
        cursor = cursor.sort(sort)
    items = await cursor.to_list(limit)
    return convert_objectid_to_str(items)


@app.get("/fixtures/")
async def get_fixtures():
    """
    Endpoint to get a list of fixtures.

    Returns:
        list: The list of fixtures with ObjectId instances converted to strings.
    """
    return await fetch_and_convert("euro-24-fixture", sort=[("fixture.id", ASCENDING)])


@app.get("/standings/")
async def get_standings():
    """
    Endpoint to get a list of standings.

    Returns:
        list: The list of standings with ObjectId instances converted to strings.
    """
    return await fetch_and_convert("euro-24-standings")


@app.get("/matches")
async def get_match_by_id(id: int):
    """
    Endpoint to get a match by its fixture ID.

    Args:
        id (int): The fixture ID of the match.

    Returns:
        dict: The match document with ObjectId instances converted to strings.

    Raises:
        HTTPException: If the match with the given fixture ID is not found.
    """
    logging.info(f"Searching for match with fixture.id: {id}")
    item = await database["euro-2024-matches"].find_one({"fixture.id": id})
    if item is None:
        logging.error(f"Match with fixture.id {id} not found")
        raise HTTPException(status_code=404, detail="Match not found")
    logging.info(f"Match found: {item}")
    return convert_objectid_to_str(item)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
