"""Untrack handler."""
from telethon.events import NewMessage
from ..client import HTTPClient
from ..translation import load_translations


async def untrack_cmd_handler(http_client: HTTPClient, event: NewMessage.Event, ) -> None:
    """Handle /untrack command."""
    resp_msg: str
    user_id = event.chat_id
    locale = await http_client.get_user_locale(user_id)
    _ = load_translations(locale)
    msg_text = event.message.text
    match msg_text.split():
        case ["/untrack", link]:
            links = await http_client.list_links(user_id=user_id)
            if link in links:
                success = await http_client.untrack_link(user_id=user_id, link=link)
                if success:
                    resp_msg = _("Ссылка\n{}\nбольше не отслеживается").format(link)
                else:
                    resp_msg = _("Произошла ошибка при удалении ссылки ❌")
            else:
                resp_msg = _("❗️Данная ссылка не отслеживалась❗️")
        case _:
            resp_msg = _("Отправьте сообщение вида:\n/untrack <link>")
    await event.client.send_message(
        entity=event.input_chat,
        message=resp_msg,
        reply_to=event.chat_id,
    )
