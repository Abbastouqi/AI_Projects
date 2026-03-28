"""Outline generation and revision logic."""
import json
from book_generator.db.client import get_db
from book_generator.services.llm import chat_json
from book_generator.prompts.templates import GENERATE_OUTLINE, IMPROVE_OUTLINE
from book_generator.core.logger import logger


def generate_outline(book_id: str, title: str, notes_before: str) -> dict:
    """Generate outline via LLM and persist to Supabase. Returns outline row."""
    logger.info(f"Generating outline for book_id={book_id}")
    prompt = GENERATE_OUTLINE.format(title=title, notes_on_outline_before=notes_before or "None")
    outline_json = chat_json(prompt)

    db = get_db()
    # Deactivate any previous outlines
    db.table("outlines").update({"is_active": False}).eq("book_id", book_id).execute()

    # Get next version number
    existing = db.table("outlines").select("version").eq("book_id", book_id).order("version", desc=True).limit(1).execute()
    version = (existing.data[0]["version"] + 1) if existing.data else 1

    row = db.table("outlines").insert({
        "book_id": book_id,
        "content": outline_json,
        "version": version,
        "is_active": True,
    }).execute().data[0]

    db.table("books").update({"status": "outline_ready"}).eq("id", book_id).execute()
    logger.info(f"Outline saved: outline_id={row['id']} version={version}")
    return row


def improve_outline(book_id: str, outline_id: str, notes_after: str) -> dict:
    """Revise an existing outline based on editor notes."""
    db = get_db()
    existing = db.table("outlines").select("content,version").eq("id", outline_id).single().execute().data
    prompt = IMPROVE_OUTLINE.format(
        outline=json.dumps(existing["content"], indent=2),
        notes_on_outline_after=notes_after,
    )
    improved = chat_json(prompt)

    db.table("outlines").update({"is_active": False}).eq("book_id", book_id).execute()
    row = db.table("outlines").insert({
        "book_id": book_id,
        "content": improved,
        "version": existing["version"] + 1,
        "is_active": True,
    }).execute().data[0]

    # Log the note
    db.table("notes_logs").insert({
        "book_id": book_id,
        "stage": "outline_after",
        "note_text": notes_after,
    }).execute()

    logger.info(f"Outline improved: new outline_id={row['id']}")
    return row


def get_active_outline(book_id: str) -> dict | None:
    db = get_db()
    result = db.table("outlines").select("*").eq("book_id", book_id).eq("is_active", True).limit(1).execute()
    return result.data[0] if result.data else None
