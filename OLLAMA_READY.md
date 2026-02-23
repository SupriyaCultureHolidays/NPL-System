# 🧠 NPL System - Ollama Integration Complete

Your Natural Language Processing system has been successfully integrated with Ollama for AI-powered Q&A! This system now supports two powerful modes:

## 🎯 What's New

### ✨ Two-Mode Q&A System

#### 1️⃣ Document-Based Q&A
Upload a file (PDF, DOCX, TXT) and ask questions about its content
- Extracts text automatically
- Finds relevant content
- Provides accurate answers based on the document
- Shows confidence scores

#### 2️⃣ General Q&A
Ask any general knowledge question without uploading a file
- Uses Ollama LLM's general knowledge
- Works offline (after model is downloaded)
- Fast and accurate responses

## 📦 What Was Added/Updated

### Backend Improvements
- ✅ Added `.env` configuration support
- ✅ Added dotenv dependency to package.json
- ✅ Improved error handling and logging
- ✅ Added health check endpoints
- ✅ Environment-based service URLs

### Python Service Enhancements
- ✅ Added DOCX file support (python-docx)
- ✅ Improved Ollama integration with better prompts
- ✅ Added configurable model selection
- ✅ Added logging and error handling
- ✅ Added endpoint for system health checks
- ✅ Better context-aware Q&A
- ✅ Fallback to spaCy when Ollama unavailable

### Configuration
- ✅ `.env.example` configuration template
- ✅ Environment-based settings for all services

### Documentation  
- ✅ `OLLAMA_SETUP.md` - Installation guide
- ✅ `OLLAMA_INTEGRATION.md` - How it works
- ✅ `STARTUP_GUIDE.md` - Step-by-step startup
- ✅ `verify.bat` - Windows verification script
- ✅ `verify.sh` - Unix/Mac verification script

### Testing
- ✅ `backend/python_service/test_system.py` - Comprehensive system test

## 🚀 Quick Start (5 Minutes)

### 1. Install Ollama
- Windows: Download from https://ollama.ai/download/windows
- Install and run

### 2. Pull a Model
```bash
ollama pull llama2
```

### 3. Run Verification
```bash
cd backend/python_service
python test_system.py
```

### 4. Start Services (4 terminals)

**Terminal 1:**
```bash
ollama serve
```

**Terminal 2:**
```bash
cd backend/python_service
uvicorn app:app --port 5000
```

**Terminal 3:**
```bash
cd backend
npm install
npm run dev
```

**Terminal 4:**
```bash
cd frontend
npm install
npm start
```

### 5. Open Browser
```
http://localhost:3000
```

## 📝 How to Use

### Web Interface
1. Open http://localhost:3000
2. **For document Q&A:**
   - Click file upload
   - Select PDF, DOCX, or TXT
   - Type your question
   - Click send
3. **For general Q&A:**
   - Just type your question
   - Click send

### API Usage

**General Question:**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "What is AI?"}'
```

**Document Question:**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Document content here",
    "question": "What is this about?",
    "features": {"answer": true}
  }'
```

**File Upload:**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -F "file=@document.pdf" \
  -F "question=What is this about?"
```

## 📋 Supported File Formats

| Format | Support | Method |
|--------|---------|--------|
| PDF (.pdf) | ✅ | pdfplumber |
| DOCX (.docx) | ✅ | python-docx |
| TXT (.txt) | ✅ | Text read |
| DOC (.doc) | ⚠️ | Via DOCX conversion |

## ⚙️ Configuration

Create `.env` in `backend/` directory:

```env
# Ollama Setup
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT=30

# Service Configuration
PORT=3000
PYTHON_SERVICE_PORT=5000
PYTHON_SERVICE_URL=http://localhost:5000

# CORS
CORS_ORIGIN=http://localhost:3000

