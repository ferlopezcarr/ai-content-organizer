"""Settings tests."""

import importlib


def test_settings_defaults(monkeypatch):
    """Settings should use default backend URL when not provided."""
    monkeypatch.delenv("BACKEND_URL", raising=False)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")

    settings_module = importlib.import_module("config.settings")
    importlib.reload(settings_module)

    assert settings_module.settings.backend_url == "http://localhost:8000"


def test_settings_env_override(monkeypatch):
    """Settings should read backend URL from environment."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("BACKEND_URL", "http://example:9999")

    settings_module = importlib.import_module("config.settings")
    importlib.reload(settings_module)

    assert settings_module.settings.backend_url == "http://example:9999"
