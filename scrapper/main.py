"""Scrapper main module."""
from fastapi import FastAPI
from .models import Link
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
