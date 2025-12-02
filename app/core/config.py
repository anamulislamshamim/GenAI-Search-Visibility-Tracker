from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class Environment(str, Enum):
    LOCAL = "LOCAL"
    CLOUD = "CLOUD"

class LLMProvider(str, Enum):
    HUGGINGFACE = "HUGGINGFACE"
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"
    OLLAMA = "OLLAMA"

class Settings(BaseSettings):
    # Load configuration from .env file 
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    # --- General ---
    ENVIRONMENT: Environment = Environment.LOCAL

    # --- LLM Settings ---
    LLM_PROVIDER: LLMProvider = LLMProvider.OLLAMA
    HUGGINGFACE_MODEL: str = "local/mock-model"
    OLLAMA_MODEL: str = "gemma:2b"
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    # --- Data Store URIs ---
    MONGO_URI: str  = "mongodb://mongodb:27017"
    MONGO_DB_NAME: str = "query_analytics"
    MONGO_COLLECTION_NAME: str = "brand_analysis"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_API_KEY: str = ""
    ES_INDEX_NAME: str = "brand_analysis"
    POSTGRES_URL: str = "postgresql://user:password@postgres:5432/main_db"
    POSTGRES_TABLE: str = "brand_analysis"

    SECRET_KEY: str ="secret-my-secret"
    ALGORITHM: str ="md5"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # BiqQuery
    GCP_PROJECT_ID: str = ""
    BQ_DATASET_ID: str = ""
    BQ_TABLE_ID: str = ""

# Initialize settings object
settings = Settings()