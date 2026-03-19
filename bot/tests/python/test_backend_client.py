"""Backend client tests."""

import importlib

import pytest


class DummyResponse:
    """Simple response stub for httpx calls."""

    def __init__(self, payload):
        self._payload = payload
        self.raise_for_status_called = False

    def raise_for_status(self):
        self.raise_for_status_called = True

    def json(self):
        return self._payload


class DummyAsyncClient:
    """Async client stub that captures calls."""

    def __init__(self, response_payload):
        self._response_payload = response_payload
        self.calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, json):
        self.calls.append(("post", url, json))
        return DummyResponse(self._response_payload)

    async def get(self, url, params):
        self.calls.append(("get", url, params))
        return DummyResponse(self._response_payload)


@pytest.mark.asyncio
async def test_extract_content(monkeypatch):
    """Extract should POST to the content extract endpoint."""
    backend_client_module = importlib.import_module("clients.backend_client")
    importlib.reload(backend_client_module)

    dummy_client = DummyAsyncClient({"ok": True})
    monkeypatch.setattr(backend_client_module.httpx, "AsyncClient", lambda timeout: dummy_client)

    client = backend_client_module.BackendClient()
    result = await client.extract_content("http://example.com")

    assert result == {"ok": True}
    assert dummy_client.calls == [
        (
            "post",
            "http://localhost:8000/content/extract",
            {"url": "http://example.com"},
        )
    ]


@pytest.mark.asyncio
async def test_confirm_content(monkeypatch):
    """Confirm should POST to the content confirm endpoint."""
    backend_client_module = importlib.import_module("clients.backend_client")
    importlib.reload(backend_client_module)

    dummy_client = DummyAsyncClient({"saved": True})
    monkeypatch.setattr(backend_client_module.httpx, "AsyncClient", lambda: dummy_client)

    client = backend_client_module.BackendClient()
    payload = {"title": "A"}
    result = await client.confirm_content(123, payload)

    assert result == {"saved": True}
    assert dummy_client.calls == [
        ("post", "http://localhost:8000/api/123/content/confirm", payload)
    ]


@pytest.mark.asyncio
async def test_ask_question(monkeypatch):
    """Ask should POST to the chat ask endpoint."""
    backend_client_module = importlib.import_module("clients.backend_client")
    importlib.reload(backend_client_module)

    dummy_client = DummyAsyncClient({"answer": "ok"})
    monkeypatch.setattr(backend_client_module.httpx, "AsyncClient", lambda: dummy_client)

    client = backend_client_module.BackendClient()
    result = await client.ask_question(321, "hello")

    assert result == {"answer": "ok"}
    assert dummy_client.calls == [
        (
            "post",
            "http://localhost:8000/api/321/chat/ask",
            {"query": "hello"},
        )
    ]


@pytest.mark.asyncio
async def test_search_knowledge(monkeypatch):
    """Search should GET the knowledge search endpoint."""
    backend_client_module = importlib.import_module("clients.backend_client")
    importlib.reload(backend_client_module)

    dummy_client = DummyAsyncClient({"results": []})
    monkeypatch.setattr(backend_client_module.httpx, "AsyncClient", lambda: dummy_client)

    client = backend_client_module.BackendClient()
    result = await client.search_knowledge(42, "query", limit=7)

    assert result == {"results": []}
    assert dummy_client.calls == [
        (
            "get",
            "http://localhost:8000/api/42/knowledge/search",
            {"q": "query", "limit": 7},
        )
    ]
