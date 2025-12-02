from datetime import datetime, timezone
from typing import Optional, Any
from pydantic import BaseModel, Field


# 1. Define the structure for data being inserted into BigQuery
# This is a sample schema for a simple log record.
class LogRecord(BaseModel):
    """
    Schema for a log record to be inserted into a BigQuery table.
    Pydantic ensures that data is validated before insertion.
    """
    user_id: str = Field(..., description="The ID of the user performing the action.")
    event_type: str = Field(..., description="The type of action/event (e.g., 'login', 'checkout').")
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc), description="The UTC timestamp of the event.")
    payload: dict[str, Any] = Field(default_factory=dict, description="Arbitrary data related to the event.")

    class Config:
        # Allows conversion from BigQuery Row objects if retrieving data
        allow_population_by_field_name = True
        # For compatibility with FastAPI and ORM/DB
        from_attributes = True


# 2. Define the structure for the query parameters
class QueryParameters(BaseModel):
    """
    Optional parameters to pass to the query execution method.
    """
    max_results: Optional[int] = 100
    timeout_ms: Optional[float] = 30000.0