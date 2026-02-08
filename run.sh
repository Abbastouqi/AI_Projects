#!/bin/bash
# Recruitment Automation System - macOS/Linux Startup Script

echo ""
echo "======================================"
echo "Recruitment Automation System"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Could not create virtual environment"
        echo "Make sure Python 3.8+ is installed"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Could not install dependencies"
        exit 1
    fi
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Update .env with your OpenAI API key before running the app!"
    echo "Edit .env and set: OPENAI_API_KEY=your_key_here"
    echo ""
fi

# Run the application
echo ""
echo "Starting Recruitment Automation System..."
echo "Launching Streamlit app..."
echo ""

streamlit run app.py
