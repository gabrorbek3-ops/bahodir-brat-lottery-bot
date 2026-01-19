from datetime import datetime
import logging

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.channel import Channel
from app.utils.telegram_utils import TelegramAPI, parse_channel_ids
from app.tasks.celery import celery_app

logger = logging.getLogger(__name__)
@celery_app.task(name="app.tasks.telegram_tasks.check_telegram_connection")
def check_telegram_connection():
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token not configured")
        return {"status": "skipped"}

    api = TelegramAPI(settings.TELEGRAM_BOT_TOKEN)
    try:
        profile = api._request("getMe")
        logger.info("Telegram bot connected: %s", profile.get("username"))
        return {"status": "ok", "username": profile.get("username")}
    except Exception as exc:
        logger.error("Telegram bot connection failed: %s", exc)
        return {"status": "error", "error": str(exc)}

@celery_app.task(name="app.tasks.telegram_tasks.sync_telegram_channels")
def sync_telegram_channels():
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token not configured")
        return {"status": "skipped"}

    channel_ids = parse_channel_ids(settings.TELEGRAM_CHANNEL_IDS)
    if not channel_ids:
        logger.info("No channel IDs configured for sync")
        return {"status": "skipped"}

    api = TelegramAPI(settings.TELEGRAM_BOT_TOKEN)
    db = SessionLocal()
    synced = 0
    try:
        for channel_id in channel_ids:
            info = api._request("getChat", {"chat_id": channel_id})
            channel = db.query(Channel).filter(Channel.telegram_id == str(channel_id)).first()
            if not channel:
                channel = Channel(telegram_id=str(channel_id))
                db.add(channel)

            channel.title = info.get("title") or channel.title
            channel.username = info.get("username") or channel.username
            channel.is_active = True
            channel.last_synced_at = datetime.utcnow()
            synced += 1
        db.commit()
    except Exception as exc:
        logger.error("Channel sync failed: %s", exc)
        db.rollback()
        return {"status": "error", "error": str(exc)}
    finally:
        db.close()

    return {"status": "ok", "synced": synced}
