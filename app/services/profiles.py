import asyncio
from typing import Any, Optional

from app.database.repositories import profile_ratings as ratings_repo
from app.database.repositories import profiles as repo
from app.database.repositories import users as users_repo

NAME_MIN, NAME_MAX = 2, 32
AGE_MIN, AGE_MAX = 18, 99
DESCRIPTION_MIN, DESCRIPTION_MAX = 10, 500

GENDER_MALE = "male"
GENDER_FEMALE = "female"


def validate_name(raw: str) -> Optional[str]:
    value = raw.strip()
    if "\n" in value:
        return None
    if not NAME_MIN <= len(value) <= NAME_MAX:
        return None
    return value


def validate_age(raw: str) -> Optional[int]:
    value = raw.strip()
    if not value.isdigit():
        return None
    age = int(value)
    if not AGE_MIN <= age <= AGE_MAX:
        return None
    return age


def validate_description(raw: str) -> Optional[str]:
    value = raw.strip()
    if not DESCRIPTION_MIN <= len(value) <= DESCRIPTION_MAX:
        return None
    return value


async def get_profile(telegram_id: int) -> Optional[dict[str, Any]]:
    return await asyncio.to_thread(repo.get_by_telegram_id, telegram_id)


async def has_profile(telegram_id: int) -> bool:
    return await get_profile(telegram_id) is not None


async def save_profile(
    telegram_id: int,
    name: str,
    age: int,
    gender: str,
    photo_file_id: str,
    description: str,
) -> dict[str, Any]:
    profile = await asyncio.to_thread(
        repo.upsert, telegram_id, name, age, gender, photo_file_id, description
    )
    user = await asyncio.to_thread(users_repo.get_by_telegram_id, telegram_id)
    if user and user.get("shadow_banned_at"):
        await asyncio.to_thread(repo.set_active, telegram_id, False)
    return profile


async def rating_summary(telegram_id: int) -> tuple[int, float]:
    return await asyncio.to_thread(ratings_repo.aggregate_for, telegram_id)


_RATERS_LIMIT = 50


def _raters_detail(telegram_id: int) -> list[dict[str, Any]]:
    rows = ratings_repo.list_raters_of(telegram_id)[:_RATERS_LIMIT]
    ids = [row["rater_telegram_id"] for row in rows]
    by_id = {user["telegram_id"]: user for user in users_repo.list_by_ids(ids)}
    return [
        {
            "username": by_id.get(row["rater_telegram_id"], {}).get("username"),
            "score": row["score"],
        }
        for row in rows
    ]


async def raters_detail(telegram_id: int) -> list[dict[str, Any]]:
    return await asyncio.to_thread(_raters_detail, telegram_id)
