import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Quote the username and password to handle special characters
username = quote_plus(db_user)
password = quote_plus(db_password)

# Construct the MongoDB URI
MONGODB_URI = f"mongodb+srv://{username}:{password}@cluster0.gffqhng.mongodb.net/"

# Create an asynchronous MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)

# Access the specified database
database = client[db_name]
