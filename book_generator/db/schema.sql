-- ============================================================
-- BOOK GENERATION SYSTEM — Supabase / PostgreSQL Schema
-- ============================================================

-- ENUM types for status gating
CREATE TYPE book_status AS ENUM (
    'pending', 'outline_generating', 'outline_ready',
    'chapters_generating', 'chapters_ready', 'compiling',
    'completed', 'paused', 'error'
);

CREATE TYPE notes_status AS ENUM (
    'yes', 'no_notes_needed', 'pending', 'done'
);

CREATE TYPE chapter_status AS ENUM (
    'pending', 'generating', 'ready', 'needs_revision', 'approved'
);

-- ============================================================
-- books
-- ============================================================
CREATE TABLE books (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           TEXT NOT NULL,
    source_type     TEXT NOT NULL CHECK (source_type IN ('excel', 'google_sheets')),
    source_ref      TEXT,                          -- file path or sheet ID
    status          book_status NOT NULL DEFAULT 'pending',

    -- human-in-the-loop fields
    notes_on_outline_before     TEXT,              -- editor notes BEFORE outline generation
    notes_on_outline_after      TEXT,              -- editor notes AFTER outline is generated
    status_outline_notes        notes_status DEFAULT 'pending',

    -- output paths
    output_docx     TEXT,
    output_txt      TEXT,

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);

-- ============================================================
-- outlines
-- ============================================================
CREATE TABLE outlines (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id         UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,

    -- raw LLM output stored as JSONB
    -- shape: { "chapters": [{ "title", "summary", "subtopics": [] }] }
    content         JSONB NOT NULL,

    version         INT NOT NULL DEFAULT 1,        -- increments on each revision
    is_active       BOOLEAN NOT NULL DEFAULT TRUE, -- only one active outline per book

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_outlines_book_id ON outlines(book_id);

-- ============================================================
-- chapters
-- ============================================================
CREATE TABLE chapters (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id         UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    outline_id      UUID NOT NULL REFERENCES outlines(id),

    chapter_number  INT NOT NULL,
    title           TEXT NOT NULL,
    content         TEXT,                          -- full generated text
    status          chapter_status NOT NULL DEFAULT 'pending',

    -- human-in-the-loop
    editor_notes    TEXT,
    chapter_notes_status notes_status DEFAULT 'pending',

    -- research context injected into prompt
    research_context TEXT,

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(book_id, chapter_number)
);

CREATE INDEX idx_chapters_book_id ON chapters(book_id);

-- ============================================================
-- chapter_summaries
-- ============================================================
CREATE TABLE chapter_summaries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id      UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    book_id         UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,

    summary         TEXT NOT NULL,                 -- 3-5 line summary for context chaining
    version         INT NOT NULL DEFAULT 1,

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_summaries_book_id ON chapter_summaries(book_id);
CREATE INDEX idx_summaries_chapter_id ON chapter_summaries(chapter_id);

-- ============================================================
-- notes_logs  (audit trail for all human notes)
-- ============================================================
CREATE TABLE notes_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id         UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    chapter_id      UUID REFERENCES chapters(id),  -- NULL if book-level note

    stage           TEXT NOT NULL,                 -- 'outline_before','outline_after','chapter'
    note_text       TEXT NOT NULL,
    added_by        TEXT DEFAULT 'editor',

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notes_book_id ON notes_logs(book_id);

-- ============================================================
-- Auto-update updated_at trigger
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_books_updated_at    BEFORE UPDATE ON books    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_outlines_updated_at BEFORE UPDATE ON outlines FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_chapters_updated_at BEFORE UPDATE ON chapters FOR EACH ROW EXECUTE FUNCTION update_updated_at();
