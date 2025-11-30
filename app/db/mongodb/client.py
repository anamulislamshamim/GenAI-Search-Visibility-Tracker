from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Configuration
MONGO_DETAILS = settings.MONGO_URI
DB_NAME = settings.MONGO_DB_NAME

# Global client objects
db_client: AsyncIOMotorClient | None = None
mongo_db = None

async def connect_to_mongodb():
    """Initializes and connects to MongoDB."""
    global db_client, mongo_db
    print("Attempting to connect to MongoDB...")
    try:
        db_client = AsyncIOMotorClient(MONGO_DETAILS)
        # Verify connection by pinging the server
        await db_client.admin.command('ping') 
        mongo_db = db_client[DB_NAME]
        print("Connected successfully to MongoDB!")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        # In a production environment, you might re-raise to halt startup
        raise

async def close_mongodb():
    """Closes the MongoDB connection."""
    global db_client
    if db_client:
        db_client.close()
        print("MongoDB connection closed.")