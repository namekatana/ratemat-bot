from typing import Iterable

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message


async def delete_messages(
    bot: Bot, chat_id: int, message_ids: Iterable[int]
) -> None:
    for message_id in message_ids:
        try:
            await bot.delete_message(chat_id, message_id)
        except TelegramAPIError:
            pass


async def delete_message(message: Message) -> None:
    try:
        await message.delete()
    except TelegramAPIError:
        pass
