@echo off
echo ========================================
echo Building ALL Executables
echo ========================================
echo.

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller
echo.

REM Build Desktop GUI
echo ========================================
echo [1/2] Building Desktop GUI...
echo ========================================
pyinstaller --name=RiphahAI-Desktop ^
    --onefile ^
    --windowed ^
    --add-data="config.example.json;." ^
    --hidden-import=pyttsx3 ^
    --hidden-import=pyttsx3.drivers ^
    --hidden-import=pyttsx3.drivers.sapi5 ^
    --hidden-import=speech_recognition ^
    --hidden-import=selenium ^
    --hidden-import=webdriver_manager ^
    main.py

echo.
echo Desktop GUI built successfully!
echo.

REM Build Web Server
echo ========================================
echo [2/2] Building Web Server...
echo ========================================
pyinstaller --name=RiphahAI-WebServer ^
    --onefile ^
    --console ^
    --add-data="templates;templates" ^
    --add-data="config.example.json;." ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    --hidden-import=pyttsx3 ^
    --hidden-import=pyttsx3.drivers ^
    --hidden-import=pyttsx3.drivers.sapi5 ^
    --hidden-import=speech_recognition ^
    --hidden-import=selenium ^
    --hidden-import=webdriver_manager ^
    web_server.py

echo.
echo Web Server built successfully!
echo.

REM Copy files to dist
echo Copying additional files...
copy config.example.json dist\
copy README.md dist\README.txt

REM Create distribution README
echo Creating distribution README...
(
echo Riphah AI Assistant - Executable Distribution
echo.
echo QUICK START:
echo.
echo 1. Desktop Application:
echo    - Double-click RiphahAI-Desktop.exe
echo    - Use the GUI interface
echo.
echo 2. Web Server:
echo    - Double-click RiphahAI-WebServer.exe
echo    - Open browser: http://localhost:5000
echo.
echo REQUIREMENTS:
echo - Windows 10/11
echo - Chrome browser
echo - Microphone for voice input
echo - Internet connection
echo.
echo COMMANDS:
echo - "apply for admission"
echo - "explore programs"
echo - "admission dates"
echo.
echo For more info, see README.txt
) > dist\QUICK_START.txt

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Files created in 'dist' folder:
echo   - RiphahAI-Desktop.exe
echo   - RiphahAI-WebServer.exe
echo   - config.example.json
echo   - README.txt
echo   - QUICK_START.txt
echo.
echo To distribute:
echo   1. Zip the 'dist' folder
echo   2. Send to your client
echo   3. Client extracts and runs .exe files
echo.
echo Press any key to open dist folder...
pause > nul
explorer dist
