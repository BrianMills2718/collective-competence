from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest
from compare import (
    RESULT_PATH as V1_RESULT_PATH,
)
from compare import (
    audit_incremental_value,
    normalize_native_profile,
    run_comparison,
    run_native_v1,
    validate_frozen_v1,
)
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


def test_v1_native_controls_match_frozen_source_context_sizes():
    native = run_native_v1()
    validate_frozen_v1(native)

    source_rows = native["source_target_permanent"]
    assert source_rows["Erythrocyte"]["minimum_size"] == 1
    assert source_rows["Monocyte"]["minimum_size"] == 2
    assert source_rows["Granulocyte"]["minimum_size"] == 2
    assert native["phenotype_only_permanent"]["minimum_size"] == 2

    assert [
        item["perturbation"] for item in source_rows["Erythrocyte"]["alternatives"]
    ] == [{"EKLF": False}, {"Fli1": True}]


def test_v1_profile_is_only_native_derived_information():
    native = run_native_v1()
    profile = normalize_native_profile(native)
    audit = audit_incremental_value(profile)

    rows = {row["source"]: row for row in profile["source_profiles"]}
    assert rows["Erythrocyte"]["source_specific_savings_vs_phenotype_only"] == 1
    assert rows["Monocyte"]["source_specific_savings_vs_phenotype_only"] == 0
    assert rows["Granulocyte"]["source_specific_savings_vs_phenotype_only"] == 0

    assert audit["added_information_fields"] == []
    assert audit["decision_changes_beyond_native"] == []
    assert audit["negative_control"]["passed"] is True
    assert audit["refuter_triggered"] is False
    assert audit["disposition"] == "no_added_value"


def test_v1_audit_flags_a_non_native_field_in_negative_control():
    profile = normalize_native_profile(run_native_v1())
    altered = deepcopy(profile)
    altered["source_profiles"][0]["field_provenance"]["invented_signal"] = {
        "kind": "cc_only",
        "path": "none",
    }
    audit = audit_incremental_value(altered)
    assert audit["added_information_fields"] == ["Erythrocyte.invented_signal"]
    assert audit["negative_control"]["passed"] is False
    assert audit["refuter_triggered"] is False


def test_v1_comparison_disposes_frozen_prediction_without_claiming_v2():
    result = run_comparison()
    assert result["prediction"]["expected_disposition"] == "no_added_value"
    assert result["prediction_supported"] is True
    assert result["disposition"] == "no_added_value"
    assert result["incremental_value_audit"]["refuter_triggered"] is False
    assert "restricted-access" in result["scope_limit"]


def test_committed_v1_result_preserves_revision_lineage():
    if not V1_RESULT_PATH.exists():
        pytest.skip("V1 evidence is written only after the implementation commit")

    result = json.loads(V1_RESULT_PATH.read_text(encoding="utf-8"))
    assert result["status"] == "complete"
    assert result["phase"] == "V1_bounded_comparator"
    assert result["disposition"] == "no_added_value"
    assert result["prediction_supported"] is True

    evidence_revision = result["environment"]["collective_competence_revision"]
    check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", evidence_revision, "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0, check.stderr
