.PHONY: help install test lint type init list next reset clean

help:
	@echo "make install   install deps with uv"
	@echo "make test      run pytest"
	@echo "make lint      run ruff check"
	@echo "make type      run mypy"
	@echo "make init      kubert init  (check tools + create cluster)"
	@echo "make next      kubert next  (run next lesson)"
	@echo "make list      kubert list  (list lessons)"
	@echo "make reset     kubert reset (delete cluster)"
	@echo "make clean     delete .venv and caches"

install:
	uv sync --extra dev

test:
	uv run pytest

lint:
	uv run ruff check .

type:
	uv run mypy

init:
	uv run kubert init

next:
	uv run kubert next

list:
	uv run kubert list

reset:
	uv run kubert reset

clean:
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
