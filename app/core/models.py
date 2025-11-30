from pydantic import BaseModel, Field
import datetime


# Request Model
class BrandQuery(BaseModel):
    brand_name: str = Field(..., description="The brand name to query the GenAI model about.", example="Daraz")


# Response Model 
class QueryResponse(BaseModel):
    brand_name: str = Field(..., example="Pathao")
    raw_llm_response: str = Field(..., description="The unedited text response from the GenAI model.")
    response_id: str | None = None
    status: str = Field(..., description="Status of the operation (e.g., 'Processing', 'Complete').", example="Processing")


class QueryRecord(BaseModel):
    """Schema for the record stored in MongoDB (Combining input query and final response)."""
    user_query: str
    response_data: QueryResponse
    timestamp: datetime.datetime
    user_id: str | None = None 


class AggregateMetrics(BaseModel):
    """Response model for aggregate metrics per brand (from PostgreSQL)."""
    brand_name: str
    total_queries: int
    average_visibility_score: float
    
    
class QueryDetails(BaseModel):
    """
    Response model for fetching a single query's detailed status/result via response_id (from MongoDB).
    Matches the structure of the 'response_data' field stored in MongoDB.
    """
    response_id: str = Field(..., description="Unique ID of the query.")
    brand_name: str
    status: str
    visibility_score: float = Field(..., description="The final calculated score (0-100).")
    raw_llm_response: str
    processed_at: datetime.datetime | None = Field(None, description="UTC timestamp when processing completed.")

