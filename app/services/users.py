import asyncio
from typing import Any

from aiogram.types import User

from app.database.repositories import users as repo


class VerificationStatus:
    PENDING_START = "pending_start"
    AWAITING_VIDEO = "awaiting_video"
    PENDING_REVIEW = "pending_review"


async def register_user(user: User) -> dict[str, Any]:
    return await asyncio.to_thread(
        repo.upsert_user,
        user.id,
        user.username,
        user.first_name,
        user.last_name,
    )


async def mark_awaiting_video(telegram_id: int) -> dict[str, Any]:
    return await asyncio.to_thread(
        repo.set_status, telegram_id, VerificationStatus.AWAITING_VIDEO
    )


async def store_verification_note(telegram_id: int, file_id: str) -> dict[str, Any]:
    return await asyncio.to_thread(
        repo.set_verification_note,
        telegram_id,
        file_id,
        VerificationStatus.PENDING_REVIEW,
    )
