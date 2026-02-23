# NPL System - Quick Reference Card

## 🚀 3-Minute Setup

### Step 1: Install
```bash
ollama pull llama2
cd backend && npm install
cd backend/python_service && pip install -r requirements.txt
cd frontend && npm install
```

### Step 2: Create .env
Copy `backend/.env.example` to `backend/.env`

### Step 3: Start (4 Terminals)
```bash
# Terminal 1
ollama serve

# Terminal 2
cd backend/python_service && uvicorn app:app --port 5000

# Terminal 3
cd backend && npm run dev

# Terminal 4
cd frontend && npm start
```

### Step 4: Open Browser
```
http://localhost:3000
```

---

## 💡 Quick Usage

### Upload Document & Ask
1. Click file upload
2. Select PDF/DOCX/TXT
3. Type question
4. Click send
5. Get answer

### Ask General Question
1. Type question
2. Click send (no file needed)
3. Get answer

---

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| App | http://localhost:3000 | Web interface |
| Backend | http://localhost:3000/health | API health |
| Python Service | http://localhost:5000/health | NLP health |
| Ollama | http://localhost:11434/api/tags | LLM status |

---

## 📝 API Endpoints

### General Q&A
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question":"What is AI?"}'
```

### Document Q&A
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"content here","question":"Q here?"}'
```

### File Upload
```bash
curl -X POST http://localhost:3000/api/analyze \
  -F "file=@document.pdf" \
  -F "question=What is this?"
```

---

## 🤖 Model Commands

```bash
# List installed
ollama list

# Install new
ollama pull mistral
ollama pull neural-chat

# Use in .env
OLLAMA_MODEL=mistral
```

---

## ⚙️ Environment Variables

```env
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT=30
PORT=3000
NODE_ENV=development
CORS_ORIGIN=http://localhost:3000
```

---

## 🧪 Verify Installation

```bash
cd backend/python_service
python test_system.py
```

Expected: ✓ All tests pass

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Ollama not responding | Run: `ollama serve` |
| Model not found | Run: `ollama pull llama2` |
| Python won't start | Run: `pip install -r requirements.txt` |
| Slow response | Use: `OLLAMA_MODEL=mistral` |
| Port in use | Change PORT in .env |

---

## 📚 Key Documentation

- **STARTUP_GUIDE.md** - Full setup guide
- **OLLAMA_INTEGRATION.md** - How it works
- **OLLAMA_SETUP.md** - Detailed installation

---

## 🎯 Supported Formats

✅ Built-in NLP:
- Tokenization
- POS tagging
- Entity recognition
- Lemmatization
- Dependency parsing

✅ Q&A Modes:
- Document-based (PDF/DOCX/TXT)
- General knowledge

---

## 💻 System Requirements

- RAM: 8GB minimum (16GB recommended)
- Disk: 20GB minimum
- Python 3.8+
- Node 16+
- Ollama installed

---

## 🔄 Typical Workflow

```
1. Start 4 terminals
2. Run: ollama serve
3. Run: uvicorn app:app --port 5000
4. Run: npm run dev  
5. Run: npm start
6. Open: http://localhost:3000
7. Upload file OR ask question
8. Get AI-powered answer!
```

---

## ⏱️ Response Times

| Scenario | Time |
|----------|------|
| Simple Q&A | 5-10s |
| Complex Q&A | 10-15s |
| PDF Analysis | 15-20s |
| DOCX Analysis | 10-15s |

---

## 🎓 Example Questions

- "What is this document about?"
- "Summarize this document"
- "Extract key points"
- "Answer this: [question]"
- "What are the main topics?"

---

## 📞 Help

1. Check logs in each terminal
2. Run: `python test_system.py`
3. Verify .env configuration
4. Check Ollama: `ollama list`
5. See STARTUP_GUIDE.md

---

## 🎉 You're Ready!

Your NPL System with Ollama is set up!

Go to: **http://localhost:3000**

Enjoy! 🚀
