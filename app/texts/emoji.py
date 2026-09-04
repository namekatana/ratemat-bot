def _custom(emoji_id: str, fallback: str) -> str:
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'


LOGO = _custom("5249424933158700653", "⭐")
PREMIUM = _custom("5249177684776362848", "💎")
MESSAGE = _custom("5249303909570225368", "✉️")
HAND = _custom("5246789592765477469", "👋")
GEAR = _custom("5249403110429862053", "⚙️")
BELL = _custom("5249211395974667980", "🔔")
