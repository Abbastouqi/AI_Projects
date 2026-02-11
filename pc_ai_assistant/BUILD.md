# PC AI Assistant - Executable Distribution

This folder contains everything needed to create a standalone Windows executable (.exe) that can be installed on any PC without requiring Python.

## 📦 Building the Executable

### Quick Method (Recommended)

1. **Open** `setup.bat` (double-click it)
2. **Wait** for the build to complete (2-5 minutes)
3. **Find** the executable in `dist\PC_AI_Assistant.exe`

That's it! You now have a standalone .exe file.

### Manual Method (Advanced)

```bash
# Install dependencies
pip install -r requirements.txt

# Build with PyInstaller
pyinstaller --onefile --windowed launcher.py
```

---

## 🚀 Using the Executable

### On Your PC (Developer)

```bash
python launcher.py
```

Or double-click: `PC_AI_Assistant.exe` (after building)

### On Any Other PC (End User)

1. Copy `dist\PC_AI_Assistant.exe` to the other PC
2. Double-click `PC_AI_Assistant.exe`
3. Browser opens automatically at http://127.0.0.1:5000
4. Use the chatbot!

**Requirements:**
- Windows 7/8/10/11 (64-bit)
- Internet connection
- ~500 MB free disk space (first run)
- Google Chrome or Edge browser

---

## 📁 Files Included

- `setup.bat` - One-click setup wizard (recommended)
- `build_exe.bat` - Manual build script
- `launcher.py` - Application entry point
- `requirements.txt` - Python dependencies
- `INSTALL.md` - Detailed installation guide
- `web_frontend.py` - Flask web application
- `templates/` - HTML templates
- `static/` - CSS styles
- `agent/` - Automation agent code
- `data/` - Application profile data

---

## ⚙️ Troubleshooting

**"Cannot find PyInstaller"**
- Run: `pip install pyinstaller`

**"Build failed with module not found"**
- Run: `pip install -r requirements.txt`
- Then run `setup.bat` again

**"Port 5000 already in use"**
- Close other apps using that port
- Or modify `launcher.py` to use a different port

**"First run is slow"**
- Normal - the .exe extracts dependencies on first launch
- Subsequent runs are faster

---

## 📖 More Information

See `INSTALL.md` for detailed usage instructions and troubleshooting.

---

## ✨ Summary

1. Run `setup.bat` → Get `dist\PC_AI_Assistant.exe`
2. Copy `.exe` to any PC → Works instantly!
3. No Python installation needed on target PCs

**That's it!** You have a fully portable admissions automation tool.

