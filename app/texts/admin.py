from typing import Any


def _plural_people(count: int) -> str:
    tail = count % 10
    tens = count % 100
    if tail == 1 and tens != 11:
        return "людина"
    if 2 <= tail <= 4 and not 12 <= tens <= 14:
        return "людини"
    return "людей"


WELCOME = (
    "🛡 <b>Ви адмін RateMat</b>\n\n"
    "Доступні розділи керування на клавіатурі нижче:\n"
    "• 🎥 Переглянути верифікацію — черга відеокружків на підтвердження;\n"
    "• 🚩 Скарги — відкриті звернення користувачів;\n"
    "• 📊 Аналітика — поточні показники бота.\n\n"
    "Сповіщення про чергу приходять лише коли вона з'являється — без спаму."
)

VERIFICATION_EMPTY = "✅ Черга верифікації порожня. Нових кружечків немає."
COMPLAINTS_EMPTY = "✅ Відкритих скарг немає."


def queue_alert(count: int) -> str:
    return (
        f"🔔 <b>Черга верифікації</b>\n\n"
        f"Зараз {count} {_plural_people(count)} чекають на перевірку.\n"
        f"Відкрий «🎥 Переглянути верифікацію», щоб опрацювати."
    )


def _display_name(user: dict[str, Any]) -> str:
    parts = [user.get("first_name"), user.get("last_name")]
    name = " ".join(part for part in parts if part)
    return name or "Без імені"


def _username(user: dict[str, Any]) -> str:
    username = user.get("username")
    return f"@{username}" if username else "—"


def verification_card(user: dict[str, Any], position: int, total: int) -> str:
    return (
        f"🎥 <b>Верифікація</b> · {position}/{total}\n\n"
        f"Ім'я: {_display_name(user)}\n"
        f"Username: {_username(user)}\n"
        f"Telegram ID: <code>{user['telegram_id']}</code>\n"
        f"Надіслано: {user.get('updated_at', '—')}\n\n"
        f"Переглянь кружечок вище та ухвали рішення."
    )


def auto_shadow_reason(reporter_count: int) -> str:
    return (
        f"На анкету поскаржилися {reporter_count} {_plural_people(reporter_count)} "
        f"за 24 години. Анкету автоматично приховано зі стрічки.\n"
        f"Підтвердь бан або зніми тіньовий бан."
    )


def complaint_card(complaint: dict[str, Any], position: int, total: int) -> str:
    username = complaint.get("target_username")
    target_id = complaint.get("target_telegram_id")
    handle = f"@{username}" if username else "—"
    if complaint.get("kind") == "auto_shadow":
        return (
            f"🕶 <b>Автоматичне тіньове блокування</b> · {position}/{total}\n\n"
            f"На кого: {handle}\n"
            f"Telegram ID: <code>{target_id or '—'}</code>\n"
            f"Створено: {complaint.get('created_at', '—')}\n\n"
            f"{complaint['reason']}"
        )
    return (
        f"🚩 <b>Скарга</b> · {position}/{total}\n\n"
        f"На кого: {handle}\n"
        f"Telegram ID: <code>{target_id or '—'}</code>\n"
        f"Від кого: <code>{complaint['reporter_telegram_id']}</code>\n"
        f"Створено: {complaint.get('created_at', '—')}\n\n"
        f"Причина:\n{complaint['reason']}"
    )


def analytics_report(data: dict[str, Any]) -> str:
    by_status = data["by_status"]
    return (
        "📊 <b>Аналітика RateMat</b>\n\n"
        f"Усього користувачів: <b>{data['total']}</b>\n"
        f"Нових за 24 год: <b>{data['new_24h']}</b>\n"
        f"Нових за 7 днів: <b>{data['new_7d']}</b>\n\n"
        "<b>За статусом верифікації</b>\n"
        f"• не почали: {by_status['pending_start']}\n"
        f"• очікують кружечок: {by_status['awaiting_video']}\n"
        f"• у черзі на перевірку: {by_status['pending_review']}\n"
        f"• підтверджені: {by_status['verified']}\n"
        f"• відхилені: {by_status['rejected']}\n"
        f"• заблоковані: {by_status['banned']}\n"
        f"• тіньовий бан: {data['shadow_banned']}\n\n"
        f"Відкритих скарг: <b>{data['open_complaints']}</b>"
    )
