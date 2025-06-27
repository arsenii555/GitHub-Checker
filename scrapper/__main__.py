"""Start scrapper."""
from scrapper.main import app
from .settings import ScrapperSettings
import uvicorn

settings = ScrapperSettings()
scrapper_url = settings.scrapper_url
http, host, port = scrapper_url.split(":")
host = host.strip("//")
port = int(port)


def cli_main():
    """Точка входа для setuptools script."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    try:
        uvicorn.run(app, host=host, port=port)
    except KeyboardInterrupt:
        print("Interrupted by user")
