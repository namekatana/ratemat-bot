import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

from app.database.repositories import complaints as complaints_repo
from app.database.repositories import users as users_repo

_STATUSES = (
    "pending_start",
    "awaiting_video",
    "pending_review",
    "verified",
    "rejected",
    "banned",
)


def _collect() -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    day_ago = (now - timedelta(days=1)).isoformat()
    week_ago = (now - timedelta(days=7)).isoformat()
    return {
        "total": users_repo.count_all(),
        "by_status": {s: users_repo.count_by_status(s) for s in _STATUSES},
        "shadow_banned": users_repo.count_shadow_banned(),
        "open_complaints": complaints_repo.count_open(),
        "new_24h": users_repo.count_created_since(day_ago),
        "new_7d": users_repo.count_created_since(week_ago),
    }


async def build_report() -> dict[str, Any]:
    return await asyncio.to_thread(_collect)
