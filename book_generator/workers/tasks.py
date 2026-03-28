"""
Celery background tasks — one per workflow stage.

State machine:
  pending → outline_generating → outline_ready
          → [paused if status_outline_notes == 'yes']
          → chapters_generating → chapters_ready
          → compiling → completed
"""
from book_generator.workers.celery_app import celery_app
from book_generator.db.client import get_db
from book_generator.services.outline_service import generate_outline, get_active_outline
from book_generator.services.chapter_service import generate_chapter
from book_generator.output.compiler import compile_book
from book_generator.notifications.notifier import notify, OUTLINE_READY, WAITING_CHAPTER_NOTES, FINAL_DRAFT_COMPLETED, WORKFLOW_PAUSED, WORKFLOW_ERROR
from book_generator.core.logger import logger


def _get_book(book_id: str) -> dict:
    return get_db().table("books").select("*").eq("id", book_id).single().execute().data


# ── Stage 1: Outline ──────────────────────────────────────────

@celery_app.task(bind=True, max_retries=3, default_retry_delay=30, name="tasks.run_outline_stage")
def run_outline_stage(self, book_id: str):
    try:
        book = _get_book(book_id)
        if not book.get("notes_on_outline_before"):
            logger.warning(f"book_id={book_id}: no notes_on_outline_before — pausing")
            get_db().table("books").update({"status": "paused"}).eq("id", book_id).execute()
            notify(WORKFLOW_PAUSED, {"book_id": book_id, "reason": "notes_on_outline_before is empty"})
            return

        get_db().table("books").update({"status": "outline_generating"}).eq("id", book_id).execute()
        outline = generate_outline(book_id, book["title"], book["notes_on_outline_before"])
        notify(OUTLINE_READY, {"book_id": book_id, "title": book["title"], "outline_id": outline["id"]})

        # Gate: check status_outline_notes
        book = _get_book(book_id)
        notes_status = book.get("status_outline_notes", "")
        if notes_status == "yes":
            logger.info(f"book_id={book_id}: waiting for outline editor notes")
            get_db().table("books").update({"status": "paused"}).eq("id", book_id).execute()
            notify(WORKFLOW_PAUSED, {"book_id": book_id, "reason": "Waiting for outline_after notes"})
        elif notes_status == "no_notes_needed":
            run_chapters_stage.delay(book_id)
        else:
            logger.info(f"book_id={book_id}: status_outline_notes='{notes_status}' — pausing")
            get_db().table("books").update({"status": "paused"}).eq("id", book_id).execute()

    except Exception as exc:
        logger.error(f"run_outline_stage failed for book_id={book_id}: {exc}")
        get_db().table("books").update({"status": "error"}).eq("id", book_id).execute()
        notify(WORKFLOW_ERROR, {"book_id": book_id, "error": str(exc)})
        raise self.retry(exc=exc)


# ── Stage 2: Chapters ─────────────────────────────────────────

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60, name="tasks.run_chapters_stage")
def run_chapters_stage(self, book_id: str):
    try:
        book = _get_book(book_id)
        outline = get_active_outline(book_id)
        if not outline:
            raise ValueError(f"No active outline for book_id={book_id}")

        chapters_meta = outline["content"].get("chapters", [])
        get_db().table("books").update({"status": "chapters_generating"}).eq("id", book_id).execute()

        # Find the last completed chapter so we can resume mid-way
        done = (
            get_db().table("chapters")
            .select("chapter_number")
            .eq("book_id", book_id)
            .in_("status", ["ready", "approved"])
            .order("chapter_number", desc=True)
            .limit(1)
            .execute()
            .data
        )
        start_from = (done[0]["chapter_number"] + 1) if done else 1

        for idx, ch_meta in enumerate(chapters_meta, start=1):
            if idx < start_from:
                continue  # already generated
            ch_meta["chapter_number"] = idx
            result = generate_chapter(book_id, outline["id"], ch_meta, book["title"])

            # Check per-chapter notes gate
            ch_row = get_db().table("chapters").select("chapter_notes_status").eq("id", result["chapter_id"]).single().execute().data
            notes_status = ch_row.get("chapter_notes_status", "")

            if notes_status == "yes":
                logger.info(f"Chapter {idx} waiting for notes — pausing workflow")
                get_db().table("books").update({"status": "paused"}).eq("id", book_id).execute()
                notify(WAITING_CHAPTER_NOTES, {
                    "book_id": book_id,
                    "chapter_id": result["chapter_id"],
                    "chapter_title": ch_meta["title"],
                })
                return  # Resume via API endpoint after notes are submitted
            elif notes_status not in ("no_notes_needed", "done", ""):
                logger.info(f"Chapter {idx} notes_status='{notes_status}' — pausing")
                get_db().table("books").update({"status": "paused"}).eq("id", book_id).execute()
                return

        get_db().table("books").update({"status": "chapters_ready"}).eq("id", book_id).execute()
        run_compile_stage.delay(book_id)

    except Exception as exc:
        logger.error(f"run_chapters_stage failed for book_id={book_id}: {exc}")
        get_db().table("books").update({"status": "error"}).eq("id", book_id).execute()
        notify(WORKFLOW_ERROR, {"book_id": book_id, "error": str(exc)})
        raise self.retry(exc=exc)


# ── Stage 3: Compile ──────────────────────────────────────────

@celery_app.task(bind=True, max_retries=2, default_retry_delay=30, name="tasks.run_compile_stage")
def run_compile_stage(self, book_id: str):
    try:
        book = _get_book(book_id)
        get_db().table("books").update({"status": "compiling"}).eq("id", book_id).execute()
        paths = compile_book(book_id, book["title"])
        notify(FINAL_DRAFT_COMPLETED, {"book_id": book_id, "title": book["title"], **paths})
        logger.info(f"Book completed: book_id={book_id}")
    except Exception as exc:
        logger.error(f"run_compile_stage failed for book_id={book_id}: {exc}")
        get_db().table("books").update({"status": "error"}).eq("id", book_id).execute()
        notify(WORKFLOW_ERROR, {"book_id": book_id, "error": str(exc)})
        raise self.retry(exc=exc)
