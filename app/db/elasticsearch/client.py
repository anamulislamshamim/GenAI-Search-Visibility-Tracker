from typing import Any 
from elasticsearch import AsyncElasticsearch
from app.core.config import settings

# Configuration
ELASTICSEARCH_DETAILS = settings.ELASTICSEARCH_URL

# Global client object
es_client: Any = None 
ES_INDEX_NAME = settings.ES_INDEX_NAME

async def connect_to_elasticsearch():
    """Initializes and connects to Elasticsearch."""
    global es_client
    print("Attempting to connect to Elasticsearch...")
    try:
        # Placeholder for AsyncElasticsearch initialization
        es_client = AsyncElasticsearch(hosts=[ELASTICSEARCH_DETAILS])
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