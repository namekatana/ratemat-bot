import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.database.repositories import anon_messages as repo
from app.database.repositories import complaints as complaints_repo
from app.database.repositories import profiles as profiles_repo
from app.database.repositories import users as users_repo
from app.texts import admin as admin_texts

BODY_MIN, BODY_MAX = 1, 500
DAILY_LIMIT = 5
WINDOW = timedelta(hours=24)

RESULT_SENT = "sent"
RESULT_BLOCKED = "blocked"
RESULT_LIMIT = "limit"
RESULT_SELF = "self"


def validate_body(raw: str) -> Optional[str]:
    value = raw.strip()
    if not BODY_MIN <= len(value) <= BODY_MAX:
        return None
    return value


def _send(
    sender_id: int, target_id: int, body: str
) -> tuple[str, Optional[int]]:
    if sender_id == target_id:
        return RESULT_SELF, None
    if repo.is_blocked(target_id, sender_id):
        return RESULT_BLOCKED, None
    since = (datetime.now(timezone.utc) - WINDOW).isoformat()
    if repo.count_recent(sender_id, since) >= DAILY_LIMIT:
        return RESULT_LIMIT, None
    row = repo.create(sender_id, target_id, body)
    return RESULT_SENT, row["id"]


async def send(
    sender_id: int, target_id: int, body: str
) -> tuple[str, Optional[int]]:
    return await asyncio.to_thread(_send, sender_id, target_id, body)


def _block(message_id: int, blocker_id: int) -> bool:
    row = repo.get(message_id)
    if not row or row["target_telegram_id"] != blocker_id:
        return False
    repo.add_block(blocker_id, row["sender_telegram_id"])
    return True


async def block(message_id: int, blocker_id: int) -> bool:
    return await asyncio.to_thread(_block, message_id, blocker_id)


def _report(message_id: int, reporter_id: int) -> bool:
    row = repo.get(message_id)
    if not row or row["target_telegram_id"] != reporter_id:
        return False
    sender_id = row["sender_telegram_id"]
    if complaints_repo.open_for_target(reporter_id, sender_id):
        return True
    sender = users_repo.get_by_telegram_id(sender_id)
    profile = profiles_repo.get_by_telegram_id(sender_id)
    complaints_repo.create(
        reporter_id,
        sender_id,
        sender.get("username") if sender else None,
        profile.get("photo_file_id") if profile else None,
        admin_texts.anon_complaint_reason(row["body"]),
    )
    return True


async def report(message_id: int, reporter_id: int) -> bool:
    return await asyncio.to_thread(_report, message_id, reporter_id)
