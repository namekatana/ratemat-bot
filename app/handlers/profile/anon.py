from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery

from app.keyboards.profile import ANON_PREFIX
from app.services.anon import block, report
from app.texts import profile as texts

router = Router(name="profile_anon")


async def _finish(callback: CallbackQuery, done: bool, done_text: str) -> None:
    if done:
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except TelegramAPIError:
            pass
    await callback.answer(
        done_text if done else texts.ANON_ACTION_STALE, show_alert=done
    )


@router.callback_query(F.data.startswith(f"{ANON_PREFIX}:block:"))
async def block_sender(callback: CallbackQuery) -> None:
    message_id = int(callback.data.rsplit(":", 1)[1])
    done = await block(message_id, callback.from_user.id)
    await _finish(callback, done, texts.ANON_BLOCK_DONE)


@router.callback_query(F.data.startswith(f"{ANON_PREFIX}:report:"))
async def report_sender(callback: CallbackQuery) -> None:
    message_id = int(callback.data.rsplit(":", 1)[1])
    done = await report(message_id, callback.from_user.id)
    await _finish(callback, done, texts.ANON_REPORT_DONE)
