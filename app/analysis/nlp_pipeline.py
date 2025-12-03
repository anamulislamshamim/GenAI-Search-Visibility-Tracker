from typing import Dict, Any, List
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer, util
import datetime

from app.db.elasticsearch.indexing import index_analysis_document, get_visibility_scores
from app.db.mongodb.storage import update_query_status_and_score
from app.db.big_query.service import get_big_query
from app.core.models import BigQueryHistoryRecord
from app.core.config import settings
from app.db.postgres.storage import insert_brand_performance


# Global NLP resources
model: SentenceTransformer | None = None
sentiment_analyzer: SentimentIntensityAnalyzer | None = None


async def initialize_nlp_models():
    """Initializes heavy NLP models like Sentence Transformers and NLTK data."""
    print("Initializing NLP models...")
    try:
        nltk.download('vader_lexicon', quiet=True)

        global sentiment_analyzer
        sentiment_analyzer = SentimentIntensityAnalyzer()

        global model
        model = SentenceTransformer('all-MiniLM-L6-v2')

        print("NLP models initialized.")
    except Exception as e:
        print(f"Failed to initialize NLP models: {e}")
        pass


def extract_keywords(text: str) -> List[str]:
    """Very simple keyword extraction."""
    keywords = set(word.lower() for word in text.split() if len(word) > 3 and word.isalpha())
    return list(keywords)[:5]


def get_sentiment_score(text: str) -> float:
    """Sentiment scoring using VADER."""
    scores = sentiment_analyzer.polarity_scores(text)
    return scores["compound"]


def generate_embedding(text: str) -> List[float]:
    """Generate embedding using SentenceTransformer."""
    if not model:
        raise ValueError("Embedding model not initialized")
    return model.encode(text, convert_to_tensor=True).tolist()


def calculate_keyword_match_score(keywords: List[str], brand_name: str, raw_text: str) -> float:
    """
    Keyword Match Score:
    Measures how relevant the extracted keywords are to the brand.
    Simple formula: (#keywords that appear in the response) / total keywords.
    Range: 0 → 1
    """
    if not keywords:
        return 0.0
    matches = sum(1 for k in keywords if k in raw_text.lower())
    return round(matches / len(keywords), 3)


def calculate_brand_frequency(brand_name: str, raw_text: str) -> float:
    """
    Brand Appearance Frequency:
    Count occurrences of brand in text relative to total tokens.
    Range: 0 → 1
    """
    tokens = raw_text.lower().split()
    if not tokens:
        return 0.0
    freq = tokens.count(brand_name.lower()) / len(tokens)
    return round(min(freq * 10, 1.0), 3)  # scaled but capped to 1.0


def calculate_semantic_similarity(raw_text: str, brand_name: str) -> float:
    """
    Semantic similarity between brand and the response using embeddings.
    Range: 0 → 1
    """
    if not model:
        return 0.0
    brand_emb = model.encode(brand_name)
    text_emb = model.encode(raw_text)
    sim = util.cos_sim(brand_emb, text_emb).item()
    return round((sim + 1) / 2, 3)  # map [-1,1] → [0,1]


def calculate_correctness_score(raw_text: str, brand_name: str) -> float:
    """
    A placeholder correctness scoring function.
    You may later expand this using a fact-check prompt or RAG lookup.
    Range: 0 → 1
    """
    # Rule-based placeholder: if brand exists in text → good
    score = 1.0 if brand_name.lower() in raw_text.lower() else 0.3
    return round(score, 3)


def calculate_model_consistency(previous_scores: List[float], current_score: float) -> float:
    """
    Model consistency score:
    Measures how stable LLM answers are for the same brand.
    Range: 0 → 1
    """
    if not previous_scores:
        return 1.0  # no history yet = fully consistent
    diffs = [abs(current_score - s) for s in previous_scores]
    stability = 1 - (sum(diffs) / len(diffs))
    return round(max(min(stability, 1.0), 0.0), 3)


def calculate_visibility_score(
    sentiment_score: float,
    semantic_similarity: float,
    keyword_match: float,
    brand_freq: float,
    correctness: float,
    consistency: float
) -> float:
    """
    Expanded visibility score using weighted formula.
    All values assumed ∈ [0,1].
    Final score mapped to 0-100.
    """

    # Weight selection: balanced & easy to justify
    weights = {
        "sentiment": 0.20,
        "semantic": 0.25,
        "keyword": 0.15,
        "brand_freq": 0.15,
        "correctness": 0.15,
        "consistency": 0.10,
    }

    score = (
        sentiment_score * weights["sentiment"] +
        semantic_similarity * weights["semantic"] +
        keyword_match * weights["keyword"] +
        brand_freq * weights["brand_freq"] +
        correctness * weights["correctness"] +
        consistency * weights["consistency"]
    )

    return round(score * 100, 2)  # Range → 0–100


async def start_analysis_pipeline(response_id: str, brand_name: str, raw_llm_response: str):
    print(f"--- Starting enhanced analysis pipeline for ID: {response_id} ---")

    # 1. Extract features
    keywords = extract_keywords(raw_llm_response)
    sentiment_score = get_sentiment_score(raw_llm_response)
    embedding_vector = generate_embedding(raw_llm_response)

    # 2. NEW: calculate advanced metrics
    keyword_match = calculate_keyword_match_score(keywords, brand_name, raw_llm_response)
    semantic_similarity = calculate_semantic_similarity(raw_llm_response, brand_name)
    brand_freq = calculate_brand_frequency(brand_name, raw_llm_response)
    correctness = calculate_correctness_score(raw_llm_response, brand_name)

    # Placeholder: get last N scores from DB to measure consistency
    previous_sentiment_scores = await get_visibility_scores(brand_name=brand_name) # You can later fetch from elasticsearch using full text.
    consistency = calculate_model_consistency(previous_sentiment_scores, sentiment_score)

    # 3. Final enhanced visibility score
    visibility_score = calculate_visibility_score(
        sentiment_score,
        semantic_similarity,
        keyword_match,
        brand_freq,
        correctness,
        consistency
    )

    # 4. Build Elasticsearch Document
    analysis_document = {
        "response_id": response_id,
        "brand_keyword": brand_name,
        "keywords": " ".join(keywords),
        "sentiment_score": sentiment_score,
        "semantic_similarity": semantic_similarity,
        "keyword_match": keyword_match,
        "brand_freq": brand_freq,
        "correctness": correctness,
        "consistency": consistency,
        "visibility_score": visibility_score,
        "timestamp": datetime.datetime.now(datetime.timezone.utc),
        "embedding_vector": embedding_vector,
    }

    # 5. Insert into Elasticsearch
    await index_analysis_document(analysis_document)

    # 6. Update MongoDB record
    await update_query_status_and_score(response_id, visibility_score)

    if settings.ENVIRONMENT == "CLOUD":
        # 7. Insert Historical Record into BigQuery (embedding removed)
        historical_doc = analysis_document.copy()
        historical_doc.pop("embedding_vector", None)
        historical_doc["llm_response"] = raw_llm_response
        bigquery_client = get_big_query()
        await bigquery_client.insert_record(record=BigQueryHistoryRecord(**historical_doc))
    else:
        await insert_brand_performance(response_id, brand_name, visibility_score)

    print(f"--- Enhanced analysis pipeline completed for {response_id} ---")
