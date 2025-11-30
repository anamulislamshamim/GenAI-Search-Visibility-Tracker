from .llm_base import LLMBase, MockHuggingFaceModel, GeminiClient
from app.core.config import settings, LLMProvider


def get_llm_service() -> LLMBase:
    """Dynamically selects and returns the correct LLM implementation based on environment settings."""
    
    if settings.LLM_PROVIDER == LLMProvider.HUGGINGFACE:
        return MockHuggingFaceModel(settings.HUGGINGFACE_MODEL)
    
    elif settings.LLM_PROVIDER == LLMProvider.GEMINI:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set for CLOUD environment.")
        return GeminiClient(api_key=settings.GEMINI_API_KEY)
    else:
        # Fallback to the mock model for safety in case of misconfiguration
        print("Warning: LLM_PROVIDER not recognized, falling back to MOCK model.")
        return MockHuggingFaceModel(settings.HUGGINGFACE_MODEL)
