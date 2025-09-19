# 🚀 Official Coral Protocol Integration Setup Guide

## 🎯 **Overview**

This guide shows you how to integrate your AI Job Application agents with:

- **Official Coral Protocol MCP** (Model Context Protocol)
- **Real-time LLM** via AIML API
- **Proper agent registration** and communication
- **Environment-based configuration**

## 📋 **Required API Keys**

### 🔑 **1. AIML API Key (Required)**

```bash
# Get your API key from: https://aimlapi.com
# Free tier available with good limits for hackathon
AIML_API_KEY=your_aiml_api_key_here
```

### 🔑 **2. Optional API Keys**

```bash
# Alternative LLM option
OPENAI_API_KEY=your_openai_api_key_here

# For real job search (optional)
LINKEDIN_API_KEY=your_linkedin_api_key
INDEED_API_KEY=your_indeed_api_key
```

## ⚙️ **Setup Steps**

### **Step 1: Install Dependencies**

```powershell
# Core packages (already installed)
pip install requests openai python-dotenv

# For official Coral Protocol MCP integration
pip install "camel-ai[all]"
```

### **Step 2: Configure Environment**

```powershell
# 1. Copy the example environment file
cp agents/.env.example agents/.env

# 2. Edit .env file with your API keys
# Set AIML_API_KEY=your_actual_api_key_here
```

### **Step 3: Verify Coral Server**

```powershell
# Make sure coral-server is running
cd coral-server
./gradlew run

# In another terminal, verify it's working
python -c "import requests; print('Coral server:', 'RUNNING' if requests.get('http://localhost:5555/api/v1/agents').status_code==200 else 'DOWN')"
```

### **Step 4: Test Official Integration**

```powershell
# Test with official MCP integration
python agents/official-cover-letter-agent.py cover-letter-generator --demo
```

## 🤖 **What the Official Integration Provides**

### **✅ Real Coral Protocol Features:**

- **MCP Communication**: Official Model Context Protocol
- **Agent Registration**: Proper Coral server registration
- **Real-time Messaging**: Live agent-to-agent communication
- **Session Management**: Integrated with coral-studio sessions
- **Tool Access**: Full access to Coral Protocol tools

### **🧠 Real LLM Integration:**

- **AIML API**: High-quality, cost-effective LLM responses
- **Multiple Models**: Access to GPT-4, Claude, Llama, etc.
- **Real-time Generation**: Actual AI-generated content
- **Customizable Parameters**: Temperature, max tokens, etc.

## 🔧 **Configuration Options**

### **Model Settings (in .env):**

```bash
# LLM Provider
MODEL_BASE_URL=https://api.aimlapi.com/v1
MODEL_NAME=openai/gpt-4o-mini         # or meta-llama/llama-3.1-8b-instruct
MODEL_TEMPERATURE=0.3                 # 0.0 = focused, 1.0 = creative
MODEL_MAX_TOKENS=4096                 # Response length limit

# Coral Protocol
CORAL_CONNECTION_URL=http://localhost:5555/devmode/hackathonApp/privkey/session1/sse
CORAL_APPLICATION_ID=hackathonApp
CORAL_SESSION_ID=session1

# Performance
AGENT_TIMEOUT=30000                   # 30 seconds
MESSAGE_WINDOW_SIZE=4096              # Context window
TOKEN_LIMIT=20000                     # Max tokens per session
```

## 🎬 **Demo Commands**

### **Test Individual Agents:**

```powershell
# Official Cover Letter Generator with real LLM
python agents/official-cover-letter-agent.py cover-letter-generator --demo

# Resume Parser (updated for MCP)
python agents/official-resume-parser-agent.py resume-parser --demo

# Job Searcher (updated for MCP)
python agents/official-job-searcher-agent.py job-searcher --demo

# Auditor (updated for MCP)
python agents/official-auditor-agent.py auditor --demo
```

### **Run Multi-Agent System:**

```powershell
# Terminal 1: Resume Parser
python agents/official-resume-parser-agent.py resume-parser

# Terminal 2: Job Searcher
python agents/official-job-searcher-agent.py job-searcher

# Terminal 3: Cover Letter Generator
python agents/official-cover-letter-agent.py cover-letter-generator

# Terminal 4: Auditor
python agents/official-auditor-agent.py auditor
```

## 🌐 **Coral Protocol URLs**

### **Connection Format:**

```
http://localhost:5555/devmode/{applicationId}/{privacyKey}/{sessionId}/sse?waitForAgents={count}&agentId={agentName}
```

### **Your Hackathon URLs:**

```bash
# Main connection
http://localhost:5555/devmode/hackathonApp/privkey/session1/sse

# With agent waiting
http://localhost:5555/devmode/hackathonApp/privkey/session1/sse?waitForAgents=4&agentId=cover-letter-generator
```

## 🎯 **Hackathon Benefits**

### **What This Integration Gives You:**

1. **Official Compliance**: Uses actual Coral Protocol standards
2. **Real AI**: Genuine LLM-powered responses, not simulations
3. **Live Communication**: Agents actually talk to each other
4. **Professional Quality**: Production-ready architecture
5. **Extensible**: Easy to add more agents and capabilities

### **Perfect for Judges:**

- **Technical Depth**: Shows understanding of MCP and agent communication
- **Real Implementation**: Actually working AI, not just mock data
- **Scalable Design**: Can handle real-world usage
- **Documentation**: Clear setup and configuration

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"CAMEL-AI not installed"**

   ```powershell
   pip install "camel-ai[all]"
   ```

2. **"AIML_API_KEY not set"**

   ```powershell
   # Add to .env file
   AIML_API_KEY=your_actual_api_key
   ```

3. **"Cannot connect to coral-server"**

   ```powershell
   # Make sure server is running
   cd coral-server && ./gradlew run
   ```

4. **"Connection timeout"**
   ```bash
   # Increase timeout in .env
   AGENT_TIMEOUT=60000
   ```

## 🎉 **You're Ready!**

Your AI Job Application Agent system now has:

- ✅ **Official Coral Protocol integration**
- ✅ **Real-time LLM responses**
- ✅ **Proper agent communication**
- ✅ **Professional architecture**
- ✅ **Hackathon compliance**

This is exactly what the Internet of Agents hackathon is looking for! 🏆
