# API Endpoints

Complete specification of backend endpoints.

## Overview

All endpoints are scoped to user_id for per-user data isolation.
Base URL: http://localhost:8000/api

## Content Ingestion

### POST /api/{user_id}/content/extract

Extract content from a LinkedIn URL and return a preview plus AI suggestions.

Request body:
```json
{
  "url": "https://linkedin.com/feed/update/urn:..."
}
```

Response:
```json
{
  "title": "Post Title",
  "preview": "First 200 characters...",
  "suggested_summary": "AI-generated summary",
  "suggested_categories": [
    {"id": 1, "name": "AI", "confidence": 0.95}
  ]
}
```

### POST /api/{user_id}/content/confirm

Save extracted content with user-selected categories and summary.

Request body:
```json
{
  "title": "Post Title",
  "extracted_text": "Full content",
  "source_url": "https://linkedin.com/...",
  "category_ids": [1, 2],
  "summary": "User summary"
}
```

Response:
```json
{
  "content_id": "uuid-here",
  "saved_at": "2026-02-19T13:50:00Z"
}
```

## Knowledge Base

### GET /api/{user_id}/knowledge/search

Query params:
- q (string, required)
- limit (int, optional, default=5)
- offset (int, optional, default=0)

Response:
```json
{
  "query": "AI trends",
  "total": 42,
  "results": [
    {
      "id": "content-uuid-1",
      "title": "Latest AI Breakthroughs",
      "summary": "Discussion of recent AI developments...",
      "source_url": "https://linkedin.com/...",
      "snippet": "These breakthroughs represent a major shift...",
      "relevance_score": 0.98,
      "created_at": "2026-02-15T10:30:00Z"
    }
  ]
}
```

### GET /api/{user_id}/knowledge/categories

Response:
```json
{
  "categories": [
    {"id": 1, "name": "AI", "count": 23}
  ]
}
```

## Chat

### POST /api/{user_id}/chat/ask

Request body:
```json
{
  "query": "What did I save about AI safety?"
}
```

Response:
```json
{
  "answer": "...",
  "sources": [
    {"title": "Post Title", "url": "https://linkedin.com/...", "snippet": "..."}
  ]
}
```

### GET /api/{user_id}/chat/history

Response:
```json
[
  {"query": "...", "response": "...", "timestamp": "2026-02-19T13:50:00Z"}
]
```
