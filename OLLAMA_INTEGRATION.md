# NPL System - Ollama Integration Guide

## Quick Start

### 1. Install Ollama
- **Windows**: Download from https://ollama.ai/download/windows
- **macOS**: Download from https://ollama.ai/download/mac
- **Linux**: `curl https://ollama.ai/install.sh | sh`

### 2. Pull a Model
```cmd
ollama pull llama2
```

### 3. Install Dependencies
```cmd
cd backend/python_service
pip install -r requirements.txt
```

### 4. Start Services

**Terminal 1** - Ollama (if not running as service):
```cmd
ollama serve
```

**Terminal 2** - Python NLP Service:
```cmd
cd backend/python_service
uvicorn app:app --host 0.0.0.0 --port 5000
```

**Terminal 3** - Node Backend:
```cmd
cd backend
npm install
npm run dev
```

**Terminal 4** - React Frontend:
```cmd
cd frontend
npm install
npm start
```

### 5. Verify Installation
```cmd
cd backend/python_service
python test_system.py
```

---

## How It Works

### Architecture
```
┌─────────────┐
│   Browser   │ (React UI)
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │ (Node.js + Express)
└──────┬──────┘
       │ HTTP
       ▼
┌──────────────────────┐
│ Python NLP Service   │ (FastAPI)
└──────┬──────────────┬┘
       │              │
    spaCy         Ollama LLM
```

### Two-Mode Q&A System

#### Mode 1: Document-Based Q&A
When you upload a file (PDF, DOCX, TXT) and ask a question:

1. **File Processing**: Extract text from the document
2. **Relevance Check**: Check if question relates to document content
3. **Context Pass**: Send document excerpt + question to Ollama
4. **Answer**: Ollama uses document context for accurate answers

Example:
```
User uploads: research_paper.pdf
User asks: "What are the main findings?"
System: Extracts text → Checks relevance → Sends context to Ollama → Returns answer based on paper
```

#### Mode 2: General Q&A
When you ask a question without uploading a file:

1. **No Context**: Question goes to Ollama without document context
2. **General Knowledge**: Ollama uses its training knowledge to answer
3. **Answer**: Returns accurate general knowledge answer

Example:
```
User asks: "What is quantum computing?"
System: Sends question to Ollama (no context) → Returns general knowledge answer
```

---

## Configuration

### Environment Variables
Create `.env` in `backend/` directory:

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT=30

# Python Service
PYTHON_SERVICE_URL=http://localhost:5000
PYTHON_SERVICE_PORT=5000

# Node Backend
PORT=3000
NODE_ENV=development

# File Handling
MAX_FILE_SIZE=50000000
SUPPORTED_FORMATS=pdf,txt,docx
```

### Supported Models
| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| llama2 | 4GB | Moderate | Good | `ollama pull llama2` |
| mistral | 4GB | Moderate | Excellent | `ollama pull mistral` |
| neural-chat | 4GB | Fast | Good | `ollama pull neural-chat` |
| dolphin-mixtral | 47GB | Slow | Excellent | `ollama pull dolphin-mixtral` |

---

## API Endpoints

### Frontend → Backend
```
POST /api/analyze
```

**Request (with file):**
```json
{
  "question": "What is this about?",
  "file": <binary>,
  "features": {"answer": true, "entities": true}
}
```

**Request (text only):**
```json
{
  "text": "Document content here",
  "question": "What is this about?",
  "features": {"answer": true, "tokens": true}
}
```

**Request (general question):**
```json
{
  "question": "What is AI?",
  "features": {"answer": true}
}
```

**Response:**
```json
{
  "answer": "Detailed answer here",
  "source": "ollama",
  "model": "llama2",
  "confidence": 0.95,
  "entities": [...],
  "tokens": [...]
}
```

### Backend → Python Service
```
POST /analyze
POST /api/analyze
GET /health
GET /
```

### Python Service → Ollama
```
POST http://localhost:11434/api/generate
```

---

## Features

### Supported File Formats
- **PDF** (.pdf) - via pdfplumber
- **DOCX** (.docx) - via python-docx
- **TXT** (.txt) - plain text

### NLP Analysis
When text is provided, the system returns:
- **Tokens**: Tokenized words
- **POS**: Part of speech tags
- **Entities**: Named entities (PERSON, ORG, LOC, etc.)
- **Lemmas**: Word lemmatization
- **Dependencies**: Dependency parsing

### Q&A Capabilities
- **Document Q&A**: Answer questions based on uploaded file content
- **General Q&A**: Answer general knowledge questions
- **Confidence Scores**: Get confidence ratings for answers
- **Evidence**: Get supporting sentences for answers

---

## Troubleshooting

### Ollama Not Running
```cmd
# Check if running
tasklist | findstr ollama

