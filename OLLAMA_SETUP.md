# Ollama Integration Setup Guide

## Overview
This system integrates Ollama for AI-powered Q&A with two capabilities:
1. **Document-based Q&A**: Upload PDFs, DOCX, or TXT files and ask questions about their content
2. **General Q&A**: Ask general knowledge questions for accurate answers

## Step 1: Install Ollama

### Windows Installation
1. Download Ollama from: https://ollama.ai/download/windows
2. Run the installer and follow the prompts
3. Ollama will run as a service in the background
4. Verify installation by opening Command Prompt and running:
   ```cmd
   ollama --version
   ```

### Verify Ollama is Running
- Ollama should be accessible at `http://localhost:11434`
- Test connection:
  ```cmd
  curl http://localhost:11434/api/tags
  ```
  or from PowerShell:
  ```powershell
  Invoke-WebRequest -Uri "http://localhost:11434/api/tags"
  ```

## Step 2: Install Models

### Option A: Recommended - Llama 2 (Fast, Good Quality)
```cmd
ollama pull llama2
```
- Size: ~4GB
- Speed: Fast
- Quality: Good for document Q&A and general questions

### Option B: Better Quality - Mistral
```cmd
ollama pull mistral
```
- Size: ~4GB
- Speed: Moderate
- Quality: Better reasoning, good for complex questions

### Option C: Best Quality - Neural Chat (Recommended for Production)
```cmd
ollama pull neural-chat
```
- Size: ~4GB
- Speed: Good
- Quality: Fast and accurate

### Option D: Document-focused - Dolphin Mixtral
```cmd
ollama pull dolphin-mixtral
```
- Size: ~47GB
- Speed: Slower but most capable
- Quality: Excellent for complex document analysis

**Recommended for your system**: Use `llama2` or `mistral` to start

## Step 3: Configure Your System

### 1. Update Environment Variables
Create or update `.env` file in the backend directory:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT=30

# Python Service
PYTHON_SERVICE_URL=http://localhost:5000
PORT=3000

# Document Processing
MAX_FILE_SIZE=50000000
SUPPORTED_FORMATS=pdf,txt,docx
```

### 2. Install required Python package for DOCX
```cmd
cd backend/python_service
pip install python-docx
```

## Step 4: Start the Services

### Terminal 1: Start Ollama (if not running as service)
```cmd
ollama serve
```

### Terminal 2: Start Python NLP Service
```cmd
cd backend/python_service
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

### Terminal 3: Start Node Backend
```cmd
cd backend
npm run dev
```
or `npm start` for production

### Terminal 4: Start React Frontend
```cmd
cd frontend
npm start
```

## Step 5: Test the Integration

### Test Document-based Q&A
1. Open the web app at `http://localhost:3000`
2. Click the file upload button
3. Upload a PDF, DOCX, or TXT file
4. Ask a question like: "What is the main topic of this document?"
5. You should get an answer based on the document content

### Test General Q&A
1. In the chat interface (without uploading a file)
2. Ask: "What is machine learning?"
3. You should get a comprehensive answer using Ollama's general knowledge

## Step 6: Troubleshooting

### Ollama not responding
```cmd
# Check if running
tasklist | findstr ollama

# Restart Ollama service on Windows
net stop ollama
net start ollama

# Or manually start
ollama serve
```

### Model not found
```cmd
# List available models
ollama list

# Pull a model if needed
ollama pull llama2
```

### Python service can't connect to Ollama
1. Verify Ollama is running on localhost:11434
2. Check firewall settings
3. Verify no port conflicts
4. Check logs in Python service terminal

### Slow responses
- Check if Ollama message queue is full
- Consider using a smaller/faster model
- Increase timeout in `.env`

## Performance Tips

1. **For faster responses**: Use `mistral` or `neural-chat` instead of larger models
2. **For better document understanding**: Use `dolphin-mixtral` or `llama2:13b`
3. **GPU acceleration**: Ollama automatically uses GPU if available
4. **Memory**: Ensure at least 8GB RAM for smooth operation

## API Endpoints

### Backend API
- `POST /api/analyze` - Send text/file with optional question

### Python Service API
- `POST /analyze` - Full analysis with Ollama integration
- `POST /api/analyze` - Alternative endpoint

### Ollama Direct API
- `POST http://localhost:11434/api/generate` - Direct model inference

## Model Characteristics

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| neural-chat | ~4GB | Fast | Good | Balanced use |
| llama2 | ~4GB | Moderate | Good | General Q&A |
| mistral | ~4GB | Moderate | Very Good | Complex questions |
| dolphin-mixtral | ~47GB | Slow | Excellent | Advanced analysis |

## Next Steps

1. Install Ollama following Step 1
2. Pull a model (Step 2) - start with `llama2`
3. Update `.env` file (Step 3)
4. Start all services (Step 4)
5. Test the system (Step 5)

For more help: https://ollama.ai
