"""Main TG Bot module."""
from telethon import TelegramClient, events
from settings import TGBotSettings
from handlers import start_cmd_handler, help_cmd_handler, list_cmd_handler, track_cmd_handler, untrack_cmd_handler

settings = TGBotSettings()

client = TelegramClient("bot_session", settings.api_id, settings.api_hash).start(bot_token=settings.token)

client.add_event_handler(
    start_cmd_handler,
    events.NewMessage(pattern="/start"),
)

client.add_event_handler(
    help_cmd_handler,
    events.NewMessage(pattern="/help"),
)

client.add_event_handler(
    list_cmd_handler,
    events.NewMessage(pattern="/list"),
)

client.add_event_handler(
    track_cmd_handler,
    events.NewMessage(pattern="/track"),
)

client.add_event_handler(
    untrack_cmd_handler,
    events.NewMessage(pattern="/untrack"),
)

client.run_until_disconnected()
