"""Main TG Bot module."""
import asyncio

from telethon import TelegramClient, events
from .settings import TGBotSettings
from .handlers import start_cmd_handler, help_cmd_handler, list_cmd_handler, track_cmd_handler, untrack_cmd_handler
from .client import HTTPClient
from functools import partial


settings = TGBotSettings()


async def main():
    """Run TG Bot and http client."""
    bot = await TelegramClient("bot_session", settings.api_id, settings.api_hash).start(bot_token=settings.token)
    http_client = HTTPClient(settings.scrapper_url)
    await http_client.start()
    track_handler = partial(track_cmd_handler, http_client)
    untrack_handler = partial(untrack_cmd_handler, http_client)
    list_handler = partial(list_cmd_handler, http_client)

    bot.add_event_handler(
        start_cmd_handler,
        events.NewMessage(pattern="/start"),
    )

    bot.add_event_handler(
        help_cmd_handler,
        events.NewMessage(pattern="/help"),
    )

    bot.add_event_handler(
        list_handler,
        events.NewMessage(pattern="/list"),
    )

    bot.add_event_handler(
        track_handler,
        events.NewMessage(pattern="/track"),
    )

    bot.add_event_handler(
        untrack_handler,
        events.NewMessage(pattern="/untrack"),
    )

    await bot.run_until_disconnected()
    await http_client.close()


if __name__ == '__main__':
    asyncio.run(main())
