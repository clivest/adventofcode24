.PHONY: test format lint all

test:
	poetry run pytest tests


format:
	poetry run ruff format

lint:
	poetry run ruff check
	poetry run mypy aoc24 tests
	poetry run ruff format --check

all: format lint test