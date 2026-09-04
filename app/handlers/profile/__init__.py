from aiogram import Router

from app.handlers.profile import anon, creation, feed, menu, premium, start


def build_profile_router() -> Router:
    router = Router(name="profile")
    router.include_router(start.router)
    router.include_router(creation.router)
    router.include_router(menu.router)
    router.include_router(premium.router)
    router.include_router(feed.router)
    router.include_router(anon.router)
    return router
