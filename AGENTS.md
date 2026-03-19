# AGENTS.md

This file gives AI agents brief project guidance and points to per-project docs for details.

## Quick Orientation

AI Content Organizer is a Python system with:
- FastAPI backend for content management, knowledge base, and RAG
- Telegram bot as the user interface
- PostgreSQL storage
- Local LLM via LM Studio at http://192.168.1.152:1234

This monorepo contains two fully independent projects that only communicate over HTTP.

## Where To Find Details

Common documentation (docs):
- System organization and architecture: [docs/service_architecture.md](docs/service_architecture.md)
- Code conventions and practices: [docs/code_conventions.md](docs/code_conventions.md)

Backend documentation (backend/docs):
- Project summary and status: [backend/docs/project_overview.md](backend/docs/project_overview.md)
- Setup and workflow: [backend/docs/building_the_project.md](backend/docs/building_the_project.md)
- Backend API reference: [backend/docs/api_endpoints.md](backend/docs/api_endpoints.md)
- Backend notes on architecture: [backend/docs/service_architecture.md](backend/docs/service_architecture.md)

Bot documentation (bot/docs):
Bot overview and setup: [bot/README.md](bot/README.md)
Bot code conventions: [bot/docs/code_conventions.md](bot/docs/code_conventions.md)
Bot testing instructions: [bot/docs/running_tests.md](bot/docs/running_tests.md)

Quick start for humans: [README.md](README.md)

## Key Rules For Agents

- Backend and bot are separate projects with no shared Python code.
- All bot communication goes through backend HTTP APIs.
- Configuration uses per-project environment files; never commit them.
- Use uv and venv for dependency management.
- Follow the conventions in the docs before adding or changing features.

Currently implemented/planned:
- ✅ LinkedIn content ingestion (URL-based extraction)
- ✅ LLM-powered summarization and categorization
- ✅ Semantic search with embeddings (pgvector)
- ✅ RAG-based Q&A
- 🔲 YouTube video ingestion
- 🔲 Webpage content ingestion
- 🔲 Web UI (would use existing backend API)
- 🔲 Auto-tagging with custom taxonomies
- 🔲 Export/backup functionality
