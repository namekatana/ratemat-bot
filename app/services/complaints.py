import asyncio
from typing import Any, Optional

from app.database.repositories import complaints as repo
from app.database.repositories import profiles as profiles_repo
from app.database.repositories import users as users_repo

REASON_MIN, REASON_MAX = 3, 500


def validate_reason(raw: str) -> Optional[str]:
    value = raw.strip()
    if not REASON_MIN <= len(value) <= REASON_MAX:
        return None
    return value


def _submit(
    reporter_telegram_id: int, target_telegram_id: int, reason: str
) -> None:
    if repo.open_for_target(reporter_telegram_id, target_telegram_id):
        return
    target_user = users_repo.get_by_telegram_id(target_telegram_id)
    target_profile = profiles_repo.get_by_telegram_id(target_telegram_id)
    username = target_user.get("username") if target_user else None
    photo_file_id = (
        target_profile.get("photo_file_id") if target_profile else None
    )
    repo.create(
        reporter_telegram_id,
        target_telegram_id,
        username,
        photo_file_id,
        reason,
    )


async def submit(
    reporter_telegram_id: int, target_telegram_id: int, reason: str
) -> None:
    await asyncio.to_thread(
        _submit, reporter_telegram_id, target_telegram_id, reason
    )


async def open_queue() -> list[dict[str, Any]]:
    return await asyncio.to_thread(repo.list_open)


async def open_count() -> int:
    return await asyncio.to_thread(repo.count_open)


async def ban(complaint_id: int, target_telegram_id: int, admin_id: int) -> None:
    await asyncio.to_thread(repo.resolve, complaint_id, "resolved_ban", admin_id)
    if target_telegram_id:
        await asyncio.to_thread(
            users_repo.set_status, target_telegram_id, "banned"
        )


async def dismiss(complaint_id: int, admin_id: int) -> None:
    await asyncio.to_thread(repo.resolve, complaint_id, "resolved_dismiss", admin_id)
