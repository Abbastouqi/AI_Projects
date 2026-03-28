# Sample Excel Input Format

The Excel file (or Google Sheet) must have these columns:

| title                        | notes_on_outline_before                          | status_outline_notes |
|------------------------------|--------------------------------------------------|----------------------|
| The Future of AI             | Focus on ethics, include real-world case studies | no_notes_needed      |
| Mastering Python             | Start with basics, end with advanced patterns    | yes                  |

- `title` — required
- `notes_on_outline_before` — editor guidance for the LLM before outline generation
- `status_outline_notes` — `yes` (editor will review outline) or `no_notes_needed` (auto-proceed)
