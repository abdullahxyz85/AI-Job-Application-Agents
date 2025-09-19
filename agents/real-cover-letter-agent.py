#!/usr/bin/env python3
"""
Coral Protocol Cover Letter Agent with Real AIML API
====================================================
Official integration for Internet of Agents Hackathon
"""

import os
import sys
import json
import time
import asyncio
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RealTimeCoverLetterAgent:
    """Cover Letter Agent with Real-time LLM via AIML API"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        
        # Initialize AIML API client
        self.llm_client = OpenAI(
            base_url=os.getenv("MODEL_BASE_URL", "https://api.aimlapi.com/v1"),
            api_key=os.getenv("AIML_API_KEY")
        )
        
        self.model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        
        # Coral server settings
        self.coral_server = "http://localhost:5555"
        self.session_url = f"{self.coral_server}/devmode/hackathonApp/privkey/session1"
        
    def generate_real_cover_letter(self, resume_data, job_data, style="professional"):
        """Generate cover letter using real LLM"""
        print(f"Generating {style} cover letter with AIML API...")
        
        # Create detailed prompt
        prompt = f"""Write a {style} cover letter for this job application:

CANDIDATE:
- Name: {resume_data.get('name', 'Alex Johnson')}
- Skills: {', '.join(resume_data.get('skills', ['React', 'TypeScript', 'Node.js']))}
- Experience: {resume_data.get('experience_level', 'Senior')} level

JOB:
- Position: {job_data.get('title', 'Senior Full Stack Developer')}
- Company: {job_data.get('company', 'TechFlow Inc')}
- Location: {job_data.get('location', 'San Francisco, CA')}

Requirements:
- {style} tone and language
- Highlight matching skills and experience
- Professional formatting with greeting and closing
- 3-4 paragraphs, approximately 150-200 words
- Personalized for the specific company and role

Generate the complete cover letter:"""

        try:
            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are an expert {style} cover letter writer who creates compelling, personalized cover letters."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            cover_letter = response.choices[0].message.content
            
            print(f"SUCCESS: Generated {len(cover_letter.split())} word cover letter")
            return cover_letter
            
        except Exception as e:
            print(f"LLM Error: {e}")
            return self.fallback_cover_letter(resume_data, job_data)
    
    def fallback_cover_letter(self, resume_data, job_data):
        """Fallback if LLM fails"""
        return f"""Dear Hiring Manager,

I am writing to express my interest in the {job_data.get('title', 'position')} role at {job_data.get('company', 'your company')}. 

With my experience in {', '.join(resume_data.get('skills', [])[:2])}, I am confident I can contribute effectively to your team.

Thank you for your consideration.

Best regards,
{resume_data.get('name', 'Candidate')}"""
    
    def communicate_with_coral_server(self, message_data):
        """Send data to coral server (simulation for now)"""
        print(f"Sending to Coral Protocol: {message_data['type']}")
        print(f"Data: {json.dumps(message_data, indent=2)}")
        
        # In a real implementation, this would use the Coral Protocol MCP
        # For now, we simulate the communication
        return {"status": "sent", "timestamp": datetime.now().isoformat()}
    
    def run_demo(self):
        """Run real-time cover letter generation demo"""
        print("="*60)
        print("CORAL PROTOCOL COVER LETTER AGENT")
        print("="*60)
        print(f"Agent: {self.agent_name}")
        print(f"LLM Model: {self.model_name}")
        print(f"Base URL: {self.llm_client.base_url}")
        print(f"Coral Server: {self.coral_server}")
        print("="*60)
        
        # Sample data (would come from other agents in real system)
        sample_resume = {
            "name": "Alex Johnson",
            "skills": ["React", "TypeScript", "Node.js", "Python", "AWS"],
            "experience_level": "Senior",
            "years_experience": "6+"
        }
        
        sample_job = {
            "title": "Senior Full Stack Developer", 
            "company": "TechFlow Inc",
            "location": "San Francisco, CA (Remote)",
            "requirements": ["React", "TypeScript", "Node.js", "AWS"]
        }
        
        print("\nDEMO: Real-time Cover Letter Generation")
        print("-"*50)
        
        # Generate cover letter using real LLM
        cover_letter = self.generate_real_cover_letter(
            sample_resume, sample_job, "professional"
        )
        
        print("\nGENERATED COVER LETTER:")
        print("="*50)
        print(cover_letter)
        print("="*50)
        
        # Prepare data for other agents
        cover_letter_data = {
            "type": "cover_letter_generated",
            "agent": self.agent_name,
            "candidate": sample_resume["name"],
            "job_title": sample_job["title"],
            "company": sample_job["company"],
            "content": cover_letter,
            "word_count": len(cover_letter.split()),
            "generated_at": datetime.now().isoformat(),
            "model_used": self.model_name
        }
        
        # Send to Coral Protocol
        result = self.communicate_with_coral_server(cover_letter_data)
        print(f"Coral Protocol Response: {result['status']}")
        
        print("\nSUCCESS: Real-time LLM integration complete!")
        print("Agent is ready for multi-agent collaboration")
        
        # Demo mode check
        if '--demo' in sys.argv:
            print("Demo complete - exiting")
            return
        
        print("\nAgent running... Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(30)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Cover Letter Agent active...")
        except KeyboardInterrupt:
            print(f"\nAgent {self.agent_name} shutting down...")

def main():
    if len(sys.argv) < 2:
        print("Usage: python real-cover-letter-agent.py <agent_name> [--demo]")
        print("Example: python real-cover-letter-agent.py cover-letter-ai --demo")
        sys.exit(1)
    
    # Check API key
    api_key = os.getenv("AIML_API_KEY")
    if not api_key:
        print("ERROR: AIML_API_KEY not set in .env file")
        print("Set your API key from https://aimlapi.com")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    agent = RealTimeCoverLetterAgent(agent_name)
    agent.run_demo()

if __name__ == "__main__":
    main()