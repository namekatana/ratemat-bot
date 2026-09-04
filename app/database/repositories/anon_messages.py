from typing import Any, Optional

from app.database.client import get_client

MESSAGES = "anon_messages"
BLOCKS = "anon_blocks"


def create(
    sender_telegram_id: int, target_telegram_id: int, body: str
) -> dict[str, Any]:
    payload = {
        "sender_telegram_id": sender_telegram_id,
        "target_telegram_id": target_telegram_id,
        "body": body,
    }
    response = get_client().table(MESSAGES).insert(payload).execute()
    return response.data[0]


def get(message_id: int) -> Optional[dict[str, Any]]:
    response = (
        get_client()
        .table(MESSAGES)
        .select("*")
        .eq("id", message_id)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def count_recent(sender_telegram_id: int, since_iso: str) -> int:
    response = (
        get_client()
        .table(MESSAGES)
        .select("id", count="exact")
        .eq("sender_telegram_id", sender_telegram_id)
        .gte("created_at", since_iso)
        .execute()
    )
    return response.count or 0


def is_blocked(blocker_telegram_id: int, blocked_telegram_id: int) -> bool:
    response = (
        get_client()
        .table(BLOCKS)
        .select("blocker_telegram_id")
        .eq("blocker_telegram_id", blocker_telegram_id)
        .eq("blocked_telegram_id", blocked_telegram_id)
        .limit(1)
        .execute()
    )
    return bool(response.data)


def add_block(blocker_telegram_id: int, blocked_telegram_id: int) -> None:
    payload = {
        "blocker_telegram_id": blocker_telegram_id,
        "blocked_telegram_id": blocked_telegram_id,
    }
    (
        get_client()
        .table(BLOCKS)
        .upsert(
            payload,
            on_conflict="blocker_telegram_id,blocked_telegram_id",
            ignore_duplicates=True,
        )
        .execute()
    )
