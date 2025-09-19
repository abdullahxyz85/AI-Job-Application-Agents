#!/usr/bin/env python3
"""
Simple test script to verify JWT authentication is working
"""
import requests
import json

# Test the authentication endpoints
BASE_URL = "http://localhost:8000"

print("🧪 Testing JWT Authentication...")

# Test 1: Sign up (or sign in if user exists)
print("\n1. Testing sign up/sign in...")
test_user = {
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "testpassword123"
}

# Try to sign in first
try:
    signin_response = requests.post(f"{BASE_URL}/api/auth/signin", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    if signin_response.status_code == 200:
        print("✅ Sign in successful")
        token_data = signin_response.json()
        token = token_data.get("access_token")
    else:
        # Try to sign up
        print("User doesn't exist, trying to sign up...")
        signup_response = requests.post(f"{BASE_URL}/api/auth/signup", json=test_user)
        
        if signup_response.status_code == 201:
            print("✅ Sign up successful")
            # Now sign in
            signin_response = requests.post(f"{BASE_URL}/api/auth/signin", json={
                "email": test_user["email"],
                "password": test_user["password"]
            })
            token_data = signin_response.json()
            token = token_data.get("access_token")
        else:
            print(f"❌ Sign up failed: {signup_response.text}")
            exit(1)

    print(f"Token preview: {token[:20]}...")

    # Test 2: Test authenticated endpoint
    print("\n2. Testing authenticated endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    me_response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    if me_response.status_code == 200:
        print("✅ /api/auth/me successful")
        print(f"User data: {json.dumps(me_response.json(), indent=2)}")
    else:
        print(f"❌ /api/auth/me failed: {me_response.status_code} - {me_response.text}")

    # Test 3: Test file upload endpoint (with dummy file)
    print("\n3. Testing file upload authentication...")
    
    # Create a simple test file content
    test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\ntrailer\n<<\n>>\nstartxref\n9\n%%EOF"
    
    files = {"file": ("test_resume.pdf", test_content, "application/pdf")}
    
    upload_response = requests.post(
        f"{BASE_URL}/api/agents/parse-resume",
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Upload response status: {upload_response.status_code}")
    if upload_response.status_code in [200, 201]:
        print("✅ File upload authentication successful")
        print(f"Response: {upload_response.json()}")
    else:
        print(f"❌ File upload failed: {upload_response.text}")

except Exception as e:
    print(f"❌ Test failed with error: {str(e)}")

print("\n🏁 Test complete!")