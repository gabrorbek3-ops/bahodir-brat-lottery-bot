from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "bahodir_brat_lottery",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    beat_schedule={
        "check-telegram-connection": {
            "task": "app.tasks.telegram_tasks.check_telegram_connection",
            "schedule": 300.0,
        },
        "sync-telegram-channels": {
            "task": "app.tasks.telegram_tasks.sync_telegram_channels",
            "schedule": 600.0,
        },
    },
)


def create_celery() -> Celery:
    celery_app.autodiscover_tasks(["app.tasks"])
    return celery_app
