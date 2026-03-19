"""Import tests for bot modules."""

import importlib


def test_imports_do_not_fail():
    """All bot modules should import cleanly."""
    modules = [
        "bot",
        "clients",
        "clients.backend_client",
        "config",
        "config.settings",
        "handlers",
        "handlers.start_handler",
    ]

    for module_name in modules:
        importlib.import_module(module_name)