# Start manually
ollama serve

# Check if listening
netstat -an | findstr 11434
```

### No Models Available
```cmd
# List installed models
ollama list

# Install a model
ollama pull llama2

# Check model file size is downloaded completely
ollama show llama2
```

### Slow Responses
1. Use a faster model: `mistral` or `dolphin-mixtral`
2. Increase timeout in `.env`: `OLLAMA_TIMEOUT=60`
3. Check system resources (RAM, CPU)
4. Consider using GPU: Ollama uses GPU automatically if available

### Python Service Won't Start
```cmd
# Check if port 5000 is in use
netstat -an | findstr 5000

# Try different port
uvicorn app:app --port 5001

# Check spacy model is installed
python -m spacy download en_core_web_sm
```

### Backend Won't Start
```cmd
# Install dependencies
cd backend
npm install

# Check if port 3000 is free
netstat -an | findstr 3000

# Start with debug
npm run dev
```

### CORS Errors
Add or update `.env`:
```env
CORS_ORIGIN=http://localhost:3000
```

---

## Performance Tips

1. **Faster Responses**
   - Use `mistral` or `neural-chat` instead of `llama2`
   - Reduce document size (truncate to first 2000 chars)
   - Increase system RAM

2. **Better Accuracy**
   - Use `dolphin-mixtral` for complex documents
   - Include more context in documents
   - Ask specific questions

3. **System Optimization**
   - Monitor memory usage: `tasklist`
   - Check Ollama CPU usage
   - Use SSD for faster file operations

---

## Testing

### Run System Tests
```cmd
cd backend/python_service
python test_system.py
```

### Manual Testing

**Test 1: General Q&A**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

**Test 2: Document Q&A**
- Open web app
- Upload a PDF/TXT file
- Ask a question about its content

**Test 3: NLP Analysis**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "John works at Microsoft", "features": {"entities": true}}'
```

---

## Example Use Cases

### Use Case 1: Research Paper Analysis
1. Upload a research paper (PDF)
2. Ask: "What are the main findings?"
3. Get answer based on paper content

### Use Case 2: Customer Support
1. No file upload
2. Ask: "How do I reset my password?"
3. Get general knowledge answer

### Use Case 3: Document Summarization
1. Upload a long document
2. Ask: "Summarize this document"
3. Get AI-generated summary

### Use Case 4: Named Entity Recognition
1. Upload text with names and locations
2. Get automatic extraction of people, places, organizations

---

## Advanced Configuration

### Using .env in Node Backend
```javascript
import dotenv from 'dotenv';
dotenv.config();

const OLLAMA_URL = process.env.OLLAMA_BASE_URL || 'http://localhost:11434';
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || 'llama2';
```

### Using .env in Python Service
```python
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))
```

### Docker Deployment (Optional)
See [Docker Setup Guide](./DOCKER_SETUP.md)

---

## FAQ

**Q: Can I use a different Ollama model?**
A: Yes! Change `OLLAMA_MODEL` in `.env` and restart services.

**Q: What's the maximum file size?**
A: Default is 50MB. Change `MAX_FILE_SIZE` in `.env`.

**Q: Can I run this on a Mac?**
A: Yes, Ollama supports Mac. Install from ollama.ai/download/mac

**Q: How much RAM do I need?**
A: At least 8GB. Larger models need more RAM.

**Q: Can I use GPU acceleration?**
A: Yes, Ollama automatically uses GPU if available (NVIDIA, AMD, Apple Silicon).

---

## Support & Resources

- **Ollama**: https://ollama.ai
- **spaCy**: https://spacy.io
- **FastAPI**: https://fastapi.tiangolo.com
- **Pdfplumber**: https://github.com/jamesturk/pdfplumber
- **python-docx**: https://python-docx.readthedocs.io

---

Last Updated: February 2026
