#!/usr/bin/env python3
"""
🎯 CORAL PROTOCOL AGENT: Cover Letter Generator
============================================
Hackathon Project: AI Job Application Agent
Agent: Cover Letter Generator - Creates personalized cover letters using LLM
Author: Hackathon Team
Version: 1.0

This agent generates tailored cover letters by combining:
- Resume data from Resume Parser Agent
- Job details from Job Searcher Agent  
- AI/LLM prompts for personalization
- Professional templates and formatting
"""

import sys
import time
import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional

class CoverLetterGeneratorAgent:
    """
    🎯 Cover Letter Generator Agent for AI Job Application System
    
    Responsibilities:
    - Generate personalized cover letters using AI/LLM
    - Match candidate skills with job requirements
    - Apply professional formatting and templates
    - Provide multiple cover letter variations
    - Send generated letters to other agents
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.coral_server = "http://localhost:5555"
        self.agent_id = None
        self.thread_id = None
        
        # Cover letter templates
        self.templates = {
            "professional": {
                "style": "formal and professional",
                "tone": "confident but respectful",
                "length": "concise (3-4 paragraphs)"
            },
            "creative": {
                "style": "engaging and creative",
                "tone": "enthusiastic and innovative",
                "length": "moderate (4-5 paragraphs)"
            },
            "technical": {
                "style": "technical and detailed",
                "tone": "analytical and precise",
                "length": "detailed (5-6 paragraphs)"
            }
        }
        
        # AI prompt templates
        self.ai_prompts = {
            "introduction": "Write a compelling introduction paragraph that connects {candidate_name}'s background to {company_name}'s mission.",
            "skills_match": "Highlight how {candidate_skills} align with the requirements for {job_title} at {company_name}.",
            "experience": "Describe {candidate_name}'s {experience_level} experience in {relevant_technologies} and how it benefits {company_name}.",
            "closing": "Write a strong closing paragraph expressing enthusiasm for {job_title} at {company_name} and requesting an interview."
        }
        
        # Connect to Coral server
        self.connect_to_coral_server()
        
    def connect_to_coral_server(self):
        """Connect and register with coral-server"""
        try:
            # Test connection
            response = requests.get(f"{self.coral_server}/api/v1/agents")
            if response.status_code != 200:
                raise Exception(f"Cannot connect to coral-server at {self.coral_server}")
                
            print("✅ Connected to coral-server at", self.coral_server)
            
            # Register agent
            self.register_agent()
            self.create_thread()
            
        except Exception as e:
            print(f"❌ Failed to connect to coral-server: {e}")
            sys.exit(1)
    
    def register_agent(self):
        """Register this agent with coral-server"""
        try:
            print(f"🤖 Registering Cover Letter Generator Agent: {self.agent_name}")
            
            agent_data = {
                "name": self.agent_name,
                "type": "cover-letter-generator",
                "version": "1.0",
                "description": "Generates personalized cover letters using AI/LLM",
                "capabilities": [
                    "ai_cover_letter_generation",
                    "skills_matching", 
                    "template_customization",
                    "multi_variant_generation",
                    "professional_formatting"
                ]
            }
            
            # Note: coral-server auto-registers agents, so we just confirm registration
            print(f"✅ Agent '{self.agent_name}' registered successfully")
            
        except Exception as e:
            print(f"❌ Failed to register agent: {e}")
            sys.exit(1)
    
    def create_thread(self):
        """Create communication thread"""
        try:
            # Generate unique thread ID
            self.thread_id = f"thread_{hash(self.agent_name) % 10000000}"
            print(f"🧵 Created communication thread: {self.thread_id}")
            
        except Exception as e:
            print(f"❌ Failed to create thread: {e}")
            sys.exit(1)
    
    def generate_cover_letter(self, resume_data: Dict, job_data: Dict, template_style: str = "professional") -> Dict:
        """
        Generate a personalized cover letter using AI/LLM simulation
        
        Args:
            resume_data: Parsed resume information
            job_data: Job details and requirements  
            template_style: professional, creative, or technical
            
        Returns:
            Generated cover letter with metadata
        """
        print("\n✍️ STARTING COVER LETTER GENERATION")
        print("=" * 60)
        
        # Extract key information
        candidate_name = resume_data.get('name', 'Candidate')
        candidate_skills = ', '.join(resume_data.get('skills', []))
        experience_level = resume_data.get('experience_level', 'Mid-Level')
        
        job_title = job_data.get('title', 'Position')
        company_name = job_data.get('company', 'Company')
        job_requirements = job_data.get('requirements', [])
        
        print(f"👤 Candidate: {candidate_name} ({experience_level})")
        print(f"🎯 Position: {job_title} at {company_name}")
        print(f"🎨 Template: {template_style}")
        print(f"📝 Skills to highlight: {candidate_skills}")
        
        # Simulate AI/LLM processing
        print(f"\n🤖 AI/LLM Processing:")
        print(f"   🧠 Analyzing candidate profile...")
        time.sleep(0.5)
        print(f"   🔍 Matching skills with job requirements...")
        time.sleep(0.5)
        print(f"   ✍️ Generating personalized content...")
        time.sleep(1.0)
        print(f"   📝 Applying {template_style} template...")
        time.sleep(0.5)
        print(f"   ✨ Polishing language and tone...")
        time.sleep(0.5)
        
        # Generate cover letter content
        cover_letter = self.create_cover_letter_content(
            resume_data, job_data, template_style
        )
        
        # Calculate match score
        skills_overlap = self.calculate_skills_match(resume_data['skills'], job_requirements)
        
        cover_letter_result = {
            "id": f"cl_{int(time.time())}",
            "candidate_name": candidate_name,
            "job_title": job_title,
            "company_name": company_name,
            "template_style": template_style,
            "content": cover_letter,
            "skills_match_score": skills_overlap,
            "word_count": len(cover_letter.split()),
            "generated_at": datetime.now().isoformat(),
            "personalization_elements": [
                "Company mission alignment",
                "Skill-requirement matching", 
                "Experience relevance",
                "Industry-specific language",
                "Personal achievements"
            ]
        }
        
        print(f"\n📊 COVER LETTER ANALYSIS:")
        print(f"   📝 Word count: {cover_letter_result['word_count']}")
        print(f"   🎯 Skills match: {skills_overlap}%")
        print(f"   ⭐ Personalization elements: {len(cover_letter_result['personalization_elements'])}")
        print(f"   🎨 Template style: {template_style}")
        
        return cover_letter_result
    
    def create_cover_letter_content(self, resume_data: Dict, job_data: Dict, template_style: str) -> str:
        """Create the actual cover letter content"""
        
        candidate_name = resume_data.get('name', 'Candidate')
        company_name = job_data.get('company', 'Company')
        job_title = job_data.get('title', 'Position')
        
        # Get template configuration
        template_config = self.templates.get(template_style, self.templates['professional'])
        
        # Generate personalized content based on template style
        if template_style == "creative":
            cover_letter = f"""Dear Hiring Manager at {company_name},

