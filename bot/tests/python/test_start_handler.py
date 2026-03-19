"""Start handler tests."""

import pytest

from handlers.start_handler import handle_start


class DummyChat:
    """Minimal chat stub."""

    def __init__(self, chat_id):
        self.id = chat_id


class DummyUpdate:
    """Minimal update stub."""

    def __init__(self, chat_id):
        self.effective_chat = DummyChat(chat_id)


class DummyBot:
    """Minimal bot stub."""

    def __init__(self):
        self.calls = []

    async def send_message(self, chat_id, text, parse_mode):
        self.calls.append({"chat_id": chat_id, "text": text, "parse_mode": parse_mode})


class DummyContext:
    """Minimal context stub."""

    def __init__(self):
        self.bot = DummyBot()


@pytest.mark.asyncio
async def test_handle_start_sends_help_message():
    """Start handler should send a help message to the user."""
    update = DummyUpdate(chat_id=10)
    context = DummyContext()

    await handle_start(update, context)

    assert len(context.bot.calls) == 1
    sent = context.bot.calls[0]
    assert sent["chat_id"] == 10
    assert "/add" in sent["text"]
    assert "AI Content Organizer" in sent["text"]
    assert sent["parse_mode"] == "Markdown"