# Environment
NODE_ENV=development
```

## 🤖 Available Models

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| llama2 | 4GB | Moderate | Good | `ollama pull llama2` |
| mistral | 4GB | Fast | Excellent | `ollama pull mistral` |
| neural-chat | 4GB | Fast | Good | `ollama pull neural-chat` |
| dolphin-mixtral | 47GB | Slow | Excellent | `ollama pull dolphin-mixtral` |
| orca-mini | 1.3GB | Very Fast | Basic | `ollama pull orca-mini` |

**For first time:** Use `llama2`
**For faster responses:** Use `mistral` or `neural-chat`
**For best quality:** Use `dolphin-mixtral` (requires 50GB+ disk)

## 🧪 Testing

### Run Full System Test
```bash
cd backend/python_service
python test_system.py
```

### Check Individual Services

**Ollama:**
```bash
curl http://localhost:11434/api/tags
```

**Python Service:**
```bash
curl http://localhost:5000/health
```

**Node Backend:**
```bash
curl http://localhost:3000/health
```

## 🔧 Troubleshooting

### Ollama not found
```bash
# Check if installed
ollama --version

# Start manually
ollama serve
```

### Model not found
```bash
# List models
ollama list

# Install
ollama pull llama2
```

### Slow responses
1. Use faster model: `ollama pull mistral`
2. Increase timeout in `.env`
3. Check system RAM (min 8GB)

### Python service won't start
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version
```

### Node backend won't start
```bash
# Reinstall dependencies
cd backend
npm install

# Check Node version
node --version
```

See `STARTUP_GUIDE.md` for more troubleshooting.

## 📚 Documentation Files

- **STARTUP_GUIDE.md** - Complete startup instructions
- **OLLAMA_SETUP.md** - Ollama installation details
- **OLLAMA_INTEGRATION.md** - How the integration works
- **README.md** (original) - Project overview

## 🔄 System Architecture

```
┌─────────────┐
│   Browser   │ (React)
└──────┬──────┘
       │
┌──────▼──────┐
│   Backend   │ (Node.js/Express)
└──────┬──────┘
       │
┌──────▼──────────────────┐
│ Python NLP Service      │ (FastAPI)
└──────┬──────────┬───────┘
       │          │
    spaCy     Ollama LLM
       │          │
   NLP Analysis   Q&A
```

## 🎓 Example Use Cases

1. **Research Paper Analysis**
   - Upload paper (PDF)
   - Ask: "What are the main findings?"
   - Get answer based on paper

2. **Document Summarization**
   - Upload document
   - Ask: "Summarize this"
   - Get AI summary

3. **General Knowledge Q&A**
   - Ask: "How does photosynthesis work?"
   - Get detailed answer

4. **Named Entity Recognition**
   - Upload text with names
   - Get automatic extraction of people, places, organizations

5. **Code Documentation**
   - Upload README or code
   - Ask: "How do I use this?"
   - Get relevant information

## 🎯 Key Features

- ✅ **Dual Mode**: Document + General Q&A
- ✅ **Multiple Formats**: PDF, DOCX, TXT
- ✅ **Fast Processing**: Response in 5-15 seconds
- ✅ **Accurate**: Uses AI language models
- ✅ **Offline**: Works without internet (after setup)
- ✅ **Configurable**: Easy model switching
- ✅ **Scalable**: Can handle large documents

## 🚀 Next Steps

1. ✅ Install Ollama
2. ✅ Pull a model (`ollama pull llama2`)
3. ✅ Run verification (`python test_system.py`)
4. ✅ Start all services
5. ✅ Open http://localhost:3000
6. ✅ Try uploading a document
7. ✅ Try asking a general question

## 💡 Tips

- Start with `.txt` files for testing
- Use smaller models (`llama2`, `mistral`) for faster responses
- Larger models need more RAM
- Ollama uses GPU if available (NVIDIA, AMD, Apple Silicon)
- Keep documents under 50MB
- Check `.env` configuration if services won't connect

## 📞 Support

If you encounter issues:
1. Check logs in terminal windows
2. Run `python test_system.py`
3. Verify all `.env` settings
4. Make sure all ports are available
5. Check `STARTUP_GUIDE.md` troubleshooting section

## 📖 Documentation

- **STARTUP_GUIDE.md** - How to start the system
- **OLLAMA_SETUP.md** - Ollama setup details  
- **OLLAMA_INTEGRATION.md** - Complete integration guide
- Original **README.md** - Project info

---

**Your NPL System is ready! Enjoy using AI-powered document analysis and Q&A!** 🎉

Last updated: February 23, 2026
