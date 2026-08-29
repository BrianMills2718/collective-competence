"""Compatibility gates for the isolated Mesa bubble-sort spike."""

from __future__ import annotations

import json

import pytest

pytest.importorskip("mesa", reason="install the mesa-spike extra to run compatibility gates")

from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import Freeze as ReferenceFreeze
from src.experiments.sorting.model import SortingWorld
from src.experiments.sorting.observe import observe as observe_reference
from src.experiments.sorting.representations import boundary_length as reference_boundary
from src.spikes.mesa_bubble import Freeze, MesaBubbleModel, boundary_length, observe

VALUES = [8, 1, 6, 0, 7, 3, 5, 2, 4]


def assert_same_scientific_state(reference: SortingWorld, mesa: MesaBubbleModel) -> None:
    assert mesa.values == reference.values
    assert [cell.cell_id for cell in mesa.line] == [cell.cell_id for cell in reference.cells]
    assert mesa.tick == reference.tick
    assert mesa.sorting_steps == reference.steps
    assert mesa.swaps == reference.swaps


@pytest.mark.parametrize("order", ["index", "reverse_index", "shuffled"])
@pytest.mark.parametrize("seed", [0, 7])
def test_mesa_matches_the_reference_tick_for_tick(order: str, seed: int) -> None:
    reference = SortingWorld.from_values(VALUES, order=order, seed=seed)
    candidate = MesaBubbleModel(VALUES, order=order, seed=seed)

    for _ in range(15):
        assert_same_scientific_state(reference, candidate)
        reference.step_tick()
        candidate.step_tick()


@pytest.mark.parametrize("mode", [Freeze.MOVEABLE, Freeze.IMMOVABLE])
def test_freezing_preserves_reference_semantics(mode: Freeze) -> None:
    reference = SortingWorld.from_values(VALUES, order="shuffled", seed=13)
    candidate = MesaBubbleModel(VALUES, order="shuffled", seed=13)
    for _ in range(3):
        reference.step_tick()
        candidate.step_tick()

    position = 4
    reference.cells[position].freeze = ReferenceFreeze(mode.value)
    candidate.freeze_positions([position], mode)

    for _ in range(12):
        assert_same_scientific_state(reference, candidate)
        reference.step_tick()
        candidate.step_tick()


def test_seeded_block_swap_matches_reference_without_consuming_model_rng() -> None:
    reference = SortingWorld.from_values(VALUES, order="shuffled", seed=21)
    candidate = MesaBubbleModel(VALUES, order="shuffled", seed=21)
    for _ in range(4):
        reference.step_tick()
        candidate.step_tick()

    apply(reference, Intervention("block_swap", {"fraction": 0.2}), seed=99)
    candidate.block_swap(0.2, seed=99)
    assert_same_scientific_state(reference, candidate)

    for _ in range(8):
        reference.step_tick()
        candidate.step_tick()
        assert_same_scientific_state(reference, candidate)


def test_json_snapshot_restore_replays_the_exact_future() -> None:
    candidate = MesaBubbleModel(VALUES, order="shuffled", seed=31)
    candidate.run(5, stop_when_quiescent=False)
    saved = json.loads(json.dumps(candidate.snapshot()))

    candidate.block_swap(0.2, seed=101)
    candidate.run(7, stop_when_quiescent=False)
    expected = candidate.snapshot()

    candidate.restore(saved)
    candidate.block_swap(0.2, seed=101)
    candidate.run(7, stop_when_quiescent=False)

    assert candidate.snapshot() == expected


def test_observation_and_representation_match_the_reference_boundary() -> None:
    reference = SortingWorld.from_values(VALUES, order="shuffled", seed=3)
    candidate = MesaBubbleModel(VALUES, order="shuffled", seed=3)
    reference.run(4, stop_when_quiescent=False)
    candidate.run(4, stop_when_quiescent=False)

    candidate_observation = observe(candidate)
    assert candidate_observation["values"] == observe_reference(reference)["values"]
    assert boundary_length(candidate_observation) == reference_boundary(
        observe_reference(reference)
    )
