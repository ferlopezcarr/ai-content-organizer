.PHONY: setup setup-backend setup-bot start-backend start-bot db-start db-stop db-clean help

setup-backend:
	cd backend && uv venv && uv sync && cp .env.example .env

setup-bot:
	cd bot && uv venv && uv sync && cp .env.example .env

setup: setup-backend setup-bot
	@echo "✓ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit backend/.env with your settings"
	@echo "2. Edit bot/.env with your Telegram token"
	@echo "3. Run: make db-start"
	@echo "4. Run: make start-backend (Terminal 1)"
	@echo "5. Run: make start-bot (Terminal 2)"

start-backend:
	cd backend && . .venv/bin/activate && python -m src

start-bot:
	cd bot && . .venv/bin/activate && python -m src

db-start:
	cd backend && docker-compose up -d postgres
	@echo "✓ PostgreSQL running at localhost:5432"

db-stop:
	cd backend && docker-compose down

db-clean:
	cd backend && docker-compose down -v

help:
	@echo "=== AI Content Organizer Monorepo ==="
	@echo ""
	@echo "Setup:"
	@echo "  make setup         - Setup both backend and bot"
	@echo "  make setup-backend - Setup backend only"
	@echo "  make setup-bot     - Setup bot only"
	@echo ""
	@echo "Running:"
	@echo "  make db-start      - Start PostgreSQL database"
	@echo "  make start-backend - Run backend API (Terminal 1)"
	@echo "  make start-bot     - Run Telegram bot (Terminal 2)"
	@echo "  make db-stop       - Stop PostgreSQL"
	@echo "  make db-clean      - Clean PostgreSQL data"
	@echo ""
	@echo "See backend/README.md and bot/README.md for more details."