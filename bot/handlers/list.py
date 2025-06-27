"""List handler."""
from telethon.events import NewMessage
from ..client import HTTPClient


async def list_cmd_handler(http_client: HTTPClient, event: NewMessage.Event, ) -> None:
    """Handle /list command."""
    resp_msg: str
    user_id = event.chat_id
    links = await http_client.list_links(user_id=user_id)
    if links:
        resp_msg = "📋 Ваши отслеживаемые репозитории\n\n" + "\n".join([f"- {link}" for link in links])
    else:
        resp_msg = "ℹ️У вас нет отслеживаемых репозиториев"
    await event.client.send_message(
        entity=event.input_chat,
        message=resp_msg,
        reply_to=event.chat_id,
    )
