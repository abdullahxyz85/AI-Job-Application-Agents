#!/usr/bin/env python3
"""
🎯 CORAL PROTOCOL AGENT: Cover Letter Generator (Official Integration)
===================================================================
Hackathon Project: AI Job Application Agent
Official Coral Protocol Integration with Real-time LLM via AIML API
Author: Hackathon Team
Version: 2.0

This agent uses:
- Official Coral Protocol MCP (Model Context Protocol)
- Real-time LLM responses via AIML API
- Proper agent registration and communication
- Environment-based configuration
"""

import asyncio
import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Coral Protocol imports (following official examples)
try:
    from camel.agents import ChatAgent
    from camel.models import ModelFactory
    from camel.toolkits import MCPToolkit
    from camel.toolkits.mcp_toolkit import MCPClient
    from camel.utils.mcp_client import ServerConfig
    from camel.types import ModelPlatformType, ModelType
    CAMEL_AVAILABLE = True
except ImportError:
    print("⚠️ CAMEL-AI not installed. Install with: pip install camel-ai[all]")
    CAMEL_AVAILABLE = False

class OfficialCoverLetterAgent:
    """
    🎯 Official Coral Protocol Cover Letter Generator Agent
    
    Features:
    - Real-time LLM integration via AIML API
    - Official Coral Protocol MCP connection
    - Proper agent registration and communication
    - Environment-based configuration
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.coral_connection_url = os.getenv(
            "CORAL_CONNECTION_URL", 
            "http://localhost:5555/devmode/hackathonApp/privkey/session1/sse?waitForAgents=4&agentId=" + agent_name
        )
        
        # Initialize AIML API client
        self.llm_client = OpenAI(
            base_url=os.getenv("MODEL_BASE_URL", "https://api.aimlapi.com/v1"),
            api_key=os.getenv("AIML_API_KEY", "your_aiml_api_key_here")
        )
        
        # Model configuration
        self.model_config = {
            "model": os.getenv("MODEL_NAME", "openai/gpt-4o-mini"),
            "temperature": float(os.getenv("MODEL_TEMPERATURE", "0.3")),
            "max_tokens": int(os.getenv("MODEL_MAX_TOKENS", "4096")),
        }
        
        self.mcp_toolkit = None
        self.camel_agent = None
        
    async def connect_to_coral_protocol(self):
        """Connect to Coral Protocol using official MCP"""
        if not CAMEL_AVAILABLE:
            print("❌ CAMEL-AI is required for official Coral Protocol integration")
            return False
            
        try:
            print(f"🌐 Connecting to Coral Protocol...")
            print(f"   📡 URL: {self.coral_connection_url}")
            
            # Create MCP client (following official examples)
            server_config = ServerConfig(
                url=self.coral_connection_url,
                timeout=float(os.getenv("AGENT_TIMEOUT", "30000")),
                sse_read_timeout=float(os.getenv("AGENT_TIMEOUT", "30000")),
                terminate_on_close=True,
                prefer_sse=True
            )
            
            mcp_client = MCPClient(server_config, timeout=float(os.getenv("AGENT_TIMEOUT", "30000")))
            self.mcp_toolkit = MCPToolkit([mcp_client])
            
            print("✅ Connected to Coral Protocol MCP server")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to Coral Protocol: {e}")
            return False
    
    async def create_camel_agent(self):
        """Create CAMEL agent with MCP tools"""
        try:
            tools = self.mcp_toolkit.get_tools()
            
            system_prompt = f"""
            You are an expert Cover Letter Generator Agent specializing in creating personalized, compelling cover letters.
            
            Your identity: {self.agent_name}
            Your role: Generate tailored cover letters that match candidate profiles with job requirements
            
            Capabilities:
            - Analyze candidate resumes and extract key strengths
            - Match candidate skills with job requirements  
            - Generate multiple cover letter variants (professional, creative, technical)
            - Apply industry best practices for cover letter writing
            - Personalize content for specific companies and roles
            
            Communication:
            - Use the MCP tools to communicate with other agents
            - Request resume data from resume-parser-agent
            - Request job details from job-searcher-agent
            - Send completed cover letters to auditor-agent
            - Always mention specific agent names in your messages
            
            Quality Standards:
            - Create compelling, error-free cover letters
            - Maintain professional tone and formatting
            - Highlight relevant achievements and skills
            - Customize for each specific opportunity
            - Ensure proper length (3-5 paragraphs)
            """
            
            # Create model factory
            model = ModelFactory.create(
                model_platform=ModelPlatformType.OPENAI,
                model_type=ModelType.GPT_4O_MINI,
                api_key=os.getenv("AIML_API_KEY"),
                url=os.getenv("MODEL_BASE_URL", "https://api.aimlapi.com/v1"),
                model_config_dict=self.model_config
            )
            
            # Create CAMEL agent
            self.camel_agent = ChatAgent(
                system_message=system_prompt,
                model=model,
                tools=tools,
                message_window_size=int(os.getenv("MESSAGE_WINDOW_SIZE", "4096")),
                token_limit=int(os.getenv("TOKEN_LIMIT", "20000"))
            )
            
            print(f"🤖 Created CAMEL agent: {self.agent_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create CAMEL agent: {e}")
            return False
    
    async def generate_cover_letter_with_llm(self, resume_data: Dict, job_data: Dict, style: str = "professional") -> str:
        """Generate cover letter using real LLM via AIML API"""
        try:
            print(f"🤖 Generating {style} cover letter with LLM...")
            
            # Prepare LLM prompt
            prompt = f"""
            Create a {style} cover letter for the following job application:
            
            CANDIDATE PROFILE:
            - Name: {resume_data.get('name', 'Candidate')}
            - Skills: {', '.join(resume_data.get('skills', []))}
            - Experience Level: {resume_data.get('experience_level', 'Mid-Level')}
            - Years of Experience: {resume_data.get('years_experience', '3-5')}
            
            JOB DETAILS:
            - Position: {job_data.get('title', 'Position')}
            - Company: {job_data.get('company', 'Company')}
            - Location: {job_data.get('location', 'Location')}
            - Requirements: {', '.join(job_data.get('requirements', []))}
            
            COVER LETTER STYLE: {style}
            
            Requirements:
            - Write a compelling, personalized cover letter
            - Highlight relevant skills and experience
            - Match candidate strengths with job requirements
            - Use {style} tone and language
            - Keep it professional and concise (3-4 paragraphs)
            - Include proper greeting and closing
            
            Generate the cover letter:
            """
            
            # Call AIML API
            response = self.llm_client.chat.completions.create(
                model=self.model_config["model"],
                messages=[
                    {"role": "system", "content": "You are an expert cover letter writer who creates compelling, personalized cover letters."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.model_config["temperature"],
                max_tokens=self.model_config["max_tokens"]
            )
            
            cover_letter = response.choices[0].message.content
            
            print(f"✅ Generated {len(cover_letter.split())} word cover letter")
            return cover_letter
            
        except Exception as e:
            print(f"❌ LLM generation failed: {e}")
            return self.fallback_cover_letter(resume_data, job_data, style)
    
    def fallback_cover_letter(self, resume_data: Dict, job_data: Dict, style: str) -> str:
        """Fallback cover letter generation if LLM fails"""
        candidate_name = resume_data.get('name', 'Candidate')
        company_name = job_data.get('company', 'Company')
        job_title = job_data.get('title', 'Position')
        
        return f"""Dear Hiring Manager at {company_name},

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background in {', '.join(resume_data.get('skills', [])[:3])} and proven track record of delivering high-quality results, I am excited about the opportunity to contribute to your team's success.

