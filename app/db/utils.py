from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.db.mongodb.client import connect_to_mongodb, close_mongodb
from app.db.elasticsearch.client import connect_to_elasticsearch, close_elasticsearch
from app.db.elasticsearch.indexing import initialize_es_index
from app.db.postgres.client import connect_to_postgres, close_postgres
from app.analysis.nlp_pipeline import initialize_nlp_models

async def connect_to_dbs():
    """Initializes and connects to all database clients."""
    # This is the central control point for connecting all databases.
    await connect_to_mongodb()
    await connect_to_postgres()
    await connect_to_elasticsearch()

    await initialize_es_index()
    await initialize_nlp_models()

async def close_dbs():
    """Closes all database connections."""
    # This is the central control point for closing all databases.
    await close_mongodb()
    await close_postgres()
    await close_elasticsearch()