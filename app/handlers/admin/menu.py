from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.is_admin import IsAdmin
from app.keyboards.reply import admin_menu
from app.services.users import register_user
from app.texts import admin as texts

router = Router(name="admin_menu")


@router.message(CommandStart(), IsAdmin())
async def handle_admin_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await register_user(message.from_user)
    await message.answer(texts.WELCOME, reply_markup=admin_menu())
