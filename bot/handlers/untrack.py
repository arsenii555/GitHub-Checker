"""Untrack handler."""
from telethon.events import NewMessage
from ..client import HTTPClient


async def untrack_cmd_handler(http_client: HTTPClient, event: NewMessage.Event, ) -> None:
    """Handle /untrack command."""
    resp_msg: str
    user_id = event.chat_id
    msg_text = event.message.text
    match msg_text.split():
        case ["/untrack", link]:
            success = await http_client.untrack_link(user_id=user_id, link=link)
            if success:
                resp_msg = f"Ссылка\n{link}\nбольше не отслеживается"
            else:
                resp_msg = "Произошла ошибка при удалении ссылки ❌"
        case _:
            resp_msg = "Отправьте сообщение вида:\n/untrack <link>"
    await event.client.send_message(
        entity=event.input_chat,
        message=resp_msg,
        reply_to=event.chat_id,
    )
