# 🎙️ AI PC Agent - Voice-Controlled Assistant

**Version**: 1.0  
**Status**: ✅ Functional  
**Date**: February 2026

A voice-controlled PC assistant with document handling, system control, and web automation capabilities. Control your computer using natural language voice commands.

---

## 🌟 Features

### 🎤 Voice Control
- Natural language voice commands
- Speech-to-text conversion
- Text-to-speech responses
- Continuous listening mode

### 📄 Document Handling
- Create and edit documents
- Read document content
- Save and manage files
- Document search

### 💻 System Control
- Open applications
- Execute system commands
- File management
- Process control

### 🌐 Web Automation
- Open websites
- Search the web
- Navigate pages
- Fill forms

### 🎨 Graphical Interface
- Modern GUI
- Real-time status updates
- Command history
- Visual feedback

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Microphone for voice input
- Speakers for audio output
- Windows/Linux/Mac OS

### Installation

1. **Navigate to project**:
```bash
cd ai_pc_agent
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure settings**:
Edit `config/settings.py` with your preferences.

4. **Set up applicant profile**:
Edit `config/applicant_profile.json` with your information.

5. **Run the application**:
```bash
python main.py
```

---

## 📖 Usage

### Voice Commands

**Document Operations**:
```
"Create a new document"
"Open document report.txt"
"Save document as notes.txt"
"Read the document"
```

**System Control**:
```
"Open calculator"
"Open notepad"
"Close application"
"Shutdown computer"
```

**Web Automation**:
```
"Open Google"
"Search for Python tutorials"
"Navigate to GitHub"
"Fill admission form"
```

**General**:
```
"What time is it?"
"What's the weather?"
"Tell me a joke"
"Exit"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         GUI Interface                    │
│  Tkinter + Status Display               │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Core Agent                       │
│  Intent Parser + Command Router         │
└─────────────────────────────────────────┘
         ↓              ↓              ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Document   │ │   System     │ │     Web      │
│   Handler    │ │   Control    │ │  Automation  │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## 📁 Project Structure

```
ai_pc_agent/
├── config/
│   ├── settings.py              # Configuration
│   ├── applicant_profile.json   # User profile
│   └── __init__.py
├── core/
│   ├── agent.py                 # Main agent logic
│   ├── gui.py                   # GUI interface
│   ├── intent_parser.py         # Command parsing
│   ├── voice_handler.py         # Voice I/O
│   └── __init__.py
├── skills/
│   ├── document_handler.py      # Document operations
│   ├── system_control.py        # System commands
│   ├── web_automation.py        # Web automation
│   └── __init__.py
├── documents/
│   └── document.txt             # Sample document
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

---

## 🔧 Configuration

### Settings
Edit `config/settings.py`:
```python
# Voice settings
VOICE_ENABLED = True
LANGUAGE = "en-US"

# System settings
AUTO_START = False
LOG_LEVEL = "INFO"

# Web automation
BROWSER = "chrome"
HEADLESS = False
```

### Applicant Profile
Edit `config/applicant_profile.json`:
```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "phone": "03001234567",
  "address": "Your Address"
}
```

---

## 🎯 Skills

### Document Handler
- `create_document(title, content)` - Create new document
- `open_document(filename)` - Open existing document
- `save_document(filename, content)` - Save document
- `read_document(filename)` - Read document content

### System Control
- `open_application(app_name)` - Open application
- `close_application(app_name)` - Close application
- `execute_command(command)` - Execute system command
- `shutdown()` - Shutdown computer

### Web Automation
- `open_website(url)` - Open website
- `search_web(query)` - Search on Google
- `fill_form(data)` - Fill web form
- `navigate(direction)` - Navigate pages

---

## 🧪 Testing

### Test Voice Recognition
```bash
python -c "from core.voice_handler import VoiceHandler; vh = VoiceHandler(); print(vh.listen())"
```

### Test Document Handler
```bash
python -c "from skills.document_handler import DocumentHandler; dh = DocumentHandler(); dh.create_document('test', 'Hello World')"
```

### Test System Control
```bash
python -c "from skills.system_control import SystemControl; sc = SystemControl(); sc.open_application('notepad')"
```

---

## 📚 Documentation

- **[AI PC Agent Report](AI_PC_AGENT_REPORT.tex)** - LaTeX report
- **Screenshots** - Visual demonstrations

---

## 🐛 Troubleshooting

### Voice Recognition Not Working
- Check microphone permissions
- Verify microphone is connected
- Test microphone in system settings
- Check internet connection (for cloud-based recognition)

### Application Won't Open
- Verify application is installed
- Check application name spelling
- Try full path to application
- Check system permissions

### Web Automation Fails
- Ensure browser is installed
- Check internet connection
- Verify website URL is correct
- Update browser driver

---

## 🔐 Security

- No sensitive data stored in code
- Credentials handled securely
- System commands validated
- Web automation sandboxed

---

## ⚡ Performance

- Voice recognition: < 2 seconds
- Command execution: < 1 second
- Document operations: < 500ms
- Web automation: Varies by task

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

This project is open source and available for educational and personal use.

---

## 👨‍💻 Author

**Abbas Touqeer**
- GitHub: [@Abbastouqi](https://github.com/Abbastouqi)
- Email: abbastouqeer399@gmail.com

---

## 🙏 Acknowledgments

- Python community for excellent libraries
- Speech recognition libraries
- Selenium for web automation
- Tkinter for GUI

---

## 📊 Statistics

- **Lines of Code**: 1,500+
- **Skills**: 3 (Document, System, Web)
- **Voice Commands**: 20+
- **Supported Operations**: 15+

---

## 🚀 Future Enhancements

- AI-powered intent understanding
- Multi-language support
- Custom skill creation
- Cloud integration
- Mobile app companion
- Advanced automation workflows

---

**Control your PC with your voice!** 🎤✨
