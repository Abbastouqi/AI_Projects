# Recruitment Automation System - API Reference

## Core Modules Documentation

### 1. Config Module (`src/config.py`)

Configuration management for the entire system.

```python
from src.config import Config

# Access configurations
Config.OPENAI_API_KEY
Config.DATABASE_PATH
Config.MIN_SCREENING_SCORE  # Default: 0.6
Config.MIN_RANKING_SCORE    # Default: 0.5

# Validate configuration
Config.validate()  # Raises error if required keys missing
```

**Key Settings:**
- `OPENAI_API_KEY`: OpenAI API authentication
- `DATABASE_PATH`: SQLite database location
- `UPLOAD_FOLDER`: Resume storage directory
- `MAX_FILE_SIZE`: Maximum upload size (10MB default)
- `MODEL_NAME`: GPT model to use (gpt-3.5-turbo)

---

### 2. Database Module (`src/database.py`)

SQLite database management and CRUD operations.

```python
from src.database import Database

db = Database()

# Add candidate
candidate_id = db.add_candidate(
    name="John Doe",
    email="john@example.com",
    phone="(555) 123-4567",
    file_path="/path/to/resume.pdf",
    parsed_data='{"skills": ["Python", "Django"]}'
)

# Add screening result
result_id = db.add_screening_result(
    candidate_id=1,
    screening_score=0.85,
    feedback="Strong candidate with excellent skills"
)

# Add ranking result
rank_id = db.add_ranking_result(
    candidate_id=1,
    job_id="JOB_001",
    ranking_score=0.92,
    comments="Best match for senior role"
)

# Schedule interview
interview_id = db.schedule_interview(
    candidate_id=1,
    date="2024-02-15",
    time="14:00",
    interviewer_email="hr@company.com",
    notes="Phone screen before in-person"
)

# Query methods
candidate = db.get_candidate(1)
all_candidates = db.get_all_candidates()
screening = db.get_screening_result(1)
rankings = db.get_ranking_results("JOB_001")
interviews = db.get_interviews()
interviews = db.get_interviews(candidate_id=1)
```

**Database Tables:**
- `candidates`: Candidate information and resumes
- `screening_results`: AI screening scores
- `ranking_results`: Job-specific rankings
- `interviews`: Interview schedules

---

### 3. Resume Parser Module (`src/resume_parser.py`)

Automatic resume parsing and information extraction.

```python
from src.resume_parser import ResumeParser

parser = ResumeParser()

# Parse resume file
parsed_data = parser.parse_resume("/path/to/resume.pdf")

# Returns dictionary with:
# {
#     "name": "John Doe",
#     "email": "john@example.com",
#     "phone": "(555) 123-4567",
#     "skills": ["Python", "Django", "AWS", ...],
#     "experience_years": 5.0,
#     "education": ["Bachelor's", "Master's"],
#     "full_text": "Raw resume text..."
# }
```

**Supported Formats:**
- PDF (.pdf)
- Word Document (.docx, .doc)
- Text (.txt)

**Extracted Information:**
- Contact information (email, phone)
- Skills identification
- Experience duration calculation
- Education level detection
- Raw text for further processing

---

### 4. Candidate Screener Module (`src/screening.py`)

AI-powered automated candidate screening using OpenAI.

```python
from src.screening import CandidateScreener

screener = CandidateScreener()

# Screen candidate
score, feedback = screener.screen_candidate(
    candidate_info={
        "name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "Django", "AWS"],
        "experience_years": 5.0,
        "education": ["Bachelor's"]
    },
    job_requirements="""
        - 5+ years Python experience
        - Django expertise
        - AWS cloud knowledge
        - Strong communication skills
    """
)

# Returns:
# score: float (0.0 - 1.0)
# feedback: str (detailed evaluation)
```

**Scoring:**
- 0.0 - 0.5: Not suitable
- 0.5 - 0.7: Potentially suitable
- 0.7 - 1.0: Strong candidate

**Features:**
- AI-powered evaluation
- Detailed feedback generation
- Fallback scoring if API unavailable
- Configurable scoring weights

---

### 5. Ranking Module (`src/ranking.py`)

NLP-based candidate ranking and job matching.

