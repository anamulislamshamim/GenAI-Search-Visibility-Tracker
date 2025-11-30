from typing import Optional
from app.db.mongodb.client import get_mongo_db
from app.auth.models.auth_models import UserInDB
from app.auth.core.utils import hash_password

USER_COLLECTION_NAME = "users"

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Retrieves a user document from MongoDB by email."""
    mongo_db = get_mongo_db()
    if mongo_db is None:
        raise ConnectionError("MongoDB client is not initialized.")
        
    user_data = await mongo_db[USER_COLLECTION_NAME].find_one({"email": email})
    
    if user_data:
        # We need to manually map MongoDB data to UserInDB model
        return UserInDB(
            email=user_data["email"],
            hashed_password=user_data["hashed_password"]
            # Map other fields as necessary
        )
    return None

async def create_user(email: str, password: str) -> Optional[UserInDB]:
    """
    Creates a new user document in MongoDB.
    Returns the created UserInDB object on success, or None if the user already exists.
    """
    mongo_db = get_mongo_db()
    if mongo_db is None:
        raise ConnectionError("MongoDB client is not initialized.")
        
    # Check if user already exists
    if await get_user_by_email(email):
        return None
    
    hashed_password = hash_password(password)
   
    user_document = {
        "email": email,
        "hashed_password": hashed_password
    }
    
    result = await mongo_db[USER_COLLECTION_NAME].insert_one(user_document)
    
    if result.inserted_id:
        print(f"User {email} created successfully.")
        # Return the newly created user object
        return UserInDB(
            email=email,
            hashed_password=hashed_password
        )
    return None