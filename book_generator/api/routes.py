"""FastAPI route definitions."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from book_generator.api.models import IngestRequest, OutlineNotesRequest, ChapterNotesRequest, ResumeRequest
from book_generator.api.schemas import (
    IngestResponse, BookSummary, BookDetail, OutlineResponse,
    ChapterSummary, ChapterDetail, NoteLog, OutlineNotesResponse,
    ChapterNotesResponse, CompileResponse, ResumeResponse
)
from book_generator.db.client import get_db
from book_generator.services.input_reader import read_input
from book_generator.services.outline_service import improve_outline, get_active_outline
from book_generator.services.chapter_service import improve_chapter
from book_generator.core.logger import logger

# Import workflow functions directly (no Celery needed)
from book_generator.services.outline_service import generate_outline
from book_generator.services.chapter_service import generate_chapter
from book_generator.output.compiler import compile_book
from book_generator.notifications.notifier import notify, OUTLINE_READY, WAITING_CHAPTER_NOTES, FINAL_DRAFT_COMPLETED, WORKFLOW_PAUSED, WORKFLOW_ERROR

router = APIRouter(prefix="/api/v1", tags=["book-generator"])


# ── Internal workflow functions (run in background) ───────────

def _run_outline(book_id: str):
    try:
        db = get_db()
        book = db.table("books").select("*").eq("id", book_id).single().execute().data
        if not book.get("notes_on_outline_before"):
            db.table("books").update({"status": "paused"}).eq("id", book_id).execute()
            notify(WORKFLOW_PAUSED, {"book_id": book_id, "reason": "notes_on_outline_before is empty"})
            return
        db.table("books").update({"status": "outline_generating"}).eq("id", book_id).execute()
        outline = generate_outline(book_id, book["title"], book["notes_on_outline_before"])
        notify(OUTLINE_READY, {"book_id": book_id, "title": book["title"], "outline_id": outline["id"]})

        book = db.table("books").select("*").eq("id", book_id).single().execute().data
        notes_status = book.get("status_outline_notes", "")
        if notes_status == "no_notes_needed":
            _run_chapters(book_id)
        else:
            db.table("books").update({"status": "paused"}).eq("id", book_id).execute()
    except Exception as exc:
        logger.error(f"Outline stage failed: {exc}")
        get_db().table("books").update({"status": "error"}).eq("id", book_id).execute()
        notify(WORKFLOW_ERROR, {"book_id": book_id, "error": str(exc)})


def _run_chapters(book_id: str):
    try:
        db = get_db()
        book = db.table("books").select("*").eq("id", book_id).single().execute().data
        from book_generator.services.outline_service import get_active_outline
        outline = get_active_outline(book_id)
        if not outline:
            raise ValueError("No active outline found")

        chapters_meta = outline["content"].get("chapters", [])
        db.table("books").update({"status": "chapters_generating"}).eq("id", book_id).execute()

        # Resume from last completed chapter
        done = db.table("chapters").select("chapter_number").eq("book_id", book_id).in_("status", ["ready", "approved"]).order("chapter_number", desc=True).limit(1).execute().data
        start_from = (done[0]["chapter_number"] + 1) if done else 1

        for idx, ch_meta in enumerate(chapters_meta, start=1):
            if idx < start_from:
                continue
            ch_meta["chapter_number"] = idx
            result = generate_chapter(book_id, outline["id"], ch_meta, book["title"])

            ch_row = db.table("chapters").select("chapter_notes_status").eq("id", result["chapter_id"]).single().execute().data
            notes_status = ch_row.get("chapter_notes_status", "")
            if notes_status == "yes":
                db.table("books").update({"status": "paused"}).eq("id", book_id).execute()
                notify(WAITING_CHAPTER_NOTES, {"book_id": book_id, "chapter_id": result["chapter_id"], "chapter_title": ch_meta["title"]})
                return

        db.table("books").update({"status": "chapters_ready"}).eq("id", book_id).execute()
        _run_compile(book_id)
    except Exception as exc:
        logger.error(f"Chapters stage failed: {exc}")
        get_db().table("books").update({"status": "error"}).eq("id", book_id).execute()
        notify(WORKFLOW_ERROR, {"book_id": book_id, "error": str(exc)})


def _run_compile(book_id: str):
    try:
        db = get_db()
        book = db.table("books").select("title").eq("id", book_id).single().execute().data
        db.table("books").update({"status": "compiling"}).eq("id", book_id).execute()
        paths = compile_book(book_id, book["title"])
        notify(FINAL_DRAFT_COMPLETED, {"book_id": book_id, "title": book["title"], **paths})
    except Exception as exc:
        logger.error(f"Compile stage failed: {exc}")
        get_db().table("books").update({"status": "error"}).eq("id", book_id).execute()
        notify(WORKFLOW_ERROR, {"book_id": book_id, "error": str(exc)})


# ── Ingest ────────────────────────────────────────────────────

@router.post("/ingest", response_model=IngestResponse, summary="Ingest books from Excel or Google Sheets")
def ingest(req: IngestRequest, bg: BackgroundTasks):
    rows = read_input(req.source_type, req.source_ref)
    if not rows:
        raise HTTPException(400, "No valid rows found in source")

    db = get_db()
    created = []
    for row in rows:
        book = db.table("books").insert({
            "title": row["title"],
            "source_type": req.source_type,
            "source_ref": req.source_ref,
            "notes_on_outline_before": row.get("notes_on_outline_before", ""),
            "status_outline_notes": row.get("status_outline_notes", "pending"),
            "status": "pending",
        }).execute().data[0]

        bg.add_task(_run_outline, book["id"])
        created.append({"book_id": book["id"], "title": book["title"]})
        logger.info(f"Ingested book: {book['id']} — {book['title']}")

    return {"created": created}


# ── Books ─────────────────────────────────────────────────────

@router.get("/books", response_model=list[BookSummary], summary="List all books")
def list_books():
    return get_db().table("books").select("id, title, status, created_at").order("created_at", desc=True).execute().data


@router.get("/books/{book_id}", response_model=BookDetail, summary="Get book details and current status")
def get_book(book_id: str):
    result = get_db().table("books").select("*").eq("id", book_id).single().execute()
    if not result.data:
        raise HTTPException(404, "Book not found")
    return result.data


# ── Outline ───────────────────────────────────────────────────

@router.get("/books/{book_id}/outline", response_model=OutlineResponse, summary="Get the active outline for a book")
def get_outline(book_id: str):
    outline = get_active_outline(book_id)
    if not outline:
        raise HTTPException(404, "No active outline")
    return outline


@router.post("/books/{book_id}/outline/notes", response_model=OutlineNotesResponse, summary="Submit editor notes to improve the outline")
def submit_outline_notes(book_id: str, req: OutlineNotesRequest, bg: BackgroundTasks):
    outline = get_active_outline(book_id)
    if not outline:
        raise HTTPException(404, "No active outline to annotate")

    improved = improve_outline(book_id, outline["id"], req.notes_on_outline_after)
    db = get_db()
    db.table("books").update({
        "notes_on_outline_after": req.notes_on_outline_after,
        "status_outline_notes": "done",
        "status": "outline_ready",
    }).eq("id", book_id).execute()

    if req.proceed:
        bg.add_task(_run_chapters, book_id)

    return {"outline_id": improved["id"], "version": improved["version"], "chapters_triggered": req.proceed}


# ── Chapters ──────────────────────────────────────────────────

@router.get("/books/{book_id}/chapters", response_model=list[ChapterSummary], summary="List all chapters for a book")
def list_chapters(book_id: str):
    return get_db().table("chapters").select("id, chapter_number, title, status, chapter_notes_status").eq("book_id", book_id).order("chapter_number").execute().data


@router.get("/books/{book_id}/chapters/{chapter_id}", response_model=ChapterDetail, summary="Get full chapter content")
def get_chapter(book_id: str, chapter_id: str):
    result = get_db().table("chapters").select("*").eq("id", chapter_id).eq("book_id", book_id).single().execute()
    if not result.data:
        raise HTTPException(404, "Chapter not found")
    return result.data


@router.post("/books/{book_id}/chapters/{chapter_id}/notes", response_model=ChapterNotesResponse, summary="Submit editor notes to revise a chapter")
def submit_chapter_notes(book_id: str, chapter_id: str, req: ChapterNotesRequest, bg: BackgroundTasks):
    improve_chapter(chapter_id, req.editor_notes)
    bg.add_task(_run_chapters, book_id)
    return {"status": "revised", "chapter_id": chapter_id}


# ── Compile ───────────────────────────────────────────────────

@router.post("/books/{book_id}/compile", response_model=CompileResponse, summary="Trigger final book compilation to .docx and .txt")
def compile(book_id: str, bg: BackgroundTasks):
    bg.add_task(_run_compile, book_id)
    return {"status": "compiling", "book_id": book_id}


# ── Resume ────────────────────────────────────────────────────

@router.post("/books/{book_id}/resume", response_model=ResumeResponse, summary="Resume a paused workflow at a specific stage")
def resume(book_id: str, req: ResumeRequest, bg: BackgroundTasks):
    if req.stage == "outline":
        bg.add_task(_run_outline, book_id)
    elif req.stage == "chapters":
        bg.add_task(_run_chapters, book_id)
    elif req.stage == "compile":
        bg.add_task(_run_compile, book_id)
    else:
        raise HTTPException(400, f"Unknown stage: {req.stage}")
    return {"resumed": req.stage, "book_id": book_id}


# ── Notes Log ─────────────────────────────────────────────────

@router.get("/books/{book_id}/notes", response_model=list[NoteLog], summary="Get full editor notes audit log")
def get_notes_log(book_id: str):
    return get_db().table("notes_logs").select("*").eq("book_id", book_id).order("created_at").execute().data
