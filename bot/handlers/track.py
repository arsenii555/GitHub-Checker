"""Track handler."""
from telethon.events import NewMessage
from ..client import HTTPClient


async def track_cmd_handler(http_client: HTTPClient, event: NewMessage.Event, ) -> None:
    """Handle /track command."""
    resp_msg: str
    user_id = event.chat_id
    msg_text = event.message.text
    match msg_text.split():
        case ["/track", link]:
            success = await http_client.track_link(user_id=user_id, link=link)
            if success:
                resp_msg = f"Ссылка\n{link}\nуспешно добавлена для отслеживания ✅"
            else:
                resp_msg = "Произошла ошибка при добавлении ссылки ❌"
        case _:
            resp_msg = "Отправьте сообщение вида:\n/track <link>"
    await event.client.send_message(
        entity=event.input_chat,
        message=resp_msg,
        reply_to=event.message,
    )
