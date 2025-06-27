"""Reader."""


class Reader:
    """Data reader class."""

    def __init__(self, users_links, links_users_hash):
        """Initialise the data reader."""
        self.users_links = users_links
        self.links_users_hash = links_users_hash

    def read_hash(self, link: str) -> str | None:
        """Read the hash of a link."""
        return self.links_users_hash[link][1]

    def get_repos_to_check(self):
        """Get the list of repos to check."""
        return self.links_users_hash.keys()
