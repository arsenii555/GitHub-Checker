"""List handler."""
from telethon.events import NewMessage


async def list_cmd_handler(event: NewMessage.Event, ) -> None:
    """Handle /list command."""
    await event.client.send_message(
        entity=event.input_chat,
        message="""Список отслеживаемых ссылок""",
        reply_to=event.chat_id,
    )
