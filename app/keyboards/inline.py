from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

START_VERIFICATION = "start_verification"


def lets_go() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Поїхали!", callback_data=START_VERIFICATION)
    )
    return builder.as_markup()
