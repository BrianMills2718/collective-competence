from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
NCA_ROOT = REPO_ROOT / "experiments" / "12-growing-nca"


def test_saved_nca_workbench_manifest_is_fresh_and_complete() -> None:
    pytest.importorskip("panel")
    from src.cockpit.growing_nca import load_growing_nca_manifest

    data = load_growing_nca_manifest(NCA_ROOT)
    assert data["evidence_mode"].startswith("saved replay")
    assert data["default_family"] == "h2"
    families = {family["id"]: family for family in data["families"]}
    assert set(families) == {"basin", "g1", "l1", "t1", "h2", "a1"}
    assert families["h2"]["disposition"] == "supported"
    assert families["a1"]["disposition"] == "mixed"
    assert families["basin"]["visual_stream"] == "formed seed 7 continuation"
    assert all(family["not_established"] for family in families.values())

    for name, expected in data["source_hashes"].items():
        actual = hashlib.sha256((NCA_ROOT / "results" / name).read_bytes()).hexdigest()
        assert actual == expected


def test_saved_nca_workbench_builds_with_visual_extra() -> None:
    pytest.importorskip("panel")
    from src.cockpit.growing_nca import build_growing_nca_evidence

    view = build_growing_nca_evidence(NCA_ROOT)
    assert "Growing NCA" in view[0].object
    shell = view[1]
    assert len(shell) == 2
