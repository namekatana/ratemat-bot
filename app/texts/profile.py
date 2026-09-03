from typing import Any

from app.services.complaints import REASON_MAX, REASON_MIN
from app.services.profiles import (
    AGE_MAX,
    AGE_MIN,
    DESCRIPTION_MAX,
    DESCRIPTION_MIN,
    NAME_MAX,
    NAME_MIN,
)

_GENDER_LABELS = {"male": "Чоловік", "female": "Жінка"}

_RATING_SLOTS = 5

VERIFIED_NEEDS_PROFILE = (
    "🎉 <b>Верифікацію пройдено!</b>\n\n"
    "Тепер створи анкету — це займе одну хвилину. "
    "Після цього ти потрапиш до стрічки та зможеш переглядати й оцінювати інші анкети."
)

CREATE_INTRO = (
    "📝 <b>Створення анкети</b>\n\n"
    "Заповнимо п'ять коротких кроків: ім'я, вік, стать, фото та опис. "
    "Анкету бачитимуть інші користувачі у стрічці й зможуть поставити оцінку від 1 до 5 зірочок.\n"
    "Переробити анкету можна будь-коли кнопкою «✏️ Змінити анкету».\n\n"
    "<b>Крок 1 з 5 · Ім'я</b>\n"
    "Напиши, як тебе звати — саме це ім'я побачать у твоїй анкеті.\n\n"
    f"<blockquote>📏 Обмеження: від {NAME_MIN} до {NAME_MAX} символів, в один рядок, без переносів</blockquote>"
)

ASK_AGE = (
    "✅ Ім'я збережено.\n\n"
    "<b>Крок 2 з 5 · Вік</b>\n"
    "Скільки тобі повних років? Надішли відповідь одним числом.\n\n"
    f"<blockquote>📏 Обмеження: ціле число від {AGE_MIN} до {AGE_MAX}</blockquote>"
)

ASK_GENDER = (
    "✅ Вік збережено.\n\n"
    "<b>Крок 3 з 5 · Стать</b>\n"
    "Обери свою стать кнопкою нижче.\n\n"
    "<blockquote>📏 Доступні варіанти: Чоловік або Жінка</blockquote>"
)

GENDER_RETRY = (
    "Скористайся кнопками нижче, щоб обрати стать.\n\n"
    "<blockquote>📏 Доступні варіанти: Чоловік або Жінка</blockquote>"
)

ASK_PHOTO = (
    "✅ Стать збережено.\n\n"
    "<b>Крок 4 з 5 · Фото</b>\n"
    "Надішли одне фото для анкети. Найкраще — світле фото, де добре видно обличчя.\n\n"
    "<blockquote>📏 Обмеження: рівно одне фото. Якщо надішлеш кілька — візьмемо перше</blockquote>"
)

ASK_DESCRIPTION = (
    "✅ Фото збережено.\n\n"
    "<b>Крок 5 з 5 · Опис</b>\n"
    "Кілька речень про себе: чим захоплюєшся, чим займаєшся, кого хочеш знайти.\n\n"
    f"<blockquote>📏 Обмеження: від {DESCRIPTION_MIN} до {DESCRIPTION_MAX} символів</blockquote>"
)

BAD_NAME = (
    "⚠️ Таке ім'я не підходить.\n\n"
    f"<blockquote>📏 Потрібно: від {NAME_MIN} до {NAME_MAX} символів, в один рядок</blockquote>"
    "Спробуй ще раз."
)
BAD_AGE = (
    "⚠️ Не вдалося розпізнати вік.\n\n"
    f"<blockquote>📏 Потрібно: ціле число від {AGE_MIN} до {AGE_MAX}</blockquote>"
    "Спробуй ще раз."
)
BAD_PHOTO = (
    "⚠️ Потрібне саме фото.\n\n"
    "<blockquote>📏 Надішли одне зображення як фото, а не файлом чи текстом</blockquote>"
    "Спробуй ще раз."
)
BAD_DESCRIPTION = (
    "⚠️ Опис не підходить.\n\n"
    f"<blockquote>📏 Потрібно: від {DESCRIPTION_MIN} до {DESCRIPTION_MAX} символів</blockquote>"
    "Спробуй ще раз."
)

PROFILE_SAVED = (
    "✅ <b>Анкету збережено!</b>\n\n"
    "Вона вже у стрічці. Керування — на клавіатурі нижче:\n"
    "• «📷 Дивитись анкети» — переглядати й оцінювати інших\n"
    "• «👤 Моя анкета» — подивитися свою анкету та середню оцінку\n"
    "• «✏️ Змінити анкету» — переробити свою анкету"
)

FEED_EMPTY = "😔 Поки що немає нових анкет для перегляду. Зазирни трохи пізніше."
FEED_CLOSED = "🏠 Головне меню. Керування — на клавіатурі нижче."
FEED_HINT = (
    "Оціни анкету зірочками на клавіатурі нижче (1–5) "
    "або натисни «⬅️ Головне меню»."
)

REPORT_ASK = (
    "🚩 <b>Скарга на анкету</b>\n\n"
    "Опиши, що не так із цією анкетою — причину побачить модератор.\n"
    "Щоб не надсилати скаргу, натисни «⬅️ Головне меню».\n\n"
    f"<blockquote>📏 Обмеження: від {REASON_MIN} до {REASON_MAX} символів</blockquote>"
)
REPORT_BAD = (
    "⚠️ Причина не підходить.\n\n"
    f"<blockquote>📏 Потрібно: текстом, від {REASON_MIN} до {REASON_MAX} символів</blockquote>"
    "Спробуй ще раз або натисни «⬅️ Головне меню»."
)
REPORT_SAVED = "✅ Скаргу надіслано. Показуємо наступну анкету."

MENU_GREETING = "👋 З поверненням! Керування — на клавіатурі нижче."

NO_PROFILE = "У тебе ще немає анкети. Натисни «Створити анкету», щоб почати."


def _gender_label(gender: str) -> str:
    return _GENDER_LABELS.get(gender, "—")


def _stars(score: float) -> str:
    filled = max(0, min(_RATING_SLOTS, round(score)))
    return "★" * filled + "☆" * (_RATING_SLOTS - filled)


def _rating_line(votes: int, average: float) -> str:
    if not votes:
        return f"{_stars(0)} · ще немає оцінок"
    return f"{_stars(average)} · {average:.1f}/5 · {votes}"


def _profile_body(profile: dict[str, Any]) -> str:
    return (
        f"<b>{profile['name']}</b>, {profile['age']} · {_gender_label(profile['gender'])}\n\n"
        f"📝 <b>Про себе</b>\n"
        f"<blockquote>{profile['description']}</blockquote>"
    )


def profile_caption(profile: dict[str, Any], previous_score: int | None = None) -> str:
    text = _profile_body(profile)
    if previous_score is not None:
        text += f"\n\n🔁 Твоя попередня оцінка: {_stars(previous_score)} ({previous_score}/5)"
    else:
        text += "\n\n⬇️ Обери оцінку зірочками на клавіатурі нижче:"
    return text


def my_profile_caption(profile: dict[str, Any], votes: int, average: float) -> str:
    return (
        "👤 <b>Твоя анкета</b>\n\n"
        f"{_profile_body(profile)}\n\n"
        f"⭐ <b>Рейтинг</b>\n{_rating_line(votes, average)}"
    )
