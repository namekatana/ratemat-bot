from typing import Any, Optional

from app.database.client import get_client

TABLE = "profiles"


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


def upsert(
    telegram_id: int,
    name: str,
    age: int,
    gender: str,
    photo_file_id: str,
    description: str,
) -> dict[str, Any]:
    payload = {
        "telegram_id": telegram_id,
        "name": name,
        "age": age,
        "gender": gender,
        "photo_file_id": photo_file_id,
        "description": description,
        "is_active": True,
    }
    response = (
        get_client()
        .table(TABLE)
        .upsert(payload, on_conflict="telegram_id", ignore_duplicates=False)
        .execute()
    )
    return response.data[0]


def list_active_excluding(
    telegram_id: int, excluded_ids: list[int], limit: int
) -> list[dict[str, Any]]:
    blocked = list({telegram_id, *excluded_ids})
    response = (
        get_client()
        .table(TABLE)
        .select("*")
        .eq("is_active", True)
        .not_.in_("telegram_id", blocked)
        .order("created_at", desc=False)
        .limit(limit)
        .execute()
    )
    return response.data


def list_active_by_ids(telegram_ids: list[int]) -> list[dict[str, Any]]:
    if not telegram_ids:
        return []
    response = (
        get_client()
        .table(TABLE)
        .select("*")
        .eq("is_active", True)
        .in_("telegram_id", telegram_ids)
        .execute()
    )
    return response.data
