"""Notification server functionality."""
from aiohttp import web
from telethon import TelegramClient
from .translation import load_translations


async def handle_notification(request: web.Request) -> web.Response:
    """Handle notifications from Scrapper."""
    try:
        data = await request.json()

        bot: TelegramClient = request.app["bot"]
        user_id = data["user_id"]
        url = data["url"]
        locale = data["locale"]
        _ = load_translations(locale)
        await bot.send_message(
            entity=user_id,
            message=_("В репозитории {} произошло обновление").format(url)
        )
        return web.json_response(
            {"status": "success", "message": "Notification sent"},
            status=200
        )

    except KeyError as e:
        print(f"Invalid notification format: {e}")
        return web.Response(status=400, text=f"Missing field: {e}")
    except Exception as e:
        print(f"Error handling notification: {str(e)}")
        return web.Response(status=500, text="Internal server error")


async def start_notification_server(bot: TelegramClient, host: str = "localhost", port: int = 9000) -> web.AppRunner:
    """Start HTTP server for notifications."""
    app = web.Application()
    app["bot"] = bot
    app.router.add_post("/notify", handle_notification)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    print(f"Notification server started at http://{host}:{port}")
    return runner
