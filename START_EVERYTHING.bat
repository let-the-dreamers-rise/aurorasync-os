@echo off
echo ========================================
echo   AuroraSync OS - Complete Startup
echo ========================================
echo.

echo This will start:
echo   1. Backend API (with ML predictions)
echo   2. Frontend UI
echo.
echo Press any key to continue...
pause >nul

echo.
echo ========================================
echo Step 1: Installing Backend Dependencies
echo ========================================
cd backend
python -m pip install -r requirements-simple.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install backend dependencies
    echo Make sure Python is installed and in PATH
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Testing ML Predictions
echo ========================================
python test_ml_predictions.py
if errorlevel 1 (
    echo.
    echo WARNING: ML test had issues, but continuing...
)

echo.
echo ========================================
echo Step 3: Starting Backend Server
echo ========================================
echo Backend will run on: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
start cmd /k "cd /d %CD% && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo Step 4: Starting Frontend
echo ========================================
cd ..\frontend
echo Frontend will run on: http://localhost:5173
echo.
start cmd /k "cd /d %CD% && npm run dev"

echo.
echo ========================================
echo ✅ STARTUP COMPLETE!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Test these pages:
echo   - Predictions: http://localhost:5173/predictions
echo   - Voice AI: http://localhost:5173/voice-ai
echo.
echo Press any key to exit (servers will keep running)
pause >nul
