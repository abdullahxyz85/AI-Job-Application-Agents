# 🤖 AI Job Application Agent - Complete Real-Time System

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **A comprehensive AI-powered job application system with real-time resume parsing, intelligent job matching, and automated cover letter generation.**

## 🌟 Features

### ✅ **Real-Time Resume Parsing**

- **PDF Text Extraction**: Extract actual data from uploaded PDF resumes
- **Contact Information Detection**: Automatically identify names, emails, phone numbers, LinkedIn profiles
- **Skills Recognition**: Parse 100+ technical skills from resume content
- **Experience Level Analysis**: Determine seniority level based on content and keywords
- **Education Extraction**: Identify degrees, institutions, and academic achievements

### ✅ **Live Job Search Integration**

- **Multiple API Support**: JSearch (RapidAPI), Adzuna APIs with automatic fallback
- **Real-Time Job Data**: Live job listings from Google Jobs, Indeed, LinkedIn, and more
- **Smart Query Generation**: Create search queries based on extracted resume skills
- **Location-Based Search**: Support for multiple countries and regions
- **Salary Information**: Display salary ranges when available

### ✅ **User Authentication & Profiles**

- **Secure JWT Authentication**: Complete sign-up/sign-in system
- **Dynamic User Profiles**: Store skills, experience, preferences
- **Resume Upload History**: Track uploaded resumes and parsing results
- **Application Tracking**: Monitor job applications and their status

### ✅ **Modern React Frontend**

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Mode**: Theme switching capability
- **Real-time Updates**: Live feedback during resume parsing and job search
- **Interactive Dashboard**: View parsed data, search results, and analytics
- **Toast Notifications**: User-friendly success/error messages

### ✅ **Production-Ready Backend**

- **FastAPI Framework**: High-performance async API
- **SQLite Database**: Complete schema with relationships
- **CORS Support**: Ready for frontend integration
- **Error Handling**: Comprehensive error responses
- **API Documentation**: Auto-generated Swagger docs

## 🏗️ Project Structure

```
coral-setup/
├── 📁 agents/                    # Backend API & AI Agents
│   ├── 🔑 complete_api.py       # Main FastAPI application
│   ├── 📄 real_resume_parser.py # PDF parsing & data extraction
│   ├── 🔍 real_job_search_api.py# Job search API integration
│   ├── ⚙️ setup_api_keys.py     # API configuration utility
│   ├── 🧪 test_*.py             # Testing utilities
│   ├── 📊 ai_job_agent.db       # SQLite database
│   └── 🔐 .env                  # Environment variables
│
├── 📁 frontend/                  # React Frontend
│   ├── 📁 src/
│   │   ├── 📁 components/       # Reusable UI components
│   │   ├── 📁 contexts/         # React contexts (Auth, Theme)
│   │   ├── 📁 pages/           # Application pages
│   │   └── 📱 App.tsx          # Main app component
│   ├── 📦 package.json
│   └── ⚙️ vite.config.ts
│
├── 📁 coral-server/             # Coral Protocol MCP Server (Kotlin/Gradle)
├── 📁 coral-studio/             # Agent Session Management UI (SvelteKit)
├── 📁 coral-example-app/        # Rust Example Application (Discord Bot)
└── 📖 README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **Node.js 18+** & **Yarn**
- **Java 11+** (for Coral Server)
- **Rust** (for Coral Example App) - Install from: https://rustup.rs/
- **Git**

### 1️⃣ Clone Repository

```bash
git clone https://github.com/abdullahxyz85/AI-Job-Application-Agents.git
cd AI-Job-Application-Agents
```

### 2️⃣ Backend Setup

```bash
# Navigate to agents directory
cd agents

# Install Python dependencies
pip install fastapi uvicorn python-multipart pydantic requests python-dotenv bcrypt PyJWT python-jose[cryptography] PyPDF2 pdfplumber email-validator

# Configure API keys (optional but recommended)
python setup_api_keys.py

# Start the backend server
python complete_api.py
```

**Backend will run on:** `http://localhost:8000`
**API Documentation:** `http://localhost:8000/docs`

### 3️⃣ Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will run on:** `http://localhost:5173`

## 🐠 Coral Protocol Components

### 🖥️ **Coral Server** (Agent Communication)

The Coral Server enables AI agents to communicate with each other through a thread-based messaging system.

```bash
# Navigate to coral-server directory
cd coral-server

# Run using Gradle (requires Java 11+)
# Windows:
gradlew.bat run

# Linux/Mac:
./gradlew run
```

**Coral Server will run on:** `http://localhost:5555`

- **MCP Inspector Access**: `http://localhost:5555/devmode/exampleApplication/privkey/session1/sse`
- **Agent Registration**: Add `?agentId=your_agent_name` to the URL

