"""Language handlers."""
from telethon import events, Button
from ..client import HTTPClient
from ..translation import load_translations


async def language_cmd_handler(http_client: HTTPClient, event: events.NewMessage.Event) -> None:
    """Handle /language command."""
    user_id = event.chat_id
    current_locale = await http_client.get_user_locale(user_id)
    _ = load_translations(current_locale)

    buttons = [
        [Button.inline("🇷🇺 Русский", b"set_lang:ru")],
        [Button.inline("🇬🇧 English", b"set_lang:en")],
    ]

    await event.client.send_message(
        entity=event.input_chat,
        message=_("Выберите язык / Choose language:"),
        buttons=buttons
    )


async def set_language_callback(http_client: HTTPClient, event: events.CallbackQuery.Event) -> None:
    """Handle language selection callback."""
    user_id = event.chat_id
    _, lang = event.data.decode().split(":")

    success = await http_client.set_user_locale(user_id, lang)
    _ = load_translations(lang)

    if success:
        response = _("Язык успешно изменён!") if lang == "ru" else _("Language changed successfully!")
    else:
        response = _("Ошибка при изменении языка!") if lang == "ru" else _("Error changing language!")

    await event.client.send_message(
        entity=event.input_chat,
        message=response,
    )
    await event.delete()