In my {resume_data.get('experience_level', 'professional')} role, I have developed expertise in {', '.join(resume_data.get('skills', [])[:2])}, which directly aligns with the requirements outlined in your job posting. My experience has taught me the importance of both technical excellence and effective collaboration.

I am particularly drawn to {company_name} because of your reputation for innovation and commitment to quality. I am confident that my skills would make me a valuable addition to your team.

Thank you for considering my application. I look forward to discussing how I can contribute to {company_name}'s continued success.

Sincerely,
{candidate_name}"""
    
    async def communicate_with_agents(self, message: str, mentions: List[str] = None):
        """Communicate with other agents via Coral Protocol"""
        try:
            if not self.camel_agent:
                print("❌ Agent not initialized")
                return
                
            # Use CAMEL agent to step with message
            response = await self.camel_agent.astep(message)
            
            if response and response.msgs:
                msg_content = response.msgs[0].to_dict()
                print(f"📤 Sent to Coral Protocol: {msg_content}")
                return msg_content
            
        except Exception as e:
            print(f"❌ Communication failed: {e}")
            return None
    
    async def run_official_demo(self):
        """Run official Coral Protocol demo with real LLM"""
        print(f"🚀 Starting Official Coral Protocol Cover Letter Agent")
        print("=" * 70)
        print(f"🤖 Agent: {self.agent_name}")
        print(f"🌐 Coral URL: {self.coral_connection_url}")
        print(f"🧠 LLM Model: {self.model_config['model']}")
        print(f"🔗 Base URL: {self.llm_client.base_url}")
        print("=" * 70)
        
        # Step 1: Connect to Coral Protocol
        connected = await self.connect_to_coral_protocol()
        if not connected:
            return
        
        # Step 2: Initialize MCP toolkit
        async with self.mcp_toolkit as connected_toolkit:
            print("✅ MCP Toolkit connected")
            
            # Step 3: Create CAMEL agent
            agent_created = await self.create_camel_agent()
            if not agent_created:
                return
            
            print(f"\n🎬 DEMO: Real-time LLM Cover Letter Generation")
            print("=" * 60)
            
            # Sample data
            sample_resume = {
                "name": "Alex Johnson",
                "skills": ["React", "TypeScript", "Node.js", "Python", "AWS", "Docker"],
                "experience_level": "Senior",
                "years_experience": "6+"
            }
            
            sample_job = {
                "title": "Senior Full Stack Developer",
                "company": "TechFlow Inc",
                "location": "San Francisco, CA (Remote)",
                "requirements": ["React", "TypeScript", "Node.js", "AWS", "Team Leadership"]
            }
            
            # Generate cover letter with real LLM
            cover_letter = await self.generate_cover_letter_with_llm(
                sample_resume, sample_job, "professional"
            )
            
            print(f"\n📄 GENERATED COVER LETTER (Real LLM):")
            print("=" * 60)
            print(cover_letter)
            print("=" * 60)
            
            # Communicate with other agents
            await self.communicate_with_agents(
                f"Cover letter generated for {sample_job['title']} at {sample_job['company']}. Ready for review.",
                mentions=["auditor-agent", "resume-parser-agent"]
            )
            
            print(f"\n✅ Official Coral Protocol integration complete!")
            print(f"🎯 Agent is now live and communicating via MCP")
            
            # Keep alive for demo
            if '--demo' not in sys.argv:
                print(f"📡 Agent running... Press Ctrl+C to stop")
                try:
                    while True:
                        await asyncio.sleep(10)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 Cover Letter Agent active on Coral Protocol...")
                except KeyboardInterrupt:
                    print(f"\n👋 Agent {self.agent_name} shutting down...")

def main():
    if len(sys.argv) < 2:
        print("Usage: python official-cover-letter-agent.py <agent_name> [--demo]")
        print("Example: python official-cover-letter-agent.py cover-letter-generator")
        print("Example: python official-cover-letter-agent.py cover-letter-generator --demo")
        print()
        print("Requirements:")
        print("  AIML_API_KEY environment variable")
        print("  coral-server running on localhost:5555")
        print("  camel-ai package installed")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    agent = OfficialCoverLetterAgent(agent_name)
    
    # Check API key
    if not os.getenv("AIML_API_KEY") or os.getenv("AIML_API_KEY") == "your_aiml_api_key_here":
        print("❌ AIML_API_KEY not set!")
        print("   Set your API key: export AIML_API_KEY='your_actual_key'")
        print("   Or create .env file with: AIML_API_KEY=your_actual_key")
        sys.exit(1)
    
    # Run async demo
    asyncio.run(agent.run_official_demo())

if __name__ == "__main__":
    main()