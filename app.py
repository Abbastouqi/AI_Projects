import streamlit as st
import json
from pathlib import Path
from src.config import Config
from src.database import Database
from src.resume_parser import ResumeParser
from src.screening import CandidateScreener
from src.ranking import CandidateRanker
from src.interview_scheduler import InterviewScheduler

# Configure page
st.set_page_config(
    page_title="Recruitment Automation System",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global configuration warnings
missing_openai_key = not Config.OPENAI_API_KEY
if missing_openai_key:
    st.sidebar.error("OPENAI_API_KEY not set. Add it to .env or your environment.")
    st.error("OpenAI API key is missing. Add `OPENAI_API_KEY` to `.env` and restart the app.")

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = Database()
if 'parser' not in st.session_state:
    st.session_state.parser = ResumeParser()
if 'screener' not in st.session_state:
    st.session_state.screener = None if missing_openai_key else CandidateScreener()
if 'ranker' not in st.session_state:
    st.session_state.ranker = None if missing_openai_key else CandidateRanker()
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = InterviewScheduler()

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .stButton > button { width: 100%; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["📊 Dashboard", "📄 Resume Upload", "✅ Candidate Screening", 
     "🏆 Ranking & Matching", "📅 Interview Scheduling", "📈 Reports"]
)

st.title("🤖 AI-Powered Recruitment Automation System")
st.markdown("---")

# ============= DASHBOARD PAGE =============
if page == "📊 Dashboard":
    st.header("Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    candidates = st.session_state.db.get_all_candidates()
    
    with col1:
        st.metric("Total Candidates", len(candidates))
    
    with col2:
        screened = sum(1 for c in candidates if st.session_state.db.get_screening_result(c['id']))
        st.metric("Screened", screened)
    
    with col3:
        st.metric("Pending Review", len(candidates) - screened)
    
    with col4:
        st.metric("System Status", "✅ Active")
    
    st.subheader("Recent Candidates")
    if candidates:
        for candidate in candidates[:5]:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{candidate['name']}**")
            with col2:
                st.write(candidate['email'])
            with col3:
                screening = st.session_state.db.get_screening_result(candidate['id'])
                if screening:
                    score = screening['screening_score']
                    st.write(f"Score: {score:.2f}")
    else:
        st.info("No candidates yet. Start by uploading resumes!")

# ============= RESUME UPLOAD PAGE =============
elif page == "📄 Resume Upload":
    st.header("Resume Upload & Parsing")
    
    st.markdown("Upload candidate resumes for automatic parsing and screening.")
    
    uploaded_files = st.file_uploader(
        "Choose resume files (PDF, DOCX, TXT)",
        type=["pdf", "docx", "doc", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.subheader("Processing Resumes...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}")
            
            # Save file
            file_path = Path(Config.UPLOAD_FOLDER) / uploaded_file.name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # Parse resume
                parsed_data = st.session_state.parser.parse_resume(str(file_path))
                
                # Add to database
                candidate_id = st.session_state.db.add_candidate(
                    name=parsed_data.get('name', 'Unknown'),
                    email=parsed_data.get('email', 'unknown@example.com'),
                    phone=parsed_data.get('phone'),
                    file_path=str(file_path),
                    parsed_data=json.dumps(parsed_data)
                )
                
                st.success(f"✅ {parsed_data.get('name', 'Candidate')} - Added (ID: {candidate_id})")
                
                # Display parsed information
                with st.expander(f"📋 Details - {parsed_data.get('name', 'Candidate')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Email:** {parsed_data.get('email')}")
                        st.write(f"**Phone:** {parsed_data.get('phone')}")
                    with col2:
                        st.write(f"**Experience:** {parsed_data.get('experience_years'):.1f} years")
                        st.write(f"**Skills:** {', '.join(parsed_data.get('skills', [])[:5])}")
            
            except Exception as e:
                st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        st.success("Resume processing complete!")

# ============= CANDIDATE SCREENING PAGE =============
elif page == "✅ Candidate Screening":
    st.header("Automated Candidate Screening")
    
    if missing_openai_key or st.session_state.screener is None:
        st.warning("Screening is unavailable until OPENAI_API_KEY is configured.")
        st.stop()

    candidates = st.session_state.db.get_all_candidates()
    
    if not candidates:
        st.warning("No candidates to screen. Please upload resumes first.")
    else:
        st.markdown("Screen candidates against job requirements using AI.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_candidate = st.selectbox(
                "Select Candidate",
                candidates,
                format_func=lambda x: f"{x['name']} ({x['email']})"
            )
        
        with col2:
            if st.button("🔍 Screen Now", use_container_width=True):
                st.session_state.screening_in_progress = True
        
        st.subheader("Job Requirements")
        job_requirements = st.text_area(
            "Enter job requirements (or use default)",
            value="",
            height=150,
            placeholder="e.g., 5+ years Python experience, AWS knowledge, etc."
        )
        
        if st.session_state.get('screening_in_progress'):
            with st.spinner("🤖 Screening candidate with AI..."):
                parsed_data = json.loads(selected_candidate['parsed_data']) if selected_candidate['parsed_data'] else {}
                
                score, feedback = st.session_state.screener.screen_candidate(
                    parsed_data,
                    job_requirements if job_requirements else None
                )
                
                # Save result
                st.session_state.db.add_screening_result(
                    selected_candidate['id'],
                    score,
                    feedback
                )
                
                st.session_state.screening_in_progress = False
                st.rerun()
        
        # Display screening results
        screening_result = st.session_state.db.get_screening_result(selected_candidate['id'])
        
        if screening_result:
            st.subheader("Screening Result")
            
            col1, col2 = st.columns(2)
            
            with col1:
                score = screening_result['screening_score']
                status = screening_result['status']
                
                if score >= 0.8:
                    color = "🟢"
                elif score >= 0.6:
                    color = "🟡"
                else:
                    color = "🔴"
                
                st.metric("Score", f"{score:.2f}/1.00", f"{color} {status.upper()}")
            
            with col2:
                st.metric("Status", screening_result['status'].upper())
            
            st.markdown("**Feedback:**")
            st.info(screening_result['feedback'])

# ============= RANKING & MATCHING PAGE =============
elif page == "🏆 Ranking & Matching":
    st.header("Candidate Ranking & Job Matching")
    
    if missing_openai_key or st.session_state.ranker is None:
        st.warning("Ranking is unavailable until OPENAI_API_KEY is configured.")
        st.stop()

    st.markdown("Rank candidates based on job requirements.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        job_id = st.text_input("Job ID", value="JOB_001")
    
    with col2:
        if st.button("🎯 Rank Candidates", use_container_width=True):
            st.session_state.ranking_triggered = True
    
    st.subheader("Job Description")
    job_description = st.text_area(
        "Enter job description",
        value="""
Senior Python Developer
5+ years of experience with Python
Strong knowledge of Django/FastAPI
AWS and Docker experience
Good communication skills
BS in Computer Science or equivalent
        """,
        height=150
    )
    
    if st.session_state.get('ranking_triggered'):
        candidates = st.session_state.db.get_all_candidates()
        
        if not candidates:
            st.warning("No candidates to rank.")
        else:
            with st.spinner("📊 Ranking candidates..."):
                # Prepare candidate data
                candidates_data = []
                for c in candidates:
                    parsed = json.loads(c['parsed_data']) if c['parsed_data'] else {}
                    candidates_data.append({
                        **c,
                        **parsed
                    })
                
                # Rank candidates
                ranked = st.session_state.ranker.rank_candidates(
                    job_description, candidates_data
                )
                
                # Save ranking results
                for r in ranked:
                    st.session_state.db.add_ranking_result(
                        r['id'],
                        job_id,
                        r['ranking_score'],
                        f"Text: {r.get('text_match', 0):.2f}, Skills: {r.get('skill_match', 0):.2f}, Exp: {r.get('experience_match', 0):.2f}"
                    )
                
                st.session_state.ranking_triggered = False
                st.rerun()
    
    # Display ranking results
    ranking_results = st.session_state.db.get_ranking_results(job_id)
    
    if ranking_results:
        st.subheader("Rankings")
        
        for result in ranking_results[:10]:
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.write(f"**{result['rank']}. {result['name']}**")
            
            with col2:
                st.write(result['email'])
            
            with col3:
                score = result['ranking_score']
                st.metric("Match", f"{score:.2%}")
            
            with col4:
                if st.button("Schedule", key=f"schedule_{result['id']}"):
                    st.session_state.selected_for_interview = result['id']

# ============= INTERVIEW SCHEDULING PAGE =============
elif page == "📅 Interview Scheduling":
    st.header("Interview Scheduling")
    
    st.markdown("Schedule interviews with top candidates.")
    
    candidates = st.session_state.db.get_all_candidates()
    
    if not candidates:
        st.warning("No candidates available.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_candidate = st.selectbox(
                "Select Candidate",
                candidates,
                format_func=lambda x: f"{x['name']} ({x['email']})"
            )
        
        with col2:
            if st.button("📅 Show Available Slots", use_container_width=True):
                st.session_state.show_slots = True
        
        if st.session_state.get('show_slots'):
            st.subheader("Available Time Slots")
            
            available_slots = st.session_state.scheduler.suggest_time_slots(num_slots=10)
            
            selected_slot = st.selectbox(
                "Select a time slot",
                available_slots,
                format_func=lambda x: f"{x['date']} at {x['time']}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                interviewer_email = st.text_input("Interviewer Email", value="hr@company.com")
            
            with col2:
                if st.button("✅ Confirm Schedule", use_container_width=True):
                    interview_info = st.session_state.scheduler.schedule_interview(
                        selected_candidate['id'],
                        selected_slot['date'],
                        selected_slot['time'],
                        interviewer_email,
                        selected_candidate['email']
                    )
                    
                    if interview_info['success']:
                        # Save to database
                        st.session_state.db.schedule_interview(
                            selected_candidate['id'],
                            selected_slot['date'],
                            selected_slot['time'],
                            interviewer_email,
                            f"Meeting scheduled: {interview_info['meeting_link']}"
                        )
                        
                        st.success("✅ Interview scheduled successfully!")
                        
                        # Show confirmation
                        st.info(f"""
                        **Interview Confirmation**
                        - Candidate: {selected_candidate['name']}
                        - Date: {selected_slot['date']}
                        - Time: {selected_slot['time']}
                        - Meeting Link: {interview_info['meeting_link']}
                        """)
                    else:
                        st.error(interview_info['message'])
        
        st.subheader("Scheduled Interviews")
        interviews = st.session_state.db.get_interviews()
        
        if interviews:
            for interview in interviews:
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**{interview['name']}**")
                
                with col2:
                    st.write(f"{interview['scheduled_date']} at {interview['scheduled_time']}")
                
                with col3:
                    st.write(f"Status: {interview['status']}")
        else:
            st.info("No interviews scheduled yet.")

# ============= REPORTS PAGE =============
elif page == "📈 Reports":
    st.header("Recruitment Reports")
    
    col1, col2 = st.columns(2)
    
    candidates = st.session_state.db.get_all_candidates()
    
    with col1:
        st.metric("Total Candidates", len(candidates))
    
    with col2:
        screened = sum(1 for c in candidates if st.session_state.db.get_screening_result(c['id']))
        st.metric("Screening Completion", f"{(screened/len(candidates)*100) if candidates else 0:.1f}%")
    
    st.subheader("Candidate Statistics")
    
    if candidates:
        st.write("**Screening Scores Distribution**")
        
        scores = []
        for c in candidates:
            screening = st.session_state.db.get_screening_result(c['id'])
            if screening:
                scores.append(screening['screening_score'])
        
        if scores:
            import pandas as pd
            import numpy as np
            
            df = pd.DataFrame({
                'Score': scores,
                'Category': pd.cut(scores, bins=[0, 0.5, 0.7, 1.0], labels=['Low', 'Medium', 'High'])
            })
            
            st.bar_chart(df['Category'].value_counts().sort_index())
    else:
        st.info("No candidates yet.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
    <p>🤖 AI-Powered Recruitment Automation System | Powered by OpenAI & Python</p>
    </div>
""", unsafe_allow_html=True)
