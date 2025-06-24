"""Writer."""


class Writer:
    """Data writer class."""

    def __init__(self, links_user_hash):
        """Initialize writer."""
        self.links_user_hash = links_user_hash

    def write_hash(self, link: str, new_hash: str):
        """Write hash."""
        self.links_user_hash[link][1] = new_hash
