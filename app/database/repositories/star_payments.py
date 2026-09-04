from typing import Any

from app.database.client import get_client

TABLE = "star_payments"


def exists(charge_id: str) -> bool:
    response = (
        get_client()
        .table(TABLE)
        .select("id")
        .eq("charge_id", charge_id)
        .limit(1)
        .execute()
    )
    return bool(response.data)


def total_stars() -> int:
    response = get_client().table(TABLE).select("stars").execute()
    return sum(row["stars"] for row in response.data)


def create(
    telegram_id: int, charge_id: str, stars: int, payload: str | None
) -> dict[str, Any]:
    entry = {
        "telegram_id": telegram_id,
        "charge_id": charge_id,
        "stars": stars,
        "payload": payload,
    }
    response = get_client().table(TABLE).insert(entry).execute()
    return response.data[0]
