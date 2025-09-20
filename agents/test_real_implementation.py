"""
Simple test script to verify our real-time resume parsing and job search implementation
"""

import sys
sys.path.append('.')

from real_resume_parser import RealResumeParser
from real_job_search_api import RealJobSearchAPI

def test_resume_parser():
    """Test the resume parser with sample text"""
    print("🧪 Testing Resume Parser")
    print("=" * 30)
    
    parser = RealResumeParser()
    
    # Sample resume text (simulates PDF content)
    sample_text = """
    John Doe
    Software Engineer
    john.doe@email.com | (555) 123-4567
    LinkedIn: linkedin.com/in/johndoe
    
    Professional Summary:
    Experienced software developer with 5+ years of experience in Python, React, and cloud technologies.
    
    Technical Skills:
    - Programming Languages: Python, JavaScript, TypeScript, Java
    - Frameworks: React, Django, FastAPI, Node.js
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS, Docker, Kubernetes
    - Tools: Git, Jenkins, Docker
    
    Experience:
    Senior Software Engineer at TechCorp (2021-2024)
    - Developed microservices using Python and FastAPI
    - Built React frontend applications
    - Implemented CI/CD pipelines
    
    Education:
    Bachelor of Science in Computer Science
    University of Technology, 2019
    """
    
    # Test individual components
    contact = parser.extract_contact_info(sample_text)
    skills = parser.extract_skills(sample_text)
    experience = parser.extract_experience_level(sample_text)
    education = parser.extract_education(sample_text)
    summary = parser.extract_summary(sample_text)
    
    print("📋 Results:")
    print(f"   👤 Name: {contact.get('name', 'Not found')}")
    print(f"   📧 Email: {contact.get('email', 'Not found')}")
    print(f"   📱 Phone: {contact.get('phone', 'Not found')}")
    print(f"   🔗 LinkedIn: {contact.get('linkedin', 'Not found')}")
    print(f"   🔧 Skills found: {len(skills)}")
    print(f"   📊 Experience level: {experience.get('level', 'Not specified')}")
    print(f"   📚 Education: {', '.join(education) if education else 'Not found'}")
    
    if len(skills) > 0:
        print(f"   🎯 Top skills: {', '.join(skills[:5])}")
    
    return len(skills) > 0

def test_job_search():
    """Test the job search API"""
    print("\n🧪 Testing Job Search API")
    print("=" * 30)
    
    api = RealJobSearchAPI()
    
    # Check API configuration
    print(f"JSearch API configured: {'✅' if api.jsearch_api_key else '❌'}")
    print(f"Adzuna API configured: {'✅' if (api.adzuna_app_id and api.adzuna_app_key) else '❌'}")
    
    # Test search (will show setup instructions if no APIs configured)
    result = api.search_jobs_with_fallback("Python Developer", "United States", 3)
    
    print("\n📋 Results:")
    print(f"   ✅ Success: {result.get('success')}")
    
    if result.get('success'):
        jobs = result.get('jobs', [])
        print(f"   💼 Jobs found: {len(jobs)}")
        print(f"   🔧 API used: {result.get('api_used', 'Unknown')}")
        
        if jobs:
            job = jobs[0]
            print(f"\n   🎯 Example job:")
            print(f"      Title: {job.get('title', 'N/A')}")
            print(f"      Company: {job.get('company', 'N/A')}")
            print(f"      Location: {job.get('location', 'N/A')}")
            print(f"      Salary: {job.get('salary', 'N/A')}")
    else:
        print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
        if result.get('setup_instructions'):
            print("\n   📝 Setup instructions available - run setup_api_keys.py")
    
    return result.get('success', False)

def main():
    """Main test function"""
    print("🚀 Real-Time Job Application Agent Test")
    print("=" * 50)
    
    # Test resume parsing
    resume_success = test_resume_parser()
    
    # Test job search
    job_success = test_job_search()
    
    # Summary
    print("\n🎯 Test Summary")
    print("=" * 20)
    print(f"Resume Parsing: {'✅ Working' if resume_success else '❌ Failed'}")
    print(f"Job Search API: {'✅ Working' if job_success else '⚠️ Need API keys'}")
    
    if not job_success:
        print("\n📋 Next Steps:")
        print("1. Run: python setup_api_keys.py")
        print("2. Get free API key from JSearch or Adzuna")
        print("3. Configure your .env file")
        print("4. Test again!")
    else:
        print("\n🎉 All systems working! Your real-time implementation is ready!")

if __name__ == "__main__":
    main()