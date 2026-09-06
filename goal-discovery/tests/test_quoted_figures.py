"""Negative controls for `scripts/check_quoted_figures.py`.

A guard nobody has seen refuse is a guard nobody knows is wired up. The first
version of that script was green for a day while the defect it was written to
catch sat live on the repository's public status page, because it compared a
package value against a string literal stored inside itself and never opened a
document. `wiki/development-log.md` recorded it as closed "by
`scripts/check_quoted_figures.py` and its two controls"; the controls did not
exist. These are them.

Each control copies the tree into a scratch git repository, introduces exactly
one defect of a shape that has actually occurred here, and asserts the checker
exits 1.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = "scripts/check_quoted_figures.py"
# `experiments/` joined this list on 2026-09-06, when the guard began reading a
# CSV result package there. A fixture that does not carry every package a check
# names turns a real check into a missing-package failure.
COPIED = ("scripts", "wiki", "roadmap", "goal-discovery/results",
          "goal-discovery/docs", "experiments")


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.email=t@example.invalid", "-c", "user.name=test", *args],
        cwd=repo, check=True, capture_output=True,
    )


class QuotedFigureControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        for rel in COPIED:
            shutil.copytree(ROOT / rel, self.repo / rel)
        # `copytree` preserves modes, and the canonical checkout of this
        # repository is deliberately mode 555 so that writes go through a
        # worktree. Without this the scratch copy inherits read-only
        # directories, every rewrite raises PermissionError, and the whole
        # class fails -- six red tests in the checkout the README calls the
        # handoff verification contract, while passing in any worktree. That
        # is exactly what happened between 2026-09-06 and this fix, and it was
        # invisible because the suite was only ever run from a worktree.
        for path in self.repo.rglob("*"):
            path.chmod(path.stat().st_mode | (0o700 if path.is_dir() else 0o600))
        git(self.repo, "init", "-q", ".")
        git(self.repo, "add", "-A", "-f")
        git(self.repo, "commit", "-qm", "base")
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        """Teardown must survive read-only trees too, or it masks the real error."""
        for path in self.repo.rglob("*"):
            try:
                path.chmod(path.stat().st_mode | (0o700 if path.is_dir() else 0o600))
            except OSError:
                pass
        self.tmp.cleanup()

    def run_checker(self):
        return subprocess.run(
            [sys.executable, CHECKER], cwd=self.repo, capture_output=True, text=True
        )

    def rewrite(self, rel: str, old: str, new: str) -> None:
        path = self.repo / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"{rel} no longer contains {old!r}; control is stale")
        path.write_text(text.replace(old, new), encoding="utf-8")

    def test_the_tree_as_committed_passes(self):
        """A control suite whose baseline is already red proves nothing."""
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("quotation(s) in prose", result.stdout)

    def test_a_figure_rounded_in_prose_is_a_failure(self):
        """The F20 defect: +1.65 quoted as +1.7, in the flattering direction."""
        self.rewrite("wiki/failure-log.md",
                     "uncoordinated arm sits 5.3 null sd up",
                     "uncoordinated arm sits 5.4 null sd up")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("writes 5.4", result.stdout)

    def test_a_figure_rewritten_as_a_word_is_a_failure(self):
        """The F21 defect, which was live: "thirty-five times" for a measured 34.49.

        A word form is not a wrong number the checker can compare -- it is a
        number that has left the checker's view entirely. Without the
        matched-nothing floor this passes, which is exactly what happened.
        """
        self.rewrite("wiki/status.html",
                     "34.5 times the matched-independent arm",
                     "thirty-five times the matched-independent arm")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("no document matches this check's context pattern",
                      result.stdout)

    def test_an_empty_check_list_is_a_failure(self):
        """A check that inspects nothing must not report a clean sweep."""
        path = self.repo / CHECKER
        text = path.read_text(encoding="utf-8")
        start = text.index("CHECKS = [")
        end = text.index("\n]\n", start) + len("\n]\n")
        path.write_text(text[:start] + "CHECKS = []\n" + text[end:], encoding="utf-8")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("passes vacuously", result.stdout)

    def test_a_figure_quoted_from_a_csv_package_is_checked_too(self):
        """Result packages are JSON or CSV depending on which experiment wrote them.

        A guard that reads only JSON stops covering the CSV half without saying
        so. This drifts the D2 repeated-disturbance cost quoted in the goal
        register away from `experiments/01-self-sorting/results/repeat.csv`.
        """
        self.rewrite("wiki/goals.md", "cost rises 52 →", "cost rises 52 → 999 not")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("writes 999", result.stdout)
        self.assertIn("repeat.csv", result.stdout)

    def test_a_missing_package_is_a_failure_not_a_skip(self):
        """The measurement is the authority; without it there is nothing to check."""
        (self.repo / "goal-discovery/results/q1-009-information/followup.json").unlink()
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("is missing", result.stdout)


if __name__ == "__main__":
    unittest.main()
