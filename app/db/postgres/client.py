import asyncpg
from typing import Any
from app.core.config import settings

# Configuration - Uses the service name defined in docker-compose.yml
POSTGRES_DETAILS = settings.POSTGRES_URL

# Global client object
postgres_pool: Any = None 

async def connect_to_postgres():
    """Initializes and connects to PostgreSQL, and ensures the table exists."""
    global postgres_pool
    print("Attempting to connect to PostgreSQL...")
    try:
        # Create a connection pool
        postgres_pool = await asyncpg.create_pool(POSTGRES_DETAILS)
        
        # Ensure the required table exists
        await _create_brand_performance_table()
        
        print("Connected successfully to PostgreSQL and table checked!")
    except Exception as e:
        print(f"Could not connect to PostgreSQL: {e}")
        # Reraise the exception to signal a failed startup
        raise

async def close_postgres():
    """Closes the PostgreSQL connection pool."""
    global postgres_pool
    if postgres_pool:
        await postgres_pool.close()
        print("PostgreSQL connection closed.")

def get_postgres_pool():
    if postgres_pool is not None:
        return postgres_pool
    else:
        raise Exception("Postgres connection error..")

async def _create_brand_performance_table():
    """Creates the brand_performance table if it does not exist."""
    CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS brand_performance (
        id SERIAL PRIMARY KEY,
        brand_name VARCHAR(255) NOT NULL,
        visibility_score REAL NOT NULL,
        query_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
        response_id VARCHAR(255) UNIQUE NOT NULL, -- Link back to MongoDB/ES document
        inserted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Use a connection from the pool to execute the DDL (Data Definition Language) query
    async with postgres_pool.acquire() as connection:
        await connection.execute(CREATE_TABLE_QUERY)