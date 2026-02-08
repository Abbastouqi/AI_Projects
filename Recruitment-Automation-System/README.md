# 🤖 AI-Powered Recruitment Automation System

An intelligent recruitment pipeline that automates resume parsing, candidate screening, ranking, and interview scheduling using AI and NLP.

## 🎯 Features

### 1. **Resume Parsing & Data Extraction**
- Automatic extraction of candidate information from resumes (PDF, DOCX, TXT)
- NLP-based skill identification
- Educational background extraction
- Experience level calculation

### 2. **Automated Candidate Screening**
- AI-powered screening using OpenAI GPT API
- Evaluation against job requirements
- Automatic scoring (0-1 scale)
- Detailed feedback generation
- Fallback scoring when API unavailable

### 3. **Candidate Ranking & Matching**
- TF-IDF based similarity matching
- Skill-based matching algorithm
- Experience level evaluation
- Job requirement alignment
- Rank ordering of candidates

### 4. **Interview Scheduling Bot**
- Automated time slot suggestion
- Conflict-free scheduling
- Meeting link generation
- Interview confirmation emails (template)
- Calendar management

### 5. **Web Interface (Streamlit)**
- Dashboard with key metrics
- Resume upload management
- Interactive screening interface
- Ranking and matching visualization
- Interview scheduling UI
- Comprehensive reporting

## 📋 Tech Stack

- **Backend**: Python 3.8+
- **Frontend**: Streamlit
- **AI/ML**: OpenAI API, scikit-learn, spacy
- **Database**: SQLite
- **File Processing**: PyPDF2, python-docx
- **Data Processing**: Pandas, NumPy

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- pip package manager

### Installation

1. **Clone/Navigate to project**:
```bash
cd recruitment-system
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Run the application**:
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 📚 Project Structure

```
recruitment-system/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── database.py            # SQLite database management
│   ├── resume_parser.py       # Resume parsing & extraction
│   ├── screening.py           # AI-powered screening
│   ├── ranking.py             # Candidate ranking & matching
│   └── interview_scheduler.py # Interview scheduling
├── app.py                     # Streamlit main application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
└── resumes/                  # Uploaded resume files storage
```

## 🔧 Configuration

Edit `.env` file to customize:

```env
OPENAI_API_KEY=your_api_key_here
DATABASE_PATH=./data/recruitment.db
UPLOAD_FOLDER=./resumes
MAX_FILE_SIZE=10485760
```

Key settings in `src/config.py`:
- Screening/ranking thresholds
- Interview duration and working hours
- OpenAI model selection

## 💼 Usage Guide

### 1. Upload Resumes
- Navigate to "📄 Resume Upload"
- Upload one or multiple resume files (PDF, DOCX, TXT)
- System automatically parses and extracts information
- Candidates added to database

### 2. Screen Candidates
- Go to "✅ Candidate Screening"
- Select a candidate
- Optionally specify job requirements
- Click "🔍 Screen Now"
- View AI-generated score and feedback

### 3. Rank & Match
- Navigate to "🏆 Ranking & Matching"
- Enter job ID and job description
- Click "🎯 Rank Candidates"
- View ranked candidate list with match percentages

### 4. Schedule Interviews
- Go to "📅 Interview Scheduling"
- Select candidate from ranked results
- View available time slots
- Confirm schedule
- System generates meeting link

### 5. View Reports
- Access "📈 Reports" for analytics
- See screening completion rates
- View candidate score distributions
- Monitor recruitment pipeline metrics

## 🤖 AI Integration

The system uses OpenAI's GPT API for:
- **Screening**: Evaluating candidates against job requirements
- **Scoring**: Generating match scores (0-1)
- **Feedback**: Providing detailed evaluation comments

### Fallback Mode
If OpenAI API is unavailable, the system uses:
- Rule-based skill matching
- Experience level evaluation
- Education assessment

## 📊 Database Schema

### Candidates
Stores candidate information and parsed resume data.

### Screening Results
Contains AI screening scores and feedback.

### Ranking Results
Job-specific candidate rankings and match scores.

### Interviews
Interview schedule and meeting details.

## 🔐 Security Notes

- Store OpenAI API key in `.env` file (not in code)
- Do not commit `.env` or any real API keys to version control
- Keep database credentials secure
- Validate all file uploads
- Implement authentication for production use
- Encrypt sensitive candidate data

## 🛠 Future Enhancements

- [ ] Email integration for interview invitations
- [ ] Video interview recording support
- [ ] Resume similarity detection (plagiarism check)
- [ ] Predictive analytics on hiring success
- [ ] Multi-language resume support
- [ ] Integration with ATS systems
- [ ] Advanced scheduling with timezone support
- [ ] Candidate communication templates
- [ ] Performance analytics and reporting
- [ ] Mobile app interface

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Resume parsing accuracy
- Additional file format support
- Enhanced screening criteria
- UX/UI improvements
- Performance optimization

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues and questions:
1. Check the README and project documentation
2. Review error messages in the Streamlit console
3. Check OpenAI API status
4. Verify `.env` configuration

## 🎓 Learning Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [SQLite Tutorial](https://www.sqlite.org/tutorial.html)
- [scikit-learn NLP Guide](https://scikit-learn.org)

## 📝 Example Workflow

1. **Setup**:
   - Configure `.env` with your OpenAI API key
   - Run `streamlit run app.py`

2. **Import Candidates**:
   - Upload 5-10 sample resumes
   - Review parsed candidate data

3. **Create Job Description**:
   - Define job requirements
   - Set experience and skill requirements

4. **Screen & Rank**:
   - Screen all candidates
   - Rank by job fit
   - Review top candidates

5. **Schedule Interviews**:
   - Schedule top 3-5 candidates
   - Generate meeting links
   - Send confirmations

6. **Analyze Results**:
   - Review reports
   - Track metrics
   - Refine criteria

---

**Built with ❤️ using Python, OpenAI, and Streamlit**
