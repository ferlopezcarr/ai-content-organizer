# Project Overview

AI Content Organizer is a Python system with a FastAPI backend and a Telegram bot. The backend manages content ingestion, knowledge base search, and RAG-based Q&A over a PostgreSQL database using a local LLM provided by LM Studio.

## Key Features

- Content ingestion from LinkedIn URLs
- Summarization and categorization with a local LLM
- Semantic search over a per-user knowledge base
- RAG-based question answering with sources
- Clean separation between backend and bot (HTTP only)

## Current Status

- Monorepo structure initialized
- Backend scaffolding ready
- Bot scaffolding ready
- Core features pending implementation

## Architecture Snapshot

User -> Telegram Bot <-> FastAPI Backend <-> PostgreSQL
                         |
                         +-> LM Studio (Local LLM)

## Next Reading

- Setup and workflow: building_the_project.md
- Architecture details: service_architecture.md
- API contracts: api_endpoints.md
