from __future__ import annotations

import itertools

from src.experiments.distributed_prediction.reachability import (
    barrier_feasible,
    moveable_order_feasible,
)
from src.experiments.opportunity_adjusted.graph import (
    decode,
    encode,
    opportunity,
    successors,
    values,
)
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import Freeze, SortingWorld


def _damaged(values_: list[int], positions: list[int], mode: str) -> SortingWorld:
    world = SortingWorld.from_values(values_, "bubble", order="index", seed=0)
    apply(
        world,
        Intervention("freeze_cells", {"positions": positions, "mode": mode}),
        seed=0,
    )
    return world


def test_graph_state_round_trips_every_observable_cell_field() -> None:
    world = SortingWorld.from_values([2, 0, 1], "selection", seed=3)
    world.cells[0].ideal_position = 2
    world.cells[1].freeze = Freeze.MOVEABLE
    restored = decode(encode(world))
    assert encode(restored) == encode(world)


def test_successors_include_value_swaps_and_selection_internal_progress() -> None:
    bubble = SortingWorld.from_values([1, 0], "bubble", seed=0)
    assert any(values(state) == (0, 1) for state in successors(encode(bubble)))

    selection = SortingWorld.from_values([0, 1], "selection", seed=0)
    next_states = list(successors(encode(selection)))
    assert any(values(state) == (0, 1) and state[1][4] == 1 for state in next_states)


def test_bubble_graph_matches_both_exact_invariants_at_size_three() -> None:
    for values_ in itertools.permutations(range(3)):
        for mask in range(1, 1 << 3):
            positions = [index for index in range(3) if mask & (1 << index)]
            immovable = _damaged(list(values_), positions, "immovable")
            modes = ["immovable" if index in positions else "none" for index in range(3)]
            assert opportunity(immovable).reachable == barrier_feasible(values_, modes)

            moveable = _damaged(list(values_), positions, "moveable")
            assert opportunity(moveable).reachable == moveable_order_feasible(values_, positions)
