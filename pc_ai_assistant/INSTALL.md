# PC AI Assistant - Installation & Usage Guide

## Quick Start (Windows)

### Option 1: Using the Executable (.exe)

1. **Download** `PC_AI_Assistant.exe` (from the `dist` folder after building)
2. **Double-click** the .exe file
3. **Browser opens automatically** at http://127.0.0.1:5000
4. **Start using** the chatbot:
   - Click **Login** to login to admissions portal
   - Click **Register** to create a new account (saves profile to YAML)
   - Click **Apply** for admission (auto-fills saved profile)

**Note:** First run may take 1-2 minutes as the app extracts files.

---

### Option 2: Running from Python (Development)

Requires: Python 3.8+, pip

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python launcher.py
```

---

## Building the .exe File

**On a Windows PC with Python installed:**

```bash
# Navigate to pc_ai_assistant folder
cd E:\AI_agent\AI_Projects\pc_ai_assistant

# Run the build script
build_exe.bat
```

The script will:
- Install PyInstaller (if not present)
- Bundle all dependencies
- Create `dist\PC_AI_Assistant.exe`

**Distributing the .exe:**
- Copy `dist\PC_AI_Assistant.exe` to any Windows PC
- **No Python installation needed** on the target PC
- Just double-click and run!

---

## Features

✅ **Login** - Enter email & password (voice or text)
✅ **Register** - Create account, saves to profile (voice or text)
✅ **Apply** - Apply for admission with auto-filled profile
✅ **Voice Guidance** - Agent greets and guides you
✅ **Voice Input** - Click "Voice" button to speak instead of typing
✅ **Job Status** - See real-time automation progress

---

## System Requirements

**For .exe file:**
- Windows 7, 8, 10, 11 (64-bit)
- ~500 MB free disk space (first run extraction)
- Internet connection
- Google Chrome or Edge browser

**For Python version:**
- Python 3.8+
- All packages in `requirements.txt`
- Google Chrome installed

---

## Troubleshooting

**Q: Browser doesn't open automatically**
- Manually open http://127.0.0.1:5000 in your browser

**Q: "Port 5000 already in use"**
- Close other applications using port 5000, or:
- Edit `launcher.py` line and change `port=5000` to `port=5001`

**Q: Voice input not working**
- Use a browser that supports Web Speech API (Chrome, Edge, Safari)
- Check microphone permissions

**Q: "Cannot find module" errors**
- Run `pip install -r requirements.txt` again
- Make sure you're in the correct directory

---

## Contact

For issues or updates, check the project repository.

---

Generated: February 10, 2026
