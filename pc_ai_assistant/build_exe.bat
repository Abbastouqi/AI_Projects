@echo off
REM PC AI Assistant Build Script for Windows
REM This script creates a standalone .exe file using PyInstaller

echo.
echo ================================================================================
echo PC AI ASSISTANT - EXE BUILDER
echo ================================================================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Create build directory
if not exist "dist" mkdir dist
if not exist "build" mkdir build

echo.
echo Building standalone executable...
echo This may take a few minutes...
echo.

REM Build with PyInstaller
pyinstaller --onefile ^
    --name "PC_AI_Assistant" ^
    --icon=icon.ico ^
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
    echo ================= BUILD SUCCESSFUL =================
    echo.
    echo ✅ Executable created: dist\PC_AI_Assistant.exe
    echo.
    echo 📖 To distribute:
    echo    1. Copy dist\PC_AI_Assistant.exe to any PC
    echo    2. Double-click to run
    echo    3. Browser will open automatically
    echo.
    echo 📝 Note: First run may take a minute to extract files
    echo.
) else (
    echo.
    echo ❌ Build failed. Check errors above.
    echo.
)

pause
