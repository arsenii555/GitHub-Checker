"""Start handler."""
from telethon.events import NewMessage
from ..client import HTTPClient
from ..translation import load_translations


async def start_cmd_handler(http_client: HTTPClient, event: NewMessage.Event, ) -> None:
    """Handle start command."""
    user_id = event.chat_id
    locale = await http_client.get_user_locale(user_id)
    _ = load_translations(locale)
    await event.client.send_message(
        entity=event.input_chat,
        message=_("""Добро пожаловать в приложение для отслеживания обновлений в GitHub репозиториях!\n
Для справки введите команду /help"""),
        reply_to=event.message,
    )
