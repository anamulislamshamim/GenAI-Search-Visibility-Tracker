import os
import asyncio
from abc import ABC, abstractmethod
from google import genai
from google.genai.errors import APIError

# --- Abstract Base Class (LLMBase) ---

class LLMBase(ABC):
    """Abstract Base Class for all LLM clients (Gemini, OpenAI, HuggingFace Mock)."""

    def __init__(self, model_name: str, api_key: str | None = None):
        self.model_name = model_name
        self.api_key = api_key
        # Initialization logic (e.g., set up client object)

    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        """Generates a text response for the given prompt."""
        pass

# For testing purpose locally
class MockHuggingFaceModel(LLMBase):
    """Mock implementation for local testing (simulates a HuggingFace model)."""
    async def generate_response(self, prompt: str) -> str:
        print(f"--- MOCK LLM CALL: {self.model_name} ---")
        # Simple rule-based mock response
        if "Daraz" in prompt:
            return "Daraz is a leading e-commerce platform in South Asia, popular for its wide range of products and delivery network. It's often mentioned in terms of online shopping deals."
        elif "Pathao" in prompt:
            return "Pathao is a popular ride-sharing, food delivery, and logistics service, primarily operating in Bangladesh and Nepal. It's known for its super-app services."
        else:
            return f"Brand X is a new entrant in the market. The general sentiment is still forming, but visibility is growing."
    
class GeminiClient(LLMBase):
    """
    Implementation for the Gemini API Client.
    Requires the 'google-genai' package to be installed.
    Uses 'gemini-2.5-flash' by default for the free-tier equivalent.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash", api_key: str | None = None):
        """
        Initializes the Gemini Client.
        The API key can be passed or automatically retrieved from the GEMINI_API_KEY
        environment variable.
        """
        super().__init__(model_name, api_key)
        
        # Use the provided key, or try to use the environment variable
        key_to_use = self.api_key if self.api_key else os.getenv("GEMINI_API_KEY")
        
        if not key_to_use:
            raise ValueError(
                "Gemini API key is required. Pass it in the constructor or "
                "set the GEMINI_API_KEY environment variable."
            )
        
        # Initialize the Google GenAI Client
        self.client = genai.Client(api_key=key_to_use)
        print(f"GeminiClient initialized with model: {self.model_name}")


    async def generate_response(self, prompt: str) -> str:
        """
        Generates a text response for the given prompt using the Gemini API.
        The call is wrapped in asyncio.to_thread to make the synchronous API call
        non-blocking for the asynchronous event loop.
        """
        try:
            # We use asyncio.to_thread to run the synchronous API call
            # in a separate thread, which prevents blocking the event loop.
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=[prompt],
            )
            
            return response.text.strip()
            
        except APIError as e:
            print(f"!!! Gemini API Error: {e} !!!")
            return f"Error: Could not generate response from Gemini API. Details: {e}"
        except Exception as e:
            print(f"!!! Unexpected Error: {e} !!!")
            return f"Error: An unexpected error occurred. Details: {e}"

async def main():
    try:
        # Initialize the client
        gemini_client = GeminiClient(api_key="your_api_key") 
        
        # Test 1
        prompt_1 = "Explain the business model of Daraz and its presence in South Asia."
        print(f"\n--- CALLING GEMINI: '{prompt_1[:50]}...' ---")
        response_1 = await gemini_client.generate_response(prompt_1)
        print("\n**Response 1:**")
        print(response_1)
        
        # Test 2
        prompt_2 = "What are the core services offered by Pathao and where is it most popular?"
        print(f"\n--- CALLING GEMINI: '{prompt_2[:50]}...' ---")
        response_2 = await gemini_client.generate_response(prompt_2)
        print("\n**Response 2:**")
        print(response_2)

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
    
# To run the example:
if __name__ == "__main__":
    asyncio.run(main())