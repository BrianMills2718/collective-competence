"""Snapshot equivalence: restoring and continuing must equal never stopping.

This is the property the whole branching protocol rests on. If it fails, every
counterfactual comparison in the program is comparing against the wrong thing.
"""

from __future__ import annotations

import json

from src.common.snapshots import state_hash
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import ALGOTYPES, Freeze, SortingWorld


def _world(algotype="bubble", seed=11):
    return SortingWorld.from_values(
        [5, 12, 1, 9, 3, 14, 7, 0, 11, 2, 8, 13, 4, 10, 6], algotype, seed=seed
    )


def test_restore_and_run_equals_uninterrupted_run():
    for algotype in ALGOTYPES:
        straight = _world(algotype)
        straight.run(30, stop_when_quiescent=False)
        expected = state_hash(straight.values)

        branched = _world(algotype)
        branched.run(10, stop_when_quiescent=False)
        snap = branched.snapshot()
        branched.run(20, stop_when_quiescent=False)  # carry on, then rewind
        branched.restore(snap)
        branched.run(20, stop_when_quiescent=False)
        assert state_hash(branched.values) == expected, algotype


def test_snapshot_survives_a_json_round_trip():
    # Snapshots are written to disk as JSON, which turns the RNG state tuple
    # into nested lists. Restoring from the file must still replay exactly.
    w = _world()
    w.run(8, stop_when_quiescent=False)
    snap = json.loads(json.dumps(w.snapshot(), default=str))
    live = _world()
    live.run(8, stop_when_quiescent=False)
    live.run(15, stop_when_quiescent=False)
    expected = state_hash(live.values)

    w.restore(snap)
    w.run(15, stop_when_quiescent=False)
    assert state_hash(w.values) == expected


def test_two_arms_from_one_snapshot_share_a_common_past():
    w = _world()
    w.run(9, stop_when_quiescent=False)
    snap = w.snapshot()

    arms = {}
    for iv in (Intervention("none", {}), Intervention("block_swap", {"fraction": 0.2})):
        w.restore(snap)
        apply(w, iv, seed=3)
        w.run(12, stop_when_quiescent=False)
        arms[iv.kind] = state_hash(w.values)
    assert arms["none"] != arms["block_swap"], "the intervention arm did not diverge"

    w.restore(snap)
    assert w.snapshot()["snapshot_id"] == snap["snapshot_id"], "restore was not exact"


def test_intervention_touches_only_its_declared_target():
    w = _world()
    w.run(9, stop_when_quiescent=False)
    before = w.snapshot()
    apply(w, Intervention("block_swap", {"fraction": 0.2}), seed=3)
    after = w.snapshot()

    for field in ("tick", "steps", "swaps", "order", "seed", "rng_state"):
        assert after[field] == before[field], f"block_swap disturbed {field}"
    assert sorted(c["value"] for c in after["cells"]) == sorted(
        c["value"] for c in before["cells"]
    ), "block_swap changed the multiset of values"


def test_freeze_intervention_only_sets_freeze():
    w = _world()
    before = w.snapshot()
    apply(w, Intervention("freeze_cells", {"fraction": 0.2, "mode": "immovable"}), seed=3)
    after = w.snapshot()
    changed = [
        (b["cell_id"], b["freeze"], a["freeze"])
        for b, a in zip(before["cells"], after["cells"])
        if b != a
    ]
    assert changed, "freeze_cells froze nothing"
    for _, was, now in changed:
        assert was == "none" and now == Freeze.IMMOVABLE.value
