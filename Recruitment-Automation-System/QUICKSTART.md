# Recruitment Automation System - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### On Windows:
1. Double-click `run.bat`
2. Wait for virtual environment setup
3. Update `.env` with your OpenAI API key
4. Browser opens automatically at `http://localhost:8501`

### On macOS/Linux:
1. Run `chmod +x run.sh` (first time only)
2. Run `./run.sh`
3. Update `.env` with your OpenAI API key
4. Browser opens automatically at `http://localhost:8501`

### Manual Setup:
```bash
# Create environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Update .env file with your OpenAI API key

# Run app
streamlit run app.py
```

## 📋 What You Need

1. **Python 3.8+** - Download from python.org
2. **OpenAI API Key** - Get free trial at platform.openai.com
3. **Sample Resumes** - PDF, DOCX, or TXT files

## 🎯 First Steps After Running

1. **Get API Key** (if you haven't):
   - Visit: https://platform.openai.com/account/api-keys
   - Create new secret key
   - Copy it

2. **Update .env file**:
   - Open `.env` in text editor
   - Replace `your_openai_api_key_here` with your actual key
   - Save file

3. **Upload Resumes**:
   - Click "📄 Resume Upload" in sidebar
   - Select resume files (can upload multiple)
   - Wait for parsing

4. **Screen Candidates**:
   - Click "✅ Candidate Screening"
   - Select a candidate
   - Click "🔍 Screen Now"
   - View AI evaluation

5. **Rank Candidates**:
   - Click "🏆 Ranking & Matching"
   - Enter job description
   - Click "🎯 Rank Candidates"
   - See top matches

6. **Schedule Interviews**:
   - Click "📅 Interview Scheduling"
   - Choose candidate and time
   - Confirm schedule

## 🆘 Troubleshooting

**"Module not found" error?**
```bash
pip install -r requirements.txt --force-reinstall
```

**"API key not found" error?**
- Check `.env` file exists
- Verify `OPENAI_API_KEY=` has your key
- Restart the app

**"Port 8501 already in use"?**
```bash
streamlit run app.py --server.port 8502
```

**Nothing happens when I click a button?**
- Check browser console (F12)
- Check terminal for error messages
- Verify API key is valid

## 📚 Documentation

- `README.md` - Full project documentation
- `SETUP.md` - Detailed setup instructions
- `API_REFERENCE.md` - Module API documentation
- `example_usage.py` - Code examples

## 💡 Tips

- Start with 3-5 test resumes
- AI screening costs money per call (check OpenAI pricing)
- Fallback mode works without API (basic scoring)
- Database stores all results locally

## 🎓 Learn More

- Python: https://python.org/
- Streamlit: https://streamlit.io/
- OpenAI: https://platform.openai.com/
- scikit-learn: https://scikit-learn.org/

## ✅ Success!

You're ready to start! 

👉 **Next Step**: Double-click `run.bat` (Windows) or `./run.sh` (Mac/Linux)

Need help? Check the full documentation in README.md or SETUP.md