### 🎨 **Coral Studio** (Session Management UI)

Web interface for creating, managing, and inspecting agent sessions.

```bash
# Navigate to coral-studio directory
cd coral-studio

# Install dependencies
yarn install

# Build and serve
yarn build
yarn preview
```

**Coral Studio will run on:** `http://localhost:4173`

**Alternative - Development Mode:**

```bash
# For development with hot reload
yarn dev
# Development server: http://localhost:5173
```

**Alternative - Docker:**

```bash
docker run -p 3000:3000 ghcr.io/coral-protocol/coral-studio
# Docker version: http://localhost:3000
```

### 🦀 **Coral Example App** (Rust Discord Bot)

Example Rust application showing Coral Protocol integration with Discord.

```bash
# Navigate to coral-example-app directory
cd coral-example-app

# Build the Rust application (requires Rust installed)
cargo build --release

# Run the Discord bot example
cargo run --bin app

# Or run the Discord integration
cargo run --bin discord
```

**Prerequisites for Rust App:**

- Install Rust: https://rustup.rs/
- Discord Bot Token (if using Discord integration)

### 🔗 **Complete Coral Protocol Setup**

To run the full Coral Protocol ecosystem:

**Terminal 1 - Coral Server:**

```bash
cd coral-server
gradlew.bat run
```

**Terminal 2 - Coral Studio:**

```bash
cd coral-studio
yarn install
yarn dev
```

**Terminal 3 - Your AI Job Agent:**

```bash
cd agents
python complete_api.py
```

**Terminal 4 - Frontend:**

```bash
cd frontend
npm run dev
```

Now you'll have:

- **Coral Server**: `http://localhost:5555` (Agent communication)
- **Coral Studio**: `http://localhost:5173` (Session management)
- **AI Job Agent**: `http://localhost:8000` (Your main app)
- **Frontend**: `http://localhost:5173` (User interface)

### 4️⃣ Access the Application

Open your browser and navigate to: `http://localhost:5173`

## 🔑 API Configuration

### Get Free API Keys (Optional but Recommended)

#### **Option 1: JSearch API (Recommended)**

