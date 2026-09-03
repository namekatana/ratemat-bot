from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.is_verified import IsVerified
from app.keyboards.profile import EDIT_PROFILE, MY_PROFILE, create_profile
from app.services.profiles import get_profile, rating_summary
from app.states.profile import ProfileForm
from app.texts import profile as texts

router = Router(name="profile_menu")


@router.message(F.text == EDIT_PROFILE, IsVerified())
async def edit_profile(message: Message, state: FSMContext) -> None:
    await state.set_state(ProfileForm.name)
    await message.answer(texts.CREATE_INTRO)


@router.message(F.text == MY_PROFILE, IsVerified())
async def my_profile(message: Message) -> None:
    profile = await get_profile(message.from_user.id)
    if profile is None:
        await message.answer(texts.NO_PROFILE, reply_markup=create_profile())
        return
    votes, average = await rating_summary(message.from_user.id)
    await message.answer_photo(
        profile["photo_file_id"],
        caption=texts.my_profile_caption(profile, votes, average),
    )
