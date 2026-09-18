"""
Model Adapter for Tencent Cloud and Deepseek API
Compatible with OpenAI format for use in ai-agents-for-beginners course
"""

import os
import openai
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

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
        # Use provided values or fall back to environment variables
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", os.getenv("GITHUB_TOKEN"))
        self.endpoint = endpoint or os.getenv("OPENAI_ENDPOINT", os.getenv("GITHUB_ENDPOINT"))
        self.model_id = model_id or os.getenv("OPENAI_CHAT_MODEL_ID", os.getenv("GITHUB_MODEL_ID"))
        
        if not self.api_key or not self.endpoint or not self.model_id:
            raise ValueError("Missing required configuration. Please set API_KEY, ENDPOINT, and MODEL_ID")
        
        # Configure OpenAI client to work with custom endpoint
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
            # Prepare the request
            response = await openai.chat.completions.acreate(
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
            response = openai.chat.completions.create(
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
            response = openai.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": "Hello, can you respond? Just say 'Connection successful'."}]
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
    Returns an OpenAI client configured for custom model
    Compatible with Microsoft Agent Framework
    """
    client = openai.AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY", os.getenv("GITHUB_TOKEN")),
        base_url=os.getenv("OPENAI_ENDPOINT", os.getenv("GITHUB_ENDPOINT")),
    )
    return client

def get_semantic_kernel_config():
    """
    Returns configuration for Semantic Kernel
    """
    return {
        "api_key": os.getenv("OPENAI_API_KEY", os.getenv("GITHUB_TOKEN")),
        "endpoint": os.getenv("OPENAI_ENDPOINT", os.getenv("GITHUB_ENDPOINT")),
        "model_id": os.getenv("OPENAI_CHAT_MODEL_ID", os.getenv("GITHUB_MODEL_ID"))
    }

def get_autogen_config():
    """
    Returns configuration for AutoGen
    """
    return {
        "api_key": os.getenv("OPENAI_API_KEY", os.getenv("GITHUB_TOKEN")),
        "base_url": os.getenv("OPENAI_ENDPOINT", os.getenv("GITHUB_ENDPOINT")),
        "model": os.getenv("OPENAI_CHAT_MODEL_ID", os.getenv("GITHUB_MODEL_ID"))
    }