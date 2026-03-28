"""All LLM prompt templates in one place."""

GENERATE_OUTLINE = """
You are an expert book author and editor.

Generate a detailed book outline for the following:
Title: {title}
Editor Notes: {notes_on_outline_before}

Instructions:
- Create 8–12 chapters
- Each chapter must have a title, a 2-3 sentence summary, and 3-5 subtopics
- Follow editor notes strictly
- Return ONLY valid JSON, no markdown fences

Return format:
{{
  "chapters": [
    {{
      "title": "...",
      "summary": "...",
      "subtopics": ["...", "..."]
    }}
  ]
}}
""".strip()

IMPROVE_OUTLINE = """
You are an expert book editor.

Improve the following book outline based on editor feedback.

Original Outline:
{outline}

Editor Notes:
{notes_on_outline_after}

Return the improved version in the exact same JSON format. Return ONLY valid JSON.
""".strip()

GENERATE_CHAPTER = """
You are a professional book author writing in an engaging, authoritative tone.

Book Title: {title}
Chapter Title: {chapter_title}
Chapter Number: {chapter_number}

Context — Previous Chapter Summaries:
{summaries}

{research_block}

Instructions:
- Maintain narrative continuity with previous chapters
- Avoid repeating content already covered
- Expand deeply and thoroughly on this chapter's topic
- Use an engaging, readable tone suitable for a general audience
- Write at least 800 words

Return a JSON object:
{{
  "content": "<full chapter text>",
  "summary": "<3-5 line summary of this chapter>"
}}
Return ONLY valid JSON.
""".strip()

SUMMARIZE_CHAPTER = """
Summarize the following book chapter in 3–5 concise lines.
Focus on: key ideas and the flow of narrative.

Chapter:
{chapter_text}

Return ONLY the summary text, no JSON.
""".strip()

IMPROVE_CHAPTER = """
You are a professional book editor.

Improve the following chapter based on editor notes.

Chapter:
{chapter_text}

Editor Notes:
{chapter_notes}

Return a JSON object:
{{
  "content": "<improved chapter text>",
  "summary": "<updated 3-5 line summary>"
}}
Return ONLY valid JSON.
""".strip()

RESEARCH_BLOCK_TEMPLATE = """
Research Context (use ONLY the following sources, do not fabricate):
{summaries}
""".strip()
