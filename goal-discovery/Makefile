.PHONY: sync baseline branch test lint dayone

sync:
	uv sync

baseline:
	uv run python -m src.experiments.sorting.run baseline

branch:
	uv run python -m src.experiments.sorting.run branch

test:
	uv run pytest -q

lint:
	uv run ruff check src tests

## dayone: everything the day-one milestone asks for, from a clean checkout
dayone: sync test baseline branch
	@echo
	@echo "day-one milestone complete -- see results/$$(cat results/LATEST)"
