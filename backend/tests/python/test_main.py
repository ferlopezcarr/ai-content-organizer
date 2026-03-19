"""Main module tests."""

import importlib.util
from pathlib import Path


def load_main_module():
    """Load backend __main__ from file path."""
    module_path = Path(__file__).resolve().parents[2] / "src" / "__main__.py"
    spec = importlib.util.spec_from_file_location("backend_main", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_main_invokes_uvicorn(monkeypatch):
    """Main should invoke uvicorn with expected settings."""
    main_module = load_main_module()

    calls = {}

    def fake_run(app, host, port, reload):
        calls["app"] = app
        calls["host"] = host
        calls["port"] = port
        calls["reload"] = reload

    monkeypatch.setattr(main_module.uvicorn, "run", fake_run)

    main_module.main()

    assert calls["app"] == "infrastructure.api.app:app"
    assert calls["host"] == main_module.settings.backend_host
    assert calls["port"] == main_module.settings.backend_port
    assert calls["reload"] == (main_module.settings.environment == "development")
