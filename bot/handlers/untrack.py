"""Untrack handler."""
from telethon.events import NewMessage


async def untrack_cmd_handler(event: NewMessage.Event, ) -> None:
    """Handle /untrack command."""
    resp_msg: str
    msg_text = event.message.text
    match msg_text.split():
        case ["/untrack", link]:
            resp_msg = f"Ссылка\n{link}\nбольше не отслеживается"
        case _:
            resp_msg = "Отправьте сообщение вида:\n/untrack <link>"
    await event.client.send_message(
        entity=event.input_chat,
        message=resp_msg,
        reply_to=event.chat_id,
    )
