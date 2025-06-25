from bot.handlers.list import list_cmd_handler
from unittest.mock import AsyncMock
import pytest


@pytest.mark.asyncio
async def test_list_handler_with_links():
    """Test /list with links."""
    mock_event = AsyncMock()
    mock_http_client = AsyncMock()

    mock_event.chat_id = 12345
    mock_event.input_chat = "input_chat_entity"

    mock_http_client.list_links.return_value = [
        "https://github.com/octocat/repo1",
        "https://github.com/octocat/repo2"
    ]

    await list_cmd_handler(mock_http_client, mock_event)

    mock_http_client.list_links.assert_awaited_once_with(user_id=12345)

    expected_message = (
        "📋 Ваши отслеживаемые репозитории\n\n"
        "- https://github.com/octocat/repo1\n"
        "- https://github.com/octocat/repo2"
    )

    mock_event.client.send_message.assert_awaited_once_with(
        entity="input_chat_entity",
        message=expected_message,
        reply_to=12345
    )
