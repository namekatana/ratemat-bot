from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

VERIFICATION_PREFIX = "vr"
COMPLAINT_PREFIX = "cr"

VERIFICATION_PREV = f"{VERIFICATION_PREFIX}:prev"
VERIFICATION_NEXT = f"{VERIFICATION_PREFIX}:next"
COMPLAINT_PREV = f"{COMPLAINT_PREFIX}:prev"
COMPLAINT_NEXT = f"{COMPLAINT_PREFIX}:next"


def verification_nav(telegram_id: int, show_arrows: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="✅ Схвалити", callback_data=f"{VERIFICATION_PREFIX}:ok:{telegram_id}"
        ),
        InlineKeyboardButton(
            text="⛔ Відхилити", callback_data=f"{VERIFICATION_PREFIX}:no:{telegram_id}"
        ),
    )
    if show_arrows:
        builder.row(
            InlineKeyboardButton(text="◀️", callback_data=VERIFICATION_PREV),
            InlineKeyboardButton(text="▶️", callback_data=VERIFICATION_NEXT),
        )
    return builder.as_markup()


def complaint_nav(
    complaint_id: int, target_telegram_id: int, show_arrows: bool
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🚫 Заблокувати",
            callback_data=f"{COMPLAINT_PREFIX}:ban:{complaint_id}:{target_telegram_id}",
        ),
        InlineKeyboardButton(
            text="✅ Залишити",
            callback_data=f"{COMPLAINT_PREFIX}:dismiss:{complaint_id}",
        ),
    )
    if show_arrows:
        builder.row(
            InlineKeyboardButton(text="◀️", callback_data=COMPLAINT_PREV),
            InlineKeyboardButton(text="▶️", callback_data=COMPLAINT_NEXT),
        )
    return builder.as_markup()
