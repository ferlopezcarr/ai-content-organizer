.PHONY: setup run test test-coverage lint format docker-db docker-db-logs docker-db-stop docker-db-clean

setup:
	uv venv
	uv sync

run:
	. .venv/bin/activate && python -m src

test:
	. .venv/bin/activate && pytest

test-coverage:
	. .venv/bin/activate && pytest --cov=src --cov-report=term-missing --cov-report=html

lint:
	. .venv/bin/activate && ruff check src tests --fix

format:
	. .venv/bin/activate && black src tests

# Database management
docker-db:
	docker-compose up -d postgres

docker-db-logs:
	docker-compose logs -f postgres

docker-db-stop:
	docker-compose down

docker-db-clean:
	docker-compose down -v
