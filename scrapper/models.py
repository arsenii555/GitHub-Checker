"""Models for scrapper."""
from pydantic import BaseModel


class Link(BaseModel):
    """Model for links."""

    url: str
    user_id: int


class User(BaseModel):
    """Model for users."""

    user_id: int
