# Service Architecture

This document covers system-wide architecture and organization shared by backend and bot.

## High-Level Layout

- Backend: FastAPI service for content ingestion, knowledge base, and RAG
- Bot: Telegram interface that calls backend over HTTP
- Storage: PostgreSQL
- LLM: LM Studio (OpenAI-compatible API)

## Communication

- Bot and backend communicate over HTTP only
- No shared Python code between projects
- All API routes are scoped by user_id for per-user isolation

## Hexagonal Architecture (Backend)

The backend follows hexagonal architecture (Ports and Adapters):

1. Domain Layer
   - Pure business logic
   - No infrastructure dependencies
   - Location: backend/src/domain/

2. Application Layer
   - Use cases and orchestration
   - Coordinates domain logic with infrastructure
   - Location: backend/src/application/

3. Infrastructure Layer
   - External adapters and implementations
   - Database access, external clients, API routes
   - Location: backend/src/infrastructure/

Inbound adapters (driving the app):
- API routes and controllers in backend/src/infrastructure/api/

Outbound adapters (driven by the app):
- External clients in backend/src/infrastructure/clients/
- Data repositories in backend/src/infrastructure/repositories/

## Vertical Slicing

Backend code is organized by feature rather than by layer:

```
backend/src/
├── domain/
│   └── content_ingestion/
│       └── models/
├── application/
│   └── content_ingestion/
│       └── services/
└── infrastructure/
    ├── clients/
    ├── repositories/
    └── api/
```

## Data Flow

1. User sends a command to the bot
2. Bot calls backend API
3. Backend accesses storage and LLM as needed
4. Backend returns a response
5. Bot formats and replies to the user
