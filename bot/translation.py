"""Translation module."""
import gettext
from pathlib import Path
from typing import Callable

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locale"


def load_translations(lang: str) -> Callable[[str], str]:
    """Load translations for specified language."""
    if lang not in ("ru", "en"):
        lang = "ru"

    if lang == "en":
        translation = gettext.translation(
            "bot",
            localedir=LOCALES_DIR,
            languages=["en_US.UTF-8"],
            fallback=False
        )
    else:
        translation = gettext.NullTranslations()
    return translation.gettext
