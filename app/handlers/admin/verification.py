from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from app.filters.is_admin import IsAdmin
from app.handlers.admin.rendering import show_verification, step_review_index
from app.keyboards.admin_inline import (
    VERIFICATION_NEXT,
    VERIFICATION_PREFIX,
    VERIFICATION_PREV,
)
from app.keyboards.profile import create_profile
from app.keyboards.reply import REVIEW_VERIFICATION
from app.services.verification_review import approve, reject
from app.texts import profile as profile_texts
from app.texts import verification as user_texts

router = Router(name="admin_verification")


async def _notify(
    callback: CallbackQuery,
    telegram_id: int,
    text: str,
    markup: InlineKeyboardMarkup | None = None,
) -> None:
    try:
        await callback.bot.send_message(telegram_id, text, reply_markup=markup)
    except TelegramAPIError:
        pass


@router.message(F.text == REVIEW_VERIFICATION, IsAdmin())
async def open_verification(message: Message, state: FSMContext) -> None:
    await state.update_data(admin_review_index=0)
    await show_verification(message.bot, message.chat.id, state)


@router.callback_query(F.data == VERIFICATION_PREV, IsAdmin())
async def previous_user(callback: CallbackQuery, state: FSMContext) -> None:
    await step_review_index(state, -1)
    await show_verification(callback.bot, callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(F.data == VERIFICATION_NEXT, IsAdmin())
async def next_user(callback: CallbackQuery, state: FSMContext) -> None:
    await step_review_index(state, 1)
    await show_verification(callback.bot, callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(F.data.startswith(f"{VERIFICATION_PREFIX}:ok:"), IsAdmin())
async def approve_user(callback: CallbackQuery, state: FSMContext) -> None:
    telegram_id = int(callback.data.rsplit(":", 1)[1])
    await approve(telegram_id)
    await _notify(
        callback,
        telegram_id,
        profile_texts.VERIFIED_NEEDS_PROFILE,
        create_profile(),
    )
    await show_verification(callback.bot, callback.message.chat.id, state)
    await callback.answer("Схвалено")


@router.callback_query(F.data.startswith(f"{VERIFICATION_PREFIX}:no:"), IsAdmin())
async def reject_user(callback: CallbackQuery, state: FSMContext) -> None:
    telegram_id = int(callback.data.rsplit(":", 1)[1])
    await reject(telegram_id)
    await _notify(callback, telegram_id, user_texts.REJECTED)
    await show_verification(callback.bot, callback.message.chat.id, state)
    await callback.answer("Відхилено")