1. Go to: [JSearch on RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
2. Sign up for free RapidAPI account
3. Subscribe to JSearch (Free tier: 150 requests/month)
4. Copy your API key
5. Add to `.env` file: `RAPIDAPI_KEY=your_api_key_here`

#### **Option 2: Adzuna API (Alternative)**

1. Go to: [Adzuna Developer](https://developer.adzuna.com/)
2. Sign up for free account (1,000 requests/month)
3. Get your App ID and App Key
4. Add to `.env` file:
   ```
   ADZUNA_APP_ID=your_app_id
   ADZUNA_APP_KEY=your_app_key
   ```

### Environment Variables

Create `.env` file in the `agents/` directory:

```env
# Job Search APIs (choose one or both)
RAPIDAPI_KEY=your_rapidapi_key_here
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

# Authentication (optional)
JWT_SECRET_KEY=your_super_secret_jwt_key_here
AIML_API_KEY=your_aiml_api_key_here
```

## 📖 Usage Guide

### 🔐 **Authentication**

1. **Sign Up**: Create a new account with email and password
2. **Sign In**: Login with your credentials
3. **Profile Management**: Update your information and preferences

### 📄 **Resume Upload & Parsing**

1. Click "Upload Resume" on your dashboard
2. Select a PDF file (your actual resume)
3. Watch real-time parsing extract your:
   - Personal information (name, email, phone)
   - Technical skills
   - Experience level
   - Education background
   - Professional summary

### 🔍 **Job Search**

1. After resume parsing, click "Find Jobs"
2. System automatically searches using your skills
3. View real job listings with:
   - Company information
   - Salary ranges
   - Job descriptions
   - Apply links
4. Filter by location, salary, job type

### 📊 **Dashboard Analytics**

- View parsing statistics
- Track application history
- Monitor job search results
- Update profile information

## 🛠️ Development

### Backend Development

```bash
cd agents

# Run with auto-reload
python complete_api.py

# Run tests
python test_real_implementation.py
python test_auth.py

# Test resume parsing
python real_resume_parser.py

# Test job search API
python real_job_search_api.py
```

### Frontend Development

```bash
cd frontend

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Testing the Complete System

```bash
cd agents

# Test all components
python test_real_implementation.py

# Test authentication only
python test_auth.py

# Debug authentication issues
# Open: http://localhost:3001/debug_auth.html
python -m http.server 3001
```

## 📡 API Endpoints

### Authentication

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - User login
- `GET /api/auth/me` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Resume Processing

- `POST /api/agents/parse-resume` - Upload and parse resume
- `GET /api/user/resume-history` - Get parsing history

### Job Search

- `POST /api/agents/find-jobs` - Search for jobs
- `POST /api/agents/apply-to-job` - Apply to a job

### System

- `GET /api/health` - Health check
- `GET /docs` - API documentation
- `GET /api/status` - System status

## 🎯 Real-Time Features

### **No More Dummy Data!**

This system provides **100% real-time functionality**:

✅ **Real Resume Parsing**: Actual PDF text extraction and analysis  
✅ **Live Job Data**: Current job listings from major job boards  
✅ **Dynamic Search**: Queries based on your actual skills  
✅ **Real Authentication**: Secure user accounts and sessions  
✅ **Live Updates**: Real-time status updates and notifications

## 🔧 Troubleshooting

### Common Issues

#### **Backend Won't Start**

```bash
# Check if port 8000 is in use
netstat -an | findstr 8000

# Install missing dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.13+
```

#### **Frontend Build Errors**

```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

#### **PDF Parsing Fails**

- **File Size**: Ensure PDF is not corrupted (>1KB)
- **Format**: Only PDF files are supported
- **Content**: PDF must contain extractable text (not just images)

#### **Job Search Returns No Results**

- **API Keys**: Configure JSearch or Adzuna API keys
- **Skills**: Ensure resume has recognizable technical skills
- **Network**: Check internet connection

#### **Sign-In Issues**

```bash
# Reset password if needed
cd agents
python fix_password.py

# Check database
python -c "import sqlite3; print('DB exists:', os.path.exists('ai_job_agent.db'))"
```

## 🚀 Production Deployment

### Backend (FastAPI)

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn complete_api:app --host 0.0.0.0 --port 8000

# Or with uvicorn
uvicorn complete_api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend (React)

```bash
# Build for production
npm run build

# Serve static files
npm install -g serve
serve -s dist -l 3000

# Or deploy to Vercel/Netlify
```

### Environment Variables for Production

```env
# Production settings
JWT_SECRET_KEY=your_super_secure_production_key_here
DATABASE_URL=postgresql://user:pass@localhost/dbname  # For PostgreSQL
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# API Keys
RAPIDAPI_KEY=your_production_rapidapi_key
ADZUNA_APP_ID=your_production_adzuna_id
ADZUNA_APP_KEY=your_production_adzuna_key
```

## 📊 Database Schema

### Users Table

```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone TEXT,
    location TEXT,
    experience_level TEXT DEFAULT 'Entry-level',
    desired_salary TEXT,
    preferred_job_types TEXT DEFAULT '["Full-time"]',
    profile_picture TEXT,
    resume_uploaded BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Skills, Education, Experience Tables

- `user_skills`: Technical skills with proficiency levels
- `user_education`: Academic background
- `user_work_experience`: Professional experience
- `job_applications`: Application tracking

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all React components
- Write tests for new features
- Update documentation
- Ensure all tests pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI**: For the excellent async framework
- **React**: For the powerful frontend library
- **JSearch API**: For comprehensive job data
- **Adzuna API**: For additional job listings
- **PyPDF2 & pdfplumber**: For PDF processing
- **Coral Protocol**: For agent communication

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/abdullahxyz85/AI-Job-Application-Agents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abdullahxyz85/AI-Job-Application-Agents/discussions)
- **Email**: abdullahxyz85@gmail.com

## 🗺️ Roadmap

### Phase 1: Core Features ✅

- [x] Real-time resume parsing
- [x] Job search integration
- [x] User authentication
- [x] React frontend
- [x] Database integration

### Phase 2: Enhanced Features 🚧

- [ ] AI-powered cover letter generation
- [ ] Interview preparation assistance
- [ ] Application tracking dashboard
- [ ] Email notifications
- [ ] Mobile app (React Native)

### Phase 3: Advanced Features 📋

- [ ] Machine learning job matching
- [ ] Salary negotiation assistant
- [ ] Company research automation
- [ ] LinkedIn integration
- [ ] ATS optimization suggestions

---

<div align="center">

**⭐ Star this repository if it helped you land your dream job! ⭐**

Made with ❤️ by [Abdullah](https://github.com/abdullahxyz85)

[🏠 Home](https://github.com/abdullahxyz85/AI-Job-Application-Agents) •
[📚 Docs](https://github.com/abdullahxyz85/AI-Job-Application-Agents/wiki) •
[🐛 Issues](https://github.com/abdullahxyz85/AI-Job-Application-Agents/issues) •
[💬 Discussions](https://github.com/abdullahxyz85/AI-Job-Application-Agents/discussions)

</div>
