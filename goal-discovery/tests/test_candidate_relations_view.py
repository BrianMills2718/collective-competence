"""Replay checks use the committed first P10 batch, never run new science."""

import json
from pathlib import Path

import pytest

pytest.importorskip("panel")

from src.cockpit.candidate_relations import build_candidate_relations, relation_margin

DIRECTORY = Path(__file__).resolve().parents[1] / "results/p10-candidate-relations"


def test_recorded_contrast_is_visible_in_pair_margin() -> None:
    data = json.loads((DIRECTORY / "evaluation.json").read_text())
    for kind, demo in data["demo"].items():
        pair, target = demo["selected_pair"], demo["target_before"]
        active, disabled = demo["traces"]["active"], demo["traces"]["disabled"]
        assert relation_margin(active[0], pair, target) < 0
        assert relation_margin(disabled[-1], pair, target) < 0
        assert (relation_margin(active[-1], pair, target) > 0) == (kind == "unequal")


def test_switching_probe_resets_replay_and_updates_identity_rows() -> None:
    view = build_candidate_relations(DIRECTORY)
    probe, player = view[2]
    player.value = 64
    assert all("tick 192" in row.object for row in view[4])
    probe.value = "equal"
    assert player.value == 0
    assert "cell-012" in view[3].object
    assert all("tick 128" in row.object for row in view[4])
    player.value = 64
    assert all("tick 192" in row.object for row in view[4])
    assert "not online inference" in view[3].object


def test_absent_evidence_is_not_a_synthetic_result(tmp_path: Path) -> None:
    view = build_candidate_relations(tmp_path)
    assert "not available" in view[0].object
    assert "No result is inferred" in view[0].object
