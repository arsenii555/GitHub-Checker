"""Start bot."""
from .main import main
import asyncio


def cli_main():
    """Точка входа для setuptools script."""
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())
