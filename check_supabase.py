from book_generator.db.client import get_db

db = get_db()

# Books
books = db.table("books").select("id,title,status,created_at,output_docx").execute().data
print(f"\n=== BOOKS TABLE ({len(books)} rows) ===")
for b in books:
    print(f"  ID     : {b['id']}")
    print(f"  Title  : {b['title']}")
    print(f"  Status : {b['status']}")
    print(f"  Output : {b['output_docx']}")
    print()

# Outlines
outlines = db.table("outlines").select("id,book_id,version,is_active,created_at").execute().data
print(f"=== OUTLINES TABLE ({len(outlines)} rows) ===")
for o in outlines:
    print(f"  ID      : {o['id']}")
    print(f"  Book ID : {o['book_id']}")
    print(f"  Version : {o['version']}  |  Active: {o['is_active']}")
    print()

# Chapters
chapters = db.table("chapters").select("chapter_number,title,status,book_id").order("chapter_number").execute().data
print(f"=== CHAPTERS TABLE ({len(chapters)} rows) ===")
for c in chapters:
    print(f"  Ch {c['chapter_number']:02d}: {c['title']}  [{c['status']}]")

# Summaries
summaries = db.table("chapter_summaries").select("id,chapter_id,version").execute().data
print(f"\n=== CHAPTER_SUMMARIES TABLE ({len(summaries)} rows) ===")
print(f"  {len(summaries)} summaries stored for context chaining")

# Notes log
notes = db.table("notes_logs").select("id,stage,note_text,created_at").execute().data
print(f"\n=== NOTES_LOGS TABLE ({len(notes)} rows) ===")
for n in notes:
    print(f"  Stage: {n['stage']} | Note: {n['note_text'][:60]}...")
