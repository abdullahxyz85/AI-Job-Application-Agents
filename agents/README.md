# AI Job Application Agents

## Architecture

This hackathon project implements a multi-agent system using Coral Protocol for automated job applications.

### Agents:

1. **resume-parser-agent.py** - Parses resumes and extracts key information
2. **job-searcher-agent.py** - Searches and scores job opportunities
3. **cover-letter-agent.py** - Generates personalized cover letters
4. **auditor-agent.py** - Provides transparency and logging

### Frontend Integration:

- React/TypeScript frontend at `../frontend/`
- Real-time updates via Coral Protocol
- User-in-the-loop approval system

### Usage:

1. Start coral-server: `cd ../coral-server && ./gradlew bootRun`
2. Start agents: `python resume-parser-agent.py`, `python job-searcher-agent.py`, etc.
3. Start frontend: `cd ../frontend && npm run dev`
4. Upload resume and watch the agents work!
