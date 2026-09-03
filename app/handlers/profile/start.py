from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.is_verified import IsVerified
from app.keyboards.profile import create_profile, main_menu
from app.services.profiles import has_profile
from app.services.users import register_user
from app.texts import profile as texts

router = Router(name="profile_start")


@router.message(CommandStart(), IsVerified())
async def verified_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await register_user(message.from_user)
    if await has_profile(message.from_user.id):
        await message.answer(texts.MENU_GREETING, reply_markup=main_menu())
        return
    await message.answer(
        texts.VERIFIED_NEEDS_PROFILE, reply_markup=create_profile()
    )
