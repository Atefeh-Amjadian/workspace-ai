import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_telegram_message(message: str) -> bool:
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"

    payload = {
        "chat_id": settings.telegram_chat_id,
        "text": message,
    }

    try:
        response = httpx.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return True

    except httpx.HTTPError as error:
        logger.error("Telegram message failed: %s", error)
        return False