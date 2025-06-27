"""List handler."""
from telethon.events import NewMessage
from ..client import HTTPClient
from ..translation import load_translations


async def list_cmd_handler(http_client: HTTPClient, event: NewMessage.Event, ) -> None:
    """Handle /list command."""
    resp_msg: str
    user_id = event.chat_id
    locale = await http_client.get_user_locale(user_id)
    _ = load_translations(locale)
    links = await http_client.list_links(user_id=user_id)
    if links:
        resp_msg = _("📋 Ваши отслеживаемые репозитории\n\n") + "\n".join([f"- {link}" for link in links])
    else:
        resp_msg = _("ℹ️У вас нет отслеживаемых репозиториев")
    await event.client.send_message(
        entity=event.input_chat,
        message=resp_msg,
        reply_to=event.chat_id,
    )
