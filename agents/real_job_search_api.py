"""
Real Job Search API - Integrates with free job search APIs to get real job listings
Supports JSearch (RapidAPI), Adzuna, and Reed APIs
Created for AI Job Application Agents project
"""

import requests
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class RealJobSearchAPI:
    """Real-time job search using free APIs instead of dummy data"""
    
    def __init__(self):
        # API Configuration
        self.jsearch_api_key = os.getenv("RAPIDAPI_KEY", "")  # Get from RapidAPI
        self.adzuna_app_id = os.getenv("ADZUNA_APP_ID", "")
        self.adzuna_app_key = os.getenv("ADZUNA_APP_KEY", "")
        
        # API Endpoints
        self.jsearch_url = "https://jsearch.p.rapidapi.com/search"
        self.adzuna_base_url = "https://api.adzuna.com/v1/api/jobs"
        
        # Request headers for different APIs
        self.jsearch_headers = {
            "X-RapidAPI-Key": self.jsearch_api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
    
    def search_jobs_jsearch(self, query: str, location: str = "United States", 
                           num_pages: int = 1, page: int = 1) -> Dict[str, Any]:
        """
        Search jobs using JSearch API (via RapidAPI)
        Free tier: 150 requests/month
        Best option for comprehensive job data
        """
        if not self.jsearch_api_key:
            return self._create_error_response("JSearch API key not configured. Get free key from RapidAPI.com")
        
        try:
            params = {
                "query": query,
                "page": str(page),
                "num_pages": str(num_pages),
                "country": "us" if location.lower() in ["united states", "usa", "us"] else "us",
                "employment_types": "FULLTIME,PARTTIME,CONTRACTOR,INTERN"
            }
            
            print(f"🔍 Searching JSearch API for: {query} in {location}")
            response = requests.get(self.jsearch_url, headers=self.jsearch_headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_jsearch_response(data, query, location)
            else:
                error_msg = f"JSearch API error: {response.status_code}"
                if response.status_code == 429:
                    error_msg += " - Rate limit exceeded (150 requests/month limit reached)"
                elif response.status_code == 401:
                    error_msg += " - Invalid API key"
                return self._create_error_response(error_msg)
                
        except Exception as e:
            return self._create_error_response(f"JSearch API request failed: {str(e)}")
    
    def search_jobs_adzuna(self, query: str, location: str = "us", 
                          results_per_page: int = 20, page: int = 1) -> Dict[str, Any]:
        """
        Search jobs using Adzuna API
        Free tier: 1,000 requests/month  
        Good alternative to JSearch
        """
        if not self.adzuna_app_id or not self.adzuna_app_key:
            return self._create_error_response("Adzuna API credentials not configured")
        
        try:
            # Map location to Adzuna country codes
            country_map = {
                "united states": "us",
                "usa": "us",
                "us": "us",
                "uk": "gb",
                "united kingdom": "gb",
                "canada": "ca",
                "australia": "au"
            }
            
            country = country_map.get(location.lower(), "us")
            url = f"{self.adzuna_base_url}/{country}/search/{page}"
            
            params = {
                "app_id": self.adzuna_app_id,
                "app_key": self.adzuna_app_key,
                "results_per_page": results_per_page,
                "what": query,
                "content-type": "application/json"
            }
            
            print(f"🔍 Searching Adzuna API for: {query} in {country.upper()}")
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_adzuna_response(data, query, location)
            else:
                error_msg = f"Adzuna API error: {response.status_code}"
                return self._create_error_response(error_msg)
                
        except Exception as e:
            return self._create_error_response(f"Adzuna API request failed: {str(e)}")
    
    def search_jobs_with_fallback(self, query: str, location: str = "United States", 
                                 max_results: int = 20) -> Dict[str, Any]:
        """
        Smart job search with API fallback
        Tries JSearch first, falls back to Adzuna if needed
        """
        print(f"🚀 Starting job search: '{query}' in {location}")
        
        # Try JSearch first (best results)
        if self.jsearch_api_key:
            result = self.search_jobs_jsearch(query, location, num_pages=1)
            if result.get("success") and len(result.get("jobs", [])) > 0:
                print(f"✅ JSearch returned {len(result['jobs'])} jobs")
                return result
            else:
                print("⚠️ JSearch failed or returned no results, trying Adzuna...")
        else:
            print("⚠️ JSearch API key not configured, trying Adzuna...")
        
        # Fallback to Adzuna
        if self.adzuna_app_id and self.adzuna_app_key:
            result = self.search_jobs_adzuna(query, location, max_results)
            if result.get("success"):
                print(f"✅ Adzuna returned {len(result.get('jobs', []))} jobs")
                return result
            else:
                print("❌ Adzuna also failed")
        else:
            print("⚠️ Adzuna credentials not configured")
        
        # If all APIs fail, return instructive error
        return self._create_setup_instructions()
    
    def _format_jsearch_response(self, data: Dict, query: str, location: str) -> Dict[str, Any]:
        """Format JSearch API response to standardized format"""
        jobs = []
        
        for job_data in data.get("data", []):
            job = {
                "id": job_data.get("job_id", ""),
                "title": job_data.get("job_title", ""),
                "company": job_data.get("employer_name", ""),
                "company_logo": job_data.get("employer_logo"),
                "location": job_data.get("job_city", "") + ", " + job_data.get("job_state", ""),
                "description": job_data.get("job_description", "")[:500] + "...",
                "salary": self._format_salary(
                    job_data.get("job_min_salary"),
                    job_data.get("job_max_salary"),
                    job_data.get("job_salary_currency", "USD")
                ),
                "employment_type": job_data.get("job_employment_type", ""),
                "posted_date": job_data.get("job_posted_at_datetime_utc", ""),
                "apply_link": job_data.get("job_apply_link", ""),
                "source": "JSearch",
                "job_highlights": job_data.get("job_highlights", {})
            }
            jobs.append(job)
        
        return {
            "success": True,
            "api_used": "JSearch (RapidAPI)",
            "search_query": query,
            "location": location,
            "total_results": len(jobs),
            "jobs": jobs,
            "searched_at": datetime.now().isoformat(),
            "api_limit_info": "150 requests/month (Free tier)"
        }
    
    def _format_adzuna_response(self, data: Dict, query: str, location: str) -> Dict[str, Any]:
        """Format Adzuna API response to standardized format"""
        jobs = []
        
        for job_data in data.get("results", []):
            job = {
                "id": job_data.get("id", ""),
                "title": job_data.get("title", ""),
                "company": job_data.get("company", {}).get("display_name", ""),
                "company_logo": None,  # Adzuna doesn't provide logos in free tier
                "location": job_data.get("location", {}).get("display_name", ""),
                "description": job_data.get("description", "")[:500] + "...",
                "salary": self._format_adzuna_salary(job_data),
                "employment_type": job_data.get("contract_type", ""),
                "posted_date": job_data.get("created", ""),
                "apply_link": job_data.get("redirect_url", ""),
                "source": "Adzuna",
                "job_highlights": {}
            }
            jobs.append(job)
        
        return {
            "success": True,
            "api_used": "Adzuna",
            "search_query": query,
            "location": location,
            "total_results": data.get("count", len(jobs)),
            "jobs": jobs,
            "searched_at": datetime.now().isoformat(),
            "api_limit_info": "1,000 requests/month (Free tier)"
        }
    
    def _format_salary(self, min_sal: Optional[float], max_sal: Optional[float], currency: str = "USD") -> str:
        """Format salary information"""
        if not min_sal and not max_sal:
            return "Not specified"
        
        if min_sal and max_sal:
            return f"${min_sal:,.0f} - ${max_sal:,.0f} {currency}"
        elif min_sal:
            return f"${min_sal:,.0f}+ {currency}"
        elif max_sal:
            return f"Up to ${max_sal:,.0f} {currency}"
        
        return "Not specified"
    
    def _format_adzuna_salary(self, job_data: Dict) -> str:
        """Format Adzuna salary data"""
        salary_min = job_data.get("salary_min")
        salary_max = job_data.get("salary_max")
        
        if salary_min or salary_max:
            return self._format_salary(salary_min, salary_max)
        return "Not specified"
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "success": False,
            "error": error_message,
            "jobs": [],
            "searched_at": datetime.now().isoformat()
        }
    
    def _create_setup_instructions(self) -> Dict[str, Any]:
        """Create response with setup instructions for APIs"""
        return {
            "success": False,
            "error": "No job search APIs configured",
            "setup_instructions": {
                "jsearch_rapidapi": {
                    "description": "Best option - aggregates jobs from Google, Indeed, LinkedIn",
                    "signup_url": "https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch",
                    "free_tier": "150 requests/month",
                    "env_variable": "RAPIDAPI_KEY"
                },
                "adzuna": {
                    "description": "Good alternative - direct API access",
                    "signup_url": "https://developer.adzuna.com/",
                    "free_tier": "1,000 requests/month",
                    "env_variables": ["ADZUNA_APP_ID", "ADZUNA_APP_KEY"]
                }
            },
            "next_steps": [
                "1. Sign up for JSearch at RapidAPI (recommended)",
                "2. Get your API key and set RAPIDAPI_KEY environment variable",
                "3. Alternatively, sign up for Adzuna API",
                "4. Restart your application after setting environment variables"
            ],
            "jobs": [],
            "searched_at": datetime.now().isoformat()
        }

# Test function
def test_job_search():
    """Test the job search APIs"""
    api = RealJobSearchAPI()
    
    print("🧪 Testing Job Search APIs...")
    print(f"JSearch API Key configured: {'Yes' if api.jsearch_api_key else 'No'}")
    print(f"Adzuna credentials configured: {'Yes' if api.adzuna_app_id and api.adzuna_app_key else 'No'}")
    
    # Test search
    result = api.search_jobs_with_fallback("Python Developer", "United States", 5)
    
    print("\n📋 Test Results:")
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"API Used: {result.get('api_used')}")
        print(f"Jobs Found: {len(result.get('jobs', []))}")
        
        # Show first job as example
        jobs = result.get('jobs', [])
        if jobs:
            job = jobs[0]
            print(f"\nExample Job:")
            print(f"  Title: {job.get('title')}")
            print(f"  Company: {job.get('company')}")
            print(f"  Location: {job.get('location')}")
            print(f"  Salary: {job.get('salary')}")
    else:
        print(f"Error: {result.get('error')}")
        if result.get('setup_instructions'):
            print("\n📝 Setup Instructions Available")

if __name__ == "__main__":
    test_job_search()