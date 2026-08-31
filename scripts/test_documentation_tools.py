"""Small positive/negative controls for documentation projections, not scientific tests."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


knowledge = module("render_knowledge_index")
agents = module("sync_agent_context")


class DocumentationControls(unittest.TestCase):
    """Exercise fail-loud metadata boundaries on disposable fixture repositories."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "roadmap").mkdir()
        self.artifact = "goal-discovery/docs/hypotheses/example.md"
        path = self.root / self.artifact
        path.parent.mkdir(parents=True)
        path.write_text("# Original evidence\n", encoding="utf-8")
        self.record = {"id": "example", "family": "test", "question": "What?",
                       "artifacts": [self.artifact], "review_status": "not_reviewed",
                       "outcome": None, "disposition": None}

    def render(self, records):
        (self.root / "roadmap/experiments.json").write_text(
            json.dumps({"schema_version": 1, "experiments": records}), encoding="utf-8")
        with patch.object(knowledge, "ROOT", self.root), patch.object(
            knowledge, "markdown_files", return_value=[self.artifact]
        ):
            return knowledge.render()

    def test_unreviewed_stays_unreviewed(self):
        output = self.render([self.record])["roadmap/experiments.md"]
        self.assertIn("not_reviewed", output)
        self.assertIn("Not assessed", output)

    def test_duplicate_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate experiment ID"):
            self.render([self.record, self.record])

    def test_missing_coverage_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing from register"):
            self.render([])

    def test_unreviewed_verdict_rejected(self):
        with self.assertRaisesRegex(ValueError, "must not assert"):
            self.render([{**self.record, "outcome": "passed"}])

    def test_outside_path_rejected(self):
        with self.assertRaisesRegex(ValueError, "out-of-scope"):
            self.render([{**self.record, "artifacts": ["../outside.md"]}])

    def test_missing_artifact_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing"):
            self.render([{**self.record, "artifacts": ["missing.md"]}])

    def test_instruction_projection_and_drift(self):
        (self.root / "CLAUDE.md").write_text("# Goal\n", encoding="utf-8")
        with patch.object(agents, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            with patch("sys.argv", ["sync_agent_context.py", "--write"]):
                self.assertEqual(agents.main(), 0)
            with patch("sys.argv", ["sync_agent_context.py", "--check"]):
                self.assertEqual(agents.main(), 0)
                (self.root / "CLAUDE.md").write_text("# Revised goal\n", encoding="utf-8")
                self.assertEqual(agents.main(), 1)


if __name__ == "__main__":
    unittest.main()
