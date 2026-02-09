@echo off
REM Recruitment Automation System - Windows Startup Script

echo.
echo ======================================
echo Recruitment Automation System
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Could not create virtual environment
        echo Make sure Python 3.8+ is installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Could not install dependencies
        pause
        exit /b 1
    )
)

REM Check for .env file
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Update .env with your OpenAI API key before running the app!
    echo Edit .env and set: OPENAI_API_KEY=your_key_here
    echo.
    pause
)

REM Run the application
echo.
echo Starting Recruitment Automation System...
echo Launching Streamlit app...
echo.

streamlit run app.py

pause
