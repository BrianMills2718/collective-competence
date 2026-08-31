"""Adversarial completion checks; fixtures are not laboratory E2E evidence."""

import copy
import hashlib
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from completion_gate import (
    GateError,
    execute_tests,
    validate_evidence,
    verify_artifact,
    verify_checkout,
    verify_runtime,
)


class CompletionGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "trace.txt").write_text(
            "Observed actual browser action and final output"
        )
        self.digest = hashlib.sha256((self.root / "trace.txt").read_bytes()).hexdigest()
        self.now = datetime.now(timezone.utc).isoformat()
        self.revision = "a" * 40
        self.contract = {
            "journeys": {"run": "Manual Run changes displayed seed"},
            "required_surfaces": ["browser", "server", "final_output"],
            "quality_questions": ["Legible?"],
            "max_evidence_age_hours": 24,
        }
        self.observation = {
            "schema_version": "1.0",
            "record_type": "end_to_end_observation",
            "observation_id": "E2E-run",
            "criterion_id": "run",
            "status": "pass",
            "scope": "Synthetic verifier fixture, not real browser evidence",
            "outcome_kind": "system_behavior",
            "execution_context": {
                "target": "fixture",
                "route": "http://127.0.0.1:5013/app",
                "configuration_ref": "trace.txt",
                "dependency_set_ref": "trace.txt",
            },
            "test_selection": {
                "criterion_id": "run",
                "changed_boundary": "manual-run",
                "failure_hypothesis": "Run does not update output",
                "discriminating_probe": "Change seed then click Run",
                "decision_if_pass": "Accept this journey",
                "decision_if_fail": "Repair",
            },
            "source_revision": self.revision,
            "observed_at": self.now,
            "producer": "browser-reviewer",
            "required_surfaces": self.contract["required_surfaces"],
            "surface_observations": [
                {
                    "surface": s,
                    "status": "observed",
                    "evidence_ref": "trace.txt",
                    "observation": "Action and consequence inspected",
                    "inspected_at": self.now,
                }
                for s in self.contract["required_surfaces"]
            ],
            "outcome": {
                "evidence_ref": "trace.txt",
                "observed_result": "Fixture changed result",
                "state_change": "Fixture seed changed",
            },
            "unexpected_events": [],
            "limitations": [],
            "journey": {
                "correlation_id": "run-1",
                "starting_state": "Ready fixture",
                "input": "seed 8",
                "steps": ["Set seed", "Click Run", "Inspect output"],
                "observation_window": {"started_at": self.now, "ended_at": self.now},
            },
        }
        self.bundle = {
            "target": "fixture",
            "route": "http://127.0.0.1:5013/app",
            "revision": self.revision,
            "contract_sha256": "b" * 64,
            "artifacts": {"trace.txt": self.digest},
            "observations": [self.observation],
            "quality_review": {
                "status": "pass",
                "reviewer": "separate-reviewer",
                "inspected_at": self.now,
                "answers": [
                    {
                        "question": "Legible?",
                        "assessment": "Controls readable",
                        "evidence_ref": "trace.txt",
                    }
                ],
                "unresolved_defects": [],
            },
            "handoff": {
                "fresh_session": True,
                "launcher_exited": True,
                "evidence_ref": "trace.txt",
                "observed_at": self.now,
            },
        }

    def check(self):
        validate_evidence(
            self.contract, self.bundle, self.root, self.revision, "b" * 64
        )

    def rejects(self, word):
        with self.assertRaisesRegex(GateError, word):
            self.check()

    def test_complete_fixture_passes(self):
        self.check()

    def test_missing_journey_rejected(self):
        self.bundle["observations"] = []
        self.rejects("journey")

    def test_duplicate_journey_rejected(self):
        self.bundle["observations"].append(copy.deepcopy(self.observation))
        self.rejects("duplicate")

    def test_failed_journey_rejected(self):
        self.observation["status"] = "fail"
        self.rejects("not passed")

    def test_no_browser_observation_rejected(self):
        self.observation["surface_observations"][0]["status"] = "missing"
        self.rejects("browser")

    def test_callback_only_evidence_rejected(self):
        self.observation["surface_observations"] = self.observation[
            "surface_observations"
        ][1:]
        self.rejects("browser")

    def test_stale_revision_rejected(self):
        self.bundle["revision"] = "c" * 40
        self.rejects("revision")

    def test_stale_observation_rejected(self):
        self.observation["source_revision"] = "c" * 40
        self.rejects("revision")

    def test_changed_contract_rejected(self):
        self.bundle["contract_sha256"] = "c" * 64
        self.rejects("contract")

    def test_changed_artifact_rejected(self):
        (self.root / "trace.txt").write_text("Changed after review")
        self.rejects("hash")

    def test_missing_artifact_rejected(self):
        (self.root / "trace.txt").unlink()
        self.rejects("artifact")

    def test_unhashed_artifact_rejected(self):
        self.observation["outcome"]["evidence_ref"] = "other.txt"
        self.rejects("registered")

    def test_escape_rejected(self):
        with self.assertRaisesRegex(GateError, "escape"):
            verify_artifact(
                self.root, "../outside.txt", {"../outside.txt": self.digest}
            )

    def test_old_evidence_rejected(self):
        self.observation["observed_at"] = "2020-01-01T00:00:00Z"
        self.rejects("stale")

    def test_future_evidence_rejected(self):
        self.observation["observed_at"] = "2099-01-01T00:00:00Z"
        self.rejects("future")

    def test_unresolved_error_rejected(self):
        self.observation["unexpected_events"] = [{"disposition": "unresolved"}]
        self.rejects("unresolved")

    def test_quality_review_required(self):
        del self.bundle["quality_review"]
        self.rejects("quality")

    def test_failed_quality_rejected(self):
        self.bundle["quality_review"]["status"] = "fail"
        self.rejects("quality")

    def test_unanswered_quality_question_rejected(self):
        self.bundle["quality_review"]["answers"] = []
        self.rejects("quality")

    def test_handoff_must_be_fresh(self):
        self.bundle["handoff"]["fresh_session"] = False
        self.rejects("fresh")

    def test_launcher_must_have_exited(self):
        self.bundle["handoff"]["launcher_exited"] = False
        self.rejects("launcher")

    def test_wrong_observation_target_rejected(self):
        self.observation["execution_context"]["target"] = "other-checkout"
        self.rejects("target")

    def test_wrong_observation_route_rejected(self):
        self.observation["execution_context"]["route"] = "http://localhost:5011/app"
        self.rejects("route")

    def test_unregistered_dependency_evidence_rejected(self):
        self.observation["execution_context"]["dependency_set_ref"] = "missing-lock.txt"
        self.rejects("registered")

    def test_test_runner_rejects_failure_skip_and_empty(self):
        for code, error in [
            ("raise SystemExit(1)", "failed"),
            ("print('1 skipped')", "skipped"),
            ("print('Ran 0 tests')", "empty"),
        ]:
            with self.subTest(code=code):
                contract = {
                    "mandatory_tests": [
                        {"id": "probe", "cwd": ".", "argv": ["{python}", "-c", code]}
                    ]
                }
                with self.assertRaisesRegex(GateError, error):
                    execute_tests(contract, self.root, sys.executable, self.root)

    def test_test_runner_saves_actual_successful_process_output(self):
        contract = {
            "mandatory_tests": [
                {
                    "id": "probe",
                    "cwd": ".",
                    "argv": ["{python}", "-c", "print('Ran 1 test; OK')"],
                }
            ]
        }
        result = execute_tests(contract, self.root, sys.executable, self.root)
        self.assertEqual(result[0]["exit_code"], 0)
        self.assertIn("Ran 1 test", (self.root / "probe.log").read_text())

    def test_checkout_rejects_wrong_revision_and_dirty_source(self):
        def git(*args):
            return subprocess.check_output(
                ["git", "-C", str(self.root), *args], text=True
            ).strip()

        git("init", "-q")
        git("add", "trace.txt")
        git(
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@invalid.test",
            "commit",
            "-qm",
            "fixture",
        )
        revision = git("rev-parse", "HEAD")
        verify_checkout(self.root, revision)
        with self.assertRaisesRegex(GateError, "revision"):
            verify_checkout(self.root, "f" * 40)
        (self.root / "trace.txt").write_text("Modified source")
        with self.assertRaisesRegex(GateError, "dirty"):
            verify_checkout(self.root, revision)

    def test_wrong_checkout_runtime_rejected_before_network(self):
        import os

        with self.assertRaisesRegex(GateError, "checkout"):
            verify_runtime(
                self.root,
                {"relative_cwd": "goal-discovery", "route": "/app"},
                {"pid": os.getpid(), "port": 5013, "start_ticks": "0"},
            )


if __name__ == "__main__":
    unittest.main()
