import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from app.database.repositories import complaints as repo
from app.database.repositories import profiles as profiles_repo
from app.database.repositories import users as users_repo
from app.texts import admin as admin_texts

REASON_MIN, REASON_MAX = 3, 500
SHADOW_THRESHOLD = 5
SHADOW_WINDOW = timedelta(hours=24)


def validate_reason(raw: str) -> Optional[str]:
    value = raw.strip()
    if not REASON_MIN <= len(value) <= REASON_MAX:
        return None
    return value


def _is_blocked(target_user: Optional[dict[str, Any]]) -> bool:
    if not target_user:
        return False
    return (
        target_user.get("verification_status") == "banned"
        or bool(target_user.get("shadow_banned_at"))
    )


def _maybe_shadow_ban(
    target_telegram_id: int,
    username: Optional[str],
    photo_file_id: Optional[str],
) -> None:
    since = (datetime.now(timezone.utc) - SHADOW_WINDOW).isoformat()
    reporters = repo.count_recent_reporters(target_telegram_id, since)
    if reporters < SHADOW_THRESHOLD:
        return
    if repo.has_open_auto_shadow(target_telegram_id):
        return
    users_repo.set_shadow_ban(target_telegram_id)
    profiles_repo.set_active(target_telegram_id, False)
    repo.create_auto_shadow(
        target_telegram_id,
        username,
        photo_file_id,
        admin_texts.auto_shadow_reason(reporters),
    )


def _submit(
    reporter_telegram_id: int, target_telegram_id: int, reason: str
) -> None:
    if repo.open_for_target(reporter_telegram_id, target_telegram_id):
        return
    target_user = users_repo.get_by_telegram_id(target_telegram_id)
    if _is_blocked(target_user):
        return
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
    _maybe_shadow_ban(target_telegram_id, username, photo_file_id)


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
    if not target_telegram_id:
        await asyncio.to_thread(repo.delete, complaint_id)
        return
    await asyncio.to_thread(users_repo.set_status, target_telegram_id, "banned")
    await asyncio.to_thread(profiles_repo.set_active, target_telegram_id, False)
    await asyncio.to_thread(repo.delete_for_target, target_telegram_id)


async def restore(
    complaint_id: int, target_telegram_id: int, admin_id: int
) -> None:
    if not target_telegram_id:
        await asyncio.to_thread(repo.delete, complaint_id)
        return
    await asyncio.to_thread(users_repo.clear_shadow_ban, target_telegram_id)
    await asyncio.to_thread(profiles_repo.set_active, target_telegram_id, True)
    await asyncio.to_thread(repo.delete_for_target, target_telegram_id)


async def dismiss(complaint_id: int, admin_id: int) -> None:
    await asyncio.to_thread(repo.delete, complaint_id)
