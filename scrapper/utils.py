"""Utility functions."""
import re
from urllib.parse import urlparse


def extract_owner_repo(url: str) -> tuple[str, str] | None:
    """
    Extract owner and repository name from GitHub URL.

    Supports:
    - Standard HTTPS/HTTP URLs
    - SSH URLs (git@github.com:owner/repo.git)
    - GitHub API URLs
    - URLs with .git extension
    - URLs with trailing slashes or subpaths

    Returns (owner, repo) or None if parsing fails.
    """
    ssh_match = re.match(r"git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/]+?)(\.git)?$", url)
    if ssh_match:
        return ssh_match.group("owner"), ssh_match.group("repo")

    parsed = urlparse(url)

    if parsed.netloc == "api.github.com":
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 3 and path_parts[0] == "repos":
            return path_parts[1], path_parts[2]

    if parsed.netloc not in {"github.com", "www.github.com"}:
        return None

    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) < 2:
        return None

    owner = path_parts[0]
    repo = path_parts[1]

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo
