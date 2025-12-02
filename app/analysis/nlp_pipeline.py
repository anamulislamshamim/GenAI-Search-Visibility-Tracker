from typing import Dict, Any, List
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
import datetime
from app.db.elasticsearch.indexing import index_analysis_document
from app.db.mongodb.storage import update_query_status_and_score
from app.db.postgres.storage import insert_brand_performance
from app.db.big_query.service import get_big_query


# Global NLP resources (initialized once)
model: SentenceTransformer | None = None
sentiment_analyzer: SentimentIntensityAnalyzer | None = None

async def initialize_nlp_models():
    """Initializes heavy NLP models like Sentence Transformers and NLTK data."""
    print("Initializing NLP models...")
    try:
        # 1. Download necessary NLTK data
        nltk.download('vader_lexicon', quiet=True)
        # 2. Initialize VADER sentiment analyzer
        global sentiment_analyzer
        sentiment_analyzer = SentimentIntensityAnalyzer()
        # 3. Initialize Sentence Transformer
        global model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("NLP models initialized.")
    except Exception as e:
        print(f"Failed to initialize NLP models: {e}")
        # In a robust application, you'd handle this failure gracefully
        pass


def extract_keywords(text: str) -> List[str]:
    """Placeholder for simple keyword extraction (e.g., using NLTK/SpaCy)."""
    # Simple example: split by whitespace and return unique words (filtered)
    keywords = set(word.lower() for word in text.split() if len(word) > 3 and word.isalpha())
    return list(keywords)[:5] # Return top 5 keywords


def get_sentiment_score(text: str) -> float:
    """Placeholder for sentiment scoring using VADER or Transformer models."""
    scores = sentiment_analyzer.polarity_scores(text)
    return scores['compound']

    
def generate_embedding(text: str) -> List[float]:
    """Generates the 384-dimensional embedding vector using all-MiniLM-L6-v2."""
    # In a real environment:
    if model:
        embedding = model.encode(text, convert_to_tensor=True).tolist()
        return embedding
    else:
        raise ("Embedding model is missing...")
    
def calculate_visibility_score(sentiment_score: float) -> float:
    """
    Feature 3: Calculates the final visibility score (0 to 100).
    The score is linearly mapped from the sentiment range [-1, 1] to [0, 100].
    Formula: (score + 1) * 50
    """
    return round((sentiment_score + 1) * 50, 2)


async def start_analysis_pipeline(response_id: str, brand_name: str, raw_llm_response: str):
    print(f"--- Starting analysis pipeline for ID: {response_id} ---")
    
    # 1. Perform Analysis
    keywords = extract_keywords(raw_llm_response)
    sentiment_score = get_sentiment_score(raw_llm_response)
    embedding_vector = generate_embedding(raw_llm_response)
    
    # 2. Perform Feature 3 Score Calculation
    visibility_score = calculate_visibility_score(sentiment_score)
    
    # 3. Construct the final document for Elasticsearch (ES)
    analysis_document = {
        "response_id": response_id,
        "brand_keyword": brand_name,
        "keywords": " ".join(keywords), 
        "sentiment_score": sentiment_score,
        "visibility_score": visibility_score, # Final calculated score
        "timestamp": datetime.datetime.now(datetime.timezone.utc),
        "embedding_vector": embedding_vector,
    }
    
    # 4. Index the analyzed document in ES (Feature 2/3 persistence)
    await index_analysis_document(analysis_document)

    # 5. Update the original record in MongoDB (Feature 3 status update)
    # Marks the process as 'Complete' and saves the final score.
    await update_query_status_and_score(response_id, visibility_score)

    # 6. Insert into PostgreSQL for Structured Reporting (Feature 4)
    # await insert_brand_performance(response_id, brand_name, visibility_score)

    # Insert Historical data to BigQuery
    historic_document = analysis_document.copy()
    historic_document.pop("embedding_vector")
    bigquery_client = get_big_query()
    await bigquery_client.insert_record(record=historic_document)

    print(f"--- Analysis and indexing complete for ID: {response_id} ---")