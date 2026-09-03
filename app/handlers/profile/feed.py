from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.is_verified import IsVerified
from app.handlers.common import delete_messages
from app.keyboards.profile import (
    BROWSE_PROFILES,
    FEED_BACK,
    FEED_REPORT,
    RATING_LABELS,
    RATING_TEXTS,
    feed_menu,
    main_menu,
    reason_menu,
)
from app.services.complaints import submit, validate_reason
from app.services.feed import next_candidate, rate
from app.states.profile import FeedForm
from app.texts import profile as texts

router = Router(name="profile_feed")

FEED_MSGS = "feed_msgs"
FEED_TARGET = "feed_target"


async def _clear_tracked(bot: Bot, chat_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    await delete_messages(bot, chat_id, data.get(FEED_MSGS, []))
    await state.update_data(**{FEED_MSGS: []})


async def _show_next(
    bot: Bot, chat_id: int, viewer_id: int, state: FSMContext
) -> None:
    await _clear_tracked(bot, chat_id, state)
    candidate = await next_candidate(viewer_id)
    if candidate is None:
        await state.update_data(**{FEED_TARGET: None})
        await bot.send_message(chat_id, texts.FEED_EMPTY, reply_markup=feed_menu())
        return
    profile = candidate["profile"]
    message = await bot.send_photo(
        chat_id,
        profile["photo_file_id"],
        caption=texts.profile_caption(profile, candidate["previous_score"]),
        reply_markup=feed_menu(),
    )
    await state.update_data(
        **{FEED_MSGS: [message.message_id], FEED_TARGET: profile["telegram_id"]}
    )


@router.message(F.text == BROWSE_PROFILES, IsVerified())
async def open_feed(message: Message, state: FSMContext) -> None:
    await state.set_state(FeedForm.viewing)
    await _show_next(message.bot, message.chat.id, message.from_user.id, state)


@router.message(FeedForm.viewing, F.text == FEED_BACK)
async def leave_feed(message: Message, state: FSMContext) -> None:
    await _clear_tracked(message.bot, message.chat.id, state)
    await state.clear()
    await message.answer(texts.FEED_CLOSED, reply_markup=main_menu())


@router.message(FeedForm.viewing, F.text.in_(RATING_TEXTS))
async def rate_current(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    target_id = data.get(FEED_TARGET)
    try:
        await message.delete()
    except TelegramAPIError:
        pass
    if target_id is None:
        await _show_next(message.bot, message.chat.id, message.from_user.id, state)
        return
    await rate(message.from_user.id, int(target_id), RATING_LABELS[message.text])
    await _show_next(message.bot, message.chat.id, message.from_user.id, state)


@router.message(FeedForm.viewing, F.text == FEED_REPORT)
async def start_complaint(message: Message, state: FSMContext) -> None:
    try:
        await message.delete()
    except TelegramAPIError:
        pass
    data = await state.get_data()
    if data.get(FEED_TARGET) is None:
        await _show_next(
            message.bot, message.chat.id, message.from_user.id, state
        )
        return
    await state.set_state(FeedForm.complaint_reason)
    await message.answer(texts.REPORT_ASK, reply_markup=reason_menu())


@router.message(FeedForm.complaint_reason, F.text == FEED_BACK)
async def cancel_complaint(message: Message, state: FSMContext) -> None:
    await _clear_tracked(message.bot, message.chat.id, state)
    await state.clear()
    await message.answer(texts.FEED_CLOSED, reply_markup=main_menu())


@router.message(FeedForm.complaint_reason, F.text)
async def save_complaint(message: Message, state: FSMContext) -> None:
    reason = validate_reason(message.text)
    if reason is None:
        await message.answer(texts.REPORT_BAD, reply_markup=reason_menu())
        return
    data = await state.get_data()
    target_id = data.get(FEED_TARGET)
    await state.set_state(FeedForm.viewing)
    if target_id is not None:
        await submit(message.from_user.id, int(target_id), reason)
    await message.answer(texts.REPORT_SAVED)
    await _show_next(message.bot, message.chat.id, message.from_user.id, state)


@router.message(FeedForm.complaint_reason)
async def complaint_reason_hint(message: Message) -> None:
    await message.answer(texts.REPORT_BAD, reply_markup=reason_menu())


@router.message(FeedForm.viewing)
async def feed_hint(message: Message) -> None:
    await message.answer(texts.FEED_HINT, reply_markup=feed_menu())
