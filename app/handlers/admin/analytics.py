from aiogram import F, Router
from aiogram.types import Message

from app.filters.is_admin import IsAdmin
from app.keyboards.reply import SHOW_ANALYTICS
from app.services.analytics import build_report
from app.texts import admin as texts

router = Router(name="admin_analytics")


@router.message(F.text == SHOW_ANALYTICS, IsAdmin())
async def show_analytics(message: Message) -> None:
    report = await build_report()
    await message.answer(texts.analytics_report(report))
