from celery import Celery
from book_generator.core.config import get_settings

celery_app = Celery(
    "book_generator",
    broker=get_settings().redis_url,
    backend=get_settings().redis_url,
    include=["book_generator.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    task_track_started=True,
    task_acks_late=True,
)
