# Architecture — Automated Book Generation System

## Tech Stack

| Layer            | Technology                          |
|------------------|-------------------------------------|
| API Framework    | FastAPI                             |
| Database         | Supabase (PostgreSQL)               |
| LLM              | OpenAI GPT-4o (swappable)           |
| Background Jobs  | Celery + Redis                      |
| Input Sources    | Excel (openpyxl) / Google Sheets    |
| Research         | SerpAPI                             |
| Output           | python-docx (.docx), plain .txt     |
| Notifications    | SMTP Email + MS Teams Webhook       |
| Config           | pydantic-settings + .env            |
| Logging          | loguru                              |

---

## Text Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT SOURCES                            │
│          Excel File  ──┬──  Google Sheets                       │
└───────────────────────┼─────────────────────────────────────────┘
                         │  POST /api/v1/ingest
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI (main.py)                          │
│  /ingest  /books  /outline  /chapters  /compile  /resume        │
└───────────────────────┬─────────────────────────────────────────┘
                         │  .delay()
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Celery Workers (Redis broker)                  │
│                                                                  │
│  ┌──────────────────┐   ┌──────────────────┐   ┌─────────────┐ │
│  │ run_outline_stage│──▶│run_chapters_stage│──▶│run_compile  │ │
│  └──────────────────┘   └──────────────────┘   └─────────────┘ │
│          │                      │                      │        │
│          ▼                      ▼                      ▼        │
│   outline_service        chapter_service          compiler      │
│   (LLM + Supabase)      (LLM + research)        (.docx/.txt)   │
└───────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supabase (PostgreSQL)                         │
│   books ──▶ outlines ──▶ chapters ──▶ chapter_summaries         │
│                                   ──▶ notes_logs                │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Notification System                            │
│              Email (SMTP)  +  MS Teams Webhook                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Workflow State Machine

```
[pending]
    │
    ▼  notes_on_outline_before present?
    │  NO  ──────────────────────────────▶ [paused]
    │  YES
    ▼
[outline_generating]
    │
    ▼  LLM generates outline
[outline_ready]
    │
    ├── status_outline_notes == "yes"       ──▶ [paused] ──▶ editor submits notes
    │                                                          ──▶ outline improved
    │                                                          ──▶ [outline_ready]
    ├── status_outline_notes == "no_notes_needed"
    │       │
    │       ▼
[chapters_generating]
    │
    │  For each chapter:
    │    ├── generate chapter (with context chaining + research)
    │    ├── save chapter + summary
    │    └── chapter_notes_status == "yes"  ──▶ [paused]
    │                                            ──▶ editor submits notes
    │                                            ──▶ chapter improved
    │                                            ──▶ resume chapters
    ▼
[chapters_ready]
    │
    ▼
[compiling]
    │
    ▼
[completed]  ──▶ .docx + .txt output files
```

---

## Human-in-the-Loop Gates

| Gate                    | Field                    | Values                              |
|-------------------------|--------------------------|-------------------------------------|
| Before outline gen      | notes_on_outline_before  | free text (required to proceed)     |
| After outline gen       | status_outline_notes     | yes / no_notes_needed / pending     |
| After outline notes     | notes_on_outline_after   | free text (triggers improvement)    |
| Per chapter             | chapter_notes_status     | yes / no_notes_needed / done        |
| Per chapter notes       | editor_notes             | free text (triggers improvement)    |

---

## API Endpoints Summary

| Method | Endpoint                                    | Purpose                          |
|--------|---------------------------------------------|----------------------------------|
| POST   | /api/v1/ingest                              | Read source, create books, start |
| GET    | /api/v1/books                               | List all books                   |
| GET    | /api/v1/books/{id}                          | Get book detail + status         |
| GET    | /api/v1/books/{id}/outline                  | Get active outline               |
| POST   | /api/v1/books/{id}/outline/notes            | Submit outline editor notes      |
| GET    | /api/v1/books/{id}/chapters                 | List chapters                    |
| GET    | /api/v1/books/{id}/chapters/{cid}           | Get chapter content              |
| POST   | /api/v1/books/{id}/chapters/{cid}/notes     | Submit chapter editor notes      |
| POST   | /api/v1/books/{id}/compile                  | Trigger final compilation        |
| POST   | /api/v1/books/{id}/resume                   | Resume paused workflow           |
| GET    | /api/v1/books/{id}/notes                    | Get full notes audit log         |
