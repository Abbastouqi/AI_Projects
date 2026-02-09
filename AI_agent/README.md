# 🤖 AI Agent - Intelligent PC Automation Assistant

A powerful voice and text-based AI agent that can perform ANY task on your PC. Features intelligent form filling, web automation, application control, and natural language understanding.

## ✨ Key Features

### 🔥 Auto-Fill Forms (Main Feature)
- **One-command form filling** - Just say "auto fill"!
- **Intelligent field detection** - Recognizes 10+ field types
- **Universal compatibility** - Works on ANY website
- **Smart matching** - 5 detection strategies

### 🌐 Web Automation
- Open any website
- Google search integration
- Browser automation with Selenium
- Form interaction and submission

### 💻 PC Control
- Open applications (Calculator, Notepad, Chrome, Word, Excel, etc.)
- System commands (Shutdown, Restart, Sleep)
- File management
- Quick access to common locations

### 🎤 Voice Control
- Speech-to-text (Google Speech API)
- Text-to-speech (pyttsx3)
- Natural language understanding
- Hands-free operation

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the agent
python web_server.py
# Open: http://localhost:5000

# Or use desktop GUI
python main.py
```

## 💬 Example Commands

```
"auto fill"                    # Auto-fill any form
"open google.com"              # Open website
"search Python tutorials"      # Google search
"open calculator"              # Open application
"fill name with John Doe"      # Manual form fill
"click submit"                 # Submit form
"shutdown computer"            # System control
```

## 📁 Project Structure

```
AI_agent/
├── agent/              # Core application (7 files)
├── templates/          # Web UI + Complete docs
├── main.py            # Desktop app
├── web_server.py      # Web server
├── config.json        # Settings
├── requirements.txt   # Dependencies
└── README.md          # This file
```

## 📖 Documentation

- **[PROJECT_INFO.md](PROJECT_INFO.md)** - Detailed project information
- **[templates/DOCS.md](templates/DOCS.md)** - Complete documentation
- **[QUICK_START.txt](QUICK_START.txt)** - Quick reference guide

## 🛠️ Technology Stack

- Python 3.8+
- Flask (Web Framework)
- Selenium (Browser Automation)
- Google Speech API
- pyttsx3 (Text-to-Speech)
- Tkinter (Desktop GUI)

## 🎯 Use Cases

1. **Form Automation** - Job applications, registrations, surveys
2. **Productivity** - Quick app launching, web searches
3. **Accessibility** - Voice-controlled PC operation
4. **Education** - University admission assistance

## 🔧 Build Executable

```bash
build_all.bat
```

Output: `dist/RiphahAI-Desktop.exe` and `dist/RiphahAI-WebServer.exe`

## 👨‍💻 Author

**Abbas Touqeer**
- GitHub: [@Abbastouqi](https://github.com/Abbastouqi)
- Email: abbastouqeer399@gmail.com

## 📄 License

Open source - Available for educational and personal use.

---

**Ready to automate? Start now!** 🚀

```bash
python web_server.py
```

Then say: **"auto fill"** on any form!
