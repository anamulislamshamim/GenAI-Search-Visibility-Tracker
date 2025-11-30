import datetime
from typing import Any, Dict
from app.db.postgres.client import postgres_pool

async def insert_brand_performance(
    response_id: str, 
    brand_name: str, 
    visibility_score: float
) -> None:
    """
    Inserts a new record into the brand_performance table after analysis is complete.
    
    Args:
        response_id: Unique ID linking to the original MongoDB/ES record.
        brand_name: The name of the brand queried.
        visibility_score: The final calculated score (0-100).
    """
    if postgres_pool is None:
        raise ConnectionError("PostgreSQL connection pool is not initialized.")

    INSERT_QUERY = """
    INSERT INTO brand_performance 
    (brand_name, visibility_score, query_timestamp, response_id) 
    VALUES ($1, $2, $3, $4);
    """
    
    # We use the current UTC time for the insertion record
    current_time = datetime.datetime.now(datetime.timezone.utc)
    
    # Execute the insert query
    async with postgres_pool.acquire() as connection:
        await connection.execute(
            INSERT_QUERY, 
            brand_name, 
            visibility_score, 
            current_time, 
            response_id
        )
    
    print(f"PostgreSQL: Inserted performance record for {brand_name} (Score: {visibility_score}).")

async def get_brand_metrics(brand_name: str) -> Dict[str, Any]:
    """
    Feature 5: Retrieves the average visibility score and count of queries for a brand.
    
    Args:
        brand_name: The brand to query metrics for.
        
    Returns:
        A dictionary containing the average score and the total number of records.
    """
    if postgres_pool is None:
        raise ConnectionError("PostgreSQL connection pool is not initialized.")

    METRICS_QUERY = """
    SELECT 
        COUNT(visibility_score) as total_queries,
        AVG(visibility_score) as average_score
    FROM brand_performance
    WHERE brand_name ILIKE $1;
    """
    
    async with postgres_pool.acquire() as connection:
        # Use fetchrow to get a single row of aggregation results
        row = await connection.fetchrow(METRICS_QUERY, brand_name)
        
        if row and row['total_queries'] > 0:
            # Convert row to dictionary for structured return
            return {
                "brand_name": brand_name,
                "total_queries": row['total_queries'],
                # PostgreSQL returns float data types, we round it for presentation
                "average_visibility_score": round(row['average_score'], 2)
            }
        
        return {
            "brand_name": brand_name,
            "total_queries": 0,
            "average_visibility_score": 0.0
        }
