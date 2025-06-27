"""Track handler."""
from telethon.events import NewMessage
from ..client import HTTPClient
from ..utils import extract_owner_repo
from ..translation import load_translations


async def track_cmd_handler(http_client: HTTPClient, event: NewMessage.Event, ) -> None:
    """Handle /track command."""
    resp_msg: str
    user_id = event.chat_id
    locale = await http_client.get_user_locale(user_id)
    _ = load_translations(locale)
    msg_text = event.message.text
    match msg_text.split():
        case ["/track", link]:
            if extract_owner_repo(link) is None:
                resp_msg = _("❌ Некорректная ссылка. Отправьте ссылку на GitHub репозиторий.")
            else:
                links = await http_client.list_links(user_id=user_id)
                if link not in links:
                    success = await http_client.track_link(user_id=user_id, link=link)
                    if success:
                        resp_msg = _("Ссылка\n{}\nуспешно добавлена для отслеживания ✅").format(link)
                    else:
                        resp_msg = _("Произошла ошибка при добавлении ссылки ❌")
                else:
                    resp_msg = _("👀Данная ссылка уже отслеживается 👀")
        case _:
            resp_msg = _("Отправьте сообщение вида:\n/track <link>")
    await event.client.send_message(
        entity=event.input_chat,
        message=resp_msg,
        reply_to=event.message,
    )
