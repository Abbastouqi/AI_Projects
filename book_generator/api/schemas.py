"""Response schemas for OpenAPI documentation."""
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class BookSummary(BaseModel):
    id: str
    title: str
    status: str
    created_at: datetime


class BookDetail(BaseModel):
    id: str
    title: str
    source_type: str
    source_ref: Optional[str] = None
    status: str
    notes_on_outline_before: Optional[str] = None
    notes_on_outline_after: Optional[str] = None
    status_outline_notes: Optional[str] = None
    output_docx: Optional[str] = None
    output_txt: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None


class OutlineResponse(BaseModel):
    id: str
    book_id: str
    content: Any
    version: int
    is_active: bool
    created_at: datetime


class ChapterSummary(BaseModel):
    id: str
    chapter_number: int
    title: str
    status: str
    chapter_notes_status: Optional[str] = None


class ChapterDetail(BaseModel):
    id: str
    book_id: str
    chapter_number: int
    title: str
    content: Optional[str] = None
    status: str
    editor_notes: Optional[str] = None
    chapter_notes_status: Optional[str] = None
    research_context: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class NoteLog(BaseModel):
    id: str
    book_id: str
    chapter_id: Optional[str] = None
    stage: str
    note_text: str
    added_by: Optional[str] = None
    created_at: datetime


class IngestResult(BaseModel):
    book_id: str
    title: str


class IngestResponse(BaseModel):
    created: list[IngestResult]


class OutlineNotesResponse(BaseModel):
    outline_id: str
    version: int
    chapters_triggered: bool


class ChapterNotesResponse(BaseModel):
    status: str
    chapter_id: str


class CompileResponse(BaseModel):
    status: str
    book_id: str


class ResumeResponse(BaseModel):
    resumed: str
    book_id: str


class HealthResponse(BaseModel):
    status: str
