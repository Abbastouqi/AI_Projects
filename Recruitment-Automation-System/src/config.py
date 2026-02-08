import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root directory
env_path = Path(__file__).parent.parent / '.env'
# Ensure .env values override any empty/older env vars in the session
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    """Application configuration."""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/recruitment.db")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./resumes")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    MIN_SCREENING_SCORE = float(os.getenv("MIN_SCREENING_SCORE", 0.7))

    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.OPENAI_API_KEY:
            print("⚠️ Warning: OPENAI_API_KEY not set.")
        return True
