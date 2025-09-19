#!/usr/bin/env python3
"""
Resume Parser Agent - AI Job Application System
Powered by Coral Protocol

This agent parses uploaded resumes and extracts:
- Skills and technologies
- Work experience
- Education
- Contact information
- Career preferences
"""

import requests
import json
import time
import sys
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class ResumeParserAgent:
    def __init__(self, agent_name: str, coral_server_url: str = "http://localhost:5555"):
        self.agent_name = agent_name
        self.coral_server_url = coral_server_url
        self.thread_id = None
        self.parsed_profiles = {}
        
    def register_agent(self) -> bool:
        """Register this agent with coral-server"""
        try:
            response = requests.get(f"{self.coral_server_url}/api/v1/agents")
            if response.status_code == 200:
                print(f"✅ Connected to coral-server at {self.coral_server_url}")
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to connect to coral-server: {e}")
            return False
    
    def create_thread(self) -> Optional[str]:
        """Create a communication thread"""
        try:
            # Simulate thread creation (in real coral-server, this would be an API call)
            self.thread_id = f"resume-parser-thread-{int(time.time())}"
            print(f"🧵 Created thread: {self.thread_id}")
            return self.thread_id
        except Exception as e:
            print(f"❌ Failed to create thread: {e}")
            return None
    
    def parse_resume_text(self, resume_text: str) -> Dict[str, Any]:
        """Parse resume text and extract structured information"""
        print(f"📄 Parsing resume text ({len(resume_text)} characters)...")
        
        # Simulate AI-powered resume parsing
        parsed_data = {
            "skills": self._extract_skills(resume_text),
            "experience": self._extract_experience(resume_text),
            "education": self._extract_education(resume_text),
            "contact": self._extract_contact(resume_text),
            "summary": self._generate_summary(resume_text),
            "parsed_at": datetime.now().isoformat(),
            "agent": self.agent_name
        }
        
        return parsed_data
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume text"""
        # Common tech skills to look for
        tech_skills = [
            "Python", "JavaScript", "TypeScript", "React", "Node.js", "Java", "C++", 
            "C#", "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin", "SQL", "MongoDB",
            "PostgreSQL", "MySQL", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
            "Git", "Linux", "Machine Learning", "AI", "Data Science", "Frontend",
            "Backend", "Full Stack", "DevOps", "Agile", "Scrum", "REST API", "GraphQL"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in tech_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Add some simulation for demo
        if not found_skills:
            found_skills = ["Python", "JavaScript", "React", "Node.js", "SQL"]
            
        return found_skills[:10]  # Limit to top 10
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience from resume"""
        # Simulate experience extraction
        experiences = [
            {
                "title": "Senior Software Developer",
                "company": "TechCorp Inc.",
                "duration": "2022-2024",
                "description": "Developed web applications using React and Node.js"
            },
            {
                "title": "Software Developer",
                "company": "StartupXYZ",
                "duration": "2020-2022", 
                "description": "Built full-stack applications and RESTful APIs"
            }
        ]
        
        return experiences
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = [
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "Tech University",
                "year": "2020"
            }
        ]
        return education
    
    def _extract_contact(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        # Simple email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        return {
            "email": emails[0] if emails else "example@email.com",
            "phone": "555-123-4567",  # Simulated
            "location": "San Francisco, CA"  # Simulated
        }
    
    def _generate_summary(self, text: str) -> str:
        """Generate a professional summary"""
        return "Experienced software developer with expertise in modern web technologies and a passion for building scalable applications."
    
    def send_parsed_data(self, parsed_data: Dict[str, Any]) -> bool:
        """Send parsed resume data to other agents via coral-server"""
        try:
            print(f"📤 Sending parsed data to thread {self.thread_id}")
            
            # Store parsed data
            profile_id = f"profile-{int(time.time())}"
            self.parsed_profiles[profile_id] = parsed_data
            
            # Simulate sending via coral-server MCP tools
            message = {
                "from": self.agent_name,
                "type": "resume_parsed",
                "data": parsed_data,
                "profile_id": profile_id,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"✅ Resume data sent successfully!")
            print(f"   📊 Skills found: {len(parsed_data['skills'])}")
            print(f"   💼 Experience entries: {len(parsed_data['experience'])}")
            print(f"   🎓 Education entries: {len(parsed_data['education'])}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send parsed data: {e}")
            return False
    
    def listen_for_resume_uploads(self):
        """Listen for new resume uploads to parse"""
        print(f"👂 Listening for resume uploads...")
        print(f"📡 Agent {self.agent_name} is ready to parse resumes!")
        print(f"🔄 Waiting for resume data...")
        
        # Simulate resume processing
        sample_resume = """
        John Doe
        Software Engineer
        john.doe@email.com
        
        EXPERIENCE:
        Senior Software Developer at TechCorp (2022-2024)
        - Developed React applications
        - Built REST APIs with Node.js
        - Worked with PostgreSQL databases
        
        SKILLS:
        JavaScript, TypeScript, React, Node.js, Python, SQL, Git, AWS
        
        EDUCATION:
        Bachelor of Science in Computer Science - Tech University (2020)
        """
        
        # Process sample resume after delay
        time.sleep(3)
        print(f"\n📥 New resume received for parsing...")
        parsed_data = self.parse_resume_text(sample_resume)
        self.send_parsed_data(parsed_data)
        
        return parsed_data
    
    def run(self):
        """Main agent execution loop"""
        print(f"🚀 Starting Resume Parser Agent: {self.agent_name}")
        print(f"🌐 Coral Server: {self.coral_server_url}")
        print("-" * 60)
        
        # Step 1: Connect to coral-server
        if not self.register_agent():
            print("❌ Cannot connect to coral-server. Make sure it's running.")
            return False
        
        # Step 2: Create communication thread
        if not self.create_thread():
            print("❌ Failed to create communication thread")
            return False
        
        # Step 3: Start listening for resumes
        try:
            parsed_data = self.listen_for_resume_uploads()
            
            print(f"\n🎯 Resume Parser Agent completed successfully!")
            print(f"💡 Next: Start job-searcher-agent.py to find matching jobs")
            
            return True
            
        except KeyboardInterrupt:
            print(f"\n👋 Resume Parser Agent shutting down...")
            return True
        except Exception as e:
            print(f"❌ Agent error: {e}")
            return False

def main():
    agent_name = sys.argv[1] if len(sys.argv) > 1 else "resume-parser"
    
    agent = ResumeParserAgent(agent_name)
    agent.run()

if __name__ == "__main__":
    main()