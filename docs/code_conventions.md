# Code Conventions

Common conventions shared by backend and bot. Project-specific additions live in each project docs folder.

## Formatting and Linting

- Formatter: black (100 character line length)
- Linter: ruff (E, F, I rules)

Run from each project:
```bash
make format
make lint
```

## Naming

Files:
- *_service.py for application services
- *_client.py for external clients
- *_repository.py for data access
- *_routes.py for FastAPI routes
- *_handler.py for Telegram handlers

Classes:
- PascalCase (ContentService, BackendClient)

Functions:
- snake_case (extract_content, handle_add)

## Imports

Order:
1. Standard library
2. Third-party
3. Local

## Error Handling

- Validate inputs early
- Return clear, user-facing error messages in bot handlers
- Use structured logging on the backend

## Testing

- Unit tests should focus on pure logic
- Integration tests should cover API boundaries
- Keep fixtures small and reusable
