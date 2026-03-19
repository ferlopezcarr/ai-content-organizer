"""Settings tests."""

import importlib


def test_settings_env_override(monkeypatch):
    """Settings should read values from environment overrides."""
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("BACKEND_HOST", "127.0.0.1")
    monkeypatch.setenv("BACKEND_PORT", "9000")
    monkeypatch.setenv("LLM_API_URL", "http://example:1234")
    monkeypatch.setenv("LLM_MODEL", "test-model")

    settings_module = importlib.import_module("config.settings")
    importlib.reload(settings_module)

    assert settings_module.settings.backend_host == "127.0.0.1"
    assert settings_module.settings.backend_port == 9000
    assert settings_module.settings.llm_api_url == "http://example:1234"
    assert settings_module.settings.llm_model == "test-model"
