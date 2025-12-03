@echo off
echo ========================================
echo AuroraSync ML Setup (No scikit-learn!)
echo ========================================
echo.

echo Step 1: Installing minimal dependencies...
python -m pip install -r requirements-simple.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Testing ML predictions...
python test_ml_predictions.py
if errorlevel 1 (
    echo ERROR: ML test failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ SUCCESS! ML predictions working!
echo ========================================
echo.
echo You can now start the backend with:
echo   start_backend.bat
echo.
pause
