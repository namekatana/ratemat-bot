from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.filters.is_verified import IsVerified
from app.keyboards.profile import (
    CREATE_PROFILE,
    GENDER_PREFIX,
    gender_choice,
    main_menu,
)
from app.services.profiles import (
    save_profile,
    validate_age,
    validate_description,
    validate_name,
)
from app.states.profile import ProfileForm
from app.texts import profile as texts

router = Router(name="profile_creation")


@router.callback_query(F.data == CREATE_PROFILE, IsVerified())
async def begin_from_button(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ProfileForm.name)
    await callback.message.answer(texts.CREATE_INTRO)
    await callback.answer()


@router.message(ProfileForm.name)
async def set_name(message: Message, state: FSMContext) -> None:
    name = validate_name(message.text or "")
    if name is None:
        await message.answer(texts.BAD_NAME)
        return
    await state.update_data(name=name)
    await state.set_state(ProfileForm.age)
    await message.answer(texts.ASK_AGE)


@router.message(ProfileForm.age)
async def set_age(message: Message, state: FSMContext) -> None:
    age = validate_age(message.text or "")
    if age is None:
        await message.answer(texts.BAD_AGE)
        return
    await state.update_data(age=age)
    await state.set_state(ProfileForm.gender)
    await message.answer(texts.ASK_GENDER, reply_markup=gender_choice())


@router.callback_query(ProfileForm.gender, F.data.startswith(f"{GENDER_PREFIX}:"))
async def set_gender(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(gender=callback.data.split(":")[1])
    await state.set_state(ProfileForm.photo)
    await callback.message.answer(texts.ASK_PHOTO)
    await callback.answer()


@router.message(ProfileForm.gender)
async def gender_wrong(message: Message) -> None:
    await message.answer(texts.GENDER_RETRY, reply_markup=gender_choice())


@router.message(ProfileForm.photo, F.photo)
async def set_photo(message: Message, state: FSMContext) -> None:
    await state.update_data(photo_file_id=message.photo[-1].file_id)
    await state.set_state(ProfileForm.description)
    await message.answer(texts.ASK_DESCRIPTION)


@router.message(ProfileForm.photo)
async def photo_wrong(message: Message) -> None:
    await message.answer(texts.BAD_PHOTO)


@router.message(ProfileForm.description)
async def set_description(message: Message, state: FSMContext) -> None:
    description = validate_description(message.text or "")
    if description is None:
        await message.answer(texts.BAD_DESCRIPTION)
        return
    data = await state.get_data()
    await save_profile(
        message.from_user.id,
        data["name"],
        data["age"],
        data["gender"],
        data["photo_file_id"],
        description,
    )
    await state.clear()
    await message.answer(texts.PROFILE_SAVED, reply_markup=main_menu())
