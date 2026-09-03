from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.keyboards.inline import START_VERIFICATION
from app.services.users import mark_awaiting_video, store_verification_note
from app.states.verification import Verification
from app.texts import verification as texts

router = Router(name="verification")


@router.callback_query(F.data == START_VERIFICATION)
async def start_verification(callback: CallbackQuery, state: FSMContext) -> None:
    await mark_awaiting_video(callback.from_user.id)
    await state.set_state(Verification.awaiting_video_note)
    await callback.message.answer(texts.REQUEST_NOTE)
    await callback.answer()


@router.message(Verification.awaiting_video_note, F.video_note)
async def receive_video_note(message: Message, state: FSMContext) -> None:
    if message.video_note.duration > settings.max_verification_note_seconds:
        await message.answer(texts.NOTE_TOO_LONG)
        return
    await store_verification_note(message.from_user.id, message.video_note.file_id)
    await state.clear()
    await message.answer(texts.AWAITING_REVIEW)


@router.message(Verification.awaiting_video_note)
async def reject_non_video_note(message: Message) -> None:
    await message.answer(texts.WRONG_CONTENT)
