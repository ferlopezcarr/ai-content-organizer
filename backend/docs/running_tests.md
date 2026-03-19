# Running Backend Tests

## Test Structure

```
backend/tests/
├── python/
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_database.py
│   ├── test_imports.py
│   ├── test_main.py
│   ├── test_settings.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── resources/
    ├── health.http
    ├── content.http
    ├── knowledge.http
    └── chat.http
```

## Run Tests

```bash
cd backend
source .venv/bin/activate
make test
```

## Coverage

```bash
make test-coverage
```

## Manual API Testing

Use REST Client .http files in `tests/resources/` to test API endpoints:

- `health.http` — Health check
- `content.http` — Content extraction and confirmation
- `knowledge.http` — Knowledge base search and categories
- `chat.http` — Chat questions and history

Open any .http file in VS Code (or compatible editor with REST Client extension) and click "Send Request" above each request.

## Tips

- Python tests have pytest fixtures for mocking; see conftest.py
- REST Client tests require the backend running on localhost:8000
