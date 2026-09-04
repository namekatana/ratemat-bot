from typing import Any

from app.database.client import get_client

TABLE = "profile_ratings"


def upsert_score(
    rater_telegram_id: int, target_telegram_id: int, score: int
) -> dict[str, Any]:
    payload = {
        "rater_telegram_id": rater_telegram_id,
        "target_telegram_id": target_telegram_id,
        "score": score,
    }
    response = (
        get_client()
        .table(TABLE)
        .upsert(payload, on_conflict="rater_telegram_id,target_telegram_id")
        .execute()
    )
    return response.data[0]


def list_rated_by(rater_telegram_id: int) -> list[dict[str, Any]]:
    response = (
        get_client()
        .table(TABLE)
        .select("target_telegram_id, score, updated_at")
        .eq("rater_telegram_id", rater_telegram_id)
        .order("updated_at", desc=False)
        .execute()
    )
    return response.data


def list_raters_of(target_telegram_id: int) -> list[dict[str, Any]]:
    response = (
        get_client()
        .table(TABLE)
        .select("rater_telegram_id, score, updated_at")
        .eq("target_telegram_id", target_telegram_id)
        .order("updated_at", desc=True)
        .execute()
    )
    return response.data


def score_for(rater_telegram_id: int, target_telegram_id: int) -> int | None:
    response = (
        get_client()
        .table(TABLE)
        .select("score")
        .eq("rater_telegram_id", rater_telegram_id)
        .eq("target_telegram_id", target_telegram_id)
        .limit(1)
        .execute()
    )
    return response.data[0]["score"] if response.data else None


def aggregate_for(target_telegram_id: int) -> tuple[int, float]:
    response = (
        get_client()
        .table(TABLE)
        .select("score")
        .eq("target_telegram_id", target_telegram_id)
        .execute()
    )
    scores = [row["score"] for row in response.data]
    if not scores:
        return 0, 0.0
    return len(scores), sum(scores) / len(scores)
