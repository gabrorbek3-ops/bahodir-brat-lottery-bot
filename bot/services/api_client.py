import asyncio
import json
import urllib.request
from typing import Any, Dict, List, Optional

from bot.config import settings

class APIClient:
    @staticmethod
    async def _request(path: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{settings.API_URL.rstrip('/')}{path}"
        data = None
        headers = {"Content-Type": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=data, headers=headers, method=method)

        def _do_request():
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode("utf-8"))

        return await asyncio.to_thread(_do_request)

    @classmethod
    async def get_tickets(cls) -> List[Dict[str, Any]]:
        return await cls._request("/tickets")

    @classmethod
    async def get_payment_card(cls) -> Dict[str, Any]:
        return await cls._request("/payment-card")

    @classmethod
    async def get_winners(cls, limit: int = 10) -> List[Dict[str, Any]]:
        return await cls._request(f"/winners?limit={limit}")

    @classmethod
    async def upsert_telegram_user(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await cls._request("/users/telegram", method="POST", payload=payload)
