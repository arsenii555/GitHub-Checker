from bot.utils import extract_owner_repo
import pytest


@pytest.mark.parametrize("url, expected", [
    # Стандартные URL
    ("https://github.com/octocat/Hello-World", ("octocat", "Hello-World")),
    ("http://github.com/octocat/hello-world", ("octocat", "hello-world")),
    ("https://github.com/octocat/hello-world/", ("octocat", "hello-world")),

    # URL с поддиректориями
    ("https://github.com/octocat/hello-world/tree/main", ("octocat", "hello-world")),
    ("https://github.com/octocat/hello-world/issues/123", ("octocat", "hello-world")),

    # URL с .git
    ("https://github.com/octocat/hello-world.git", ("octocat", "hello-world")),
    ("http://github.com/octocat/hello-world.git", ("octocat", "hello-world")),

    # SSH форматы
    ("git@github.com:octocat/hello-world.git", ("octocat", "hello-world")),
    ("git@github.com:octocat/Hello-World", ("octocat", "Hello-World")),

    # GitHub API URL
    ("https://api.github.com/repos/octocat/hello-world", ("octocat", "hello-world")),

    # Регистр и спецсимволы
    ("https://github.com/python/cpython", ("python", "cpython")),
    ("https://github.com/django/django", ("django", "django")),
    ("https://github.com/user/project-name", ("user", "project-name")),
    ("https://github.com/user/project.name", ("user", "project.name")),
    ("https://github.com/USER/REPO", ("USER", "REPO")),

    # Невалидные URL
    ("https://github.com/invalid", None),
    ("https://example.com/octocat/hello-world", None),
    ("not-a-url", None),
    ("https://github.com/", None),
    ("https://github.com//", None),
    ("", None),
])
def test_extract_owner_repo(url, expected):
    assert extract_owner_repo(url) == expected


def test_case_sensitivity():
    """GitHub is case-sensitive, so we preserve case"""
    assert extract_owner_repo("https://github.com/OctoCat/Hello-World") == ("OctoCat", "Hello-World")
    assert extract_owner_repo("https://github.com/octocat/hello-world") == ("octocat", "hello-world")
    assert extract_owner_repo("https://github.com/OCTOCAT/HELLO-WORLD") == ("OCTOCAT", "HELLO-WORLD")


def test_special_characters():
    """Test special characters in owner/repo names"""
    assert extract_owner_repo("https://github.com/user-name/repo_name") == ("user-name", "repo_name")
    assert extract_owner_repo("https://github.com/user.name/repo.name") == ("user.name", "repo.name")
    assert extract_owner_repo("https://github.com/123user/456repo") == ("123user", "456repo")
    assert extract_owner_repo("https://github.com/üser/näme") == ("üser", "näme")
