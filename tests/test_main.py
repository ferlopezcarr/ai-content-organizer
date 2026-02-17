from src import __main__ as main_module


def test_main_callable():
    assert hasattr(main_module, "main") and callable(main_module.main)
