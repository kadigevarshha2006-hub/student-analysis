@echo off
title ResumeAI - Intelligent Resume & Job Matcher
echo =======================================================
echo          Starting ResumeAI Application
echo =======================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from python.org and check "Add Python to PATH".
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv backend\venv
    echo [INFO] Installing required dependencies...
    backend\venv\Scripts\pip.exe install -r requirements.txt
)

echo [INFO] Starting FastAPI backend server on http://localhost:8000 ...
echo [INFO] Opening your web browser...
start http://localhost:8000

REM Launch Uvicorn Server bound to all interfaces
backend\venv\Scripts\uvicorn.exe backend.main:app --reload --host 0.0.0.0 --port 8000

pause
