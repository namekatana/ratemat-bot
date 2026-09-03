from aiogram import Router

from app.handlers.admin import analytics, complaints, menu, verification


def build_admin_router() -> Router:
    router = Router(name="admin")
    router.include_router(menu.router)
    router.include_router(verification.router)
    router.include_router(complaints.router)
    router.include_router(analytics.router)
    return router
