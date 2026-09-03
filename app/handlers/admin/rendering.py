from aiogram import Bot
from aiogram.fsm.context import FSMContext

from app.handlers.common import delete_messages
from app.keyboards.admin_inline import complaint_nav, verification_nav
from app.services.complaints import open_queue
from app.services.verification_review import pending_queue
from app.texts import admin as texts

REVIEW_INDEX = "admin_review_index"
REVIEW_MSGS = "admin_review_msgs"
COMPLAINT_INDEX = "admin_complaint_index"
COMPLAINT_MSGS = "admin_complaint_msgs"


def _clamp(index: int, length: int) -> int:
    if length == 0:
        return 0
    return max(0, min(index, length - 1))


async def show_verification(bot: Bot, chat_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    await delete_messages(bot, chat_id, data.get(REVIEW_MSGS, []))
    queue = await pending_queue()
    if not queue:
        await state.update_data(**{REVIEW_MSGS: [], REVIEW_INDEX: 0})
        await bot.send_message(chat_id, texts.VERIFICATION_EMPTY)
        return
    index = _clamp(data.get(REVIEW_INDEX, 0), len(queue))
    user = queue[index]
    note = await bot.send_video_note(
        chat_id, video_note=user["verification_file_id"]
    )
    card = await bot.send_message(
        chat_id,
        texts.verification_card(user, index + 1, len(queue)),
        reply_markup=verification_nav(user["telegram_id"], len(queue) > 1),
    )
    await state.update_data(
        **{REVIEW_INDEX: index, REVIEW_MSGS: [note.message_id, card.message_id]}
    )


async def show_complaint(bot: Bot, chat_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    await delete_messages(bot, chat_id, data.get(COMPLAINT_MSGS, []))
    queue = await open_queue()
    if not queue:
        await state.update_data(**{COMPLAINT_MSGS: [], COMPLAINT_INDEX: 0})
        await bot.send_message(chat_id, texts.COMPLAINTS_EMPTY)
        return
    index = _clamp(data.get(COMPLAINT_INDEX, 0), len(queue))
    complaint = queue[index]
    caption = texts.complaint_card(complaint, index + 1, len(queue))
    markup = complaint_nav(
        complaint["id"],
        complaint.get("target_telegram_id") or 0,
        len(queue) > 1,
    )
    photo_file_id = complaint.get("target_photo_file_id")
    if photo_file_id:
        card = await bot.send_photo(
            chat_id, photo_file_id, caption=caption, reply_markup=markup
        )
    else:
        card = await bot.send_message(chat_id, caption, reply_markup=markup)
    await state.update_data(
        **{COMPLAINT_INDEX: index, COMPLAINT_MSGS: [card.message_id]}
    )


async def step_review_index(state: FSMContext, delta: int) -> None:
    data = await state.get_data()
    await state.update_data(**{REVIEW_INDEX: data.get(REVIEW_INDEX, 0) + delta})


async def step_complaint_index(state: FSMContext, delta: int) -> None:
    data = await state.get_data()
    await state.update_data(**{COMPLAINT_INDEX: data.get(COMPLAINT_INDEX, 0) + delta})
