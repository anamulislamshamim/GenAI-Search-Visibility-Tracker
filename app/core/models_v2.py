from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone


# ============================================================
# MongoDB Schemas (User Profiles, Configurations, Query Logs)
# ============================================================

class User(BaseModel):
    user_id: str = Field(..., description="Unique user ID")
    email: str
    full_name: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


class UserConfig(BaseModel):
    user_id: str
    default_model: str = "gemini-pro"
    safe_search: bool = True
    max_tokens: int = 2048
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


class QueryLog(BaseModel):
    """
    MongoDB stores lightweight, mutable logs about user activity.
    """
    log_id: str
    user_id: str
    brand: str
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    llm_model: str = "gemini-pro"
    status: str = "completed"   # success / failed


# ============================================================
# BigQuery Schema (Historical LLM Responses - Immutable)
# ============================================================

class HistoricalRecord(BaseModel):
    """
    Stored in BigQuery; never updated or deleted.
    Represents raw LLM responses.
    """
    record_id: str
    user_id: str
    brand: str
    llm_model: str
    query_timestamp: datetime
    llm_response: str
    prompt_used: str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


# ============================================================
# Elasticsearch Schema (Ranking, Hybrid Search, Vectors)
# ============================================================

class SearchIndexDocument(BaseModel):
    """
    Indexed into Elasticsearch to enable:
    - keyword search
    - semantic/vector search
    - scoring/ranking
    """
    doc_id: str
    brand: str
    llm_response: str
    keywords: List[str] = []
    vector_embedding: List[float]   # from HuggingFace embedding API
    ranking_score: Optional[float] = None
    semantic_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


# ============================================================
# Request/Response Schemas for FastAPI Endpoints
# ============================================================

class BrandQueryRequest(BaseModel):
    user_id: str
    brand: str
    model: Optional[str] = "gemini-pro"


class BrandQueryResponse(BaseModel):
    brand: str
    llm_response: str
    visibility_score: float
    semantic_score: float
    ranking_score: float
    timestamp: datetime
