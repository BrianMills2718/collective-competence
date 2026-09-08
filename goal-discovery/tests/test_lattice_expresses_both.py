"""One substrate, two kinds of system, and the boundaries it refuses to cross.

Spec §28 says the substrate should be a discrete interacting dynamical system of
which *"a standard cellular automaton is a particularly constrained case."* That
is a claim about generality, and a docstring cannot carry it. Here both cases
are instantiated on the same `Lattice`, and the cellular automaton is checked
against binomial coefficients -- ground truth computed from `math.comb`, not
from this code, so the test cannot pass by agreeing with itself.

The rest of the file checks the three commitments that make goal DISCOVERY
possible on this substrate rather than merely convenient: an analyst cannot read
white-box state, a counterfactual restores an exact snapshot rather than a
similar-looking one, and a conserving system cannot quietly gain or lose
entities.
"""

from __future__ import annotations

import sys
import unittest
from math import comb
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "goal-discovery"))

from src.lattice.core import (  # noqa: E402
    Faults, RuleViolation, build, restore, snapshot, step_synchronous,
)
from src.lattice.observe import (  # noqa: E402
    FULL_STATE, LOCAL_ONLY, HiddenChannel, NEVER_EXPOSED, Observation, inversions,
)
from src.lattice.specimens import elementary_ca, sorting  # noqa: E402


