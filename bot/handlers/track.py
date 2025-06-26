"""Track handler."""
from telethon.events import NewMessage


async def track_cmd_handler(event: NewMessage.Event, ) -> None:
    """Handle /track command."""
    resp_msg: str
    msg_text = event.message.text
    match msg_text.split():
        case ["/track", link]:
            resp_msg = f"Ссылка\n{link}\nуспешно добавлена для отслеживания ✅"
        case _:
            resp_msg = "Отправьте сообщение вида:\n/track <link>"
    await event.client.send_message(
        entity=event.input_chat,
        message=resp_msg,
        reply_to=event.message,
    )
