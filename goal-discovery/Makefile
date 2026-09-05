.PHONY: sync baseline branch test lint dayone

# The extras are not optional here. tests/test_scale_evidence.py and
# tests/test_sorting_laboratory.py import holoviews unconditionally, so a bare
# `uv sync` leaves a checkout on which `make test` reports 2 collection errors
# and runs 0 tests -- while the authoring machine, which has the extras, reports
# a full green suite. `make dayone` claims to work "from a clean checkout" and
# did not. Skipping the two modules was rejected: that trades a loud failure for
# quiet lost coverage, the defect pattern this repository already had to repair.
#
# --all-extras rather than the three the README names: measured on this checkout,
# the README's documented verification command runs 456 tests and the full extra
# set runs 467. Optional-dependency modules that are genuinely absent still skip
# with a stated reason, which is the correct behaviour; under-installing turns
# eleven of them into tests that simply never run.
EXTRAS := --all-extras

sync:
	uv sync $(EXTRAS)

baseline:
	uv run python -m src.experiments.sorting.run baseline

branch:
	uv run python -m src.experiments.sorting.run branch

test:
	uv run $(EXTRAS) pytest -q

lint:
	uv run ruff check src tests

## dayone: everything the day-one milestone asks for, from a clean checkout
dayone: sync test baseline branch
	@echo
	@echo "day-one milestone complete -- see results/$$(cat results/LATEST)"
