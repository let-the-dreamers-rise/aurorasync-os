@echo off
echo Installing AuroraSync Backend Dependencies...
echo.

python -m pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To start the backend, run: start_backend.bat
pause
