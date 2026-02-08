# Recruitment Automation System - Installation & Setup Guide

## 📋 System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (free trial available at https://platform.openai.com)
- 500MB free disk space
- Windows, macOS, or Linux

## 🔧 Installation Steps

### Step 1: Prepare Your Environment

**Windows (PowerShell):**
```powershell
# Navigate to project directory
cd recruitment-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux (Terminal):**
```bash
# Navigate to project directory
cd recruitment-system

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web interface framework
- `openai` - AI API integration
- `PyPDF2` - PDF processing
- `python-docx` - Word document processing
- `scikit-learn` - Machine learning & NLP
- `pandas` & `numpy` - Data processing

### Step 3: Configure API Keys

1. Get your OpenAI API key:
   - Visit https://platform.openai.com/account/api-keys
   - Create a new API key
   - Copy the key (you'll only see it once)

2. Setup environment file:
   ```bash
   # Copy the example file
   copy .env.example .env        # Windows
   cp .env.example .env          # macOS/Linux
   
   # Edit .env and add your API key
   # Open .env in your text editor and replace YOUR_API_KEY
   ```

3. Verify .env file:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
   DATABASE_PATH=./data/recruitment.db
   UPLOAD_FOLDER=./resumes
   MAX_FILE_SIZE=10485760
   ```

### Step 4: Initialize Project (Optional)

```bash
python setup.py
```

This will:
- Create necessary directories
- Initialize SQLite database
- Verify configuration

### Step 5: Run the Application

```bash
streamlit run app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  URL: http://localhost:8501
```

Open http://localhost:8501 in your web browser.

## ✅ Verification Checklist

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Virtual environment activated
- [ ] All packages installed (`pip list | grep streamlit`)
- [ ] `.env` file created with OpenAI API key
- [ ] Database directories exist (`data/`, `resumes/`)
- [ ] Application starts without errors

## 🚀 First Time Usage

1. **Dashboard**: View empty dashboard on startup
2. **Upload Resumes**: 
   - Click "📄 Resume Upload"
   - Upload sample resumes (PDF, DOCX, or TXT)
   - System automatically parses them
3. **Screen Candidates**:
   - Go to "✅ Candidate Screening"
   - Select a candidate
   - Click "🔍 Screen Now" to use AI screening
4. **Rank Candidates**:
   - Navigate to "🏆 Ranking & Matching"
   - Paste a job description
   - Click "🎯 Rank Candidates"
5. **Schedule Interviews**:
   - Go to "📅 Interview Scheduling"
   - Select candidate and time slot
   - Confirm scheduling

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall packages:
pip install -r requirements.txt --force-reinstall
```

### Issue: "OPENAI_API_KEY environment variable is not set"

**Solution:**
1. Check `.env` file exists in project root
2. Verify it contains: `OPENAI_API_KEY=sk-xxxxxxx`
3. Restart the application: `streamlit run app.py`

### Issue: "Failed to establish a new connection" (OpenAI)

**Solution:**
1. Check internet connection
2. Verify API key is valid: https://platform.openai.com/account/api-keys
3. Check OpenAI status: https://status.openai.com

### Issue: "Port 8501 is already in use"

**Solution:**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Issue: "Permission denied" on .env file (macOS/Linux)

**Solution:**
```bash
chmod 644 .env
```

## 📚 Usage Examples

### Example 1: Upload and Screen a Resume

```bash
# 1. Start the app
streamlit run app.py

# 2. In browser:
# - Click "📄 Resume Upload"
# - Upload your resume or a sample resume
# - Review parsed information
```

### Example 2: Run Programmatically

```bash
# Activate virtual environment first
python example_usage.py
```

### Example 3: Access Database Directly

```python
from src.database import Database

db = Database()
candidates = db.get_all_candidates()
for candidate in candidates:
    print(candidate['name'], candidate['email'])
```

## 🆘 Getting Help

1. **Check Configuration**:
   ```bash
   python -c "from src.config import Config; Config.validate()"
   ```

2. **View Debug Information**:
   - Open browser console (F12)
   - Check Streamlit terminal for errors

3. **Test Individual Components**:
   ```python
   from src.database import Database
   db = Database()
   print(db.get_all_candidates())
   ```

4. **Verify API Key**:
   ```python
   import openai
   openai.api_key = "your-key-here"
   openai.Model.list()
   ```

## 💡 Tips & Best Practices

1. **Organize Resumes**:
   - Keep resumes in standard formats (PDF recommended)
   - Use consistent naming (e.g., FirstName_LastName.pdf)

2. **Job Descriptions**:
   - Be detailed with requirements
   - List technical skills explicitly
   - Mention experience level

3. **Performance**:
   - Start with 5-10 resumes for testing
   - Screening API calls cost money - use fallback mode when needed
   - Database stores results for later analysis

4. **Production Deployment**:
   - Use proper secret management (AWS Secrets Manager, etc.)
   - Implement user authentication
   - Add email integration
   - Setup regular database backups

## 📦 Updating Packages

To get the latest versions:

```bash
# Upgrade all packages
pip install -r requirements.txt --upgrade

# Update specific package
pip install --upgrade streamlit
```

## 🚪 Stopping the Application

```bash
# Press Ctrl+C in terminal running Streamlit
# Or close the browser tab
```

## 📝 Next Steps

1. ✅ Complete installation
2. 📤 Upload some test resumes
3. 🔍 Run candidate screening
4. 🎯 Test ranking functionality
5. 📅 Schedule sample interviews
6. 📊 Review reports and analytics

---

**Happy recruiting! 🎉**

For more detailed information, see [README.md](README.md)
