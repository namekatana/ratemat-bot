from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.inline import lets_go
from app.services.assets import welcome_photo
from app.services.users import register_user
from app.texts.start import WELCOME

router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await register_user(message.from_user)
    await message.answer_photo(
        photo=welcome_photo(),
        caption=WELCOME,
        reply_markup=lets_go(),
    )
