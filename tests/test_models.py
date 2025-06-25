# tests/unit/test_models.py
import pytest
from scrapper.models import Link, User


def test_link_model_validation():
    """Test link model validation."""
    valid_link = Link(user_id=123, url="https://github.com/octocat/repo")
    assert valid_link.url == "https://github.com/octocat/repo"

    with pytest.raises(ValueError):
        Link(user_id=123, url="invalid-url")


def test_user_model():
    """Test user model"""
    user = User(user_id=12345)
    assert user.user_id == 12345
    assert str(user) == "User 12345"


def test_link_str_representation():
    """Test string representation"""
    link = Link(user_id=123, url="https://example.com")
    assert str(link) == "Link(123, https://example.com)"


def test_link_equality():
    """Test link equality."""
    link1 = Link(user_id=1, url="https://example.com")
    link2 = Link(user_id=1, url="https://example.com")
    link3 = Link(user_id=2, url="https://example.com")

    assert link1 == link2
    assert link1 != link3


def test_user_equality():
    """Test user equality."""
    user1 = User(user_id=123)
    user2 = User(user_id=123)
    user3 = User(user_id=456)

    assert user1 == user2
    assert user1 != user3
