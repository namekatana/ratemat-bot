import asyncio
from typing import Any

from app.database.repositories import users as repo


async def pending_queue() -> list[dict[str, Any]]:
    return await asyncio.to_thread(repo.list_pending_review)


async def pending_count() -> int:
    return await asyncio.to_thread(repo.count_by_status, "pending_review")


async def approve(telegram_id: int) -> dict[str, Any]:
    return await asyncio.to_thread(repo.set_status, telegram_id, "verified")


async def reject(telegram_id: int) -> dict[str, Any]:
    return await asyncio.to_thread(repo.set_status, telegram_id, "rejected")
