-- ============================================================
-- BOOK GENERATION SYSTEM — Safe/Idempotent Schema
-- Run this even if schema was already applied — no errors
-- ============================================================

-- ENUM types (only create if they don't exist)
DO $$ BEGIN
    CREATE TYPE book_status AS ENUM (
        'pending', 'outline_generating', 'outline_ready',
        'chapters_generating', 'chapters_ready', 'compiling',
        'completed', 'paused', 'error'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE notes_status AS ENUM (
        'yes', 'no_notes_needed', 'pending', 'done'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE chapter_status AS ENUM (
        'pending', 'generating', 'ready', 'needs_revision', 'approved'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- books
CREATE TABLE IF NOT EXISTS books (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title                   TEXT NOT NULL,
    source_type             TEXT NOT NULL CHECK (source_type IN ('excel', 'google_sheets')),
    source_ref              TEXT,
    status                  book_status NOT NULL DEFAULT 'pending',
    notes_on_outline_before TEXT,
    notes_on_outline_after  TEXT,
    status_outline_notes    notes_status DEFAULT 'pending',
    output_docx             TEXT,
    output_txt              TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at            TIMESTAMPTZ
);

-- outlines
CREATE TABLE IF NOT EXISTS outlines (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id    UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    content    JSONB NOT NULL,
    version    INT NOT NULL DEFAULT 1,
    is_active  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_outlines_book_id ON outlines(book_id);

-- chapters
CREATE TABLE IF NOT EXISTS chapters (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id              UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    outline_id           UUID NOT NULL REFERENCES outlines(id),
    chapter_number       INT NOT NULL,
    title                TEXT NOT NULL,
    content              TEXT,
    status               chapter_status NOT NULL DEFAULT 'pending',
    editor_notes         TEXT,
    chapter_notes_status notes_status DEFAULT 'pending',
    research_context     TEXT,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(book_id, chapter_number)
);

CREATE INDEX IF NOT EXISTS idx_chapters_book_id ON chapters(book_id);

-- chapter_summaries
CREATE TABLE IF NOT EXISTS chapter_summaries (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    book_id    UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    summary    TEXT NOT NULL,
    version    INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_summaries_book_id     ON chapter_summaries(book_id);
CREATE INDEX IF NOT EXISTS idx_summaries_chapter_id  ON chapter_summaries(chapter_id);

-- notes_logs
CREATE TABLE IF NOT EXISTS notes_logs (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id    UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    chapter_id UUID REFERENCES chapters(id),
    stage      TEXT NOT NULL,
    note_text  TEXT NOT NULL,
    added_by   TEXT DEFAULT 'editor',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notes_book_id ON notes_logs(book_id);

-- updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$ BEGIN
    CREATE TRIGGER trg_books_updated_at
        BEFORE UPDATE ON books FOR EACH ROW EXECUTE FUNCTION update_updated_at();
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TRIGGER trg_outlines_updated_at
        BEFORE UPDATE ON outlines FOR EACH ROW EXECUTE FUNCTION update_updated_at();
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TRIGGER trg_chapters_updated_at
        BEFORE UPDATE ON chapters FOR EACH ROW EXECUTE FUNCTION update_updated_at();
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
