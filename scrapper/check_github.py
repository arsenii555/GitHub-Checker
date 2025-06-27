"""GitHub checker."""
import aiohttp
from .utils import extract_owner_repo


class GitHubChecker:
    """GitHub checker class."""

    def __init__(self, config, reader, writer, client):
        """Initialize GitHub checker."""
        self.config = config
        self.writer = writer
        self.reader = reader
        self.client = client
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.config.github_api_key}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    async def get_repo_hash(self, repo_url: str) -> int | None:
        """Get current repo hash."""
        try:
            owner, repo = extract_owner_repo(repo_url)

            async with aiohttp.ClientSession() as session:
                url = f"https://api.github.com/repos/{owner}/{repo}"
                async with session.get(url, headers=self.headers) as response:
                    data = await response.json()
                    return hash(str(data))
        except Exception as e:
            print("Error getting info from GitHub", e)
            return None

    async def check_for_updates(self, repo_url: str) -> bool:
        """Check for updates and update state atomically."""
        current_hash = await self.get_repo_hash(repo_url)
        if not current_hash:
            return False
        last_hash = self.reader.read_hash(repo_url)
        if last_hash and last_hash != current_hash:
            self.writer.write_hash(repo_url, current_hash)
            return True
        if not last_hash:
            self.writer.write_hash(repo_url, current_hash)
        return False

    async def check_all_repositories(self) -> None:
        """Check all repositories for updates."""
        for url in self.reader.links_users_hash:
            if await self.check_for_updates(url):
                users, _ = self.reader.links_users_hash[url]
                for user_id in users:
                    note = {"user_id": user_id, "url": url, "message": "update"}
                    print(note)
                    await self.client.send_notification(note)
