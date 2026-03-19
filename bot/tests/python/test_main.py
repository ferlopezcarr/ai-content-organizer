"""Main module tests."""

import importlib.util
import logging
from pathlib import Path
from unittest.mock import MagicMock, patch


def load_main_module():
    """Load the bot __main__ module from file path."""
    module_path = Path(__file__).resolve().parents[2] / "src" / "__main__.py"
    spec = importlib.util.spec_from_file_location("bot_main", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_main_logs_startup(caplog):
    """Main should log startup messages and register handlers."""
    caplog.set_level(logging.INFO)

    main_module = load_main_module()

    # Mock the Application to avoid actually connecting to Telegram
    with patch.object(main_module, "Application") as mock_app_class:
        mock_builder = MagicMock()
        mock_app = MagicMock()
        mock_app.run_polling = MagicMock()
        mock_builder.token.return_value.build.return_value = mock_app
        mock_app_class.builder.return_value = mock_builder

        main_module.main()

    # Check log messages
    assert "Starting AI Content Organizer Bot" in caplog.text
    assert "Bot handlers registered" in caplog.text
    assert "Bot is now running" in caplog.text
