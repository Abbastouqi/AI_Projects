"""Chapter generation, revision, and summary logic."""
import json
from book_generator.db.client import get_db
from book_generator.services.llm import chat_json
from book_generator.services.research import get_research_context
from book_generator.prompts.templates import (
    GENERATE_CHAPTER, IMPROVE_CHAPTER, RESEARCH_BLOCK_TEMPLATE
)
from book_generator.core.logger import logger


def _get_previous_summaries(book_id: str, before_chapter_number: int) -> str:
    """Fetch ordered summaries of all chapters before the given number."""
    db = get_db()
    chapters = (
        db.table("chapters")
        .select("id, chapter_number, title")
        .eq("book_id", book_id)
        .lt("chapter_number", before_chapter_number)
        .order("chapter_number")
        .execute()
        .data
    )
    if not chapters:
        return "This is the first chapter."

    summaries = []
    for ch in chapters:
        s = (
            db.table("chapter_summaries")
            .select("summary")
            .eq("chapter_id", ch["id"])
            .order("version", desc=True)
            .limit(1)
            .execute()
            .data
        )
        if s:
            summaries.append(f"Chapter {ch['chapter_number']} — {ch['title']}: {s[0]['summary']}")
    return "\n".join(summaries) if summaries else "No previous summaries available."


def generate_chapter(book_id: str, outline_id: str, chapter_meta: dict, book_title: str) -> dict:
    """
    Generate a single chapter.
    chapter_meta: { "chapter_number": int, "title": str, "summary": str, "subtopics": [] }
    """
    chapter_number = chapter_meta["chapter_number"]
    chapter_title = chapter_meta["title"]
    db = get_db()

    logger.info(f"Generating chapter {chapter_number}: '{chapter_title}' for book_id={book_id}")

    # Context chaining
    summaries = _get_previous_summaries(book_id, chapter_number)

    # Optional research enrichment
    research_context = get_research_context(chapter_title, book_title)
    research_block = RESEARCH_BLOCK_TEMPLATE.format(summaries=research_context) if research_context else ""

    prompt = GENERATE_CHAPTER.format(
        title=book_title,
        chapter_title=chapter_title,
        chapter_number=chapter_number,
        summaries=summaries,
        research_block=research_block,
    )

    result = chat_json(prompt)
    content = result.get("content", "")
    summary = result.get("summary", "")

    # Upsert chapter row
    existing = db.table("chapters").select("id").eq("book_id", book_id).eq("chapter_number", chapter_number).execute()
    if existing.data:
        chapter_id = existing.data[0]["id"]
        db.table("chapters").update({
            "content": content,
            "status": "ready",
            "research_context": research_context,
            "outline_id": outline_id,
        }).eq("id", chapter_id).execute()
    else:
        chapter_id = db.table("chapters").insert({
            "book_id": book_id,
            "outline_id": outline_id,
            "chapter_number": chapter_number,
            "title": chapter_title,
            "content": content,
            "status": "ready",
            "research_context": research_context,
        }).execute().data[0]["id"]

    # Save summary (auto-increment version)
    existing_s = db.table("chapter_summaries").select("version").eq("chapter_id", chapter_id).order("version", desc=True).limit(1).execute()
    summary_version = (existing_s.data[0]["version"] + 1) if existing_s.data else 1
    db.table("chapter_summaries").insert({
        "chapter_id": chapter_id,
        "book_id": book_id,
        "summary": summary,
        "version": summary_version,
    }).execute()

    logger.info(f"Chapter {chapter_number} saved: chapter_id={chapter_id}")
    return {"chapter_id": chapter_id, "chapter_number": chapter_number, "title": chapter_title}


def improve_chapter(chapter_id: str, editor_notes: str) -> dict:
    """Revise a chapter based on editor notes."""
    db = get_db()
    ch = db.table("chapters").select("content, chapter_number, book_id, title").eq("id", chapter_id).single().execute().data
    prompt = IMPROVE_CHAPTER.format(chapter_text=ch["content"], chapter_notes=editor_notes)
    result = chat_json(prompt)

    db.table("chapters").update({
        "content": result["content"],
        "status": "approved",
        "editor_notes": editor_notes,
        "chapter_notes_status": "done",
    }).eq("id", chapter_id).execute()

    # Save updated summary
    existing_versions = db.table("chapter_summaries").select("version").eq("chapter_id", chapter_id).order("version", desc=True).limit(1).execute()
    next_version = (existing_versions.data[0]["version"] + 1) if existing_versions.data else 1
    db.table("chapter_summaries").insert({
        "chapter_id": chapter_id,
        "book_id": ch["book_id"],
        "summary": result["summary"],
        "version": next_version,
    }).execute()

    db.table("notes_logs").insert({
        "book_id": ch["book_id"],
        "chapter_id": chapter_id,
        "stage": "chapter",
        "note_text": editor_notes,
    }).execute()

    logger.info(f"Chapter improved: chapter_id={chapter_id}")
    return result
