#!/usr/bin/env python3
"""
🔐 COMPLETE AUTHENTICATION & DYNAMIC DATA SYSTEM
===============================================
Full-stack AI Job Application Agent with:
- User Authentication (Sign Up / Sign In)
- Dynamic User Profiles
- Real Data Integration
- Complete API Management
"""

import asyncio
import os
import json
import sqlite3
import uuid
import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

# Import our real parsers
from real_resume_parser import RealResumeParser
from real_job_search_api import RealJobSearchAPI

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import requests
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv(dotenv_path="c:/Users/Admin/Desktop/coral-setup/agents/.env")

print("🔧 Environment Variable Check:")
print(f"  - AIML_API_KEY: {'✅ Found' if os.getenv('AIML_API_KEY') else '❌ Missing'}")
print(f"  - JWT_SECRET_KEY: {'✅ Found' if os.getenv('JWT_SECRET_KEY') else '❌ Using default'}")

# Import our existing agent
import sys
import importlib.util
sys.path.append('.')

# JWT Configuration - Use consistent key
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_super_secret_jwt_key_change_in_production_2024")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_HOURS = 24

# Security
security = HTTPBearer()

# Pydantic Models
class UserSignUp(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[str] = "Mid-Level"
    desired_salary: Optional[str] = None
    preferred_job_types: Optional[List[str]] = ["Full-time"]

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    user_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    experience_level: str
    desired_salary: Optional[str] = None
    preferred_job_types: List[str]
    profile_picture: Optional[str] = None
    resume_uploaded: bool = False
    skills: List[str] = []
    education: List[Dict] = []
    work_experience: List[Dict] = []
    created_at: str
    updated_at: str

class ResumeUpload(BaseModel):
    filename: str
    content: str

class JobApplicationRequest(BaseModel):
    preferences: Optional[Dict[str, Any]] = None

class AgentStatus(BaseModel):
    agent_id: str
    user_id: str
    status: str
    current_step: str
    progress: int
    results: Optional[Dict[str, Any]] = None

# Database Setup
def init_database():
    """Initialize comprehensive database schema"""
    conn = sqlite3.connect('ai_job_agent.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            phone TEXT,
            location TEXT,
            experience_level TEXT DEFAULT 'Mid-Level',
            desired_salary TEXT,
            preferred_job_types TEXT,  -- JSON array
            profile_picture TEXT,
            resume_uploaded BOOLEAN DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # User Skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            proficiency_level TEXT DEFAULT 'Intermediate',
            years_experience INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # User Education table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_education (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            institution_name TEXT NOT NULL,
            degree TEXT NOT NULL,
            field_of_study TEXT,
            start_date TEXT,
            end_date TEXT,
            gpa TEXT,
            is_current BOOLEAN DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # User Work Experience table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_work_experience (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            company_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            description TEXT,
            start_date TEXT,
            end_date TEXT,
            is_current BOOLEAN DEFAULT 0,
            salary TEXT,
            location TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Resumes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT,
            parsed_data TEXT,  -- JSON
            upload_date TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Job Applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            job_data TEXT,  -- JSON
            cover_letter TEXT,
            status TEXT DEFAULT 'applied',
            applied_date TEXT NOT NULL,
            response_date TEXT,
            interview_date TEXT,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Agent Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_sessions (
            agent_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            status TEXT NOT NULL,
            current_step TEXT,
            progress INTEGER DEFAULT 0,
            results TEXT,  -- JSON
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Enhanced Audit Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            agent_id TEXT,
            timestamp TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            status TEXT NOT NULL,
            data TEXT,
            ip_address TEXT,
            user_agent TEXT
        )
    ''')
    
    # Migration: Add resume_uploaded column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN resume_uploaded BOOLEAN DEFAULT 0")
        print("🔄 Migration: Added resume_uploaded column to users table")
    except Exception:
        # Column already exists, ignore
        pass
    
    conn.commit()
    conn.close()
    print("✅ Database initialized with complete schema")

# Database Helper Functions
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('ai_job_agent.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    # Get user from database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ? AND is_active = 1", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return dict(user)

# Global state management
active_agents: Dict[str, Any] = {}
agent_status: Dict[str, AgentStatus] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Complete AI Job Application System")
    print("🔐 Authentication & Dynamic Data Ready")
    init_database()
    yield
    # Shutdown
    print("🔄 Shutting down system")

# Initialize FastAPI app
app = FastAPI(
    title="AI Job Application Agent - Complete System",
    description="Full-stack AI job application automation with authentication and dynamic data",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Endpoints
@app.post("/api/auth/signup")
async def sign_up(user_data: UserSignUp):
    """User registration"""
    try:
        print(f"🔍 Debug: Registration attempt for email: {user_data.email}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT email FROM users WHERE email = ?", (user_data.email,))
        existing_user = cursor.fetchone()
        print(f"🔍 Debug: Existing user found: {existing_user is not None}")
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user_id = str(uuid.uuid4())
        password_hash = hash_password(user_data.password)
        now = datetime.now().isoformat()
        
        print(f"🔍 Debug: Created user_id: {user_id}")
        print(f"🔍 Debug: Password hash created: {len(password_hash)} chars")
        
        cursor.execute('''
            INSERT INTO users (
                user_id, full_name, email, password_hash, phone, location,
                experience_level, desired_salary, preferred_job_types,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, user_data.full_name, user_data.email, password_hash,
            user_data.phone, user_data.location, user_data.experience_level,
            user_data.desired_salary, json.dumps(user_data.preferred_job_types),
            now, now
        ))
        
        conn.commit()
        print(f"✅ Debug: User successfully created and committed to database")
        conn.close()
        
        # Create access token
        access_token = create_access_token(data={"sub": user_id})
        
        return {
            "success": True,
            "message": "User registered successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/api/auth/signin")
async def sign_in(user_credentials: UserSignIn):
    """User authentication"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print(f"🔍 Debug: Attempting login for email: {user_credentials.email}")
        
        # Get user by email
        cursor.execute("SELECT * FROM users WHERE email = ? AND is_active = 1", (user_credentials.email,))
        user = cursor.fetchone()
        
        print(f"🔍 Debug: User found: {user is not None}")
        if user:
            print(f"🔍 Debug: User ID: {user['user_id']}")
            print(f"🔍 Debug: Password verification: {verify_password(user_credentials.password, user['password_hash'])}")
        
        conn.close()
        
        if not user or not verify_password(user_credentials.password, user['password_hash']):
            print(f"❌ Debug: Login failed for {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user['user_id']})
        
        return {
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user['user_id']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@app.get("/api/auth/me")
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile with complete data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        user_id = current_user['user_id']
        
        # Get user skills
        cursor.execute("SELECT * FROM user_skills WHERE user_id = ?", (user_id,))
        skills = [dict(skill) for skill in cursor.fetchall()]
        
        # Get user education
        cursor.execute("SELECT * FROM user_education WHERE user_id = ?", (user_id,))
        education = [dict(edu) for edu in cursor.fetchall()]
        
        # Get work experience
        cursor.execute("SELECT * FROM user_work_experience WHERE user_id = ?", (user_id,))
        work_experience = [dict(exp) for exp in cursor.fetchall()]
        
        # Get resume info
        cursor.execute("SELECT * FROM resumes WHERE user_id = ? AND is_active = 1", (user_id,))
        resume_info = cursor.fetchone()
        
        conn.close()
        
        # Build complete profile
        profile = {
            "user_id": current_user['user_id'],
            "full_name": current_user['full_name'],
            "email": current_user['email'],
            "phone": current_user['phone'],
            "location": current_user['location'],
            "experience_level": current_user['experience_level'],
            "desired_salary": current_user['desired_salary'],
            "preferred_job_types": json.loads(current_user['preferred_job_types'] or '["Full-time"]'),
            "profile_picture": current_user.get('profile_picture'),
            "resume_uploaded": resume_info is not None,
            "skills": skills,
            "education": education,
            "work_experience": work_experience,
            "created_at": current_user['created_at'],
            "updated_at": current_user['updated_at']
        }
        
        return {
            "success": True,
            "profile": profile
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {str(e)}"
        )

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Enhanced health check with system status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "authentication": True,
            "dynamic_data": True,
            "coral_server": await check_coral_server(),
            "aiml_api": check_aiml_api_config(),
            "database": check_database_health()
        }
    }

# ==================================================================
# AGENT INTEGRATION ENDPOINTS
# ==================================================================

@app.post("/api/agents/parse-resume")
async def parse_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Parse resume using AI agents and extract skills/experience"""
    try:
        print(f"🔍 Debug: Resume upload for user: {current_user['user_id']}")
        print(f"🔍 Debug: File name: {file.filename}")
        print(f"🔍 Debug: Content type: {file.content_type}")
        
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid file type",
                    "message": "Only PDF files are supported",
                    "suggestions": ["Please upload a PDF file", "Convert your resume to PDF format"]
                }
            )
        
        # Read the uploaded file
        file_content = await file.read()
        print(f"🔍 Debug: File '{file.filename}' - Size: {len(file_content)} bytes")
        
        # Check file size
        if len(file_content) == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Empty file",
                    "message": "The uploaded file is empty",
                    "suggestions": ["Please select a valid PDF file", "Check that the file uploaded correctly"]
                }
            )
        
        # REAL RESUME PARSING - Replace dummy data with actual parsing
        print("🚀 Starting real resume parsing...")
        resume_parser = RealResumeParser()
        parsed_result = resume_parser.parse_resume(file_content)
        
        # Handle parsing errors gracefully
        if not parsed_result.get("success"):
            error_msg = parsed_result.get("error", "Unknown parsing error")
            print(f"❌ Parsing failed: {error_msg}")
            
            # Determine appropriate HTTP status code
            status_code = 422  # Unprocessable Entity for corrupted/invalid PDF
            if "invalid pdf" in error_msg.lower() or "no /root object" in error_msg.lower():
                status_code = 400  # Bad Request for clearly invalid files
            
            raise HTTPException(
                status_code=status_code,
                detail={
                    "error": "Resume parsing failed",
                    "message": error_msg,
                    "filename": file.filename,
                    "suggestions": [
                        "Please make sure the file is a valid, non-corrupted PDF",
                        "Try re-uploading the file",
                        "If the issue persists, try converting your resume to a new PDF",
                        "Make sure the PDF is not password protected"
                    ]
                }
            )
        
        # Extract real data from parsed resume
        contact_info = parsed_result.get("contact_info", {})
        skills_found = parsed_result.get("skills", [])
        experience_level = parsed_result.get("experience_level", "Not specified")
        
        print(f"✅ Real parsing complete:")
        print(f"   Name: {contact_info.get('name', 'Not found')}")
        print(f"   Email: {contact_info.get('email', 'Not found')}")
        print(f"   Skills found: {len(skills_found)}")
        print(f"   Experience level: {experience_level}")
        print(f"   Experience: {experience_level}")
        
        # Update user's resume status in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print(f"🔍 Debug: Updating resume_uploaded status")
        cursor.execute(
            "UPDATE users SET resume_uploaded = ? WHERE user_id = ?",
            (True, current_user['user_id'])
        )
        
        print(f"🔍 Debug: Adding skills to database")
        # Add parsed skills to user profile
        for skill in skills_found:
            cursor.execute("""
                INSERT OR IGNORE INTO user_skills (user_id, skill_name, proficiency_level, years_experience, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (current_user['user_id'], skill, "Intermediate", 2, datetime.utcnow().isoformat()))
        
        conn.commit()
        conn.close()
        print(f"✅ Debug: Resume processing completed successfully")
        
        return {
            "success": True,
            "message": "Resume parsed successfully",
            "skills_count": len(skills_found),
            "experience_years": 3,
            "skills": skills_found
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Debug: Resume parsing error: {str(e)}")
        print(f"❌ Debug: Error type: {type(e)}")
        import traceback
        print(f"❌ Debug: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Resume parsing failed: {str(e)}"
        )

@app.post("/api/agents/find-jobs")
async def find_jobs(
    current_user: dict = Depends(get_current_user)
):
    """Find jobs matching user profile using AI agents"""
    try:
        # Get user skills from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT skill_name FROM user_skills WHERE user_id = ?",
            (current_user['user_id'],)
        )
        user_skills = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # REAL JOB SEARCH - Replace dummy data with actual API calls
        print("🚀 Starting real job search...")
        job_search_api = RealJobSearchAPI()
        
        # Create search query from user skills
        if user_skills:
            # Use top skills for search query
            primary_skills = user_skills[:3]  # Top 3 skills
            search_query = " ".join(primary_skills) + " developer"
        else:
            search_query = "software developer"  # Default search
        
        # Perform real job search
        job_results = job_search_api.search_jobs_with_fallback(
            query=search_query,
            location="United States",
            max_results=20
        )
        
        if not job_results.get("success"):
            # If API fails, return helpful error message
            return {
                "success": False,
                "error": job_results.get("error", "Job search failed"),
                "setup_instructions": job_results.get("setup_instructions"),
                "next_steps": job_results.get("next_steps"),
                "jobs": [],
                "user_skills": user_skills,
                "search_query": search_query
            }
        
        # Format jobs for frontend
        formatted_jobs = []
        for i, job in enumerate(job_results.get("jobs", [])[:10]):  # Limit to 10 jobs
            formatted_job = {
                "id": job.get("id", f"job_{i+1}"),
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "type": job.get("employment_type", "Full-time"),
                "salary": job.get("salary", "Not specified"),
                "description": job.get("description", "")[:300] + "...",  # Truncate
                "apply_link": job.get("apply_link", ""),
                "posted_date": job.get("posted_date", ""),
                "source": job.get("source", ""),
                "match_score": 85,  # Could implement skill matching later
                "applied": False
            }
            formatted_jobs.append(formatted_job)
        
        print(f"✅ Found {len(formatted_jobs)} real jobs using query: {search_query}")
        
        return {
            "success": True,
            "jobs": formatted_jobs,
            "total_count": job_results.get("total_results", len(formatted_jobs)),
            "user_skills": user_skills,
            "search_query": search_query,
            "api_used": job_results.get("api_used"),
            "api_limit_info": job_results.get("api_limit_info")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Job search failed: {str(e)}"
        )

@app.post("/api/agents/apply-to-job")
async def apply_to_job(
    job_application: dict,
    current_user: dict = Depends(get_current_user)
):
    """Apply to a job using AI-generated cover letter"""
    try:
        job_id = job_application.get("job_id")
        job_title = job_application.get("job_title", "Position")
        company = job_application.get("company", "Company")
        
        # Simulate cover letter generation (replace with actual agent call)
        # TODO: Integrate with actual cover letter generator agent
        cover_letter = f"""
Dear Hiring Manager at {company},

I am excited to apply for the {job_title} position. With my background in software development 
and experience with Python, React, and machine learning, I believe I would be a valuable 
addition to your team.

My technical skills include:
- Python development and FastAPI frameworks
- Frontend development with React and JavaScript  
- Database design and SQL optimization
- Machine learning and data analysis

I am particularly drawn to {company} because of your innovative approach and commitment to 
technology excellence. I would welcome the opportunity to contribute to your team's success.

Thank you for considering my application.

Best regards,
{current_user.get('full_name', 'Applicant')}
        """.strip()
        
        # Store application in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        application_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO job_applications (
                application_id, user_id, job_id, company, job_title,
                cover_letter, status, applied_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            application_id, current_user['user_id'], job_id, company, 
            job_title, cover_letter, 'applied', datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"Successfully applied to {job_title} at {company}",
            "application_id": application_id,
            "cover_letter": cover_letter
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Job application failed: {str(e)}"
        )

async def check_coral_server():
    """Check if Coral Protocol server is running"""
    try:
        response = requests.get("http://localhost:5555", timeout=2)
        return "connected" if response.status_code in [200, 404] else "disconnected"
    except:
        return "disconnected"

def check_aiml_api_config():
    """Check if AIML API is configured"""
    api_key = os.getenv("AIML_API_KEY")
    return "configured" if api_key and api_key != "your_aiml_api_key_here" else "not_configured"

def check_database_health():
    """Check database connectivity"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        conn.close()
        return "connected"
    except:
        return "error"

if __name__ == "__main__":
    print("🚀 Starting Complete AI Job Application System")
    print("🔐 Authentication & Dynamic Data Integration")
    print("🌐 React Frontend Integration Ready")
    print("📡 Coral Protocol Integration Active")
    print("🤖 AIML API Integration Enabled")
    print()
    print("🔑 Required Environment Variables:")
    print("  - AIML_API_KEY (for AI responses)")
    print("  - JWT_SECRET_KEY (for authentication)")
    print("  - Optional: MODEL_BASE_URL, MODEL_NAME")
    print()
    print("📊 Database: ai_job_agent.db (auto-created)")
    print("🌐 API Docs: http://localhost:8000/docs")
    print()
    
    uvicorn.run(
        "complete_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )