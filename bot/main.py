"""Main TG Bot module."""
import asyncio
from telethon import TelegramClient, events
from .settings import TGBotSettings
from .client import HTTPClient
from .notification import start_notification_server
from functools import partial
from .handlers import (start_cmd_handler,
                       help_cmd_handler,
                       list_cmd_handler,
                       track_cmd_handler,
                       untrack_cmd_handler,
                       language_cmd_handler,
                       set_language_callback)

settings = TGBotSettings()
bot_url = settings.bot_url
http, host, port = bot_url.split(":")
host = host.strip("//")
port = int(port)


async def main():
    """Run TG Bot and http client."""
    bot = await TelegramClient("bot_session", settings.api_id, settings.api_hash).start(bot_token=settings.token)

    http_client = HTTPClient(settings.scrapper_url)
    await http_client.start()

    start_handler = partial(start_cmd_handler, http_client)
    help_handler = partial(help_cmd_handler, http_client)
    track_handler = partial(track_cmd_handler, http_client)
    untrack_handler = partial(untrack_cmd_handler, http_client)
    list_handler = partial(list_cmd_handler, http_client)
    language_handler = partial(language_cmd_handler, http_client)

    bot.add_event_handler(
        start_handler,
        events.NewMessage(pattern="/start"),
    )

    bot.add_event_handler(
        help_handler,
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

    bot.add_event_handler(
        language_handler,
        events.NewMessage(pattern="/language"),
    )

    bot.add_event_handler(
        partial(set_language_callback, http_client),
        events.CallbackQuery(pattern=rb"set_lang:(ru|en)"),
    )

    runner = await start_notification_server(bot=bot, host=host, port=port)
    try:
        await bot.run_until_disconnected()
        print("Bot disconnected")
    finally:
        print("Shutting down...")
        await runner.cleanup()
        await http_client.close()
        print("HTTP client and notification server stopped")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
