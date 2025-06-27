"""HTTP client."""
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

    async def send_notification(self, note):
        """Send notification."""
        payload = note
        await self._request("POST", "notify", json=payload)
