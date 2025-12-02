from google.cloud.bigquery import Client, SchemaField
from google.cloud.bigquery.job import QueryJob
from google.api_core import exceptions
from typing import Any, List, Dict, Optional
from google.cloud import bigquery
from asyncio import to_thread
from app.db.big_query.client import BigQueryClient
from app.db.big_query.schemas import QueryParameters
from app.core.models import BigQueryHistoryRecord
from app.core.config import settings
from datetime import datetime, timezone


class BigQueryService:
    """
    Service layer for all BigQuery data operations.
    """
    def __init__(self, dataset_id: str, table_id: str, project_id: Optional[str] = None):
        self.client: Client = BigQueryClient(project_id=project_id).get_client()
        self.table_ref = self.client.dataset(dataset_id).table(table_id)
        self.full_table_id = f"{project_id}.{dataset_id}.{table_id}"
        print(f"BigQuery Service connected to table: {self.full_table_id}")


    def run_query(self, sql_query: str, params: QueryParameters = QueryParameters()) -> List[Dict[str, Any]]:
        try:
            # Configure job and run query
            job_config = bigquery.QueryJobConfig()
            query_job: QueryJob = self.client.query(
                sql_query,
                job_config=job_config,
                timeout=params.timeout_ms / 1000  # Convert ms to seconds
            )

            # Wait for the job to complete and fetch results
            results = query_job.result(max_results=params.max_results)
            
            # Convert BigQuery Row objects to standard Python dictionaries
            return [dict(row) for row in results]

        except exceptions.GoogleAPICallError as e:
            print(f"BigQuery Query Error: {e}")
            raise RuntimeError(f"Failed to execute query: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during query execution: {e}")
            raise
    
    async def insert_record(self, record: BigQueryHistoryRecord) -> bool:
        """
        Inserts a single BigQueryHistoryRecord into the configured BigQuery table asynchronously.
        
        Uses to_thread.run_sync to safely call the synchronous BigQuery client 
        without blocking the main FastAPI event loop.

        Args:
            record: A validated BigQueryHistoryRecord Pydantic model instance.
        
        Returns:
            True if insertion was successful, False otherwise.
        """
        # Convert the Pydantic model to a dictionary suitable for insertion
        row_to_insert = record.model_dump()
        
        # BigQuery expects the timestamp as a string or compatible object
        # row_to_insert['timestamp'] = row_to_insert['timestamp'].isoformat()
        # Convert ALL datetime fields to ISO 8601 strings
        for key, value in row_to_insert.items():
            if isinstance(value, datetime):
                # BigQuery DATETIME must be naive (no timezone)
                naive = value.replace(tzinfo=None)
                # Output example: "2025-12-02T04:46:22.924708"
                row_to_insert[key] = naive.isoformat()
                
                # Define the synchronous function to execute in the thread pool
                def sync_insert():
                    return self.client.insert_rows_json(
                        table=self.table_ref,
                        json_rows=[row_to_insert]
                    )

        try:
            # Use to_thread.run_sync to run the blocking database call
            errors = await to_thread(sync_insert)
            
            if errors:
                print(f"Errors occurred during row insertion: {errors}")
                return False
            
            print(f"Successfully inserted 1 record into {self.full_table_id}")
            return True

        except Exception as e:
            print(f"An error occurred during asynchronous insertion: {e}")
            return False
    
    async def get_brand_metrics(self, brand_name: str) -> Dict[str, float]:
        # Add wildcards for partial matching
        search_value = f"%{brand_name}%"

        query = f"""
            SELECT
                COUNT(visibility_score) AS total_queries,
                AVG(visibility_score) AS average_score
            FROM `{self.full_table_id}`
            WHERE LOWER(brand_name) LIKE LOWER(@brand_name);
        """

        # BigQuery query parameters
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("brand_name", "STRING", search_value)
            ]
        )

        # Execute the query synchronously
        results = self.run_query(sql_query=query, job_config=job_config)

        # Parse first row (BigQuery always returns at least 1 row)
        if results:
            row = results[0]
            return {
                "brand_name": brand_name,
                "total_queries": row.get("total_queries", 0),
                "average_score": float(row.get("average_score", 0.0)) if row.get("average_score") is not None else 0.0
            }

        # Fallback
        return {"total_queries": 0, "average_score": 0.0}


BQ_SERVICE = None
async def connect_to_big_query():
    """Initializes and connects to MongoDB."""
    global BQ_SERVICE
    print("Attempting to connect to BigQuery...")
    try:
        BQ_SERVICE = BigQueryService(dataset_id=settings.BQ_DATASET_ID, table_id=settings.BQ_TABLE_ID, project_id=settings.GCP_PROJECT_ID)
    except Exception as e:
        print(f"Could not connect to BigQuery: {e}")
        # In a production environment, you might re-raise to halt startup
        raise

async def close_big_query():
    """Closes the MongoDB connection."""
    global BQ_SERVICE
    if BQ_SERVICE:
        BQ_SERVICE.client.close()
        print("BigQuery connection closed.")

def get_big_query():
    if BQ_SERVICE is not None:
        return BQ_SERVICE
    else:
        raise Exception("BigQuery connection error!")