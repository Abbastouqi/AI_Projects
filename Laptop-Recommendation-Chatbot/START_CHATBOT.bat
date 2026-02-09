@echo off
echo ========================================
echo   Starting Laptop Chatbot Backend
echo ========================================
echo.

cd backend
echo Installing dependencies...
pip install fastapi uvicorn python-dotenv sqlalchemy pydantic pydantic-settings

echo.
echo Starting backend server...
python main.py

pause
