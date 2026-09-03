from datetime import datetime, timezone
from typing import Any

from app.database.client import get_client

TABLE = "complaints"


def create(
    reporter_telegram_id: int,
    target_telegram_id: int,
    target_username: str | None,
    target_photo_file_id: str | None,
    reason: str,
) -> dict[str, Any]:
    payload = {
        "reporter_telegram_id": reporter_telegram_id,
        "target_telegram_id": target_telegram_id,
        "target_username": target_username,
        "target_photo_file_id": target_photo_file_id,
        "reason": reason,
    }
    response = get_client().table(TABLE).insert(payload).execute()
    return response.data[0]


def open_for_target(
    reporter_telegram_id: int, target_telegram_id: int
) -> dict[str, Any] | None:
    response = (
        get_client()
        .table(TABLE)
        .select("id")
        .eq("reporter_telegram_id", reporter_telegram_id)
        .eq("target_telegram_id", target_telegram_id)
        .eq("status", "open")
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def list_open() -> list[dict[str, Any]]:
    response = (
        get_client()
        .table(TABLE)
        .select("*")
        .eq("status", "open")
        .order("created_at", desc=False)
        .execute()
    )
    return response.data


def count_open() -> int:
    response = (
        get_client()
        .table(TABLE)
        .select("id", count="exact")
        .eq("status", "open")
        .execute()
    )
    return response.count or 0


def resolve(complaint_id: int, status: str, admin_id: int) -> dict[str, Any]:
    payload = {
        "status": status,
        "resolved_by": admin_id,
        "resolved_at": datetime.now(timezone.utc).isoformat(),
    }
    response = (
        get_client().table(TABLE).update(payload).eq("id", complaint_id).execute()
    )
    return response.data[0]
