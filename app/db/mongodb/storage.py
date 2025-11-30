import datetime
from typing import Any, Dict
from bson.objectid import ObjectId
from app.core.config import settings
from app.db.mongodb.client import get_mongo_db


COLLECTION_NAME = settings.MONGO_COLLECTION_NAME

async def insert_query_record(document: dict[str, Any]) -> str:
    mongo_db = get_mongo_db()
    if mongo_db is None:
        raise ConnectionError("MongoDB client is not initialized. Check startup event.")
        
    # MongoDB creates the collection implicitly upon the first insertion if it doesn't exist.
    result = await mongo_db[COLLECTION_NAME].insert_one(document)
    
    return str(result.inserted_id)

async def update_query_status_and_score(response_id: str, visibility_score: float) -> None:
    mongo_db = get_mongo_db()
    if mongo_db is None:
        raise ConnectionError("MongoDB client is not initialized. Cannot update record.")

    # Convert the string ID back to a native MongoDB ObjectId for the lookup
    try:
        object_id = ObjectId(response_id)
    except Exception as e:
        print(f"Invalid ObjectId format: {e}")
        return

    update_data = {
        # Update the status, score, and add a processed timestamp inside the nested response_data object
        "$set": {
            "response_data.status": "Complete",
            "response_data.visibility_score": visibility_score,
            "response_data.processed_at": datetime.datetime.now(datetime.timezone.utc),
        }
    }
    
    result = await mongo_db[COLLECTION_NAME].update_one(
        {"_id": object_id},
        update_data
    )
    
    if result.matched_count == 0:
        print(f"Warning: MongoDB record with ID {response_id} not found for update.")

async def get_query_details_by_id(response_id: str) -> Dict[str, Any] | None:
    """
    Feature 5: Retrieves the full query record (including status and score) from MongoDB.
    """
    mongo_db = get_mongo_db()
    if mongo_db is None:
        raise ConnectionError("MongoDB client is not initialized. Cannot fetch record.")

    try:
        object_id = ObjectId(response_id)
    except Exception:
        return None # Return None if ID is invalid

    # Fetch the document by its _id
    document = await mongo_db[COLLECTION_NAME].find_one({"_id": object_id})
    
    if document:
        # Convert ObjectId to string for Pydantic compatibility
        document['response_data']['response_id'] = str(document.pop('_id')) 
        # MongoDB stores the full QueryRecord structure, we extract the response_data
        return document['response_data']
    
    return None