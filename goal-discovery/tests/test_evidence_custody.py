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


def test_nothing_cited_is_actually_lost():
    """The baseline's only exception is a command's output path, not missing evidence.

    An earlier version of this test asserted that results/p12-reproduction was
    permanently lost. That was wrong: p12_reference_inference_results.md names it
    inside a fenced shell block as the --directory a reproduction command writes
    to, so it was never a stored package. Any entry that IS a loss must say so
    with status absent_everywhere, and there are none.
    """
    packages = json.loads(BASELINE.read_text())["packages"]
    lost = {k: v for k, v in packages.items() if v["status"] == "absent_everywhere"}
    assert not lost, f"evidence recorded as lost: {sorted(lost)}"
    assert all(v["status"] == "command_output_path" for v in packages.values()), packages


def test_a_scan_that_finds_no_citations_at_all_is_a_failure_not_a_pass():
    """Family M: zero read as success. Found by auditing this guard, 2026-09-05.

    The guard printed `PASS: 0 cited result packages tracked ... 0 new drift` and
    exited 0 on a repository containing no documents. A repository whose records
    are supposed to cite evidence, in which the scan finds no citation at all, has
    told us the scan is broken -- a renamed lab directory, a changed file
    extension, a regex that stopped matching -- not that custody is clean.
    """
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "repo"
        (empty / "scripts").mkdir(parents=True)
        (empty / "goal-discovery" / "results").mkdir(parents=True)
        (empty / "scripts" / "evidence_custody_baseline.json").write_text('{"packages": {}}')
        (empty / "notes.md").write_text("a document that cites no result package\n")
        subprocess.run(["git", "init", "--quiet"], cwd=empty, check=True)
        subprocess.run(["git", "add", "-A"], cwd=empty, check=True, capture_output=True)
        subprocess.run(
            ["git", "-c", "user.email=t@t", "-c", "user.name=t",
             "commit", "--quiet", "-m", "fixture"],
            cwd=empty, check=True, capture_output=True,
        )
        r = _run(empty)
        assert r.returncode == 1, f"a scan that found nothing reported success:\n{r.stdout}"
        assert "broken scan" in r.stdout
