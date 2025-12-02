from typing import Dict, Any, Optional, List
from app.db.elasticsearch.client import ES_INDEX_NAME, get_es_client
from elasticsearch import AsyncElasticsearch

# Index mapping defines the schema for documents in Elasticsearch
INDEX_MAPPING: Dict[str, Any] = {
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
                "dims": 384,
                "index": True,        # allowed in serverless if vector search is enabled
                "similarity": "cosine"
            }
        }
    }
}

async def initialize_es_index():
    """Checks if the index exists and creates it if it doesn't."""
    es_client = get_es_client()
    if not await es_client.ping():
        raise ConnectionError("Elasticsearch client is not initialized.")

    if not await es_client.indices.exists(index=ES_INDEX_NAME):
        await es_client.indices.create(index=ES_INDEX_NAME, body=INDEX_MAPPING)
        print(f"Elasticsearch index '{ES_INDEX_NAME}' created successfully.")
    else:
        print(f"Elasticsearch index '{ES_INDEX_NAME}' already exists.")
    print(f"Elasticsearch index setup simulated for '{ES_INDEX_NAME}'.")


async def get_visibility_scores(brand_name: str) -> List[Dict[str, Any]]:
    es_client: AsyncElasticsearch = get_es_client()

    query = {
        "query": {
            "match": {
                "keywords": brand_name  # full-text search
            }
        },
        "_source": ["sentiment_score"],
        "size": 1000
    }

    response = await es_client.search(index=ES_INDEX_NAME, body=query)

    hits = response.get("hits", {}).get("hits", [])
    visibility_scores = [hit["_source"]["visibility_score"] for hit in hits if "visibility_score" in hit["_source"]]

    return visibility_scores


async def index_analysis_document(document: Dict[str, Any]) -> None:
    """Inserts the final analysis document into Elasticsearch."""
    es_client = get_es_client()
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