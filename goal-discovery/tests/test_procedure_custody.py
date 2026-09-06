"""Procedure custody is explicit and independently guarded from result custody."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "scripts/check_experiment_reproducibility.py"
MARKER = "**Procedure custody: not preserved.**"


def _run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _record(custody: dict | None) -> dict:
    record = {
        "id": "T-001",
        "ontology_contract_version": 1,
        "outcome_source": "goal-discovery/docs/hypotheses/t_001_results.md",
    }
    if custody is not None:
        record["procedure_custody"] = custody
    return record


def _fixture(tmp_path: Path, record: dict | None, files: dict[str, str] | None = None) -> Path:
    root = tmp_path / "repo"
    (root / "roadmap").mkdir(parents=True)
    data = {
        "ontology_contract_policy": {"required_version": 1},
        "experiments": [] if record is None else [record],
    }
    (root / "roadmap/experiments.json").write_text(json.dumps(data), encoding="utf-8")
    for relative, text in (files or {}).items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "--quiet", "-m", "fixture"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return root


def test_current_repository_has_a_complete_procedure_custody_sweep():
    result = _run(REPO)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "15 current-contract experiment(s)" in result.stdout
    assert "14 with tracked runnable Python procedure(s)" in result.stdout
    assert "1 explicitly not preserved" in result.stdout


def test_missing_custody_mapping_fails_closed(tmp_path):
    root = _fixture(tmp_path, _record(None))
    result = _run(root)
    assert result.returncode == 1
    assert "missing procedure_custody mapping" in result.stdout


def test_empty_current_contract_sweep_fails_instead_of_passing_vacuously(tmp_path):
    root = _fixture(tmp_path, None)
    result = _run(root)
    assert result.returncode == 1
    assert "empty sweep is not a pass" in result.stdout


def test_missing_runnable_entrypoint_is_not_counted_as_custody(tmp_path):
    custody = {
        "status": "runnable_python",
        "entrypoints": ["goal-discovery/src/experiments/demo/run.py"],
    }
    root = _fixture(tmp_path, _record(custody))
    result = _run(root)
    assert result.returncode == 1
    assert "entrypoint is not a tracked file" in result.stdout


def test_python_file_without_main_guard_is_not_a_runnable_entrypoint(tmp_path):
    path = "goal-discovery/src/experiments/demo/run.py"
    custody = {"status": "runnable_python", "entrypoints": [path]}
    root = _fixture(tmp_path, _record(custody), {path: "def helper():\n    return 1\n"})
    result = _run(root)
    assert result.returncode == 1
    assert "no structural main guard" in result.stdout


def test_tracked_top_level_supporting_script_need_not_have_a_main_guard(tmp_path):
    runner = "goal-discovery/src/experiments/demo/run.py"
    probe = "goal-discovery/results/demo/probe.py"
    custody = {
        "status": "runnable_python",
        "entrypoints": [runner],
        "supporting_scripts": [probe],
    }
    files = {
        runner: 'def main():\n    return 0\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n',
        probe: 'print("diagnostic")\n',
    }
    root = _fixture(tmp_path, _record(custody), files)
    result = _run(root)
    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_supporting_script_fails_custody(tmp_path):
    runner = "goal-discovery/src/experiments/demo/run.py"
    probe = "goal-discovery/results/demo/probe.py"
    custody = {
        "status": "runnable_python",
        "entrypoints": [runner],
        "supporting_scripts": [probe],
    }
    files = {
        runner: 'def main():\n    return 0\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n',
    }
    root = _fixture(tmp_path, _record(custody), files)
    result = _run(root)
    assert result.returncode == 1
    assert "supporting script is not a tracked file" in result.stdout


def test_not_preserved_requires_disclosure_in_the_experiment_result(tmp_path):
    outcome = "goal-discovery/docs/hypotheses/t_001_results.md"
    custody = {
        "status": "not_preserved",
        "reason": "The procedure source was not committed.",
        "disclosure_artifact": outcome,
    }
    root = _fixture(tmp_path, _record(custody), {outcome: "# Result\nNo custody note here.\n"})
    result = _run(root)
    assert result.returncode == 1
    assert "lacks the procedure-custody marker" in result.stdout


def test_explicit_not_preserved_disclosure_passes_structural_custody(tmp_path):
    outcome = "goal-discovery/docs/hypotheses/t_001_results.md"
    custody = {
        "status": "not_preserved",
        "reason": "The procedure source was not committed.",
        "disclosure_artifact": outcome,
    }
    root = _fixture(tmp_path, _record(custody), {outcome: f"# Result\n\n{MARKER} No runner survives.\n"})
    result = _run(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 explicitly not preserved" in result.stdout
