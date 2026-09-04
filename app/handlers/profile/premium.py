from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery

from app.filters.is_verified import IsVerified
from app.handlers.common import delete_message, delete_messages
from app.keyboards.profile import PREMIUM, main_menu
from app.services.assets import premium_photo
from app.services.premium import (
    PREMIUM_PAYLOAD,
    PREMIUM_STARS,
    activate,
    status,
)
from app.texts import profile as texts

router = Router(name="profile_premium")

PREMIUM_MSGS = "premium_msgs"


async def clear_premium(bot: Bot, chat_id: int, state: FSMContext) -> None:
    data = await state.get_data()
    await delete_messages(bot, chat_id, data.get(PREMIUM_MSGS, []))
    await state.update_data(**{PREMIUM_MSGS: []})


async def _send_offer(message: Message, caption: str) -> list[int]:
    try:
        card = await message.answer_photo(premium_photo(), caption=caption)
    except FileNotFoundError:
        card = await message.answer(caption)
    invoice = await message.answer_invoice(
        title="RateMat Преміум",
        description=texts.PREMIUM_INVOICE_DESC,
        payload=PREMIUM_PAYLOAD,
        currency="XTR",
        prices=[LabeledPrice(label="Преміум · 30 днів", amount=PREMIUM_STARS)],
    )
    return [card.message_id, invoice.message_id]


@router.message(F.text == PREMIUM, IsVerified())
async def open_premium(message: Message, state: FSMContext) -> None:
    await clear_premium(message.bot, message.chat.id, state)
    await delete_message(message)
    current = await status(message.from_user.id)
    caption = texts.premium_extend(current) if current else texts.PREMIUM_PITCH
    tracked = await _send_offer(message, caption)
    await state.update_data(**{PREMIUM_MSGS: tracked})


@router.pre_checkout_query()
async def confirm_checkout(query: PreCheckoutQuery) -> None:
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def payment_done(message: Message, state: FSMContext) -> None:
    await clear_premium(message.bot, message.chat.id, state)
    payment = message.successful_payment
    until = await activate(
        message.from_user.id,
        payment.telegram_payment_charge_id,
        payment.total_amount,
        payment.invoice_payload,
    )
    await message.answer(texts.premium_thanks(until), reply_markup=main_menu())
