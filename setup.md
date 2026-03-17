# AI Activity Assist - Setup and Execution Guide

This guide details how to install, configure, and run all components of the AI Powered User Monitoring System.

## Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- [Ollama](https://ollama.com/) (installed locally or available via network)
- PostgreSQL (Optional, defaults to SQLite for easy setup)

## 1. Project Initialization

### Backend & Agents (Python)
Open a terminal in the root of the project (`E:\Coding\aiupmassist`) and run:
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate
# (Mac/Linux)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend (React/TypeScript)
Open a second terminal in the root of the project and run:
```bash
cd frontend
npm install
```

## 2. Configuration (`.env`)
A `.env` file must be present at the root of the project (`E:\Coding\aiupmassist\.env`). Here is the required structure:
```env
# Database
DATABASE_URL=sqlite:///./activityassist.db

# JWT Auth
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Storage (Local or S3)
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=./storage

# AI/LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_VISION_MODEL=llava
# Also ensure your agent test credentials match these:
AGENT_USERNAME=testuser
AGENT_PASSWORD=testpass
```

## 3. Running the Components

You will need **4 separate terminal windows** to run all components simultaneously.

### Terminal 1: Ollama (AI Model)
Ensure your chosen vision model is downloaded and running.
```bash
ollama run llava
```
*(Leave this running in the background. The API runs on port 11434 by default).*

### Terminal 2: FastAPI Backend
With your python virtual environment activated:
```bash
cd api
uvicorn main:app --reload --port 8000
```
*The API will be available at `http://localhost:8000`. The DB tables are auto-created on startup.*

### Terminal 3: React Frontend UI
```bash
cd frontend
npm run dev
```
*Access the dashboard at `http://localhost:5173`. You can register a user via the UI/API before logging in.*

### Terminal 4: AI Sequence Processor Worker
With your python virtual environment activated:
```bash
python ai/processor.py
```
*This background worker constantly queries the DB for unclustered activities, analyzes the images via Ollama, and groups them into resilient SOP sequences while ignoring interruptions.*

### Terminal 5 (Optional for Testing Agent locally): Monitoring Agent
With your python virtual environment activated:
```bash
python monitor/agent.py
```
*This starts tracking your mouse/keyboard and taking screenshots every 10 seconds. It compresses images locally then uploads them to the Backend API. Press `Ctrl+C` to stop it.*

## 4. Verification Flow
1. Start the **Backend** and **Frontend**.
2. Open the Frontend UI, click the `Register/Login` and enter your credentials (e.g., `testuser` / `testpass`).
3. Start the **Monitoring Agent**. Perform a few arbitrary tasks on your computer (open notepad, browse the web).
4. Start the **AI sequence processor worker** to cluster your activities.
5. Watch the Frontend Dashboard update with new clustered SOPs waiting for your approval.
