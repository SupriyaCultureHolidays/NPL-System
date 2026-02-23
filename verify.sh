#!/bin/bash

echo "========================================"
echo "NPL System - Verify Ollama Integration"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    exit 1
fi

echo "[INFO] Running verification tests..."
echo ""

cd backend/python_service
python3 test_system.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Verification failed"
    exit 1
fi

echo ""
echo "[SUCCESS] All systems verified!"
echo ""
echo "Next steps:"
echo "1. Open 4 terminals"
echo "2. In Terminal 1: ollama serve"
echo "3. In Terminal 2: cd backend/python_service && uvicorn app:app --port 5000"
echo "4. In Terminal 3: cd backend && npm run dev"
echo "5. In Terminal 4: cd frontend && npm start"
echo ""
echo "Then open: http://localhost:3000"
