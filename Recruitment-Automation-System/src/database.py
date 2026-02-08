import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any
from src.config import Config

class Database:
    """SQLite database handler."""
    
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self._init_db()
    
    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize database tables."""
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    file_path TEXT,
                    parsed_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS screening_results (
                    candidate_id INTEGER PRIMARY KEY,
                    screening_score REAL,
                    feedback TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
                );
                
                CREATE TABLE IF NOT EXISTS ranking_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER,
                    job_id TEXT,
                    ranking_score REAL,
                    match_details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
                );
                
                CREATE TABLE IF NOT EXISTS interviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER,
                    scheduled_date TEXT,
                    scheduled_time TEXT,
                    interviewer_email TEXT,
                    meeting_link TEXT,
                    status TEXT DEFAULT 'Scheduled',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
                );
            """)
            self._ensure_ranking_match_details(conn)

    def _ensure_ranking_match_details(self, conn: sqlite3.Connection):
        """Ensure match_details column exists for older databases."""
        cols = [row[1] for row in conn.execute("PRAGMA table_info(ranking_results)").fetchall()]
        if "match_details" not in cols:
            conn.execute("ALTER TABLE ranking_results ADD COLUMN match_details TEXT")

    def add_candidate(self, name: str, email: str, phone: str, file_path: str, parsed_data: str) -> int:
        with self._get_conn() as conn:
            cursor = conn.execute(
                "INSERT INTO candidates (name, email, phone, file_path, parsed_data) VALUES (?, ?, ?, ?, ?)",
                (name, email, phone, file_path, parsed_data)
            )
            return cursor.lastrowid

    def get_all_candidates(self) -> List[Dict]:
        with self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM candidates ORDER BY created_at DESC").fetchall()
            return [dict(row) for row in rows]

    def add_screening_result(self, candidate_id: int, score: float, feedback: str):
        status = "Recommended" if score >= Config.MIN_SCREENING_SCORE else "Review" if score >= 0.5 else "Rejected"
        with self._get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO screening_results (candidate_id, screening_score, feedback, status) VALUES (?, ?, ?, ?)",
                (candidate_id, score, feedback, status)
            )

    def get_screening_result(self, candidate_id: int) -> Dict:
        with self._get_conn() as conn:
            row = conn.execute("SELECT * FROM screening_results WHERE candidate_id = ?", (candidate_id,)).fetchone()
            return dict(row) if row else None

    def add_ranking_result(self, candidate_id: int, job_id: str, score: float, details: str):
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO ranking_results (candidate_id, job_id, ranking_score, match_details) VALUES (?, ?, ?, ?)",
                (candidate_id, job_id, score, details)
            )

    def get_ranking_results(self, job_id: str) -> List[Dict]:
        with self._get_conn() as conn:
            query = """
                SELECT r.*, c.name, c.email 
                FROM ranking_results r 
                JOIN candidates c ON r.candidate_id = c.id 
                WHERE r.job_id = ? 
                ORDER BY r.ranking_score DESC
            """
            rows = conn.execute(query, (job_id,)).fetchall()
            return [dict(row) for row in rows]

    def schedule_interview(self, candidate_id: int, date: str, time: str, email: str, link: str):
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO interviews (candidate_id, scheduled_date, scheduled_time, interviewer_email, meeting_link) VALUES (?, ?, ?, ?, ?)",
                (candidate_id, date, time, email, link)
            )

    def get_interviews(self) -> List[Dict]:
        with self._get_conn() as conn:
            query = """
                SELECT i.*, c.name 
                FROM interviews i 
                JOIN candidates c ON i.candidate_id = c.id 
                ORDER BY i.scheduled_date, i.scheduled_time
            """
            rows = conn.execute(query).fetchall()
            return [dict(row) for row in rows]