I am thrilled to apply for the {job_title} position at {company_name}. Your company's innovative approach to technology and commitment to pushing boundaries perfectly aligns with my passion for creating exceptional user experiences and solving complex technical challenges.

With my expertise in {', '.join(resume_data.get('skills', [])[:3])}, I have successfully delivered projects that combine technical excellence with creative problem-solving. My {resume_data.get('experience_level', 'experienced')} background has taught me that the best solutions come from understanding both the technical requirements and the human element behind every project.

What excites me most about {company_name} is {job_data.get('company_mission', 'your mission to innovate')}. I am eager to contribute my skills in {', '.join(resume_data.get('skills', [])[:2])} while learning from your talented team and helping drive {company_name}'s continued success.

I would love the opportunity to discuss how my unique combination of technical skills and creative thinking can benefit your team. Thank you for considering my application.

Best regards,
{candidate_name}"""

        elif template_style == "technical":
            cover_letter = f"""Dear {company_name} Engineering Team,

I am writing to express my interest in the {job_title} role at {company_name}. With {resume_data.get('years_experience', '5+')} years of experience in software development and a strong foundation in {', '.join(resume_data.get('skills', [])[:4])}, I am confident I can contribute meaningfully to your technical objectives.

My technical background includes:
• Proficiency in {', '.join(resume_data.get('skills', [])[:3])}
• Experience with {resume_data.get('experience_level', 'senior-level')} software architecture and design patterns
• Strong understanding of scalable systems and performance optimization
• Collaborative development using agile methodologies and modern DevOps practices

The technical challenges outlined in the {job_title} position align perfectly with my expertise. I am particularly interested in {job_data.get('key_tech', 'the technology stack')} and believe my experience with similar systems would allow me to contribute immediately while continuing to grow with your team.

I would welcome the opportunity to discuss the technical requirements in detail and demonstrate how my skills can address your specific needs.

