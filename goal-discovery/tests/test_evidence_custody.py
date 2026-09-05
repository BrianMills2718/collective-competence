"""Every result package a tracked document cites must be openable from a clone.

This exists because the opposite went unnoticed. On 2026-09-04 thirteen result
packages -- the whole constructive arm and the whole instrument-qualification
sequence -- were written, cited by committed result records, and never tracked,
because `goal-discovery/.gitignore` protects evidence with an allowlist that
encodes the packages existing when it was last edited. Ignored files do not
appear in `git status`, so nothing failed. Three port-fidelity tests that call
themselves the substrate's acceptance criterion turned green by skipping.

`tests/CLAUDE.md`: "Missing optional data is missing evidence, not a passed
experiment."
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "scripts/check_evidence_custody.py"
BASELINE = REPO / "scripts/evidence_custody_baseline.json"


def _run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root)],
        capture_output=True, text=True, check=False,  # returncode is the assertion
    )


def test_no_cited_result_package_has_drifted_out_of_git():
    r = _run(REPO)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "0 new drift" in r.stdout


def test_the_checker_actually_fails_when_a_package_drifts():
    """Negative control: if this passes trivially the gate is decoration.

    Mirrors the pattern in test_reproducibility -- a guard that cannot be shown
    to fail is exactly the shape of the defect this whole file is about. Built
    as a synthetic repository rather than a clone so it tests the rule, not this
    repository's current contents.
    """
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp) / "repo"
        (fake / "scripts").mkdir(parents=True)
        (fake / "goal-discovery/results/kept").mkdir(parents=True)
        (fake / "scripts/evidence_custody_baseline.json").write_text('{"packages": {}}')
        (fake / "goal-discovery/results/kept/result.json").write_text("{}")
        (fake / "notes.md").write_text(
            "cites [kept](results/kept/) and [drifted](../../results/drifted/)\n"
        )
        subprocess.run(["git", "init", "--quiet"], cwd=fake, check=True)
        subprocess.run(["git", "add", "-A"], cwd=fake, check=True, capture_output=True)
        subprocess.run(
            ["git", "-c", "user.email=t@t", "-c", "user.name=t",
             "commit", "--quiet", "-m", "fixture"],
            cwd=fake, check=True, capture_output=True,
        )
        r = _run(fake)
        assert r.returncode == 1, f"gate did not fire:\n{r.stdout}{r.stderr}"
        assert "results/drifted" in r.stdout
        assert "drifted out of Git" in r.stdout
        assert "results/kept" not in r.stdout, "a tracked package must not be reported"


def test_baseline_records_the_one_package_lost_everywhere():
    """p12-reproduction is cited by a tracked result and exists nowhere.

    Recorded rather than quietly dropped, per the repository rule against
    revising historical outcomes to make the current picture look stronger.
    """
    packages = json.loads(BASELINE.read_text())["packages"]
    lost = [k for k, v in packages.items() if v["status"] == "absent_everywhere"]
    assert lost == ["p12-reproduction"], lost
