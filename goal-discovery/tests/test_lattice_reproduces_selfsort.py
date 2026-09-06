"""The substrate's gate: it must reproduce the founding experiment exactly.

The previous shared contract could not express sorting and said so in its own
docstring. That is the failure this substrate exists to fix, so "it expresses
the founding experiment" is not asserted in prose anywhere -- it is this file.

Both implementations are run over the same seeds and their FULL trajectories
compared, step by step: the operation count and the complete configuration after
every step. Comparing only the final state would pass on two systems that
reached the same answer by different paths and at different cost, and cost is a
measured quantity here.

The last four tests are the controls. A comparison that cannot fail proves
nothing, and this repository has recorded five separate green checks whose scope
was narrower than a reader assumed, so each control perturbs one thing and
requires the comparison to go red.
"""

from __future__ import annotations

import importlib.util
import random
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "goal-discovery"))

_spec = importlib.util.spec_from_file_location(
    "selfsort_reference", REPO / "experiments/01-self-sorting/selfsort.py")
selfsort = importlib.util.module_from_spec(_spec)
sys.modules["selfsort_reference"] = selfsort
_spec.loader.exec_module(selfsort)

from src.lattice.core import Faults as LatticeFaults  # noqa: E402
from src.lattice.specimens import sorting  # noqa: E402

N = 10
BUDGET = 300
TRIALS = 40
CONTROLLER_NAMES = {
    "decentralized": "decentralized",
    "watchdog": "central_watchdog",
    "closed": "central_closed",
}
CONDITIONS = {
    "clean": (lambda: selfsort.Faults(), 0),
    "p_fail": (lambda: selfsort.Faults(p_fail=0.30), 0),
    "frozen": (lambda: selfsort.Faults(frozen={3}), 0),
    "dead": (lambda: selfsort.Faults(dead={5}), 0),
    "unreliable": (lambda: selfsort.Faults(unreliable={2: 0.9}), 0),
    "heterogeneous": (lambda: selfsort.Faults(), 3),
}


def reference_trace(controller: str, seed: int, faults, n_type_b: int) -> list:
    rng = random.Random(seed)
    values = list(range(N))
    rng.shuffle(values)
    type_b = set(rng.sample(range(N), n_type_b)) if n_type_b else set()
    rules = {v: (selfsort.RULE_DESCEND if v in type_b else selfsort.RULE_ASCEND)
             for v in range(N)}
    world = selfsort.World(a=values, rules=rules, faults=faults, rng=rng)
    trace = []
    for _ in selfsort.CONTROLLERS[CONTROLLER_NAMES[controller]](world, BUDGET):
        trace.append((world.ops, tuple(world.a)))
    return trace


def lattice_trace(controller: str, seed: int, faults, n_type_b: int) -> list:
    lat, rule = sorting.make(N, seed=seed, faults=faults, n_type_b=n_type_b)
    trace = []
    for _ in sorting.CONTROLLERS[controller](lat, rule, BUDGET):
        trace.append((lat.ops, tuple(lat.occupants)))
    return trace


def _lattice_faults(reference) -> LatticeFaults:
    return LatticeFaults(
        p_fail=reference.p_fail,
        unreliable=dict(reference.unreliable),
        frozen=set(reference.frozen),
        dead=set(reference.dead),
    )


class SubstrateReproducesTheFoundingExperiment(unittest.TestCase):

    def compare(self, controller: str, condition: str) -> int:
        make_faults, n_type_b = CONDITIONS[condition]
        identical = 0
        for seed in range(TRIALS):
            ref = reference_trace(controller, seed, make_faults(), n_type_b)
            got = lattice_trace(controller, seed,
                                _lattice_faults(make_faults()), n_type_b)
            if ref == got:
                identical += 1
        return identical

    def test_every_controller_and_condition_reproduces_step_for_step(self):
        failures = []
        for controller in CONTROLLER_NAMES:
            for condition in CONDITIONS:
                got = self.compare(controller, condition)
                if got != TRIALS:
                    failures.append(f"{controller}/{condition}: {got}/{TRIALS}")
        self.assertEqual(
            failures, [],
            "the substrate no longer reproduces selfsort.py. Every recorded "
            "sorting result depends on this, so a change here is a change to "
            "published numbers:\n" + "\n".join(failures))

    def test_the_traces_are_long_enough_to_be_evidence(self):
        """A comparison over near-empty traces would pass trivially."""
        trace = reference_trace("decentralized", 0, selfsort.Faults(), 0)
        self.assertGreater(len(trace), 100,
                           "reference trace too short to discriminate anything")
        self.assertGreater(len({state for _, state in trace}), 10,
                           "the reference barely moves; this is not a trajectory")


class TheComparisonCanFail(unittest.TestCase):
    """Controls. Each breaks one thing and requires the comparison to go red."""

    def compare_one(self, controller="decentralized", seed=0, mutate=None) -> bool:
        ref = reference_trace(controller, seed, selfsort.Faults(p_fail=0.30), 0)
        lat, rule = sorting.make(N, seed=seed, faults=LatticeFaults(p_fail=0.30))
        if mutate:
            mutate(lat)
        got = []
        for _ in sorting.CONTROLLERS[controller](lat, rule, BUDGET):
            got.append((lat.ops, tuple(lat.occupants)))
        return ref == got

    def test_unmutated_comparison_passes(self):
        """The controls below mean nothing unless the baseline is green."""
        self.assertTrue(self.compare_one(), "baseline comparison already fails")

    def test_a_different_seed_diverges(self):
        ref = reference_trace("decentralized", 0, selfsort.Faults(p_fail=0.30), 0)
        other = lattice_trace("decentralized", 1,
                              LatticeFaults(p_fail=0.30), 0)
        self.assertNotEqual(ref, other, "two different seeds produced identical "
                                        "trajectories; the seed does nothing")

    def test_one_extra_draw_from_the_random_stream_diverges(self):
        """The initiator draw is in the stream; getting it wrong is invisible
        without this. It is exactly the defect this substrate shipped with."""
        def take_a_draw(lat):
            lat.rng.random()
        self.assertFalse(self.compare_one(mutate=take_a_draw),
                         "an extra draw from the random stream changed nothing; "
                         "the comparison is not sensitive to draw order")

    def test_a_single_swapped_pair_diverges(self):
        def swap(lat):
            lat.occupants[0], lat.occupants[1] = lat.occupants[1], lat.occupants[0]
        self.assertFalse(self.compare_one(mutate=swap),
                         "perturbing the initial configuration changed nothing")

    def test_dropping_a_fault_diverges(self):
        def clear(lat):
            lat.faults.p_fail = 0.0
        self.assertFalse(self.compare_one(mutate=clear),
                         "removing the fault rate changed nothing; faults are "
                         "not reaching the substrate")


if __name__ == "__main__":
    unittest.main()
