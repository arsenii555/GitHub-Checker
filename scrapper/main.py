"""Scrapper main module."""
from fastapi import FastAPI
from .models import Link, User
from collections import defaultdict


users_links = defaultdict(set)
app = FastAPI(title="Scrapper")


@app.post("/track")
async def track_link(link: Link):
    """Track link endpoint."""
    user = link.user_id
    link = link.url
    users_links[user].add(link)
    return {"message": "link added", "success": True}


@app.post("/untrack")
async def untrack_link(link: Link):
    """Untrack link endpoint."""
    user = link.user_id
    link = link.url
    users_links[user].discard(link)
    return {"message": "link removed", "success": True}


@app.get("/list")
async def list_links(user: User):
    """List links endpoint."""
    user_id = user.user_id
    links = list(users_links[user_id])
    return {"links": links}
