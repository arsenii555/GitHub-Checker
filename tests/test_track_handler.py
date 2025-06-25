import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.handlers.track import track_cmd_handler


@pytest.mark.asyncio
async def test_track_handler_valid_url_new_link():
    """Test for valid url new link."""
    mock_http_client = AsyncMock()
    mock_event = AsyncMock()

    mock_event.chat_id = 12345
    mock_event.input_chat = "input_chat_entity"

    mock_message = MagicMock()
    mock_message.id = 123
    mock_message.text = "/track https://github.com/octocat/hello-world"
    mock_event.message = mock_message

    mock_http_client.list_links.return_value = []

    mock_http_client.track_link.return_value = True

    await track_cmd_handler(mock_http_client, mock_event)

    mock_http_client.list_links.assert_awaited_once_with(user_id=12345)

    mock_http_client.track_link.assert_awaited_once_with(
        user_id=12345,
        link="https://github.com/octocat/hello-world"
    )

    mock_event.client.send_message.assert_awaited_once_with(
        entity="input_chat_entity",
        message="Ссылка\nhttps://github.com/octocat/hello-world\nуспешно добавлена для отслеживания ✅",
        reply_to=mock_message
    )


@pytest.mark.asyncio
async def test_track_handler_valid_url_existing_link():
    """Test for valid url existing link."""
    mock_http_client = AsyncMock()
    mock_event = AsyncMock()

    mock_event.chat_id = 12345
    mock_event.input_chat = "input_chat_entity"

    mock_message = MagicMock()
    mock_message.id = 123
    mock_message.text = "/track https://github.com/octocat/hello-world"
    mock_event.message = mock_message

    mock_http_client.list_links.return_value = ["https://github.com/octocat/hello-world"]

    await track_cmd_handler(mock_http_client, mock_event)

    mock_http_client.list_links.assert_awaited_once_with(user_id=12345)

    mock_http_client.track_link.assert_not_awaited()

    mock_event.client.send_message.assert_awaited_once_with(
        entity="input_chat_entity",
        message="👀Данная ссылка уже отслеживается 👀",
        reply_to=mock_message
    )


@pytest.mark.asyncio
async def test_track_handler_invalid_url():
    """Test for invalid url."""
    mock_http_client = AsyncMock()
    mock_event = AsyncMock()

    mock_event.chat_id = 12345
    mock_event.input_chat = "input_chat_entity"
    mock_event.message.text = "/track not-a-valid-url"
    mock_event.message.id = 123

    await track_cmd_handler(mock_http_client, mock_event)

    mock_http_client.list_links.assert_not_awaited()
    mock_http_client.track_link.assert_not_awaited()

    mock_event.client.send_message.assert_awaited_once_with(
        entity="input_chat_entity",
        message="❌ Некорректная ссылка. Отправьте ссылку на GitHub репозиторий.",
        reply_to=mock_event.message
    )


@pytest.mark.asyncio
async def test_track_handler_invalid_command_format():
    """Test for invalid command format."""
    mock_http_client = AsyncMock()
    mock_event = AsyncMock()

    mock_event.chat_id = 12345
    mock_event.input_chat = "input_chat_entity"
    mock_event.message.text = "/track"
    mock_event.message.id = 123

    await track_cmd_handler(mock_http_client, mock_event)

    mock_http_client.list_links.assert_not_awaited()
    mock_http_client.track_link.assert_not_awaited()

    mock_event.client.send_message.assert_awaited_once_with(
        entity="input_chat_entity",
        message="Отправьте сообщение вида:\n/track <link>",
        reply_to=mock_event.message
    )
