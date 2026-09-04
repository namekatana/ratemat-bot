import asyncio
from typing import Any, Optional

from app.database.repositories import profile_ratings as ratings_repo
from app.database.repositories import profiles as repo
from app.database.repositories import users as users_repo

_FRESH_BATCH = 25


def _prefer_premium(
    profiles: list[dict[str, Any]]
) -> tuple[dict[str, Any], bool]:
    ids = [item["telegram_id"] for item in profiles]
    premium_ids = set(users_repo.list_premium_ids(ids))
    for item in profiles:
        if item["telegram_id"] in premium_ids:
            return item, True
    return profiles[0], profiles[0]["telegram_id"] in premium_ids


def _next_candidate(viewer_telegram_id: int) -> Optional[dict[str, Any]]:
    rated = ratings_repo.list_rated_by(viewer_telegram_id)
    rated_ids = [row["target_telegram_id"] for row in rated]
    fresh = repo.list_active_excluding(
        viewer_telegram_id, rated_ids, limit=_FRESH_BATCH
    )
    if fresh:
        profile, is_premium = _prefer_premium(fresh)
        return {
            "profile": profile,
            "previous_score": None,
            "is_premium": is_premium,
        }
    if not rated_ids:
        return None
    ordered = repo.list_active_by_ids(rated_ids)
    by_id = {item["telegram_id"]: item for item in ordered}
    score_by_id = {row["target_telegram_id"]: row["score"] for row in rated}
    for target_id in rated_ids:
        profile = by_id.get(target_id)
        if profile:
            is_premium = bool(users_repo.list_premium_ids([target_id]))
            return {
                "profile": profile,
                "previous_score": score_by_id.get(target_id),
                "is_premium": is_premium,
            }
    return None


async def next_candidate(viewer_telegram_id: int) -> Optional[dict[str, Any]]:
    return await asyncio.to_thread(_next_candidate, viewer_telegram_id)


async def rate(
    rater_telegram_id: int, target_telegram_id: int, score: int
) -> None:
    await asyncio.to_thread(
        ratings_repo.upsert_score, rater_telegram_id, target_telegram_id, score
    )
