@echo off
echo Installing ML packages with pre-built wheels...
echo This avoids compilation issues with Python 3.13
echo.

REM Install packages that don't need compilation first
python -m pip install fastapi uvicorn[standard] pydantic pydantic-settings sqlalchemy python-dotenv python-multipart alembic

REM Install ML packages using pre-built wheels only (no compilation)
python -m pip install --only-binary :all: numpy pandas joblib

REM Try to install scikit-learn with pre-built wheel
python -m pip install --only-binary :all: scikit-learn

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Scikit-learn pre-built wheel not available for Python 3.13
    echo Trying alternative approach...
    echo.
    
    REM Try installing from conda-forge or use older compatible version
    python -m pip install scikit-learn==1.4.0 --only-binary :all:
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Could not install scikit-learn with pre-built wheels.
        echo.
        echo RECOMMENDATION: Use Python 3.11 or 3.12 for full ML support
        echo OR use simplified backend (requirements-simple.txt)
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo All packages installed successfully!
echo You can now start the backend with ML support.
echo.
pause
