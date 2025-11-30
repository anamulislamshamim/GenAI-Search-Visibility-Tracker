from typing import Dict, Any
from db.elasticsearch.client import es_client, ES_INDEX_NAME

# Index mapping defines the schema for documents in Elasticsearch
INDEX_MAPPING: Dict[str, Any] = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "response_id": {"type": "keyword"},
            "brand_keyword": {"type": "keyword"},
            "keywords": {"type": "text"},
            "sentiment_score": {"type": "float"},
            "visibility_score": {"type": "float"},
            "timestamp": {"type": "date"},
            "embedding_vector": {
                "type": "dense_vector",
                # The model 'all-MiniLM-L6-v2' produces a 384-dimensional vector
                "dims": 384, 
                "index": True,
                "similarity": "cosine"
            }
        }
    }
}

async def initialize_es_index():
    """Checks if the index exists and creates it if it doesn't."""
    if es_client is None:
        raise ConnectionError("Elasticsearch client is not initialized.")

    if not await es_client.indices.exists(index=ES_INDEX_NAME):
        await es_client.indices.create(index=ES_INDEX_NAME, body=INDEX_MAPPING)
        print(f"Elasticsearch index '{ES_INDEX_NAME}' created successfully.")
    else:
        print(f"Elasticsearch index '{ES_INDEX_NAME}' already exists.")
    print(f"Elasticsearch index setup simulated for '{ES_INDEX_NAME}'.")


async def index_analysis_document(document: Dict[str, Any]) -> None:
    """Inserts the final analysis document into Elasticsearch."""
    if es_client is None:
        raise ConnectionError("Elasticsearch client is not initialized.")
        
    # We use the response_id as the document ID in Elasticsearch
    doc_id = document.get("response_id")
    if not doc_id:
        raise ValueError("Document must contain a 'response_id' for indexing.")

    await es_client.index(
        index=ES_INDEX_NAME,
        id=doc_id,
        document=document
    )
    print(f"Document with ID {doc_id} successfully indexed in ES.")