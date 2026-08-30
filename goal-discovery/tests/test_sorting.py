"""System invariants and the published rules the replication must honour."""

from __future__ import annotations

import pytest

from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import ALGOTYPES, Cell, Freeze, SortingWorld


def test_values_are_conserved():
    for algotype in ALGOTYPES:
        w = SortingWorld.from_values(list(reversed(range(15))), algotype, seed=2)
        before = sorted(w.values)
        w.run(500)
        assert sorted(w.values) == before, algotype


def test_a_frozen_cell_never_initiates():
    # Freeze every cell: nothing may move, whatever the arrangement.
    w = SortingWorld.from_values([4, 3, 2, 1, 0], "bubble", seed=1)
    for c in w.cells:
        c.freeze = Freeze.MOVEABLE
    before = list(w.values)
    w.run(50, stop_when_quiescent=False)
    assert w.values == before


def test_freeze_intervention_accepts_exact_positions():
    w = SortingWorld.from_values([4, 3, 2, 1, 0], "bubble", seed=1)
    apply(
        w,
        Intervention("freeze_cells", {"positions": [1, 3], "mode": "immovable"}),
        seed=99,
    )
    assert [cell.freeze for cell in w.cells] == [
        Freeze.NONE,
        Freeze.IMMOVABLE,
        Freeze.NONE,
        Freeze.IMMOVABLE,
        Freeze.NONE,
    ]


def test_moveable_frozen_cell_can_still_be_swapped_by_a_neighbour():
    # Value 0 is frozen at position 2, so it must travel to position 0 without
    # ever acting: only its neighbours can carry it there.
    w = SortingWorld.from_values([4, 3, 0, 1, 2], "bubble", seed=1)
    w.cells[2].freeze = Freeze.MOVEABLE
    frozen_id = w.cells[2].cell_id
    w.run(2000)
    assert w.values == sorted(w.values), "a passive cell should be routed around"
    assert [c.cell_id for c in w.cells].index(frozen_id) == 0, "the frozen cell was not carried"


def test_immovable_frozen_cell_blocks_and_can_prevent_sorting():
    # An immovable cell partitions the line. Value 0 is pinned at position 2 and
    # cannot reach position 0, so the array cannot sort. This is a limit of the
    # system, not a bug, and the paper reports both freeze kinds separately
    # because they behave oppositely.
    w = SortingWorld.from_values([4, 3, 0, 1, 2], "bubble", seed=1)
    w.cells[2].freeze = Freeze.IMMOVABLE
    pinned = w.cells[2].cell_id
    w.run(2000)
    assert w.values != sorted(w.values), "an immovable blocker should prevent sorting here"
    assert [c.cell_id for c in w.cells].index(pinned) == 2, "the pinned cell moved"


def test_selection_cell_advances_its_ideal_position_when_it_loses():
    # The paper omits this; SelectionSortCell.should_move_to in the reference
    # implementation is what settles it. If this regresses, the replication has
    # silently stopped matching the source.
    w = SortingWorld(cells=[Cell(9, "selection", cell_id=0), Cell(1, "selection", cell_id=1)])
    w.rng.seed(0)
    w.cells[1].ideal_position = 0
    w.cells[0].ideal_position = 0
    w._act_selection(0)  # value 9 at position 0, ideal 0 == own position: no move
    assert w.cells[0].ideal_position == 0
    w._act_selection(1)  # value 1 beats 9 at position 0, so it swaps
    assert w.values == [1, 9]


def test_a_step_is_charged_for_every_comparison_not_only_for_swaps():
    w = SortingWorld.from_values(list(range(8)), "bubble", seed=1)  # already sorted
    w.step_tick()
    assert w.swaps == 0
    assert w.steps > 0, "looking must cost the same primitive as acting"


def test_mismatched_algotype_list_is_rejected_loudly():
    with pytest.raises(ValueError, match="one per cell"):
        SortingWorld.from_values([1, 2, 3], ["bubble", "bubble"])


def test_unknown_activation_order_is_rejected_loudly():
    w = SortingWorld.from_values([2, 1], "bubble", seed=1)
    w.order = "whatever"  # type: ignore[assignment]
    with pytest.raises(ValueError, match="unknown activation order"):
        w.step_tick()


def test_quiescence_implies_the_goal_for_an_undamaged_array():
    """The regression this suite missed.

    An earlier quiescence check asked whether a probe activation changed the
    *values*, which reads a selection cell advancing its ideal position as
    inaction and halted the run a few ticks short of sorted. Nothing here
    noticed, and a validation run reported selection reaching the goal in 1 of
    40 seeds as though it were a property of the published rule.

    With no frozen cells and one algotype throughout, quiescence must mean
    sorted, for every algotype and every start.
    """
    import random as _random

    for algotype in ALGOTYPES:
        for seed in range(6):
            values = list(range(25))
            _random.Random(seed).shuffle(values)
            w = SortingWorld.from_values(values, algotype, seed=seed)
            w.run(20_000)
            assert w.quiescent(), f"{algotype} seed {seed} hit the tick cap"
            assert w.values == sorted(w.values), (
                f"{algotype} seed {seed} declared quiescence at {w.values}"
            )


def test_quiescence_notices_a_selection_cell_that_only_moves_its_ideal_position():
    # Value 9 sits left of value 1 with its ideal position on itself, so it
    # will not move; the cell holding 1 has an in-bounds ideal position it has
    # not reached. That is a pending action even though the array is unchanged.
    w = SortingWorld(cells=[Cell(9, "selection", cell_id=0), Cell(1, "selection", cell_id=1)])
    w.cells[0].ideal_position = 0
    w.cells[1].ideal_position = 0
    assert not w.quiescent()
