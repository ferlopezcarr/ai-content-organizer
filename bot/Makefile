.PHONY: setup run test test-coverage lint format

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
