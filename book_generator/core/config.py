from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str

    openai_api_key: str
    openai_model: str = "gpt-4o"

    serpapi_key: str = ""

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "amazonnn399@gmail.com"
    smtp_pass: str = "mphill@Cs22"
    notify_email: str = "abbastouqeer399@gmail.com"

    teams_webhook_url: str = ""

    redis_url: str = "redis://localhost:6379/0"

    google_sheets_credentials_json: str = "credentials.json"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
