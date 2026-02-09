# 🤖 AI Agent - Complete Documentation

## Quick Start

### Start the Agent
```bash
# Web Interface (Recommended)
python web_server.py
# Then open: http://localhost:5000

# Desktop GUI
python main.py
```

---

## 🎯 Main Commands

### Auto-Fill Forms (NEW! 🔥)
```
"auto fill"                    # Automatically fill entire form!
"autofill"                     # Quick command
"fill this form"               # Natural language
```

**Example:**
```
1. "open example.com/contact"
2. "auto fill"
3. "click submit"
```

### Manual Form Filling
```
"fill name with John Doe"
"fill email with john@email.com"
"fill phone with 1234567890"
"click submit"
"press enter"
```

### Web Browsing
```
"open google.com"
"open youtube.com"
"search Python tutorials"
"search for AI news"
```

### Open Applications
```
"open notepad"
"open calculator"
"open chrome"
"open word"
"open excel"
```

### System Commands
```
"shutdown computer"
"restart computer"
"sleep computer"
"open downloads"
"open documents"
```

### Riphah University
```
"apply for admission"
"explore programs"
"admission dates"
```

---

## 📋 Complete Workflows

### Workflow 1: Auto-Fill Form
```
1. "open google.com/forms"
2. "auto fill"
3. "click submit"
```

### Workflow 2: Manual Form
```
1. "open example.com/contact"
2. "fill name with John Doe"
3. "fill email with john@email.com"
4. "click submit"
```

### Workflow 3: Web Search
```
1. "search Python tutorials"
2. "open first result"
```

### Workflow 4: Quick Access
```
1. "open calculator"
2. "open notepad"
```

---

## ✨ Auto-Fill Features

### What Gets Filled Automatically?
- ✅ Name (name, full name, username)
- ✅ Email (email, e-mail, mail)
- ✅ Phone (phone, mobile, telephone)
- ✅ Address (address, street, location)
- ✅ City (city, town)
- ✅ Country (country, nation)
- ✅ Message (message, comment, description)
- ✅ Subject (subject, topic)
- ✅ Company (company, organization)
- ✅ Website (website, url)

### Works On
- ✅ Google Forms
- ✅ Contact Forms
- ✅ Registration Forms
- ✅ Job Applications
- ✅ Survey Forms
- ✅ ANY HTML form!

---

## 🎤 Voice Commands

All commands work with voice!

**Desktop**: Click microphone button
**Web**: Click microphone icon in browser

Just say:
- "Auto fill"
- "Open calculator"
- "Search AI news"
- "Click submit"

---

## 🔧 Configuration

Edit `config.json`:
```json
{
  "selenium_driver_path": "",
  "selenium_headless": false,
  "voice_enabled": true,
  "tts_enabled": true,
  "log_level": "INFO"
}
```

---

## 🛠️ Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
copy config.example.json config.json
```

### 3. Run
```bash
python web_server.py
```

---

## 🐛 Troubleshooting

### Voice Not Working
- Check microphone permissions
- Use Chrome or Edge browser
- Run: `python test_speech.py`

### Form Not Filling
- Wait for page to load
- Make sure form is visible
- Try manual: "fill name with John"

### Application Won't Open
- Check app is installed
- Run as Administrator
- Try full path

---

## 📦 Build Executables

### Build All
```bash
build_all.bat
```

### Build Desktop Only
```bash
build_desktop.bat
```

### Build Web Server Only
```bash
build_web.bat
```

Executables will be in `dist/` folder.

---

## 🎓 Speech Features

### Speech-to-Text
- **Desktop**: Google Speech API (free, requires internet)
- **Web**: Web Speech API (browser-based)
- **Accuracy**: 90-95%

### Text-to-Speech
- **Desktop**: pyttsx3 (offline)
- **Web**: Web Speech API (browser-based)
- **Quality**: High

### Test Speech
```bash
python test_speech.py
```

---

## 📁 Project Structure

```
AI_agent/
├── agent/                    # Core application
│   ├── config.py            # Configuration
│   ├── controller.py        # Main controller
│   ├── gui.py               # Desktop GUI
│   ├── input_handler.py     # Command parsing
│   ├── speech_engine.py     # Speech features
│   ├── task_executor.py     # Task execution
│   └── web_automation.py    # Browser control
├── templates/
│   ├── chatbot.html         # Web interface
│   └── DOCS.md              # This file
├── main.py                  # Desktop app
├── web_server.py            # Web server
├── config.json              # Configuration
└── requirements.txt         # Dependencies
```

---

## 🎨 Customization

### Add New Commands

1. Edit `agent/input_handler.py`:
```python
elif 'my command' in normalized:
    intent = 'my_task'
```

2. Edit `agent/task_executor.py`:
```python
class MyTask(Task):
    name = 'my_task'
    
    def execute(self, command: Command) -> TaskResult:
        # Your code here
        return TaskResult(success=True, message="Done!")
```

---

## ✅ Requirements

- Python 3.8+
- Chrome browser
- Microphone (for voice)
- Internet (for speech recognition)

---

## 🎉 Summary

Your AI agent can:
- ✅ Auto-fill forms on ANY website
- ✅ Control your PC with voice/text
- ✅ Open any application
- ✅ Browse any website
- ✅ Search the web
- ✅ Automate tasks
- ✅ Understand natural language

**Start now:**
```bash
python web_server.py
```

**Try:**
```
"open google.com/forms"
"auto fill"
"click submit"
```

**Enjoy! 🚀**
