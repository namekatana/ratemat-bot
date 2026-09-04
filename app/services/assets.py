from aiogram.types import FSInputFile

from app.config import PHOTOS_DIR

WELCOME_PHOTO = "welcome.jpg"
PREMIUM_PHOTO = "premium.jpg"


def photo(name: str) -> FSInputFile:
    path = PHOTOS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Photo asset not found: {path}")
    return FSInputFile(path)


def welcome_photo() -> FSInputFile:
    return photo(WELCOME_PHOTO)


def premium_photo() -> FSInputFile:
    return photo(PREMIUM_PHOTO)
