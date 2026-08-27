"""Experiment 002 mechanics: determinism, snapshots, and the structural facts
the 001/002 contrast rests on."""

from __future__ import annotations

import json

import pytest

from src.experiments.bowl.interventions import BowlIntervention, apply
from src.experiments.bowl.model import BowlWorld
from src.experiments.bowl.observe import observe
from src.experiments.bowl.representations import evaluate, settled_fraction


def w(seed: int = 4000, n: int = 8) -> BowlWorld:
    return BowlWorld.from_seed(n, seed, spread=10.0)


def test_same_seed_replays_identically():
    a, b = w(), w()
    a.run(120, stop_at_goal=False)
    b.run(120, stop_at_goal=False)
    assert a.state_key() == b.state_key()


def test_restore_and_run_equals_uninterrupted_run():
    straight = w()
    straight.run(150, stop_at_goal=False)
    expected = straight.state_key()

    branched = w()
    branched.run(50, stop_at_goal=False)
    snap = branched.snapshot()
    branched.run(80, stop_at_goal=False)
    branched.restore(snap)
    branched.run(100, stop_at_goal=False)
    assert branched.state_key() == expected


def test_snapshot_survives_a_json_round_trip():
    a = w()
    a.run(40, stop_at_goal=False)
    snap = json.loads(json.dumps(a.snapshot(), default=str))
    live = w()
    live.run(40, stop_at_goal=False)
    live.run(60, stop_at_goal=False)
    expected = live.state_key()
    a.restore(snap)
    a.run(60, stop_at_goal=False)
    assert a.state_key() == expected


def test_the_bowl_converges_from_varied_starts():
    for seed in range(6):
        world = w(4000 + seed)
        world.run(4000)
        assert world.at_goal(), f"seed {seed} left max|x| unsettled"


def test_a_frozen_coordinate_strands_the_system():
    """The structural fact the 001/002 contrast rests on.

    No coordinate can act on another, so a frozen one is stranded and the goal
    becomes unreachable. In the sorting array a frozen cell's neighbours carry
    it; here there is nobody to do that.
    """
    world = w()
    world.coords[0].frozen = True
    world.run(4000)
    assert world.quiescent(), "should settle as far as it can"
    assert not world.at_goal(), "a frozen coordinate must strand the bowl"


def test_freezing_is_invisible_to_every_representation():
    """D4b's premise. If freezing changed a representation the test would be
    measuring state damage and the 001 comparison would be void."""
    world = w()
    world.run(60, stop_at_goal=False)
    before = evaluate(observe(world))
    apply(world, BowlIntervention("freeze_coords", {"count": 3}), seed=1)
    after = evaluate(observe(world))
    assert before == after


def test_state_damage_is_visible_to_the_representations():
    world = w()
    world.run(60, stop_at_goal=False)
    before = evaluate(observe(world))
    apply(world, BowlIntervention("displace", {"count": 2, "magnitude": 6.0}), seed=1)
    assert evaluate(observe(world)) != before


def test_settled_fraction_counts_coordinates_inside_tolerance():
    world = w(n=4)
    for c in world.coords:
        c.x, c.v = 0.0, 0.0
    assert settled_fraction(observe(world)) == 1.0
    world.coords[0].x = 5.0
    assert settled_fraction(observe(world)) == pytest.approx(0.75)


def test_divergent_parameters_fail_loudly_rather_than_producing_nonsense():
    world = BowlWorld.from_seed(4, 1, spread=10.0, stiffness=9.0, damping=0.0)
    with pytest.raises(FloatingPointError, match="do not give a stable descent"):
        world.run(4000, stop_at_goal=False)


def test_unknown_intervention_is_rejected_loudly():
    with pytest.raises(ValueError, match="unknown intervention kind"):
        apply(w(), BowlIntervention("teleport", {}), seed=1)
