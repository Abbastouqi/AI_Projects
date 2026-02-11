@echo off
REM Simple step-by-step setup wizard for PC AI Assistant

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo   PC AI ASSISTANT - SETUP WIZARD
echo ================================================================================
echo.
echo This wizard will help you build a standalone .exe file for distribution.
echo.

REM Check Python
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found: %PYTHON_VERSION%
echo.

REM Install dependencies
echo Step 2: Installing dependencies...
call pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Run this in PowerShell as Administrator and try again
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

REM Build executable
echo Step 3: Building executable...
echo (This may take 2-5 minutes)
echo.
call pyinstaller --onefile ^
    --name "PC_AI_Assistant" ^
    --hidden-import=flask ^
    --hidden-import=yaml ^
    --hidden-import=playwright ^
    --collect-all flask ^
    --collect-all yaml ^
    --collect-all playwright ^
    --collect-all jinja2 ^
    --add-data "templates:templates" ^
    --add-data "static:static" ^
    --add-data "data:data" ^
    --add-data "agent:agent" ^
    --add-data "config.yaml:." ^
    --windowed ^
    launcher.py

if %errorlevel% equ 0 (
    echo.
    echo ================================================================================
    echo   ✅ BUILD SUCCESSFUL
    echo ================================================================================
    echo.
    echo 📦 Executable file created:
    echo    dist\PC_AI_Assistant.exe
    echo.
    echo 🚀 To run:
    echo    Double-click: dist\PC_AI_Assistant.exe
    echo.
    echo 📤 To distribute:
    echo    1. Copy dist\PC_AI_Assistant.exe to any Windows PC
    echo    2. No Python needed on the target PC
    echo.
    echo 📖 For more info, read: INSTALL.md
    echo.
) else (
    echo.
    echo ❌ Build failed. Check errors above.
    echo.
)

pause
