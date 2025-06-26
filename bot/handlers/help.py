"""Help handler."""
from telethon.events import NewMessage


async def help_cmd_handler(event: NewMessage.Event, ) -> None:
    """Handle /help command."""
    await event.client.send_message(
        entity=event.input_chat,
        message="""Доступны следующие команды:
/start - запуск бота
/help - получение справки о командах
/track <ссылка> - добавить новую ссылку для отслеживания
/untrack <ссылка> - прекратить отслеживание ссылки
/list - вывести список отслеживаемых ссылок""",
        reply_to=event.message,
    )
