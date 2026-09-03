import asyncio
import time

from app.database.repositories import admins as repo

_CACHE_TTL_SECONDS = 60
_cache: dict[str, object] = {"ids": frozenset(), "fetched_at": 0.0}


async def get_admin_ids() -> frozenset[int]:
    now = time.monotonic()
    if now - float(_cache["fetched_at"]) > _CACHE_TTL_SECONDS:
        ids = await asyncio.to_thread(repo.list_admin_ids)
        _cache["ids"] = frozenset(ids)
        _cache["fetched_at"] = now
    return _cache["ids"]  # type: ignore[return-value]


async def is_admin(telegram_id: int) -> bool:
    return telegram_id in await get_admin_ids()
