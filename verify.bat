@echo off
echo ========================================
echo NPL System - Verify Ollama Integration
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    exit /b 1
)

echo [INFO] Running verification tests...
echo.

cd backend\python_service
python test_system.py

if errorlevel 1 (
    echo.
    echo [ERROR] Verification failed
    exit /b 1
)

echo.
echo [SUCCESS] All systems verified!
echo.
echo Next steps:
echo 1. Open 4 terminals
echo 2. In Terminal 1: ollama serve
echo 3. In Terminal 2: cd backend\python_service ^&^& uvicorn app:app --port 5000
echo 4. In Terminal 3: cd backend ^&^& npm run dev
echo 5. In Terminal 4: cd frontend ^&^& npm start
echo.
echo Then open: http://localhost:3000
