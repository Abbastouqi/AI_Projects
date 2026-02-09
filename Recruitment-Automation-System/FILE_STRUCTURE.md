# 📁 Project File Structure & Descriptions

## Root Level Files

### **Core Application**
- **`app.py`** (860 lines)
  - Main Streamlit web application
  - Complete UI with 6 modules (Dashboard, Resume Upload, Screening, Ranking, Scheduling, Reports)
  - Session state management
  - Interactive forms and data visualization

### **Configuration & Setup**
- **`.env.example`**
  - Environment variables template
  - Copy as `.env` and fill with your settings
  - Required: OPENAI_API_KEY

- **`project.json`**
  - Project metadata in JSON format
  - Module descriptions
  - Features summary
  - Tech stack details

- **`setup.py`** (70 lines)
  - Project initialization script
  - Creates directories
  - Initializes database
  - Validates configuration

- **`requirements.txt`**
  - Python package dependencies
  - All required packages with versions
  - Install with: `pip install -r requirements.txt`

### **Startup Scripts**
- **`run.bat`** (Windows)
  - Automatic setup on Windows
  - Creates virtual environment
  - Installs dependencies
  - Launches Streamlit app

- **`run.sh`** (macOS/Linux)
  - Automatic setup on Unix-like systems
  - Creates virtual environment
  - Installs dependencies
  - Launches Streamlit app

### **Example Code**
- **`example_usage.py`** (250+ lines)
  - Complete workflow examples
  - Shows how to use each module
  - Demonstrates database operations
  - Includes fallback handling

## Documentation Files

- **`README.md`** (400+ lines)
  - Comprehensive project documentation
  - Feature overview
  - Tech stack details
  - Installation instructions
  - Usage guide
  - API reference
  - Future enhancements
  - Learning resources

- **`SETUP.md`** (300+ lines)
  - Step-by-step installation guide
  - System requirements
  - Configuration instructions
  - Troubleshooting guide
  - Usage examples
  - Best practices
  - Updating packages

- **`QUICKSTART.md`** (150+ lines)
  - 5-minute quick start
  - Simple setup instructions
  - First time usage guide
  - Quick troubleshooting

- **`API_REFERENCE.md`** (400+ lines)
  - Module API documentation
  - Function signatures
  - Parameter descriptions
  - Return value specifications
  - Code examples
  - Data models
  - Performance notes

- **`PROJECT_SUMMARY.md`** (250+ lines)
  - Project overview
  - What's included
  - Quick start instructions
  - Tech stack summary
  - Workflow examples
  - Getting help guide

## Source Code Directory (`src/`)

### **Module Files**

#### **`config.py`** (35 lines)
- Configuration management
- Environment variable loading
- System settings and thresholds
- Validation methods
- Constants definition

#### **`database.py`** (240 lines)
- SQLite database management
- Database initialization
- CRUD operations for candidates
- Screening results management
- Ranking results storage
- Interview scheduling
- Query methods
- Row factory for dictionary results

#### **`resume_parser.py`** (250 lines)
- Resume file parsing
- Supports: PDF, DOCX, TXT
- Information extraction:
  - Name and contact info
  - Skills identification
  - Education level detection
  - Experience calculation
- Regular expression patterns
- Text processing utilities

#### **`screening.py`** (200 lines)
- AI-powered candidate screening
- OpenAI GPT integration
- Scoring algorithm (0-1 scale)
- Feedback generation
- Fallback screening (no API)
- Prompt engineering
- Response parsing
- Error handling

#### **`ranking.py`** (300 lines)
- NLP-based candidate ranking
- TF-IDF vectorization
- Cosine similarity matching
- Multi-factor scoring:
  - Text similarity (40%)
  - Skill matching (40%)
  - Experience relevance (20%)
- Skill extraction
- Job requirement parsing
- Ranking and sorting

#### **`interview_scheduler.py`** (250 lines)
- Interview scheduling system
- Time slot generation
- Conflict detection and prevention
- Meeting link generation
- Calendar management
- Interview rescheduling
- Email confirmation templates
- Working hours configuration
- Weekend exclusion

#### **`__init__.py`**
- Package initialization
- Module imports

## Data Directories

### **`data/`**
- SQLite database storage
- Will contain `recruitment.db` after first run
- Stores all candidate, screening, ranking, and interview data

### **`resumes/`**
- Uploaded resume files storage
- Supports: PDF, DOCX, TXT formats
- Organized by upload time

## Summary

**Total Files**: 20+
**Total Lines of Code**: 3000+
**Documentation Lines**: 1500+
**Supported File Formats**: PDF, DOCX, TXT
**Database**: SQLite
**Web Framework**: Streamlit
**AI Integration**: OpenAI GPT

---

## File Size Overview

| Component | Type | Size |
|-----------|------|------|
| app.py | Python | ~30KB |
| src/database.py | Python | ~12KB |
| src/resume_parser.py | Python | ~10KB |
| src/ranking.py | Python | ~12KB |
| src/screening.py | Python | ~8KB |
| src/interview_scheduler.py | Python | ~10KB |
| README.md | Markdown | ~20KB |
| SETUP.md | Markdown | ~15KB |
| API_REFERENCE.md | Markdown | ~18KB |
| **Total** | **All Files** | **~150KB** |

---

## Getting Started

1. **For Quick Setup**: Read `QUICKSTART.md`
2. **For Full Setup**: Read `SETUP.md`
3. **For Code Examples**: Check `example_usage.py`
4. **For API Details**: See `API_REFERENCE.md`
5. **For Everything**: Read `README.md`

---

## Key Capabilities

✅ Resume Parsing (PDF, DOCX, TXT)
✅ AI Screening with OpenAI GPT
✅ NLP-based Ranking
✅ Automated Interview Scheduling
✅ Database Management
✅ Web Dashboard (Streamlit)
✅ Error Handling & Fallbacks
✅ Production-Ready Code

---

**All files are ready to use. No compilation needed!**

Just follow the Quick Start guide to get running in 5 minutes.
