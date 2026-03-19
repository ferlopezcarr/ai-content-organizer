# Bot Code Conventions

Common conventions live in [docs/code_conventions.md](../../docs/code_conventions.md).

This file covers bot-specific guidance.

## Project Structure

```
src/
├── config/          # Settings
├── clients/         # Backend HTTP client
├── handlers/        # Telegram command handlers
└── bot.py           # Bot initialization
```

## Naming

Files:
- *_handler.py for Telegram handlers
- *_client.py for external clients

Classes:
- PascalCase (BackendClient, AddHandler)

Functions:
- snake_case (handle_add, fetch_content)

## Handler Pattern

Handlers should:
- Validate input early
- Call backend_client methods
- Handle errors and return a clear message
- Keep formatting logic in handlers/utils.py
