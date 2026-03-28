"""Notification system: Email (SMTP) + MS Teams Webhook."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import httpx
from book_generator.core.config import get_settings
from book_generator.core.logger import logger

# ── Event types ───────────────────────────────────────────────
OUTLINE_READY = "outline_ready"
WAITING_CHAPTER_NOTES = "waiting_chapter_notes"
FINAL_DRAFT_COMPLETED = "final_draft_completed"
WORKFLOW_PAUSED = "workflow_paused"
WORKFLOW_ERROR = "workflow_error"

_SUBJECTS = {
    OUTLINE_READY: "📘 Book Outline Ready for Review",
    WAITING_CHAPTER_NOTES: "✏️ Chapter Awaiting Your Notes",
    FINAL_DRAFT_COMPLETED: "✅ Final Book Draft Completed",
    WORKFLOW_PAUSED: "⏸️ Book Workflow Paused",
    WORKFLOW_ERROR: "❌ Book Workflow Error",
}


def _build_body(event: str, context: dict) -> str:
    lines = [f"Event: {event}"]
    for k, v in context.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)


def send_email(event: str, context: dict) -> None:
    s = get_settings()
    if not s.smtp_user or not s.notify_email:
        logger.warning("Email not configured — skipping email notification")
        return
    subject = _SUBJECTS.get(event, f"Book Generator: {event}")
    body = _build_body(event, context)
    msg = MIMEMultipart()
    msg["From"] = s.smtp_user
    msg["To"] = s.notify_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(s.smtp_host, s.smtp_port) as server:
            server.starttls()
            server.login(s.smtp_user, s.smtp_pass)
            server.sendmail(s.smtp_user, s.notify_email, msg.as_string())
        logger.info(f"Email sent: {subject}")
    except Exception as e:
        logger.error(f"Email send failed: {e}")


def send_teams(event: str, context: dict) -> None:
    s = get_settings()
    if not s.teams_webhook_url:
        logger.warning("Teams webhook not configured — skipping")
        return
    subject = _SUBJECTS.get(event, event)
    facts = [{"name": k, "value": str(v)} for k, v in context.items()]
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": subject,
        "sections": [{
            "activityTitle": subject,
            "facts": facts,
            "markdown": True,
        }],
    }
    try:
        resp = httpx.post(s.teams_webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info(f"Teams notification sent: {subject}")
    except Exception as e:
        logger.error(f"Teams notification failed: {e}")


def notify(event: str, context: dict) -> None:
    """Send both email and Teams notifications."""
    send_email(event, context)
    send_teams(event, context)
