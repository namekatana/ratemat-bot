import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.database.repositories import star_payments as payments_repo
from app.database.repositories import users as users_repo

PREMIUM_STARS = 98
PREMIUM_DAYS = 30
PREMIUM_PAYLOAD = "premium_30d"


def _parse(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value)


def _current_until(telegram_id: int) -> Optional[datetime]:
    user = users_repo.get_by_telegram_id(telegram_id)
    until = _parse(user.get("premium_until")) if user else None
    if until and until > datetime.now(timezone.utc):
        return until
    return None


def _activate(
    telegram_id: int, charge_id: str, stars: int, payload: Optional[str]
) -> datetime:
    now = datetime.now(timezone.utc)
    if payments_repo.exists(charge_id):
        return _current_until(telegram_id) or now
    payments_repo.create(telegram_id, charge_id, stars, payload)
    base = _current_until(telegram_id) or now
    until = base + timedelta(days=PREMIUM_DAYS)
    users_repo.set_premium_until(telegram_id, until.isoformat())
    return until


async def status(telegram_id: int) -> Optional[datetime]:
    return await asyncio.to_thread(_current_until, telegram_id)


async def activate(
    telegram_id: int, charge_id: str, stars: int, payload: Optional[str]
) -> datetime:
    return await asyncio.to_thread(
        _activate, telegram_id, charge_id, stars, payload
    )
