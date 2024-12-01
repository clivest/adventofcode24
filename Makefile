.PHONY: test format lint all

test:
	pytest tests


format:
	ruff format

lint:
	ruff check
	mypy aoc24 tests
	ruff format --check

all: format lint test