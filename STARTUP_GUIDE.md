# NPL System - Complete Startup Guide

## 📋 Prerequisites

- **Ollama**: Download from https://ollama.ai
- **Node.js**: v16+ (https://nodejs.org/)
- **Python**: v3.8+ (https://python.org/)
- **RAM**: Minimum 8GB (16GB recommended)

## 🚀 Step-by-Step Installation

### Step 1: Install Ollama

#### Windows
1. Download from: https://ollama.ai/download/windows
2. Run the installer
3. Verify: `ollama --version`

#### macOS
1. Download from: https://ollama.ai/download/mac
2. Install and open
3. Verify: `ollama --version`

#### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

### Step 2: Pull an AI Model

Choose one model:

**Fast Option (Recommended for first time):**
```bash
ollama pull llama2
```

**Better Quality Option:**
```bash
ollama pull mistral
```

**Best Quality (if you have 16GB+ RAM):**
```bash
ollama pull dolphin-mixtral
```

**Check installed models:**
```bash
ollama list
```

### Step 3: Clone/Setup Project

```bash
cd c:\Users\hp\Desktop\NPLSystem
```

Or download from GitHub and extract.

### Step 4: Install Dependencies

**Backend:**
```bash
cd backend
npm install
```

**Python Service:**
```bash
cd backend/python_service
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 5: Configure Environment

Create `.env` file in `backend/` directory:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT=30

# Service Ports
PORT=3000
PYTHON_SERVICE_PORT=5000

# CORS
CORS_ORIGIN=http://localhost:3000

# Environment
NODE_ENV=development
```

## 🛠️ Start Services

**Open 4 terminals (or use tmux/screen):**

### Terminal 1: Ollama
```bash
ollama serve
```
Expected output: `Listening on 127.0.0.1:11434`

### Terminal 2: Python NLP Service
```bash
cd backend/python_service
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```
Expected output: `Uvicorn running on http://0.0.0.0:5000`

### Terminal 3: Node Backend
```bash
cd backend
npm run dev
```
Expected output: `Server running on port 3000`

### Terminal 4: React Frontend
```bash
cd frontend
npm start
```
Expected output: Browser opens at `http://localhost:3000`

## ✅ Verify Installation

### Quick Test Script
```bash
cd backend/python_service
python test_system.py
```

This will check:
- ✓ Ollama running
- ✓ Python service running
- ✓ Node backend running
- ✓ Q&A working (general)
- ✓ Q&A working (with text)

### Manual Tests

**Test 1: Backend is running**
```bash
curl http://localhost:3000
```
Should return: `{"message":"Welcome to NPL System","status":"running"}`

**Test 2: Python service is running**
```bash
curl http://localhost:5000/health
```

**Test 3: Ollama is running**
```bash
curl http://localhost:11434/api/tags
```

**Test 4: Text Q&A**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question":"What is AI?"}'
```

## 🎯 Using the System

### Via Web UI

1. Open: http://localhost:3000
2. Two options:

**Option A: Upload Document + Ask Question**
- Click upload button
- Select PDF, DOCX, or TXT file
- Download or type your question
- Click send
- Get answer based on document

**Option B: Ask General Question**
- Type your question
- Click send (no file needed)
- Get general knowledge answer

### Via API (curl)

**General Q&A:**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "features": {
      "answer": true
    }
  }'
```

**Document Q&A (text):**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning is...",
    "question": "What is ML?",
    "features": {
      "answer": true,
      "entities": true
    }
  }'
```

**File Upload (multipart):**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -F "file=@document.pdf" \
  -F "question=What is this about?" \
  -F "features={\"answer\":true}"
```

## 📊 Response Examples

### Successful Q&A Response
```json
{
  "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
  "source": "ollama",
  "model": "llama2",
  "confidence": 0.95,
  "entities": [
    {"text": "Machine learning", "label": "NORP"},
    {"text": "artificial intelligence", "label": "ORG"}
  ]
}
```

### With Text Analysis
```json
{
  "answer": "The main finding is...",
  "tokens": ["The", "main", "finding", "..."],
  "pos": [{"The": "DET"}, {"main": "ADJ"}, ...],
  "entities": [
    {"text": "University of X", "label": "ORG"}
  ],
  "lemmas": [{"tokens": "token"}],
  "confidence": 0.87
}
```

## 🔄 Batch Automation Scripts

### Windows Batch File (start.bat)
Create `start.bat` in project root:
```batch
@echo off
start "Ollama" cmd /k "ollama serve"
start "Python Service" cmd /k "cd backend\python_service && uvicorn app:app --port 5000"
start "Backend" cmd /k "cd backend && npm run dev"
start "Frontend" cmd /k "cd frontend && npm start"
echo All services started!
```

Run: `start.bat`

### Linux/Mac Startup Script (start.sh)
Create `start.sh` in project root:
```bash
#!/bin/bash
trap cleanup EXIT

cleanup() {
    kill $PID_OLLAMA $PID_PYTHON $PID_BACKEND $PID_FRONTEND 2>/dev/null
}

ollama serve &
PID_OLLAMA=$!

cd backend/python_service
uvicorn app:app --port 5000 &
PID_PYTHON=$!

cd ../../backend
npm run dev &
PID_BACKEND=$!

cd ../frontend
npm start &
PID_FRONTEND=$!

wait
```

Run: `chmod +x start.sh && ./start.sh`

## 🐛 Troubleshooting

### Issue: "Ollama is not responding"
```bash
# Check if running
tasklist | findstr ollama

# Start manually
ollama serve

# Check if port is open
netstat -an | findstr 11434
```

### Issue: "Model not found"
```bash
# List models
ollama list

# Pull a model
ollama pull llama2
```

### Issue: "Python service won't start"
```bash
# Check Python version
python --version

# Install dependencies again
pip install -r requirements.txt

# Check if port 5000 is free
lsof -i :5000  # macOS/Linux
netstat -an | findstr 5000  # Windows
```

### Issue: "Backend won't start"
```bash
# Reinstall Node modules
cd backend
rm -rf node_modules
npm install

# Check Node version
node --version

# Try different port
PORT=3001 npm run dev
```

### Issue: "Responses are slow"
1. Use faster model: `ollama pull mistral`
2. Update `.env`: `OLLAMA_TIMEOUT=60`
3. Check system RAM
4. Reduce document size

### Issue: "CORS error"
Update `.env`:
```env
CORS_ORIGIN=http://localhost:3000
```

### Issue: "Cannot upload large files"
Update `backend/index.js` max payload size:
```javascript
app.use(express.json({ limit: '100mb' }));
```

## 🎓 Changing Models

### List available models
```bash
ollama list
```

### Switch to a different model
1. Edit `.env`: `OLLAMA_MODEL=mistral`
2. Restart backend and python service
3. That's it! System will automatically use new model

### Available models
- `llama2` - Balanced (4GB)
- `mistral` - Fast & Smart (4GB)
- `neural-chat` - Optimized Chat (4GB)
- `dolphin-mixtral` - Most Powerful (47GB)
- `orca-mini` - Small & Fast (1.3GB)

## 📈 Performance Metrics

| Operation | Time | Model |
|-----------|------|-------|
| General Q&A | 5-10s | llama2 |
| General Q&A | 3-5s | mistral |
| File parsing | 1-2s | - |
| Total response | 10-15s | end-to-end |

## 🔒 Production Deployment

For production, consider:
1. Use `.env` for all secrets
2. Set `NODE_ENV=production`
3. Use process manager (PM2)
4. Add reverse proxy (nginx)
5. Enable SSL/TLS
6. Monitor resource usage

## 📞 Support

If you encounter issues:
1. Check logs in each terminal
2. Run `python test_system.py`
3. Verify `.env` configuration
4. Check Ollama is running: `ollama serve`
5. Check ports are available

## 📚 Resources

- **Ollama Docs**: https://ollama.ai
- **FastAPI**: https://fastapi.tiangolo.com
- **Express**: https://expressjs.com
- **React**: https://react.dev
- **spaCy**: https://spacy.io

---

**All set! Open http://localhost:3000 and start using your NLP system!** 🎉
