"""
API Configuration Setup for Real-Time Job Application Agent
===========================================================

This script helps you set up API keys for real job search functionality.
Choose between JSearch (RapidAPI) or Adzuna API based on your preference.

🎯 RECOMMENDED: JSearch API via RapidAPI
- Best job aggregation (Google Jobs, Indeed, LinkedIn)
- 150 free requests/month
- Easy setup with single API key

Alternative: Adzuna API
- Direct API access  
- 1,000 free requests/month
- Requires App ID + App Key
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with API configuration"""
    print("🚀 Setting up your Job Search API Configuration")
    print("=" * 50)
    
    # Check if .env already exists
    env_file = Path(".env")
    if env_file.exists():
        print("📋 Found existing .env file")
        with open(env_file, 'r') as f:
            content = f.read()
            print(content)
        
        update = input("\n❓ Update existing .env file? (y/n): ").lower()
        if update != 'y':
            return
    
    print("\n🎯 API Setup Options:")
    print("1. JSearch API (RapidAPI) - RECOMMENDED")
    print("   - Get free key at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch")
    print("   - 150 requests/month free")
    print("   - Best job data quality")
    print()
    print("2. Adzuna API")
    print("   - Get free key at: https://developer.adzuna.com/")
    print("   - 1,000 requests/month free")
    print("   - More requests but basic data")
    print()
    
    choice = input("❓ Which API do you want to set up? (1 for JSearch, 2 for Adzuna, both for both): ")
    
    env_content = []
    
    if choice in ['1', 'both']:
        print("\n🔑 JSearch API Setup:")
        print("1. Go to: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch")
        print("2. Sign up for RapidAPI (free)")
        print("3. Subscribe to JSearch (free tier)")
        print("4. Copy your X-RapidAPI-Key from the dashboard")
        
        api_key = input("\n🔑 Enter your RapidAPI Key (or press Enter to skip): ").strip()
        if api_key:
            env_content.append(f"RAPIDAPI_KEY={api_key}")
            print("✅ JSearch API key configured!")
        else:
            env_content.append("# RAPIDAPI_KEY=your_rapidapi_key_here")
    
    if choice in ['2', 'both']:
        print("\n🔑 Adzuna API Setup:")
        print("1. Go to: https://developer.adzuna.com/")
        print("2. Sign up for free account")
        print("3. Create new application")
        print("4. Copy your App ID and App Key")
        
        app_id = input("\n🆔 Enter your Adzuna App ID (or press Enter to skip): ").strip()
        app_key = input("🔑 Enter your Adzuna App Key (or press Enter to skip): ").strip()
        
        if app_id and app_key:
            env_content.append(f"ADZUNA_APP_ID={app_id}")
            env_content.append(f"ADZUNA_APP_KEY={app_key}")
            print("✅ Adzuna API credentials configured!")
        else:
            env_content.append("# ADZUNA_APP_ID=your_app_id_here")
            env_content.append("# ADZUNA_APP_KEY=your_app_key_here")
    
    # Add other environment variables if they don't exist
    env_content.extend([
        "",
        "# Other API configurations (if needed)",
        "# AIML_API_KEY=your_aiml_api_key_here",
        "# JWT_SECRET_KEY=your_jwt_secret_key_here"
    ])
    
    # Write to .env file
    with open(".env", "w") as f:
        f.write("\n".join(env_content))
    
    print(f"\n✅ Configuration saved to {env_file.absolute()}")
    print("\n🚀 Next Steps:")
    print("1. Restart your API server after setting up keys")
    print("2. Test resume upload and job search functionality")
    print("3. Check the console logs to see real parsing in action")

def test_configuration():
    """Test the current API configuration"""
    print("\n🧪 Testing Current Configuration")
    print("=" * 40)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    adzuna_id = os.getenv("ADZUNA_APP_ID")
    adzuna_key = os.getenv("ADZUNA_APP_KEY")
    
    print(f"JSearch API (RapidAPI): {'✅ Configured' if rapidapi_key else '❌ Not configured'}")
    print(f"Adzuna API: {'✅ Configured' if (adzuna_id and adzuna_key) else '❌ Not configured'}")
    
    if not rapidapi_key and not (adzuna_id and adzuna_key):
        print("\n⚠️ No API keys configured!")
        print("Run this script to set up your free API keys.")
        return False
    
    # Test the APIs
    print("\n🔍 Testing API connections...")
    try:
        from real_job_search_api import RealJobSearchAPI
        api = RealJobSearchAPI()
        result = api.search_jobs_with_fallback("Python Developer", max_results=1)
        
        if result.get("success"):
            print(f"✅ API Test Successful!")
            print(f"   API Used: {result.get('api_used')}")
            print(f"   Jobs Found: {len(result.get('jobs', []))}")
        else:
            print(f"❌ API Test Failed: {result.get('error')}")
    except Exception as e:
        print(f"❌ Test Error: {e}")
    
    return True

if __name__ == "__main__":
    print("🤖 AI Job Application Agent - API Setup")
    print("=" * 50)
    
    while True:
        print("\n📋 Options:")
        print("1. Set up API keys")
        print("2. Test current configuration")
        print("3. Exit")
        
        choice = input("\n❓ Choose option (1-3): ")
        
        if choice == "1":
            create_env_file()
        elif choice == "2":
            test_configuration()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")