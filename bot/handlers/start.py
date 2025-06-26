"""Start handler."""
from telethon.events import NewMessage


async def start_cmd_handler(event: NewMessage.Event, ) -> None:
    """Handle start command."""
    await event.client.send_message(
        entity=event.input_chat,
        message="""Добро пожаловать в приложение для отслеживания обновлений в GitHub репозиториях!\n
Для справки введите команду /help""",
        reply_to=event.message,
    )