```python
from src.ranking import CandidateRanker

ranker = CandidateRanker()

# Rank candidates for a job
ranked_candidates = ranker.rank_candidates(
    job_description="""
        Senior Python Developer
        - 5+ years of experience
        - Django/FastAPI expertise
        - AWS and Docker knowledge
    """,
    candidates=[
        {
            "id": 1,
            "name": "John Doe",
            "skills": ["Python", "Django", "AWS"],
            "experience_years": 5.0,
            "full_text": "..."
        },
        # ... more candidates
    ]
)

# Returns sorted list with ranking scores:
# [
#     {
#         "id": 1,
#         "name": "John Doe",
#         "ranking_score": 0.92,
#         "rank": 1,
#         "text_match": 0.85,
#         "skill_match": 0.95,
#         "experience_match": 0.90
#     },
#     ...
# ]
```

**Ranking Factors:**
- Text similarity (40%): TF-IDF matching
- Skill match (40%): Required skills overlap
- Experience (20%): Years and relevance

---

### 6. Interview Scheduler Module (`src/interview_scheduler.py`)

Automated interview scheduling and conflict management.

```python
from src.interview_scheduler import InterviewScheduler

scheduler = InterviewScheduler()

# Get available time slots
slots = scheduler.suggest_time_slots(
    num_slots=5,      # Number of slots to suggest
    days_ahead=30     # Look ahead in days
)

# Each slot contains:
# {
#     "date": "2024-02-15",
#     "time": "14:00",
#     "datetime": "2024-02-15T14:00:00",
#     "available": True
# }

# Schedule interview
interview = scheduler.schedule_interview(
    candidate_id=1,
    date="2024-02-15",
    time="14:00",
    interviewer_email="hr@company.com",
    candidate_email="john@example.com"
)

# Reschedule interview
rescheduled = scheduler.reschedule_interview(
    interview_id=1,
    new_date="2024-02-16",
    new_time="15:00"
)

# Get interview calendar
calendar = scheduler.get_interview_calendar(days_ahead=30)

# Send confirmation email (template)
confirmation = scheduler.send_interview_confirmation(
    candidate_email="john@example.com",
    candidate_name="John Doe",
    date="2024-02-15",
    time="14:00",
    meeting_link="https://meet.google.com/xyz"
)
```

**Features:**
- Conflict-free scheduling
- Auto-generated meeting links
- Customizable working hours (default: 9 AM - 5 PM)
- Weekend exclusion
- Email confirmation templates

---

## Data Models

### Candidate
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "file_path": "./resumes/john_doe.pdf",
    "parsed_data": "{...}",
    "created_at": "2024-02-01 10:30:45",
    "updated_at": "2024-02-01 10:30:45"
}
```

### Screening Result
```json
{
    "id": 1,
    "candidate_id": 1,
    "screening_score": 0.85,
    "status": "passed",
    "feedback": "Strong technical background...",
    "created_at": "2024-02-01 10:35:22"
}
```

### Ranking Result
```json
{
    "id": 1,
    "candidate_id": 1,
    "job_id": "JOB_001",
    "ranking_score": 0.92,
    "rank": 1,
    "comments": "Best skill match",
    "created_at": "2024-02-01 10:40:00"
}
```

### Interview
```json
{
    "id": 1,
    "candidate_id": 1,
    "scheduled_date": "2024-02-15",
    "scheduled_time": "14:00",
    "duration_minutes": 60,
    "interviewer_email": "hr@company.com",
    "status": "scheduled",
    "meeting_link": "https://meet.google.com/...",
    "notes": "Phone screen",
    "created_at": "2024-02-01 11:00:00"
}
```

---

## Error Handling

All modules handle errors gracefully:

```python
try:
    parsed = parser.parse_resume(file_path)
except FileNotFoundError:
    print("Resume file not found")
except ValueError as e:
    print(f"Unsupported file format: {e}")
except Exception as e:
    print(f"Error parsing resume: {e}")
```

---

## Performance Considerations

- **Resume Parsing**: ~1-2 seconds per resume
- **AI Screening**: ~2-3 seconds per candidate (API dependent)
- **Ranking**: ~1 second for 10 candidates
- **Interview Scheduling**: Instant

---

## Limits

- Maximum file size: 10MB (configurable)
- Database: SQLite (suitable for < 100k candidates)
- OpenAI API: Rate limits apply (check your plan)

---

## Examples

See `example_usage.py` for complete workflow examples.

---

**Last Updated**: 2024-02-08
