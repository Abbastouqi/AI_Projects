# 🤖 AI Agent - PC Automation Assistant

Voice and text-based AI agent that can perform ANY task on your PC!

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the agent
python web_server.py
# Open: http://localhost:5000

# Or use desktop GUI
python main.py
```

## 🎯 Main Features

- **Auto-Fill Forms** - "auto fill" fills entire forms automatically! 🔥
- **Web Browsing** - "open google.com", "search AI news"
- **Open Apps** - "open calculator", "open notepad", "open chrome"
- **System Control** - "shutdown computer", "restart", "sleep"
- **Voice Control** - Speak your commands naturally
- **Riphah University** - Admission assistance

## 💬 Example Commands

```
"auto fill"                    # Auto-fill any form
"open google.com"              # Open website
"search Python tutorials"      # Google search
"open calculator"              # Open app
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

**Complete guide**: [templates/DOCS.md](templates/DOCS.md)
- All commands
- Workflows
- Configuration
- Troubleshooting

## 🎉 Try It Now!

```bash
python web_server.py
```

Then say:
```
"open google.com/forms"
"auto fill"
"click submit"
```

Done! 🚀

## 🔧 Build Executable (Optional)

```bash
build_all.bat
```

Output: `dist/RiphahAI-Desktop.exe` and `dist/RiphahAI-WebServer.exe`
