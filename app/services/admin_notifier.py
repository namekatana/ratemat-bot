import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from app.services.admins import get_admin_ids
from app.services.verification_review import pending_count
from app.texts import admin as texts

_POLL_SECONDS = 60
logger = logging.getLogger(__name__)


async def _broadcast(bot: Bot, text: str) -> None:
    for admin_id in await get_admin_ids():
        try:
            await bot.send_message(admin_id, text)
        except TelegramAPIError:
            logger.warning("Failed to notify admin %s", admin_id)


async def run_admin_notifier(bot: Bot) -> None:
    try:
        previous = await pending_count()
    except Exception:
        previous = 0
    while True:
        await asyncio.sleep(_POLL_SECONDS)
        try:
            current = await pending_count()
        except Exception:
            continue
        if previous == 0 and current > 0:
            await _broadcast(bot, texts.queue_alert(current))
        previous = current
