#!/usr/bin/env python3
"""
Test AIML API Integration - Windows Compatible
==============================================
Simple test to verify AIML API is working before full Coral integration
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_aiml_api():
    """Test AIML API connection and response"""
    print("TESTING AIML API INTEGRATION")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("AIML_API_KEY")
    if not api_key or api_key == "your_aiml_api_key_here":
        print("[ERROR] AIML_API_KEY not set!")
        print("   Please set your API key in .env file")
        return False
    
    print(f"[INFO] API Key: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        # Initialize client
        client = OpenAI(
            base_url="https://api.aimlapi.com/v1",
            api_key=api_key
        )
        
        print("[INFO] Connecting to AIML API...")
        
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
        cover_letter = response.choices[0].message.content
        model_used = response.model
        
        print(f"[SUCCESS] Model: {model_used}")
        print(f"[SUCCESS] Response ({len(cover_letter.split())} words):")
        print("-" * 30)
        print(cover_letter)
        print("-" * 30)
        print("[SUCCESS] AIML API is working!")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] API test failed: {e}")
        return False

def main():
    """Main test function"""
    print("AI Job Application Agent - AIML API Test")
    print("=" * 60)
    
    success = test_aiml_api()
    
    print("\n" + "=" * 60)
    if success:
        print("[FINAL] TEST PASSED - AIML API Working!")
        print("[NEXT] Ready for full Coral Protocol integration")
    else:
        print("[FINAL] TEST FAILED - Fix API configuration")
        print("[HELP] Check your .env file and API key")

if __name__ == "__main__":
    main()