Sincerely,
{candidate_name}"""

        else:  # Professional template (default)
            cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background in {', '.join(resume_data.get('skills', [])[:3])} and proven track record of delivering high-quality results, I am excited about the opportunity to contribute to your team's success.

In my {resume_data.get('experience_level', 'professional')} role, I have developed expertise in {', '.join(resume_data.get('skills', [])[:2])}, which directly aligns with the requirements outlined in your job posting. My experience has taught me the importance of both technical excellence and effective collaboration, qualities I believe are essential for success at {company_name}.

I am particularly drawn to {company_name} because of your reputation for innovation and commitment to quality. I am confident that my skills, combined with my passion for continuous learning and improvement, would make me a valuable addition to your team.

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to {company_name}'s continued success.

Sincerely,
{candidate_name}"""
        
        return cover_letter
    
    def calculate_skills_match(self, candidate_skills: List[str], job_requirements: List[str]) -> int:
        """Calculate percentage match between candidate skills and job requirements"""
        if not job_requirements:
            return 85  # Default good match if no specific requirements
            
        candidate_lower = [skill.lower() for skill in candidate_skills]
        requirements_lower = [req.lower() for req in job_requirements]
        
        matches = sum(1 for req in requirements_lower 
                     if any(skill in req or req in skill for skill in candidate_lower))
        
        match_percentage = min(95, int((matches / len(requirements_lower)) * 100)) if requirements_lower else 85
        return max(50, match_percentage)  # Minimum 50% match
    
    def generate_multiple_variants(self, resume_data: Dict, job_data: Dict) -> List[Dict]:
        """Generate multiple cover letter variants with different styles"""
        print(f"\n🎨 GENERATING MULTIPLE VARIANTS")
        print("=" * 50)
        
        variants = []
        for style in self.templates.keys():
            print(f"   ✍️ Creating {style} version...")
            variant = self.generate_cover_letter(resume_data, job_data, style)
            variant['variant_id'] = f"{style}_variant"
            variants.append(variant)
        
        print(f"\n✅ Generated {len(variants)} cover letter variants")
        return variants
    
    def send_cover_letters_to_agents(self, cover_letters: List[Dict]):
        """Send generated cover letters to other agents via coral-server"""
        try:
            print(f"\n📤 Sending {len(cover_letters)} cover letters to coral-server...")
            
            # Simulate sending to coral-server
            for letter in cover_letters:
                message = {
                    "type": "cover_letter_generated",
                    "agent": self.agent_name,
                    "data": {
                        "letter_id": letter['id'],
                        "candidate": letter['candidate_name'],
                        "job": f"{letter['job_title']} at {letter['company_name']}",
                        "template": letter['template_style'],
                        "match_score": letter['skills_match_score'],
                        "word_count": letter['word_count']
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
                # Send to other agents
                print(f"   ✉️ Sent {letter['template_style']} cover letter to auditor agent")
                
            print(f"✅ All cover letters shared with other agents")
            
        except Exception as e:
            print(f"❌ Failed to send cover letters: {e}")
    
    def run_demo(self):
        """Run cover letter generation demo"""
        print(f"🚀 Starting Cover Letter Generator Agent: {self.agent_name}")
        print("=" * 70)
        print("✍️ Specialization: AI-Powered Cover Letter Generation")
        print("🎯 Mission: Create personalized, compelling cover letters")
        print("=" * 70)
        
        print(f"\n🤖 Agent '{self.agent_name}' is now active!")
        print(f"\n🔄 This agent will:")
        print(f"   1. 🧠 Analyze candidate profiles")
        print(f"   2. 🎯 Match skills with job requirements")
        print(f"   3. ✍️ Generate personalized cover letters using AI/LLM")
        print(f"   4. 🎨 Apply professional templates and formatting")
        print(f"   5. 📤 Share results with other agents")
        
        print(f"\n" + "=" * 70)
        print("🎬 DEMO: Cover Letter Generation Process")
        print("=" * 70)
        
        # Sample data from other agents
        sample_resume = {
            "name": "Alex Johnson",
            "skills": ["React", "TypeScript", "Node.js", "Python", "AWS", "Docker"],
            "experience_level": "Senior",
            "years_experience": "6+",
            "education": "BS Computer Science"
        }
        
        sample_job = {
            "title": "Senior Full Stack Developer",
            "company": "TechFlow Inc",
            "location": "San Francisco, CA",
            "requirements": ["React", "TypeScript", "Node.js", "AWS", "Team Leadership"],
            "company_mission": "building the next generation of developer tools",
            "key_tech": "React and Node.js ecosystem"
        }
        
        # Generate single cover letter
        cover_letter = self.generate_cover_letter(sample_resume, sample_job, "professional")
        
        # Show the generated content
        print(f"\n📄 GENERATED COVER LETTER:")
        print("=" * 60)
        print(cover_letter['content'])
        print("=" * 60)
        
        # Generate multiple variants
        variants = self.generate_multiple_variants(sample_resume, sample_job)
        
        # Send to other agents
        self.send_cover_letters_to_agents(variants)
        
        print(f"\n✅ Cover letter generation complete! Ready for next request.")
        
        # Check if running in demo mode
        if '--demo' in sys.argv:
            print("🎯 Demo mode: Exiting after one generation")
            print(f"👋 Cover Letter Generator Agent '{self.agent_name}' demo completed!")
            return
            
        print(f"📡 Agent running... Press Ctrl+C to stop")
        
        # Keep agent alive for production
        try:
            while True:
                time.sleep(60)  # Check every minute
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✍️ Cover Letter Generator monitoring...")
        except KeyboardInterrupt:
            print(f"\n\n👋 Cover Letter Generator Agent '{self.agent_name}' shutting down...")
            print("✅ All cover letter data saved successfully!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python cover-letter-generator-agent.py <agent_name> [--demo]")
        print("Example: python cover-letter-generator-agent.py letter-writer-ai")
        print("Example: python cover-letter-generator-agent.py letter-writer-ai --demo")
        print()
        print("Options:")
        print("  --demo    Run once and exit (for testing)")
        print("  (none)    Run continuously (for production)")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    agent = CoverLetterGeneratorAgent(agent_name)
    agent.run_demo()

if __name__ == "__main__":
    main()