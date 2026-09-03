from aiogram import Router

from app.handlers import start, verification
from app.handlers.admin import build_admin_router
from app.handlers.profile import build_profile_router


def build_router() -> Router:
    router = Router(name="root")
    router.include_router(build_admin_router())
    router.include_router(build_profile_router())
    router.include_router(start.router)
    router.include_router(verification.router)
    return router
