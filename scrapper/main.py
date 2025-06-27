"""Scrapper main module."""
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from .models import Link, User
from .settings import ScrapperSettings
from collections import defaultdict
from .check_github import GitHubChecker
from .reader import Reader
from .writer import Writer
from .client import HTTPClient
settings = ScrapperSettings()

users_links = defaultdict(set)
links_users_hash = dict()


reader = Reader(users_links, links_users_hash)
writer = Writer(links_users_hash)
client = HTTPClient(settings.bot_url)
checker = GitHubChecker(settings, reader, writer, client)


@asynccontextmanager
async def scrapper_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Scrapper lifespan."""
    print("Starting scrapper background tasks")
    app.state.reader = reader
    app.state.writer = writer
    app.state.client = client
    await app.state.client.start()
    app.state.checker = checker
    app.state.check_task = asyncio.create_task(check_repositories_periodically(app))

    yield

    app.state.check_task.cancel()
    try:
        await app.state.check_task
    except asyncio.CancelledError:
        print("Background task cancelled successfully")
    await app.state.client.close()

app = FastAPI(title="Scrapper", lifespan=scrapper_lifespan)


async def check_repositories_periodically(app, interval: int = 10):
    """Check repositories periodically."""
    checker: GitHubChecker = app.state.checker
    while True:
        try:
            print("Starting repositories check cycle")
            await checker.check_all_repositories()
        except Exception as e:
            print(f"Error in repository check: {str(e)}")
        finally:
            await asyncio.sleep(interval)


@app.post("/track")
async def track_link(link: Link):
    """Track link endpoint."""
    user_id = link.user_id
    link = link.url
    users_links[user_id].add(link)
    if link not in links_users_hash:
        links_users_hash[link] = [set(), None]
    links_users_hash[link][0].add(user_id)
    return {"message": "link added", "success": True}


@app.post("/untrack")
async def untrack_link(link: Link):
    """Untrack link endpoint."""
    user_id = link.user_id
    link = link.url
    users_links[user_id].discard(link)
    links_users_hash[link][0].discard(user_id)
    return {"message": "link removed", "success": True}


@app.get("/list")
async def list_links(user: User):
    """List links endpoint."""
    user_id = user.user_id
    links = list(users_links[user_id])
    return {"links": links}
