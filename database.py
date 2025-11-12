from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
    mongodb.db = mongodb.client[os.getenv("DB_NAME", "doveable_ai")]
    print("Connected to MongoDB")

async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        print("Closed MongoDB connection")

def get_database():
    return mongodb.db
