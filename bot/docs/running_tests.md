# Running Bot Tests

## Test Structure

```
bot/tests/
├── python/
│   ├── conftest.py
│   ├── test_backend_client.py
│   ├── test_imports.py
│   ├── test_main.py
│   ├── test_settings.py
│   ├── test_start_handler.py
│   └── fixtures/
```

## Run Tests

```bash
cd bot
source .venv/bin/activate
make test
```

## Coverage

```bash
make test-coverage
```

## Tips

- Mock backend_client for handler tests
- Keep Telegram objects in fixtures for reuse
- Use async fixtures and pytest-asyncio for async handler tests
