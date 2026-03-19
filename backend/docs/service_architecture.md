# Backend Architecture Notes

Common architecture details live in [docs/service_architecture.md](../../docs/service_architecture.md).

This file focuses on backend-specific notes.

## Backend Components

### Content Ingestion

Flow:
1. Bot sends POST /api/{user_id}/content/extract
2. Backend extracts content from URL
3. LLM suggests summary and categories
4. Bot confirms and POST /api/{user_id}/content/confirm
5. Content is saved to PostgreSQL

### Knowledge Base

- Content is indexed for semantic search
- Users query via GET /api/{user_id}/knowledge/search
- Categories are listed via GET /api/{user_id}/knowledge/categories

### Chat / RAG

- Bot sends POST /api/{user_id}/chat/ask
- Backend retrieves context and calls LLM
- Response includes answer and sources
