from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

BROWSE_PROFILES = "📷 Дивитись анкети"
MY_PROFILE = "👤 Моя анкета"
EDIT_PROFILE = "✏️ Змінити анкету"

CREATE_PROFILE = "profile:create"
GENDER_PREFIX = "pg"

FEED_BACK = "⬅️ Головне меню"
FEED_REPORT = "🚩 Поскаржитися"
RATING_LABELS = {
    "⭐": 1,
    "⭐⭐": 2,
    "⭐⭐⭐": 3,
    "⭐⭐⭐⭐": 4,
    "⭐⭐⭐⭐⭐": 5,
}
RATING_TEXTS = frozenset(RATING_LABELS)


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=BROWSE_PROFILES))
    builder.row(KeyboardButton(text=MY_PROFILE), KeyboardButton(text=EDIT_PROFILE))
    return builder.as_markup(resize_keyboard=True)


def feed_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="⭐"),
        KeyboardButton(text="⭐⭐"),
        KeyboardButton(text="⭐⭐⭐"),
    )
    builder.row(KeyboardButton(text="⭐⭐⭐⭐"), KeyboardButton(text="⭐⭐⭐⭐⭐"))
    builder.row(KeyboardButton(text=FEED_REPORT))
    builder.row(KeyboardButton(text=FEED_BACK))
    return builder.as_markup(resize_keyboard=True)


def reason_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=FEED_BACK))
    return builder.as_markup(resize_keyboard=True)


def create_profile() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📝 Створити анкету", callback_data=CREATE_PROFILE)
    )
    return builder.as_markup()


def gender_choice() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Чоловік", callback_data=f"{GENDER_PREFIX}:male"),
        InlineKeyboardButton(text="Жінка", callback_data=f"{GENDER_PREFIX}:female"),
    )
    return builder.as_markup()
