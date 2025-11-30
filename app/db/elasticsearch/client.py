from typing import Any, Optional
from elasticsearch import AsyncElasticsearch
from app.core.config import settings

# Configuration
ELASTICSEARCH_DETAILS = settings.ELASTICSEARCH_URL
es_client: Optional[AsyncElasticsearch] = None 
# Global client object
ES_INDEX_NAME = settings.ES_INDEX_NAME
API_KEY = settings.ELASTICSEARCH_API_KEY

async def connect_to_elasticsearch():
    """Initializes and connects to Elasticsearch."""
    global es_client
    print("Attempting to connect to Elasticsearch...")
    try:
        # Placeholder for AsyncElasticsearch initialization
        es_client = AsyncElasticsearch(hosts=[ELASTICSEARCH_DETAILS], api_key=API_KEY)
        if not await es_client.ping():
            raise ConnectionError("Elasticsearch client failed to ping.")
        print("Connected successfully to Elasticsearch!")
    except Exception as e:
        print(f"Could not connect to Elasticsearch: {e}")
        # Reraise the exception to signal a failed startup
        raise

async def close_elasticsearch():
    """Closes the Elasticsearch connection."""
    global es_client
    if es_client:
        # if isinstance(es_client, AsyncElasticsearch):
        #     await es_client.close()
        es_client = None
        print("Elasticsearch connection closed.")

def get_es_client() -> AsyncElasticsearch:
    """
    Safely retrieves the initialized Elasticsearch client.
    This function is used by other modules (like indexing.py)
    to avoid accessing 'None' before the connection is established.
    """
    if es_client is None:
        # This error should only happen if a function tries to use ES before startup is complete
        raise ConnectionError("Elasticsearch client is not initialized. Check application startup sequence.")
    return es_client