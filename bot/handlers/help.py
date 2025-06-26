"""Help handler."""
from telethon.events import NewMessage
from ..translation import load_translations
from ..client import HTTPClient


async def help_cmd_handler(http_client: HTTPClient, event: NewMessage.Event, ) -> None:
    """Handle /help command."""
    user_id = event.chat_id
    locale = await http_client.get_user_locale(user_id)
    _ = load_translations(locale)
    await event.client.send_message(
        entity=event.input_chat,
        message=_("""Доступны следующие команды:
/start - запуск бота
/help - получение справки о командах
/language - выбор языка
/track <ссылка> - добавить новую ссылку для отслеживания
/untrack <ссылка> - прекратить отслеживание ссылки
/list - вывести список отслеживаемых ссылок"""),
        reply_to=event.message,
    )
