#!/usr/bin/env python3
"""
🧪 Test AIML API Integration
===========================
Simple test to verify AIML API is working before full Coral integration
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_aiml_api():
    """Test AIML API connection and response"""
    print("Testing AIML API Integration")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("AIML_API_KEY")
    if not api_key or api_key == "your_aiml_api_key_here":
        print("❌ AIML_API_KEY not set!")
        print("   Please set your API key in .env file")
        return False
    
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        # Initialize client
        client = OpenAI(
            base_url="https://api.aimlapi.com/v1",
            api_key=api_key
        )
        
        print("🌐 Connecting to AIML API...")
        
        # Test request
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for testing API integration."
                },
                {
                    "role": "user",
                    "content": "Generate a short professional cover letter introduction for a software developer applying to TechFlow Inc. Keep it under 100 words."
                }
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        # Extract response
        message = response.choices[0].message.content
        
        print("✅ AIML API Response:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        
        print(f"📊 Response Stats:")
        print(f"   Words: {len(message.split())}")
        print(f"   Characters: {len(message)}")
        print(f"   Model: {response.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ AIML API Test Failed: {e}")
        return False

if __name__ == "__main__":
    success = test_aiml_api()
    
    if success:
        print("\n🎉 AIML API integration is working!")
        print("✅ Ready to use with Coral Protocol agents")
    else:
        print("\n❌ Fix API configuration before proceeding")
        print("💡 Get your API key from: https://aimlapi.com")