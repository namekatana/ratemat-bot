from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.filters.is_admin import IsAdmin
from app.handlers.admin.rendering import show_complaint, step_complaint_index
from app.keyboards.admin_inline import (
    COMPLAINT_NEXT,
    COMPLAINT_PREFIX,
    COMPLAINT_PREV,
)
from app.keyboards.reply import REVIEW_COMPLAINTS
from app.services.complaints import ban, dismiss
from app.texts import moderation as user_texts

router = Router(name="admin_complaints")


@router.message(F.text == REVIEW_COMPLAINTS, IsAdmin())
async def open_complaints(message: Message, state: FSMContext) -> None:
    await state.update_data(admin_complaint_index=0)
    await show_complaint(message.bot, message.chat.id, state)


@router.callback_query(F.data == COMPLAINT_PREV, IsAdmin())
async def previous_complaint(callback: CallbackQuery, state: FSMContext) -> None:
    await step_complaint_index(state, -1)
    await show_complaint(callback.bot, callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(F.data == COMPLAINT_NEXT, IsAdmin())
async def next_complaint(callback: CallbackQuery, state: FSMContext) -> None:
    await step_complaint_index(state, 1)
    await show_complaint(callback.bot, callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(F.data.startswith(f"{COMPLAINT_PREFIX}:ban:"), IsAdmin())
async def ban_target(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, complaint_id, target_id = callback.data.split(":")
    target_telegram_id = int(target_id)
    await ban(int(complaint_id), target_telegram_id, callback.from_user.id)
    if target_telegram_id:
        try:
            await callback.bot.send_message(target_telegram_id, user_texts.BANNED)
        except TelegramAPIError:
            pass
    await show_complaint(callback.bot, callback.message.chat.id, state)
    await callback.answer("Заблоковано")


@router.callback_query(F.data.startswith(f"{COMPLAINT_PREFIX}:dismiss:"), IsAdmin())
async def dismiss_complaint(callback: CallbackQuery, state: FSMContext) -> None:
    complaint_id = int(callback.data.rsplit(":", 1)[1])
    await dismiss(complaint_id, callback.from_user.id)
    await show_complaint(callback.bot, callback.message.chat.id, state)
    await callback.answer("Залишено")
