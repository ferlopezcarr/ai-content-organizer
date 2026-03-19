"""Tests for add handler."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from handlers.add_handler import handle_add


class DummyChat:
    """Minimal chat stub."""

    def __init__(self, chat_id):
        self.id = chat_id


class DummyMessage:
    """Minimal message stub."""

    def __init__(self, chat_id):
        self.chat = DummyChat(chat_id)
        self.reply_text = AsyncMock(return_value=MagicMock(delete=AsyncMock()))


class DummyUpdate:
    """Minimal update stub."""

    def __init__(self, chat_id):
        self.effective_chat = DummyChat(chat_id)
        self.message = DummyMessage(chat_id)


class DummyContext:
    """Minimal context stub."""

    def __init__(self, args=None):
        self.args = args or []


@pytest.mark.asyncio
async def test_handle_add_no_url():
    """Should show usage message when no URL provided."""
    update = DummyUpdate(chat_id=10)
    context = DummyContext(args=[])

    await handle_add(update, context)

    update.message.reply_text.assert_called_once()
    call_text = update.message.reply_text.call_args[0][0]
    assert "provide a URL" in call_text
    assert "Usage:" in call_text


@pytest.mark.asyncio
@patch("handlers.add_handler.backend_client.extract_content")
async def test_handle_add_success(mock_extract):
    """Should extract content and display success message."""
    mock_extract.return_value = {
        "url": "https://linkedin.com/posts/123",
        "title": "Test Post",
        "author": "John Doe",
        "text": "This is a test post about AI.",
        "metadata": {"image": "https://example.com/image.jpg"},
    }

    update = DummyUpdate(chat_id=10)
    context = DummyContext(args=["https://linkedin.com/posts/123"])

    await handle_add(update, context)

    mock_extract.assert_called_once_with("https://linkedin.com/posts/123")

    # Should send processing message, delete it, then send result
    assert update.message.reply_text.call_count == 2

    # Check the final message
    final_call_text = update.message.reply_text.call_args_list[1][0][0]
    assert "Content Extracted Successfully" in final_call_text
    assert "Test Post" in final_call_text
    assert "John Doe" in final_call_text


@pytest.mark.asyncio
@patch("handlers.add_handler.backend_client.extract_content")
async def test_handle_add_unsupported_url(mock_extract):
    """Should show error message for unsupported URLs."""
    # Simulate HTTP 400 error with unsupported URL detail
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"detail": "Unsupported URL"}

    mock_extract.side_effect = httpx.HTTPStatusError(
        "Bad Request", request=MagicMock(), response=response
    )

    update = DummyUpdate(chat_id=10)
    context = DummyContext(args=["https://twitter.com/user"])

    await handle_add(update, context)

    # Should send processing message then error message
    assert update.message.reply_text.call_count == 2

    # Check error message
    error_call_text = update.message.reply_text.call_args_list[1][0][0]
    assert "Failed to extract content" in error_call_text
    assert "not supported" in error_call_text


@pytest.mark.asyncio
@patch("handlers.add_handler.backend_client.extract_content")
async def test_handle_add_network_error(mock_extract):
    """Should show network error message on connection failure."""
    mock_extract.side_effect = httpx.RequestError("Connection refused")

    update = DummyUpdate(chat_id=10)
    context = DummyContext(args=["https://linkedin.com/posts/123"])

    await handle_add(update, context)

    # Should send processing message then error message
    assert update.message.reply_text.call_count == 2

    # Check error message
    error_call_text = update.message.reply_text.call_args_list[1][0][0]
    assert "Network Error" in error_call_text
    assert "backend service" in error_call_text


@pytest.mark.asyncio
@patch("handlers.add_handler.backend_client.extract_content")
async def test_handle_add_extraction_failure(mock_extract):
    """Should show error message when extraction fails."""
    # Simulate HTTP 400 error with extraction failure
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"detail": "Failed to extract content"}

    mock_extract.side_effect = httpx.HTTPStatusError(
        "Bad Request", request=MagicMock(), response=response
    )

    update = DummyUpdate(chat_id=10)
    context = DummyContext(args=["https://linkedin.com/posts/invalid"])

    await handle_add(update, context)

    # Should send processing message then error message
    assert update.message.reply_text.call_count == 2

    # Check error message
    error_call_text = update.message.reply_text.call_args_list[1][0][0]
    assert "Failed to extract content" in error_call_text


@pytest.mark.asyncio
@patch("handlers.add_handler.backend_client.extract_content")
async def test_handle_add_long_text_preview(mock_extract):
    """Should truncate long text in preview."""
    long_text = "A" * 500
    mock_extract.return_value = {
        "url": "https://linkedin.com/posts/123",
        "title": "Long Post",
        "author": "Jane Doe",
        "text": long_text,
        "metadata": {},
    }

    update = DummyUpdate(chat_id=10)
    context = DummyContext(args=["https://linkedin.com/posts/123"])

    await handle_add(update, context)

    # Check the final message has truncated text
    final_call_text = update.message.reply_text.call_args_list[1][0][0]
    assert "..." in final_call_text
    # Should not contain the full text
    assert long_text not in final_call_text
