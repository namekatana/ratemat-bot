from datetime import datetime, timezone
from typing import Any, Optional

from app.database.client import get_client

TABLE = "users"


def get_by_telegram_id(telegram_id: int) -> Optional[dict[str, Any]]:
    response = (
        get_client()
        .table(TABLE)
        .select("*")
        .eq("telegram_id", telegram_id)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def list_pending_review() -> list[dict[str, Any]]:
    response = (
        get_client()
        .table(TABLE)
        .select("*")
        .eq("verification_status", "pending_review")
        .order("updated_at", desc=False)
        .execute()
    )
    return response.data


def count_by_status(status: str) -> int:
    response = (
        get_client()
        .table(TABLE)
        .select("id", count="exact")
        .eq("verification_status", status)
        .execute()
    )
    return response.count or 0


def count_all() -> int:
    response = get_client().table(TABLE).select("id", count="exact").execute()
    return response.count or 0


def count_created_since(iso_timestamp: str) -> int:
    response = (
        get_client()
        .table(TABLE)
        .select("id", count="exact")
        .gte("created_at", iso_timestamp)
        .execute()
    )
    return response.count or 0


def upsert_user(
    telegram_id: int,
    username: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
) -> dict[str, Any]:
    payload = {
        "telegram_id": telegram_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    response = (
        get_client()
        .table(TABLE)
        .upsert(payload, on_conflict="telegram_id", ignore_duplicates=False)
        .execute()
    )
    return response.data[0]


def set_status(telegram_id: int, status: str) -> dict[str, Any]:
    response = (
        get_client()
        .table(TABLE)
        .update({"verification_status": status})
        .eq("telegram_id", telegram_id)
        .execute()
    )
    return response.data[0]


def set_shadow_ban(telegram_id: int) -> dict[str, Any]:
    response = (
        get_client()
        .table(TABLE)
        .update({"shadow_banned_at": datetime.now(timezone.utc).isoformat()})
        .eq("telegram_id", telegram_id)
        .execute()
    )
    return response.data[0]


def clear_shadow_ban(telegram_id: int) -> dict[str, Any]:
    response = (
        get_client()
        .table(TABLE)
        .update({"shadow_banned_at": None})
        .eq("telegram_id", telegram_id)
        .execute()
    )
    return response.data[0]


def count_shadow_banned() -> int:
    response = (
        get_client()
        .table(TABLE)
        .select("id", count="exact")
        .not_.is_("shadow_banned_at", "null")
        .execute()
    )
    return response.count or 0


def list_by_ids(telegram_ids: list[int]) -> list[dict[str, Any]]:
    if not telegram_ids:
        return []
    response = (
        get_client()
        .table(TABLE)
        .select("telegram_id, username")
        .in_("telegram_id", telegram_ids)
        .execute()
    )
    return response.data


def list_premium_ids(telegram_ids: list[int]) -> list[int]:
    if not telegram_ids:
        return []
    now = datetime.now(timezone.utc).isoformat()
    response = (
        get_client()
        .table(TABLE)
        .select("telegram_id")
        .in_("telegram_id", telegram_ids)
        .gt("premium_until", now)
        .execute()
    )
    return [row["telegram_id"] for row in response.data]


def count_premium() -> int:
    now = datetime.now(timezone.utc).isoformat()
    response = (
        get_client()
        .table(TABLE)
        .select("id", count="exact")
        .gt("premium_until", now)
        .execute()
    )
    return response.count or 0


def set_premium_until(telegram_id: int, until_iso: str) -> dict[str, Any]:
    response = (
        get_client()
        .table(TABLE)
        .update({"premium_until": until_iso})
        .eq("telegram_id", telegram_id)
        .execute()
    )
    return response.data[0]


def set_verification_note(telegram_id: int, file_id: str, status: str) -> dict[str, Any]:
    response = (
        get_client()
        .table(TABLE)
        .update({"verification_file_id": file_id, "verification_status": status})
        .eq("telegram_id", telegram_id)
        .execute()
    )
    return response.data[0]
