"""The historical Ants integrity correction must survive artifact/UI loading."""

from __future__ import annotations

import json
from copy import deepcopy

import pandas as pd
import panel as pn
import pytest

from src.cockpit.scale_evidence import (
    _reviewed_summary,
    build_scale_evidence,
    load_scale_evidence,
)


def _legacy_summary() -> dict:
    return {
        "decision": "abstain-no-go",
        "integrity": {
            "passed": True,
            "gates": {"annulus_removal_all_eight": True, "complete_trajectories": True},
            "instantaneous_annulus_removal_fraction": 1.0,
            "minimum_post_step_annulus_gap_fraction": 0.246,
        },
        "scoring": {
            "decision": "abstain-no-go",
            "mae": {"persistence": 90.0, "primary": 17.0, "local": 21.0,
                    "colony": 19.0, "trail": 27.0},
            "trail_seed_wins": {"local": 3, "colony": 3},
        },
    }


def test_legacy_integrity_reinterpretation_is_corrected_without_mutating_source() -> None:
    source = _legacy_summary()
    original = deepcopy(source)
    reviewed = _reviewed_summary(source)

    assert source == original
    assert reviewed["stored_decision"] == "abstain-no-go"
    assert reviewed["decision"] == "stop-integrity-failure"
    assert not reviewed["integrity"]["passed"]
    assert not reviewed["integrity"]["gates"]["annulus_removal_all_eight"]
    assert reviewed["scoring"] == original["scoring"]
    assert "rejected" in reviewed["display_correction"]


def test_original_gate_cannot_be_overridden_by_instantaneous_assignment() -> None:
    source = _legacy_summary()
    source["integrity"]["minimum_annulus_removal_fraction"] = 0.25
    source["integrity"]["minimum_post_step_annulus_gap_fraction"] = 1.0
    reviewed = _reviewed_summary(source)
    assert reviewed["decision"] == "stop-integrity-failure"
    assert reviewed["integrity"]["minimum_annulus_removal_fraction"] == 0.25


@pytest.mark.parametrize("value", [None, float("nan"), float("inf")])
def test_missing_or_invalid_recorded_gate_is_not_a_pass(value) -> None:
    source = _legacy_summary()
    source["integrity"]["minimum_post_step_annulus_gap_fraction"] = value
    with pytest.raises(ValueError, match="recorded annulus-removal evidence"):
        _reviewed_summary(source)


def test_loader_and_view_preserve_raw_evidence_and_expose_corrected_stop(tmp_path) -> None:
    pn.extension("tabulator")
    source = _legacy_summary()
    pd.DataFrame([
        {"model": model, "mae": mae} for model, mae in source["scoring"]["mae"].items()
    ]).to_csv(tmp_path / "scores.csv", index=False)
    pd.DataFrame([
        {"seed": seed, **source["scoring"]["mae"]} for seed in range(1101, 1109)
    ]).to_csv(tmp_path / "held_seed_errors.csv", index=False)
    (tmp_path / "summary.json").write_text(json.dumps(source), encoding="utf-8")
    (tmp_path / "metadata.json").write_text(json.dumps({
        "netlogo_version": "7.0.4", "protocol": "P7-004", "source_model_modified": False,
    }), encoding="utf-8")
    before = (tmp_path / "summary.json").read_bytes()

    data = load_scale_evidence(tmp_path)
    view = build_scale_evidence(data)

    assert data.summary["decision"] == "stop-integrity-failure"
    assert (tmp_path / "summary.json").read_bytes() == before
    assert "INTEGRITY STOP" in view[1].object
    markdown = "\n".join(str(pane.object) for pane in view.select(pn.pane.Markdown))
    assert "diagnostic" in markdown.lower()
    assert "all integrity gates passed" not in markdown
    assert "Stored artifact decision" in markdown
    assert "24.6%" in markdown
