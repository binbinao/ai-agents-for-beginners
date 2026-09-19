"""
Connection Test Script for Custom Model Adapter
Tests connectivity to Tencent Cloud or Deepseek models
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_basic_connection():
    """Test basic connection using OpenAI library"""
    # Get configuration from environment
    api_key = os.getenv("OPENAI_API_KEY", os.getenv("GITHUB_TOKEN"))
    endpoint = os.getenv("OPENAI_ENDPOINT", os.getenv("GITHUB_ENDPOINT"))
    model_id = os.getenv("OPENAI_CHAT_MODEL_ID", os.getenv("GITHUB_MODEL_ID"))
    
    if not all([api_key, endpoint, model_id]):
        print("❌ Error: Missing required environment variables!")
        print(f"  OPENAI_API_KEY/GITHUB_TOKEN: {'Set' if api_key else 'Missing'}")
        print(f"  OPENAI_ENDPOINT/GITHUB_ENDPOINT: {'Set' if endpoint else 'Missing'}")
        print(f"  OPENAI_CHAT_MODEL_ID/GITHUB_MODEL_ID: {'Set' if model_id else 'Missing'}")
        return False
    
    print(f"Attempting connection with:")
    print(f"  Endpoint: {endpoint}")
    print(f"  Model: {model_id}")
    print(f"  API Key: {'*' * (len(api_key) - 4) + api_key[-4:] if api_key else 'Not set'}")
    
    try:
        # Use an explicit blocking client instead of the module-level
        # openai.chat.completions accessors. Those work, but only because they share
        # openai's process-global default client -- this script is a diagnostic, so it
        # must not depend on (or leave behind) ambient global configuration.
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url=endpoint)

        # Test the connection
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Please respond with 'Connection test successful' and nothing else."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        print(f"✅ Connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_custom_adapter():
    """Test connection using the custom adapter"""
    try:
        from model_adapter import CustomModelAdapter
        
        print("\n--- Testing Custom Model Adapter ---")
        adapter = CustomModelAdapter()
        
        # Test connection
        success = adapter.test_connection()
        return success
        
    except ImportError as e:
        print(f"❌ Could not import model_adapter: {e}")
        return False
    except Exception as e:
        print(f"❌ Custom adapter test failed: {e}")
        return False

def test_framework_configs():
    """Test framework-specific configurations (no network calls)"""
    try:
        from model_adapter import get_openai_client, get_semantic_kernel_config, get_autogen_config
        
        print("\n--- Testing Framework Configurations ---")
        
        checks = []

        # Test OpenAI client
        try:
            client = get_openai_client()
            print("✅ OpenAI client configuration: OK")
            checks.append(True)
        except Exception as e:
            print(f"❌ OpenAI client configuration failed: {e}")
            checks.append(False)
        
        # Test Semantic Kernel config
        try:
            sk_config = get_semantic_kernel_config()
            print(f"✅ Semantic Kernel configuration: OK")
            print(f"   Model: {sk_config.get('model_id', 'Not set')}")
            checks.append(bool(sk_config.get("model_id")))
        except Exception as e:
            print(f"❌ Semantic Kernel configuration failed: {e}")
            checks.append(False)
        
        # Test AutoGen config
        try:
            ag_config = get_autogen_config()
            print(f"✅ AutoGen configuration: OK")
            print(f"   Model: {ag_config.get('model', 'Not set')}")
            checks.append(bool(ag_config.get("model")))
        except Exception as e:
            print(f"❌ AutoGen configuration failed: {e}")
            checks.append(False)
        
        return all(checks)
        
    except ImportError as e:
        print(f"❌ Could not import framework configs: {e}")
        return False

async def test_async_functionality():
    """Test asynchronous functionality"""
    try:
        from model_adapter import CustomModelAdapter
        
        print("\n--- Testing Async Functionality ---")
        adapter = CustomModelAdapter()
        
        # Test async chat completion
        messages = [
            {"role": "user", "content": "Hello! Please respond with 'Async test successful' and nothing else."}
        ]
        
        response = await adapter.chat_completion(messages)
        print(f"✅ Async completion successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Async functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Custom Model Connection for AI Agents Course")
    print("="*60)
    
    # Test 1: Basic connection
    print("\n--- Test 1: Basic Connection ---")
    basic_success = test_basic_connection()
    
    # Test 2: Custom adapter
    adapter_success = test_custom_adapter()
    
    # Test 3: Framework configs
    framework_success = test_framework_configs()
    
    # Test 4: Async functionality
    async_success = asyncio.run(test_async_functionality())
    
    print("\n" + "="*60)
    print("📊 Test Summary:")
    print(f"  Basic Connection: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"  Custom Adapter: {'✅ PASS' if adapter_success else '❌ FAIL'}")
    print(f"  Framework Configs: {'✅ PASS' if framework_success else '❌ FAIL'}")
    print(f"  Async Functionality: {'✅ PASS' if async_success else '❌ FAIL'}")
    
    all_success = all([basic_success, adapter_success, framework_success, async_success])
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_success else '❌ SOME TESTS FAILED'}")
    
    if all_success:
        print("\n🎉 Your custom model is ready to use with the AI Agents course!")
        print("   You can now run the Jupyter notebooks with your Tencent Cloud or Deepseek model.")
    else:
        print("\n⚠️  Please check your configuration and environment variables.")
        print("   Make sure to update the .env file with your actual API keys and endpoints.")
    
    return all_success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)