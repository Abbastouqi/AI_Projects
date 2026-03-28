from pydantic import BaseModel
from typing import Optional


class IngestRequest(BaseModel):
    source_type: str          # "excel" or "google_sheets"
    source_ref: str           # file path or sheet ID


class OutlineNotesRequest(BaseModel):
    notes_on_outline_after: str
    proceed: bool = True      # if True, trigger chapter generation after improvement


class ChapterNotesRequest(BaseModel):
    editor_notes: str


class ResumeRequest(BaseModel):
    """Resume a paused workflow from a specific stage."""
    stage: str                # "outline" | "chapters" | "compile"
