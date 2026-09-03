import asyncio
from typing import Any, Optional

from app.database.repositories import profile_ratings as ratings_repo
from app.database.repositories import profiles as repo


def _next_candidate(viewer_telegram_id: int) -> Optional[dict[str, Any]]:
    rated = ratings_repo.list_rated_by(viewer_telegram_id)
    rated_ids = [row["target_telegram_id"] for row in rated]
    fresh = repo.list_active_excluding(viewer_telegram_id, rated_ids, limit=1)
    if fresh:
        return {"profile": fresh[0], "previous_score": None}
    if not rated_ids:
        return None
    ordered = repo.list_active_by_ids(rated_ids)
    by_id = {item["telegram_id"]: item for item in ordered}
    score_by_id = {row["target_telegram_id"]: row["score"] for row in rated}
    for target_id in rated_ids:
        profile = by_id.get(target_id)
        if profile:
            return {"profile": profile, "previous_score": score_by_id.get(target_id)}
    return None


async def next_candidate(viewer_telegram_id: int) -> Optional[dict[str, Any]]:
    return await asyncio.to_thread(_next_candidate, viewer_telegram_id)


async def rate(
    rater_telegram_id: int, target_telegram_id: int, score: int
) -> None:
    await asyncio.to_thread(
        ratings_repo.upsert_score, rater_telegram_id, target_telegram_id, score
    )
