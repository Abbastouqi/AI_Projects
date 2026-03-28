from supabase import create_client, Client
from book_generator.core.config import get_settings
from functools import lru_cache


@lru_cache
def get_db() -> Client:
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_key)
