"""
Example script showing how to use the recruitment system programmatically.
"""

import json
from src.database import Database
from src.resume_parser import ResumeParser
from src.screening import CandidateScreener
from src.ranking import CandidateRanker
from src.interview_scheduler import InterviewScheduler
from src.config import Config

def example_workflow():
    """Demonstrate the complete recruitment workflow."""
    
    print("=" * 60)
    print("AI-Powered Recruitment Automation System - Example Workflow")
    print("=" * 60)
    
    # Initialize components
    db = Database()
    parser = ResumeParser()
    screener = CandidateScreener()
    ranker = CandidateRanker()
    scheduler = InterviewScheduler()
    
    print("\n1️⃣  RESUME PARSING")
    print("-" * 60)
    
    # Example: Parse a resume
    sample_resume_path = "resumes/sample.pdf"
    try:
        parsed_data = parser.parse_resume(sample_resume_path)
        print(f"✅ Parsed resume successfully")
        print(f"   Name: {parsed_data.get('name')}")
        print(f"   Email: {parsed_data.get('email')}")
        print(f"   Skills: {', '.join(parsed_data.get('skills', [])[:5])}")
        print(f"   Experience: {parsed_data.get('experience_years'):.1f} years")
    except FileNotFoundError:
        print("ℹ️  Sample resume not found. Skipping parsing example.")
        print("   Upload a resume using the web interface to test parsing.")
    except Exception as e:
        print(f"ℹ️  Note: {str(e)}")
    
    print("\n2️⃣  CANDIDATE DATABASE")
    print("-" * 60)
    
    # Create sample candidates
    candidates = db.get_all_candidates()
    if candidates:
        print(f"✅ Found {len(candidates)} candidates in database")
        for candidate in candidates[:3]:
            print(f"   - {candidate['name']} ({candidate['email']})")
    else:
        print("ℹ️  No candidates in database yet.")
        print("   Upload resumes using the web interface to populate the database.")
    
    print("\n3️⃣  CANDIDATE SCREENING")
    print("-" * 60)
    
    if candidates:
        sample_candidate = candidates[0]
        parsed = json.loads(sample_candidate['parsed_data']) if sample_candidate['parsed_data'] else {}
        
        job_requirements = """
        - 5+ years of Python programming experience
        - Strong knowledge of Django or FastAPI
        - AWS cloud experience
        - Docker and Kubernetes proficiency
        - Excellent communication skills
        """
        
        print(f"Screening: {sample_candidate['name']}")
        print("Job Requirements: Senior Python Developer")
        
        try:
            score, feedback = screener.screen_candidate(parsed, job_requirements)
            print(f"✅ Screening Score: {score:.2f}/1.00")
            print(f"   Feedback: {feedback[:100]}...")
        except Exception as e:
            print(f"ℹ️  Screening requires OpenAI API key. Check your .env file.")
    else:
        print("ℹ️  No candidates to screen.")
    
    print("\n4️⃣  CANDIDATE RANKING")
    print("-" * 60)
    
    if candidates:
        candidate_data = []
        for c in candidates[:5]:
            parsed = json.loads(c['parsed_data']) if c['parsed_data'] else {}
            candidate_data.append({**c, **parsed})
        
        job_description = """
        Senior Software Engineer - Python/Django
        
        Required:
        - 5+ years of professional software development experience
        - Expertise in Python and Django framework
        - AWS cloud platform experience
        - Docker containerization knowledge
        - RESTful API design and development
        
        Nice to have:
        - Kubernetes experience
        - Machine Learning knowledge
        - PostgreSQL expertise
        - Agile methodology experience
        """
        
        print("Ranking candidates for: Senior Software Engineer")
        ranked = ranker.rank_candidates(job_description, candidate_data)
        
        print("✅ Top candidates:")
        for r in ranked[:3]:
            print(f"   {r.get('rank')}. {r.get('name')} - Match: {r.get('ranking_score'):.2%}")
    else:
        print("ℹ️  No candidates to rank.")
    
    print("\n5️⃣  INTERVIEW SCHEDULING")
    print("-" * 60)
    
    # Get available slots
    slots = scheduler.suggest_time_slots(num_slots=5)
    print("✅ Available interview slots:")
    for i, slot in enumerate(slots[:3], 1):
        print(f"   {i}. {slot['date']} at {slot['time']}")
    
    if candidates:
        sample_candidate = candidates[0]
        if slots:
            slot = slots[0]
            result = scheduler.schedule_interview(
                sample_candidate['id'],
                slot['date'],
                slot['time'],
                "hr@company.com",
                sample_candidate['email']
            )
            
            if result['success']:
                print(f"\n✅ Interview scheduled!")
                print(f"   Meeting Link: {result['meeting_link']}")
            else:
                print(f"❌ Scheduling failed: {result['message']}")
    
    print("\n6️⃣  REPORTS & ANALYTICS")
    print("-" * 60)
    
    total_candidates = len(candidates)
    screened = sum(1 for c in candidates if db.get_screening_result(c['id']))
    completion_rate = (screened / total_candidates * 100) if total_candidates > 0 else 0
    
    print(f"📊 Pipeline Summary:")
    print(f"   Total Candidates: {total_candidates}")
    print(f"   Screened: {screened}")
    print(f"   Completion Rate: {completion_rate:.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ Example workflow complete!")
    print("=" * 60)
    print("\n📌 Next steps:")
    print("1. Run: streamlit run app.py")
    print("2. Upload resumes through the web interface")
    print("3. Use the application to screen and rank candidates")
    print("4. Schedule interviews with top candidates")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    example_workflow()
