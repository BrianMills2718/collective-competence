"""The shared lattice carries a passive-relaxation / feedback-regulation contrast."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "goal-discovery"))

from src.lattice.core import restore, snapshot  # noqa: E402
from src.lattice.specimens import regulation  # noqa: E402


class PassiveAndFeedbackAreDifferentMechanisms(unittest.TestCase):

    def test_both_reach_the_same_unloaded_region(self):
        cfg = regulation.Config()
        for arm in ("passive", "feedback"):
            lat = regulation.make(140)
            transition = regulation.rule(arm, cfg)
            self.assertIsNotNone(
                regulation.recovery_time(lat, transition, setpoint=cfg.setpoint),
                f"{arm} never reached the common criterion",
            )

    def test_feedback_recovers_faster_from_displacement(self):
        cfg = regulation.Config()
        for amount in (-40, -20, 20, 40):
            passive = regulation.make(cfg.setpoint)
            feedback = regulation.make(cfg.setpoint)
            regulation.displace(passive, amount)
            regulation.displace(feedback, amount)
            p = regulation.recovery_time(passive, regulation.rule("passive", cfg))
            f = regulation.recovery_time(feedback, regulation.rule("feedback", cfg))
            self.assertIsNotNone(p)
            self.assertIsNotNone(f)
            self.assertLess(f, p, f"feedback did not beat passive after {amount:+d}")


class PersistentLoadExposesRegulation(unittest.TestCase):

    @staticmethod
    def _late_error(arm: regulation.Arm, load: int, *, blocked=False, disabled=False):
        cfg = regulation.Config()
        lat = regulation.make(cfg.setpoint)
        transition = regulation.rule(
            arm, cfg, load=load,
            sensor_blocked=blocked,
            actuator_disabled=disabled,
        )
        trace = regulation.evolve(lat, transition, 100)
        return sum(abs(x - cfg.setpoint) for x in trace[-20:]) / 20

    def test_feedback_reduces_steady_error_under_load(self):
        for load in (-4, -2, 2, 4):
            passive = self._late_error("passive", load)
            feedback = self._late_error("feedback", load)
            self.assertLess(feedback, passive)

    def test_blocking_the_sensor_removes_the_advantage(self):
        for load in (-4, -2, 2, 4):
            passive = self._late_error("passive", load)
            blocked = self._late_error("feedback", load, blocked=True)
            self.assertEqual(blocked, passive)

    def test_disabling_actuation_removes_the_advantage(self):
        for load in (-4, -2, 2, 4):
            passive = self._late_error("passive", load)
            disabled = self._late_error("feedback", load, disabled=True)
            self.assertEqual(disabled, passive)


class TheSpecimenUsesTheSharedCounterfactualContract(unittest.TestCase):

    def test_regulation_uses_nonconserving_centred_lattice_semantics(self):
        lat = regulation.make()
        self.assertEqual((lat.conserving, lat.centred, lat.radius, lat.ring),
                         (False, True, 0, True))

    def test_snapshot_restore_keeps_the_regulation_system_definition(self):
        lat = regulation.make(140)
        transition = regulation.rule("feedback")
        regulation.evolve(lat, transition, 3)
        restored = restore(snapshot(lat))
        self.assertEqual(
            (restored.occupants, restored.ops, restored.conserving,
             restored.centred, restored.radius, restored.ring),
            (lat.occupants, lat.ops, lat.conserving,
             lat.centred, lat.radius, lat.ring),
        )


if __name__ == "__main__":
    unittest.main()
