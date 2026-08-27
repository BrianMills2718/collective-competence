"""Determinism. For a deterministic system a failure here blocks everything else."""

from __future__ import annotations

from src.common.snapshots import state_hash
from src.experiments.sorting.model import ALGOTYPES, SortingWorld


def _run(algotype: str, seed: int, ticks: int, order: str = "shuffled") -> list[str]:
    w = SortingWorld.from_values(
        [8, 2, 6, 1, 9, 3, 7, 4, 5, 0, 14, 11, 13, 10, 12], algotype, order=order, seed=seed
    )
    hashes = [state_hash(w.values)]
    for _ in range(ticks):
        w.step_tick()
        hashes.append(state_hash(w.values))
    return hashes


def test_same_seed_gives_byte_identical_history():
    for algotype in ALGOTYPES:
        assert _run(algotype, 7, 40) == _run(algotype, 7, 40), algotype


def test_different_seeds_diverge_for_a_stochastic_rule():
    # bubble picks a side by coin flip, so the seed must actually matter;
    # if this passes trivially the RNG is not being consulted at all.
    assert _run("bubble", 1, 12) != _run("bubble", 2, 12)


def test_activation_order_changes_the_history():
    # The brief warns that update ordering must never be hidden. If these agree,
    # the declared order is not reaching the scheduler.
    assert _run("bubble", 3, 12, order="index") != _run("bubble", 3, 12, order="reverse_index")


def test_all_algotypes_sort_a_shuffled_array():
    for algotype in ALGOTYPES:
        w = SortingWorld.from_values(list(reversed(range(20))), algotype, seed=5)
        w.run(6000)
        assert w.values == sorted(w.values), f"{algotype} left {w.values}"
