from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

REVIEW_VERIFICATION = "🎥 Переглянути верифікацію"
REVIEW_COMPLAINTS = "🚩 Скарги"
SHOW_ANALYTICS = "📊 Аналітика"


def admin_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=REVIEW_VERIFICATION))
    builder.row(
        KeyboardButton(text=REVIEW_COMPLAINTS),
        KeyboardButton(text=SHOW_ANALYTICS),
    )
    return builder.as_markup(resize_keyboard=True)
