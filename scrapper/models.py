"""Models for scrapper."""
from pydantic import BaseModel, field_validator
import re


class Link(BaseModel):
    """Model for links."""

    url: str
    user_id: int

    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        """Validate URL format using regex."""
        pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # TLD
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # OR ip
            r'(?::\d+)?'  # port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not pattern.match(v):
            raise ValueError('Invalid URL format')
        return v

    def __str__(self):
        """Return string representation."""
        return f"Link({self.user_id}, {self.url})"

    def __eq__(self, other):
        """Equality check."""
        if not isinstance(other, Link):
            return False
        return self.url == other.url and self.user_id == other.user_id


class User(BaseModel):
    """Model for users."""

    user_id: int

    def __str__(self):
        """Return string representation."""
        return f"User {self.user_id}"

    def __eq__(self, other):
        """Equality check."""
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id


class Locale(BaseModel):
    """Model for locales."""

    locale: str
