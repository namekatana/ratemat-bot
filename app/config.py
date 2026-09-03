from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
PHOTOS_DIR = ASSETS_DIR / "photos"


@dataclass(frozen=True)
class Settings:
    bot_token: str
    supabase_url: str
    supabase_service_key: str
    max_verification_note_seconds: int = 5


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_settings() -> Settings:
    return Settings(
        bot_token=_required("BOT_TOKEN"),
        supabase_url=_required("SUPABASE_URL"),
        supabase_service_key=_required("SUPABASE_SERVICE_KEY"),
    )


settings = load_settings()
