.PHONY: test format lint all

test:
	pytest tests


format:
	ruff format

lint:
	ruff check
	mypy aoc24 tests

all: format lint test