@echo off
echo Starting NPL System with Ollama Integration...
echo.
echo Opening 4 terminals - keep them all running
echo.

REM Terminal 1: Ollama
start "Ollama" cmd /k "ollama serve"
timeout /t 3

REM Terminal 2: Python Service
start "Python NLP Service" cmd /k "cd /d C:\Users\hp\Desktop\NPLSystem\backend\python_service && python -m uvicorn app:app --reload --port 5000"
timeout /t 3

REM Terminal 3: Node Backend
start "Node Backend" cmd /k "cd /d C:\Users\hp\Desktop\NPLSystem\backend && npm run dev"
timeout /t 3

REM Terminal 4: React Frontend
start "React Frontend" cmd /k "cd /d C:\Users\hp\Desktop\NPLSystem\frontend && npm start"
timeout /t 3

echo.
echo All services starting...
echo Wait 10 seconds, then open: http://localhost:3000
echo.
timeout /t 10
start "" http://localhost:3000

echo Done! All 4 terminals should be running.
