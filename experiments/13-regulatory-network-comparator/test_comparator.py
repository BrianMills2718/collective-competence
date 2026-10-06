from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from reproduce_native import (
    MANIFEST,
    RESULT_PATH,
    ensure_model,
    git_blob_sha,
    package_version,
    run_native_reproduction,
    sha256,
    validate_against_frozen_p0,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def canonical_controls(values):
    return sorted(values, key=lambda item: json.dumps(item, sort_keys=True))


def test_provider_and_model_are_exactly_pinned():
    assert MANIFEST["provider"]["package"] == "biodivine_aeon"
    assert MANIFEST["provider"]["version"] == "1.4.2"
    assert MANIFEST["provider"]["license"] == "MIT"
    assert (
        MANIFEST["provider"]["commit"]
        == "abc98ec3794d4eaa9aa5dcd77c4aca00c316c1dd"
    )
    spec = MANIFEST["upstream_case_study"]
    assert spec["model_git_blob"] == "41a5404b5e11733a4ac52b6bbf1cc2d1823ab764"
    assert (
        spec["model_sha256"]
        == "13f3c96b5498b1d7eda008ecc4717b78238b33aee283efe271717089829e916b"
    )
    assert package_version() == MANIFEST["provider"]["version"]

    model_path = ensure_model()
    data = model_path.read_bytes()
    assert sha256(data) == spec["model_sha256"]
    assert git_blob_sha(data) == spec["model_git_blob"]


def test_native_aeon_reproduction_matches_frozen_p0():
    result = run_native_reproduction()
    validate_against_frozen_p0(result)

    phenotypes = result["native_outputs"]["phenotypes"]
    assert all(row["selected_cardinality"] == 1 for row in phenotypes.values())

    control = result["native_outputs"]["permanent_control"]
    expected = MANIFEST["p0_expectations"]["permanent_control"]
    assert control["minimum_size"] == 1
    assert control["alternatives"] == canonical_controls(expected["alternatives"])


def test_native_reproduction_preserves_upstream_marker_ambiguity():
    result = run_native_reproduction()
    assert result["native_outputs"]["attractor_count"] == 6
    monocyte = result["native_outputs"]["phenotypes"]["Monocyte"]
    assert monocyte["match_count"] == 2
    assert monocyte["match_cardinalities"] == [1, 1]
    assert "first attractor intersecting" in result["upstream"]["selection_rule"]
    assert "cJun=True matches two" in result["selection_limit"]


def test_committed_result_preserves_p0_contract_and_revision_lineage():
    if not RESULT_PATH.exists():
        pytest.skip("P0 evidence is written only after the implementation commit")

    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    validate_against_frozen_p0(result)

    assert result["status"] == "complete"
    assert result["phase"] == "P0_native_reproduction"
    assert result["provider"]["version"] == MANIFEST["provider"]["version"]
    assert (
        result["upstream"]["model_sha256"]
        == MANIFEST["upstream_case_study"]["model_sha256"]
    )
    assert result["native_outputs"]["phenotypes"]["Monocyte"]["match_count"] == 2

    evidence_revision = result["environment"]["collective_competence_revision"]
    check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", evidence_revision, "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0, check.stderr