class TheConstrainedCaseIsActuallyAConstrainedCase(unittest.TestCase):

    def test_rule_90_is_the_sierpinski_triangle(self):
        """Row t, offset d from the seed cell, is C(t, (t+d)/2) mod 2.

        Independent ground truth: nothing below consults the substrate to decide
        what the answer should be.
        """
        size, steps = 65, 20
        lat, rule = elementary_ca.make(90, size=size)
        rows = elementary_ca.evolve(lat, rule, steps)
        mid = size // 2
        checked = 0
        for t, row in enumerate(rows):
            for d in range(-t, t + 1):
                want = (comb(t, (t + d) // 2) % 2) if (t + d) % 2 == 0 else 0
                self.assertEqual(row[(mid + d) % size], want,
                                 f"rule 90 disagrees with C({t},...) at row {t}, offset {d}")
                checked += 1
        self.assertGreater(checked, 400, "too few cells compared to mean anything")

    def test_rule_110_is_not_left_right_symmetric(self):
        """A cheap guard that the neighbourhood is not being read symmetrically.

        Rule 90 is symmetric, so it would pass even if left and right were
        swapped. Rule 110 is not, so it catches what rule 90 cannot.
        """
        lat, rule = elementary_ca.make(110, size=41)
        rows = elementary_ca.evolve(lat, rule, 8)
        mid = 41 // 2
        final = rows[-1]
        left = sum(final[mid - k] for k in range(1, 9))
        right = sum(final[mid + k] for k in range(1, 9))
        self.assertNotEqual(left, right,
                            "rule 110 came out symmetric; the neighbourhood is "
                            "probably being read without regard to direction")

    def test_both_specimens_use_the_same_lattice_class(self):
        sort_lat, _ = sorting.make(10, seed=0)
        ca_lat, _ = elementary_ca.make(90, size=21)
        self.assertIs(type(sort_lat), type(ca_lat))
        self.assertNotEqual(
            (sort_lat.conserving, sort_lat.centred),
            (ca_lat.conserving, ca_lat.centred),
            "the two specimens differ in no declared property, so nothing has "
            "been demonstrated about generality")


class TheAnalystCannotReadWhiteBoxState(unittest.TestCase):

    def test_forbidden_channels_raise_rather_than_return_nothing(self):
        for hidden in sorted(NEVER_EXPOSED):
            with self.assertRaises(HiddenChannel, msg=f"{hidden} was exposable"):
                Observation({hidden})

    def test_an_empty_contract_is_refused(self):
        with self.assertRaises(HiddenChannel):
            Observation(set())

    def test_local_only_really_withholds_the_global_statistic(self):
        lat, rule = sorting.make(10, seed=4)
        reading = LOCAL_ONLY.read(lat)
        self.assertNotIn("inversions", reading)
        self.assertNotIn("occupants", reading)
        self.assertIn("inversions", FULL_STATE.read(lat),
                      "the full-state contract withholds it too, so the two "
                      "contracts do not differ and the distinction is fictional")

    def test_the_lattice_holds_no_reference_to_any_measurement(self):
        """The mechanical form of 'the target lives only in the measurement'."""
        lat, _ = sorting.make(10, seed=0)
        for name, value in vars(lat).items():
            self.assertFalse(
                callable(value) and getattr(value, "__module__", "") ==
                "src.lattice.observe",
                f"lattice field {name} holds a measurement; the goal has moved "
                "inside the system")


class CounterfactualsRestoreAnExactState(unittest.TestCase):

    @staticmethod
    def _arm(snap, rule, steps, disturb=None):
        """Restore a snapshot, optionally disturb it, and record the PATH.

        The path, not the endpoint. Sorting ends in an absorbing state, so two
        arms that took different routes at different cost both finish at
        [0, 1, ... n-1] and an endpoint comparison reports them identical. The
        control below caught exactly that in the first version of this file.
        """
        lat = restore(snap)
        if disturb:
            disturb(lat)
        trace = []
        for _ in zip(range(steps),
                     sorting.CONTROLLERS["decentralized"](lat, rule, 10_000)):
            trace.append((lat.ops, tuple(lat.occupants)))
        return trace

    def _snapshot_mid_run(self):
        lat, rule = sorting.make(12, seed=7, faults=Faults(p_fail=0.2))
        for _ in zip(range(60), sorting.CONTROLLERS["decentralized"](lat, rule, 10_000)):
            pass
        return snapshot(lat), rule

    def test_two_restores_of_one_snapshot_stay_identical(self):
        snap, rule = self._snapshot_mid_run()
        self.assertEqual(self._arm(snap, rule, 300), self._arm(snap, rule, 300),
                         "two arms restored from one snapshot diverged, so an "
                         "intervention comparison would measure noise")

    def test_a_snapshot_without_the_random_state_would_not_be_enough(self):
        """The control for the test above: prove the rng state is load-bearing."""
        snap, rule = self._snapshot_mid_run()
        baseline = self._arm(snap, rule, 300)
        nudged = self._arm(snap, rule, 300, disturb=lambda lat: lat.rng.random())
        self.assertNotEqual(baseline, nudged,
                            "advancing one arm's random stream changed nothing, "
                            "so the previous test would pass without it")

    def test_the_paths_compared_above_are_long_enough_to_differ(self):
        """And that the comparison is not passing on a pair of empty traces."""
        snap, rule = self._snapshot_mid_run()
        trace = self._arm(snap, rule, 300)
        self.assertEqual(len(trace), 300)
        self.assertGreater(len({state for _, state in trace}), 5,
                           "the arm barely moves; this is not a trajectory")

    def test_restoring_rewinds_the_operation_count(self):
        lat, rule = sorting.make(10, seed=2)
        for _ in zip(range(40), sorting.CONTROLLERS["decentralized"](lat, rule, 10_000)):
            pass
        snap = snapshot(lat)
        spent = lat.ops
        for _ in zip(range(40), sorting.CONTROLLERS["decentralized"](lat, rule, 10_000)):
            pass
        self.assertGreater(lat.ops, spent)
        self.assertEqual(restore(snap).ops, spent)

    def test_restore_preserves_nondefault_system_semantics(self):
        lat, _ = elementary_ca.make(90, size=9)
        restored = restore(snapshot(lat))
        self.assertEqual(
            (restored.conserving, restored.centred, restored.radius, restored.ring),
            (lat.conserving, lat.centred, lat.radius, lat.ring),
            "snapshot restore changed the declared system, so counterfactual arms "
            "would not be the same specimen",
        )


class AConservingSystemCannotGainOrLoseEntities(unittest.TestCase):

    def test_a_rule_that_duplicates_an_occupant_is_refused(self):
        lat = build([0, 1, 2, 3])
        with self.assertRaises(RuleViolation):
            lat.apply(0, lambda before, initiator: (before[0], before[0]))

    def test_a_rule_that_destroys_an_occupant_is_refused(self):
        lat = build([0, 1, 2, 3])
        with self.assertRaises(RuleViolation):
            lat.apply(0, lambda before, initiator: (before[0], None))

    def test_the_same_rule_is_allowed_when_the_system_declares_it_does_not_conserve(self):
        lat = build([0, 1, 2, 3], conserving=False)
        lat.apply(0, lambda before, initiator: (before[0], before[0]))
        self.assertEqual(lat.occupants[:2], [0, 0])

    def test_sorting_conserves_across_a_whole_run(self):
        lat, rule = sorting.make(12, seed=11, faults=Faults(p_fail=0.3))
        start = sorted(x for x in lat.occupants if x is not None)
        for _ in sorting.CONTROLLERS["decentralized"](lat, rule, 2_000):
            pass
        self.assertEqual(sorted(x for x in lat.occupants if x is not None), start)
        self.assertEqual(inversions(lat), 0, "did not finish sorting in budget")


if __name__ == "__main__":
    unittest.main()
