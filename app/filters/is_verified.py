import asyncio
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from app.database.repositories import users as users_repo


class IsVerified(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        if event.from_user is None:
            return False
        user = await asyncio.to_thread(
            users_repo.get_by_telegram_id, event.from_user.id
        )
        return bool(user) and user["verification_status"] == "verified"
