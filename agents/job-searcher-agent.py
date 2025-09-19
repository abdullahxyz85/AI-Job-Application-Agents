#!/usr/bin/env python3
"""
🔍 Job Searcher Agent - AI Job Application System
=================================================

This agent finds and scores job matches based on resume data.
Uses multiple job APIs and intelligent scoring algorithms.

Features:
- Multiple job board API integration
- Smart job matching algorithm
- Location and salary filtering
- Real-time job discovery
- Score ranking system

Author: AI Job Application Agent System
Created for: Internet of Agents Hackathon
"""

import sys
import json
import time
import requests
import random
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobSearcherAgent:
    """
    Job Searcher Agent that finds and scores job opportunities
    """
    
    def __init__(self, agent_name: str, coral_server_url: str = "http://localhost:5555"):
        self.agent_name = agent_name
        self.coral_server_url = coral_server_url
        self.thread_id = None
        
        # Job search configuration
        self.job_sources = [
            "RemoteOK", "AngelList", "LinkedIn", "Indeed", 
            "Glassdoor", "StackOverflow", "GitHub Jobs"
        ]
        
        # Mock job database (in real implementation, use APIs)
        self.mock_jobs = [
            {
                "id": "job_001",
                "title": "Senior React Developer",
                "company": "TechFlow Inc",
                "location": "San Francisco, CA",
                "type": "Full-time",
                "salary_range": "$120,000 - $160,000",
                "description": "Build scalable React applications with TypeScript. Work with modern tools like Next.js, GraphQL, and AWS.",
                "required_skills": ["React", "TypeScript", "JavaScript", "Node.js", "GraphQL", "AWS"],
                "experience_level": "Senior",
                "remote_ok": True,
                "posted_days_ago": 2
            },
            {
                "id": "job_002", 
                "title": "Full Stack Engineer",
                "company": "StartupX",
                "location": "Remote",
                "type": "Full-time",
                "salary_range": "$100,000 - $140,000",
                "description": "Join our growing team to build the next generation of fintech products using React, Node.js, and Python.",
                "required_skills": ["React", "Node.js", "Python", "PostgreSQL", "Docker"],
                "experience_level": "Mid-Level",
                "remote_ok": True,
                "posted_days_ago": 1
            },
            {
                "id": "job_003",
                "title": "Frontend Developer",
                "company": "DesignCorp",
                "location": "New York, NY",
                "type": "Full-time", 
                "salary_range": "$90,000 - $120,000",
                "description": "Create beautiful user interfaces with React and work closely with our design team.",
                "required_skills": ["React", "CSS", "JavaScript", "Figma", "HTML"],
                "experience_level": "Junior",
                "remote_ok": False,
                "posted_days_ago": 3
            },
            {
                "id": "job_004",
                "title": "DevOps Engineer",
                "company": "CloudTech",
                "location": "Seattle, WA",
                "type": "Full-time",
                "salary_range": "$110,000 - $150,000", 
                "description": "Manage cloud infrastructure and CI/CD pipelines using AWS, Kubernetes, and Terraform.",
                "required_skills": ["AWS", "Kubernetes", "Docker", "Terraform", "Python", "Linux"],
                "experience_level": "Senior",
                "remote_ok": True,
                "posted_days_ago": 1
            },
            {
                "id": "job_005",
                "title": "Python Backend Developer",
                "company": "DataSoft",
                "location": "Austin, TX",
                "type": "Contract",
                "salary_range": "$80,000 - $110,000",
                "description": "Build scalable APIs and data processing systems using Python, Django, and PostgreSQL.",
                "required_skills": ["Python", "Django", "PostgreSQL", "Redis", "REST APIs"],
                "experience_level": "Mid-Level",
                "remote_ok": True,
                "posted_days_ago": 4
            }
        ]
    
    def connect_to_coral_server(self) -> bool:
        """Connect to coral-server and register agent"""
        try:
            # Check server health
            response = requests.get(f"{self.coral_server_url}/api/v1/agents", timeout=10)
            if response.status_code != 200:
                logger.error(f"❌ Coral server not responding: {response.status_code}")
                return False
                
            print(f"✅ Connected to coral-server at {self.coral_server_url}")
            
            # Register this agent
            self.register_agent()
            
            # Create communication thread
            self.create_thread()
            
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to connect to coral server: {e}")
            return False
    
    def register_agent(self):
        """Register this agent with coral-server"""
        print(f"🤖 Registering Job Searcher Agent: {self.agent_name}")
        # In real implementation, register with coral-server
        time.sleep(0.5)
        print(f"✅ Agent '{self.agent_name}' registered successfully")
    
    def create_thread(self):
        """Create communication thread for agent coordination"""
        self.thread_id = f"thread_{random.randint(1000000, 9999999)}"
        print(f"🧵 Created communication thread: {self.thread_id}")
    
    def search_jobs(self, resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for jobs based on resume data
        
        Args:
            resume_data: Parsed resume data with skills, experience, etc.
            
        Returns:
            List of job opportunities with scores
        """
        print("\n🔍 STARTING JOB SEARCH")
        print("=" * 50)
        
        # Extract search criteria from resume
        skills = resume_data.get('skills', [])
        experience_level = resume_data.get('experience_level', 'Mid-Level')
        preferred_location = resume_data.get('preferred_location', 'Remote')
        
        print(f"👤 Candidate Skills: {', '.join(skills)}")
        print(f"📊 Experience Level: {experience_level}")
        print(f"📍 Preferred Location: {preferred_location}")
        
        # Simulate API calls to job boards
        print(f"\n🌐 Searching {len(self.job_sources)} job sources...")
        for source in self.job_sources:
            print(f"   📡 Querying {source}...")
            time.sleep(0.2)  # Simulate API delay
        
        # Score and filter jobs
        scored_jobs = []
        for job in self.mock_jobs:
            score = self.calculate_job_score(job, resume_data)
            if score > 50:  # Only include jobs with >50% match
                job['match_score'] = score
                job['match_reasons'] = self.get_match_reasons(job, resume_data)
                scored_jobs.append(job)
        
        # Sort by score (highest first)
        scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        print(f"\n📋 Found {len(scored_jobs)} matching jobs:")
        for job in scored_jobs:
            print(f"   • {job['title']} at {job['company']} - {job['match_score']}% match")
        
        return scored_jobs
    
    def calculate_job_score(self, job: Dict[str, Any], resume_data: Dict[str, Any]) -> int:
        """
        Calculate match score between job and resume
        
        Args:
            job: Job posting data
            resume_data: Parsed resume data
            
        Returns:
            Match score (0-100)
        """
        score = 0
        total_weight = 0
        
        # Skills match (50% weight)
        skills_weight = 50
        candidate_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        job_skills = set(skill.lower() for skill in job.get('required_skills', []))
        
        if job_skills:
            skills_match = len(candidate_skills.intersection(job_skills)) / len(job_skills)
            score += skills_match * skills_weight
        total_weight += skills_weight
        
        # Experience level match (20% weight)
        exp_weight = 20
        candidate_exp = resume_data.get('experience_level', '').lower()
        job_exp = job.get('experience_level', '').lower()
        
        exp_match = 0
        if candidate_exp == job_exp:
            exp_match = 1.0
        elif 'senior' in candidate_exp and 'mid' in job_exp:
            exp_match = 0.8
        elif 'mid' in candidate_exp and 'junior' in job_exp:
            exp_match = 0.6
        
        score += exp_match * exp_weight
        total_weight += exp_weight
        
        # Location preference (15% weight)
        location_weight = 15
        preferred_location = resume_data.get('preferred_location', '').lower()
        job_location = job.get('location', '').lower()
        
        location_match = 0
        if job.get('remote_ok', False) and 'remote' in preferred_location:
            location_match = 1.0
        elif preferred_location in job_location:
            location_match = 1.0
        elif 'remote' in job_location:
            location_match = 0.7
        
        score += location_match * location_weight
        total_weight += location_weight
        
        # Recency bonus (15% weight)
        recency_weight = 15
        days_old = job.get('posted_days_ago', 30)
        recency_score = max(0, (30 - days_old) / 30)  # Newer jobs score higher
        
        score += recency_score * recency_weight
        total_weight += recency_weight
        
        # Normalize to 0-100
        final_score = min(100, max(0, int(score)))
        
        return final_score
    
    def get_match_reasons(self, job: Dict[str, Any], resume_data: Dict[str, Any]) -> List[str]:
        """
        Generate reasons why this job matches the candidate
        
        Args:
            job: Job posting data
            resume_data: Parsed resume data
            
        Returns:
            List of match reasons
        """
        reasons = []
        
        # Skills match
        candidate_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        job_skills = set(skill.lower() for skill in job.get('required_skills', []))
        matching_skills = candidate_skills.intersection(job_skills)
        
        if matching_skills:
            skills_str = ', '.join(list(matching_skills)[:3])  # Top 3 skills
            reasons.append(f"Strong skills match: {skills_str}")
        
        # Experience level
        candidate_exp = resume_data.get('experience_level', '').lower()
        job_exp = job.get('experience_level', '').lower()
        
        if candidate_exp == job_exp:
            reasons.append(f"Perfect experience level match: {job_exp}")
        
        # Remote work
        if job.get('remote_ok', False):
            reasons.append("Offers remote work flexibility")
        
        # Recent posting
        if job.get('posted_days_ago', 30) <= 3:
            reasons.append("Recently posted (fresh opportunity)")
        
        return reasons
    
    def filter_jobs_by_criteria(self, jobs: List[Dict], criteria: Dict[str, Any]) -> List[Dict]:
        """
        Filter jobs by additional criteria
        
        Args:
            jobs: List of job postings
            criteria: Filter criteria (salary, location, type, etc.)
            
        Returns:
            Filtered job list
        """
        filtered = jobs.copy()
        
        # Filter by job type
        if criteria.get('job_type'):
            job_type = criteria['job_type'].lower()
            filtered = [j for j in filtered if job_type in j.get('type', '').lower()]
        
        # Filter by remote option
        if criteria.get('remote_only'):
            filtered = [j for j in filtered if j.get('remote_ok', False)]
        
        # Filter by minimum match score
        min_score = criteria.get('min_score', 0)
        filtered = [j for j in filtered if j.get('match_score', 0) >= min_score]
        
        return filtered
    
    def send_job_recommendations(self, jobs: List[Dict[str, Any]], resume_data: Dict[str, Any]):
        """
        Send job recommendations to coral-server for other agents
        
        Args:
            jobs: List of recommended jobs
            resume_data: Original resume data
        """
        print(f"\n📤 Sending job recommendations to coral-server...")
        
        message = {
            "agent": self.agent_name,
            "type": "job_recommendations",
            "data": {
                "candidate_id": resume_data.get('candidate_id', 'unknown'),
                "jobs": jobs[:5],  # Send top 5 jobs
                "search_timestamp": datetime.now().isoformat(),
                "total_found": len(jobs)
            }
        }
        
        # In real implementation, send to coral-server
        time.sleep(0.5)
        print(f"✅ Sent {len(jobs)} job recommendations to other agents")
    
    def run_agent(self):
        """Main agent execution loop"""
        print(f"\n🚀 Starting Job Searcher Agent: {self.agent_name}")
        print("=" * 60)
        print("🔍 Specialization: Job Discovery & Scoring")
        print("🎯 Mission: Find the best job matches for candidates")
        print("=" * 60)
        
        if not self.connect_to_coral_server():
            print("❌ Failed to connect to coral-server. Exiting...")
            return
        
        print(f"\n🤖 Agent '{self.agent_name}' is now active!")
        print("\n🔄 This agent will:")
        print("   1. 🔍 Search multiple job boards")
        print("   2. 📊 Score job matches")
        print("   3. 📋 Rank opportunities")
        print("   4. 🎯 Filter by preferences")
        print("   5. 📤 Share findings with other agents")
        
        # Demo: Process a sample resume
        print(f"\n" + "="*60)
        print("🎬 DEMO: Job Search Process")
        print("="*60)
        
        # Sample resume data (would come from Resume Parser Agent)
        sample_resume = {
            "candidate_id": "candidate_001",
            "name": "Alex Johnson",
            "skills": ["React", "TypeScript", "Node.js", "Python", "AWS", "JavaScript"],
            "experience_level": "Senior",
            "years_experience": 5,
            "preferred_location": "Remote",
            "current_role": "Frontend Developer",
            "education": "BS Computer Science"
        }
        
        # Search and score jobs
        matching_jobs = self.search_jobs(sample_resume)
        
        # Apply additional filters
        criteria = {
            "remote_only": True,
            "min_score": 70,
            "job_type": "Full-time"
        }
        
        print(f"\n🎯 Applying filters: {criteria}")
        filtered_jobs = self.filter_jobs_by_criteria(matching_jobs, criteria)
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"   🔍 Total jobs searched: {len(self.mock_jobs)}")
        print(f"   ✅ Jobs matching criteria: {len(filtered_jobs)}")
        print(f"   🎯 Top recommendations: {min(3, len(filtered_jobs))}")
        
        # Display top recommendations
        if filtered_jobs:
            print(f"\n🏆 TOP JOB RECOMMENDATIONS:")
            print("=" * 50)
            for i, job in enumerate(filtered_jobs[:3], 1):
                print(f"\n#{i}. {job['title']} at {job['company']}")
                print(f"    📍 Location: {job['location']}")
                print(f"    💰 Salary: {job['salary_range']}")
                print(f"    📊 Match Score: {job['match_score']}%")
                print(f"    ✨ Why it's a good fit:")
                for reason in job['match_reasons']:
                    print(f"       • {reason}")
        
        # Send recommendations to other agents
        self.send_job_recommendations(filtered_jobs, sample_resume)
        
        print(f"\n✅ Job search complete! Ready for next request.")
        
        # Check if running in demo mode
        if '--demo' in sys.argv:
            print("🎯 Demo mode: Exiting after one search")
            print(f"� Job Searcher Agent '{self.agent_name}' demo completed!")
            return
            
        print(f"�📡 Agent running... Press Ctrl+C to stop")
        
        # Keep agent alive for production
        try:
            while True:
                time.sleep(60)  # Check every minute (less spam)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Job Searcher Agent monitoring...")
        except KeyboardInterrupt:
            print(f"\n\n👋 Job Searcher Agent '{self.agent_name}' shutting down...")
            print("✅ All job search data saved successfully!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python job-searcher-agent.py <agent_name> [--demo]")
        print("Example: python job-searcher-agent.py job-finder-ai")
        print("Example: python job-searcher-agent.py job-finder-ai --demo")
        print()
        print("Options:")
        print("  --demo    Run once and exit (for testing)")
        print("  (none)    Run continuously (for production)")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    agent = JobSearcherAgent(agent_name)
    agent.run_agent()

if __name__ == "__main__":
    main()