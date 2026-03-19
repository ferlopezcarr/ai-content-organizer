"""Import tests for backend modules."""

import importlib


def test_imports_do_not_fail():
    """All backend modules should import cleanly."""
    modules = [
        "config",
        "config.settings",
        "config.database",
        "config.logging_config",
        "infrastructure",
        "infrastructure.api.app",
        "application",
        "domain",
    ]

    for module_name in modules:
        importlib.import_module(module_name)
