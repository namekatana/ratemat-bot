def _custom(emoji_id: str, fallback: str) -> str:
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'


LOGO = _custom("5246851728057343045", "⭐")
PREMIUM = _custom("5249148255660452124", "💎")
MESSAGE = _custom("5249304459326041707", "✉️")
HAND = _custom("5249212504076232856", "👋")
GEAR = _custom("5249255647022719351", "⚙️")
BELL = _custom("5249246116490292800", "🔔")
