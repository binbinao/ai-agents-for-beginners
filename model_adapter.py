"""
Model Adapter for Tencent Cloud and Deepseek API
Compatible with OpenAI format for use in ai-agents-for-beginners course
"""

import os
import openai
from openai import AsyncOpenAI, OpenAI
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()


def _resolve_config() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Resolve (api_key, endpoint, model_id) from the environment.

    OPENAI_* are the names used by the local custom-model path. They fall back to
    GITHUB_* so the same adapter also works against GitHub Models.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GITHUB_TOKEN")
    endpoint = os.getenv("OPENAI_ENDPOINT") or os.getenv("GITHUB_ENDPOINT")
    model_id = os.getenv("OPENAI_CHAT_MODEL_ID") or os.getenv("GITHUB_MODEL_ID")
    return api_key, endpoint, model_id


class CustomModelAdapter:
    """
    Adapter to use Tencent Cloud or Deepseek models with OpenAI-compatible format
    Works with Microsoft Agent Framework, Semantic Kernel, and AutoGen
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 endpoint: Optional[str] = None, 
                 model_id: Optional[str] = None):
        """
        Initialize the custom model adapter
        
        Args:
            api_key: Your API key for Tencent Cloud or Deepseek
            endpoint: The API endpoint URL
            model_id: The model name to use
        """
        env_key, env_endpoint, env_model = _resolve_config()
        # Use provided values or fall back to environment variables
        self.api_key = api_key or env_key
        self.endpoint = endpoint or env_endpoint
        self.model_id = model_id or env_model
        
        if not self.api_key or not self.endpoint or not self.model_id:
            raise ValueError("Missing required configuration. Please set API_KEY, ENDPOINT, and MODEL_ID")
        
        # Explicit clients are the source of truth for this adapter's own calls.
        self.client = OpenAI(api_key=self.api_key, base_url=self.endpoint)
        self.async_client = AsyncOpenAI(api_key=self.api_key, base_url=self.endpoint)

        # Intentional global side effect: with openai>=1.0 the module-level
        # openai.chat.completions accessors resolve to a shared *blocking* default
        # client, and assigning openai.api_key / openai.base_url does redirect it
        # (verified against openai 3.16.2). Course notebooks construct framework
        # clients themselves and may rely on this ambient configuration, so do not
        # delete this as "dead code". It is process-global, which is exactly why this
        # class also keeps explicit self.client / self.async_client for its own calls.
        openai.api_key = self.api_key
        openai.base_url = self.endpoint
        
        print(f"Custom Model Adapter initialized with:")
        print(f"  Endpoint: {self.endpoint}")
        print(f"  Model: {self.model_id}")
        print(f"  API Key: {'*' * (len(self.api_key) - 4) + self.api_key[-4:] if self.api_key else 'Not set'}")
    
    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """
        Perform chat completion using the custom model
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional arguments to pass to the API
            
        Returns:
            API response object
        """
        try:
            response = await self.async_client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                **kwargs
            )
            return response
        except Exception as e:
            print(f"Error in chat completion: {e}")
            raise

    def sync_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """
        Synchronous version of chat completion
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                **kwargs
            )
            return response
        except Exception as e:
            print(f"Error in sync chat completion: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test the connection to the custom model
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": "Hello, can you respond? Just say 'Connection successful'."}],
                max_tokens=16
            )
            print(f"Test response: {response.choices[0].message.content}")
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False


# Convenience function to create adapter from environment
def create_default_adapter() -> CustomModelAdapter:
    """
    Create a model adapter using environment variables
    """
    return CustomModelAdapter()

# Async context manager for use with async frameworks
class AsyncCustomModelAdapter(CustomModelAdapter):
    """
    Extended adapter with async context manager support
    """
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

# Compatibility functions for different frameworks

def get_openai_client():
    """
    Returns an async OpenAI client configured for custom model
    Compatible with Microsoft Agent Framework
    """
    api_key, endpoint, _ = _resolve_config()
    return AsyncOpenAI(api_key=api_key, base_url=endpoint)

def get_sync_openai_client():
    """
    Returns a blocking OpenAI client configured for custom model.

    Preferred over the module-level openai.chat.completions accessors: those resolve
    to openai's shared default client, so they only see this endpoint if someone has
    already mutated the process-global openai.api_key / openai.base_url. An explicit
    client keeps the caller independent of ambient global state.
    """
    api_key, endpoint, _ = _resolve_config()
    return OpenAI(api_key=api_key, base_url=endpoint)

def get_semantic_kernel_config():
    """
    Returns configuration for Semantic Kernel
    """
    api_key, endpoint, model_id = _resolve_config()
    return {
        "api_key": api_key,
        "endpoint": endpoint,
        "model_id": model_id
    }

def get_autogen_config():
    """
    Returns configuration for AutoGen

    Note the key names differ from get_semantic_kernel_config(): AutoGen's
    OpenAI-compatible client expects 'base_url' and 'model'.
    """
    api_key, endpoint, model_id = _resolve_config()
    return {
        "api_key": api_key,
        "base_url": endpoint,
        "model": model_id
    }