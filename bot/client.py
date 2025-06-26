"""HTTP client."""
from typing import List

import aiohttp


class HTTPClient:
    """HTTP client."""

    def __init__(self, base_url: str):
        """Initialize HTTP client."""
        self.base_url = base_url
        self.session = None

    async def start(self):
        """Create session."""
        self.session = aiohttp.ClientSession()

    async def close(self):
        """Close session."""
        if self.session:
            self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs):
        """Send request and return response."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with self.session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json() if response.status != 204 else None

    async def track_link(self, user_id: int, link: str) -> bool:
        """Send track link request."""
        payload = {"url": link, "user_id": user_id}
        response = await self._request("POST", "/track", json=payload)
        return response is not None and response.get("success", False)

    async def untrack_link(self, user_id: int, link: str) -> bool:
        """Send untrack link request."""
        payload = {"url": link, "user_id": user_id}
        response = await self._request("POST", "/untrack", json=payload)
        return response is not None and response.get("success", False)

    async def list_links(self, user_id: int) -> List[str]:
        """Send list links request."""
        payload = {"user_id": user_id}
        response = await self._request("GET", "/list", json=payload)
        return response.get("links", []) if response else []
