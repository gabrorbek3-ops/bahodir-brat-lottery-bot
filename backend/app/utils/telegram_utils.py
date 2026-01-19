import asyncio
import json
import logging
import urllib.request
import urllib.parse
from typing import Dict, List, Optional, Union

from app.core.config import settings

logger = logging.getLogger(__name__)

class TelegramAPI:
    def __init__(self, token: str) -> None:
        self.token = token
        self.base_url = settings.TELEGRAM_API_BASE.rstrip("/")

    def _build_url(self, method: str) -> str:
        return f"{self.base_url}/bot{self.token}/{method}"

    def _request(self, method: str, params: Optional[Dict] = None) -> Dict:
        url = self._build_url(method)
        if params:
            query = urllib.parse.urlencode(params)
            url = f"{url}?{query}"
        with urllib.request.urlopen(url) as response:
            payload = response.read().decode("utf-8")
        data = json.loads(payload)
        if not data.get("ok"):
            raise RuntimeError(data.get("description", "Telegram API error"))
        return data["result"]

    async def get_me(self) -> Dict:
        return await asyncio.to_thread(self._request, "getMe")

    async def get_chat(self, chat_id: Union[str, int]) -> Dict:
        return await asyncio.to_thread(self._request, "getChat", {"chat_id": chat_id})


def parse_channel_ids(raw: str) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]

async def init_telegram_bot() -> None:
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token is not set")
        return

    api = TelegramAPI(settings.TELEGRAM_BOT_TOKEN)
    try:
        profile = await api.get_me()
        logger.info("Telegram bot connected: %s", profile.get("username"))
    except Exception as exc:
        logger.error("Failed to connect Telegram bot: %s", exc)
