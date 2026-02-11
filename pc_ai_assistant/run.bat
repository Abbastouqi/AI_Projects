@echo off
REM Quick start script - Run the application directly from Python

cd /d "%~dp0"

echo ================================================================================
echo PC AI ASSISTANT
echo ================================================================================
echo.

REM Activate venv if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Install requirements if needed
echo Checking dependencies...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -q -r requirements.txt
)

echo.
echo ✅ Starting application...
echo.
echo 📱 Open your browser to: http://127.0.0.1:5000
echo 🛑 Press Ctrl+C to stop
echo.

python launcher.py

pause
