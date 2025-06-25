import pytest
from unittest.mock import AsyncMock, MagicMock
from scrapper.check_github import GitHubChecker


@pytest.fixture
def mock_checker():
    """Fixture to mock GitHub checker."""
    config = MagicMock()
    reader = MagicMock()
    writer = MagicMock()
    client = AsyncMock()

    checker = GitHubChecker(config, reader, writer, client)
    checker.get_repo_hash = AsyncMock()
    return checker


@pytest.mark.asyncio
async def test_check_for_updates_with_change(mock_checker):
    """Test for updates."""
    mock_checker.reader.read_hash.return_value = "old_hash"
    mock_checker.get_repo_hash.return_value = "new_hash"

    result = await mock_checker.check_for_updates("https://github.com/octocat/repo")
    assert result is True
    mock_checker.writer.write_hash.assert_called_with(
        "https://github.com/octocat/repo", "new_hash"
    )


@pytest.mark.asyncio
async def test_check_for_updates_no_change(mock_checker):
    """Test for updates without change."""
    mock_checker.reader.read_hash.return_value = "same_hash"
    mock_checker.get_repo_hash.return_value = "same_hash"

    result = await mock_checker.check_for_updates("https://github.com/octocat/repo")
    assert result is False


@pytest.mark.asyncio
async def test_check_for_updates_first_check(mock_checker):
    """Test first repository check"""
    mock_checker.reader.read_hash.return_value = None
    mock_checker.get_repo_hash.return_value = "initial_hash"

    result = await mock_checker.check_for_updates("https://github.com/octocat/repo")
    assert result is False
    mock_checker.writer.write_hash.assert_called_with(
        "https://github.com/octocat/repo", "initial_hash"
    )


@pytest.mark.asyncio
async def test_check_all_repositories(mock_checker):
    """Test for checking all repositories."""
    mock_checker.reader.links_users_hash = {
        "https://github.com/octocat/repo1": (set([123, 456]), "hash1"),
        "https://github.com/octocat/repo2": (set([123]), "hash2"),
    }

    mock_checker.check_for_updates = AsyncMock(side_effect=[True, False])

    await mock_checker.check_all_repositories()

    assert mock_checker.client.send_notification.await_count == 2

    calls = mock_checker.client.send_notification.await_args_list

    first_call_note = calls[0].args[0]
    assert first_call_note["user_id"] in (123, 456)
    assert first_call_note["url"] == "https://github.com/octocat/repo1"
    assert first_call_note["message"] == "update"

    second_call_note = calls[1].args[0]
    assert second_call_note["user_id"] in (123, 456)
    assert second_call_note["url"] == "https://github.com/octocat/repo1"
    assert second_call_note["message"] == "update"
