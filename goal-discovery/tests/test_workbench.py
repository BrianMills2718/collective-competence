from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.workbench.analysis import evaluate_representations
from src.workbench.data import load_x02_dataset
from src.workbench.static import render_evidence_png

HEADER = (
    '"[run number]","seed-number","activation-order","max-ticks",'
    '"perturb-fraction","intervention-seed","freeze-count","freeze-mode-choice",'
    '"[step]","ticks","boundary-length","sorted?","quiescent?","values",'
    '"cell-ids-by-position","freeze-modes-by-position","swap-count",'
    '"comparison-count","last-event"\n'
)
PREAMBLE = (
    '"BehaviorSpace results (NetLogo 7.0.4)","Table version 2.0"\n'
    '"model.nlogox"\n'
    '"test"\n'
    '"date"\n'
    '"min-pxcor","max-pxcor","min-pycor","max-pycor"\n'
    '"0","2","-1","1"\n'
)


def _write_fixture(directory: Path) -> None:
    baseline = (
        PREAMBLE
        + HEADER
        + (
            '"1","101","index","50","0.25","91","1","moveable","0","0",'
            '"1","false","false","[2 0 1]","[0 1 2]","[none none none]",'
            '"0","0","setup"\n'
            '"1","101","index","50","0.25","91","1","moveable","1","1",'
            '"0","true","true","[0 1 2]","[1 2 0]","[none none none]",'
            '"2","3","sorted"\n'
        )
    )
    frozen = (
        PREAMBLE
        + HEADER
        + (
            '"1","101","index","50","0.25","91","1","immovable","0","0",'
            '"1","false","true","[2 0 1]","[0 1 2]","[immovable none none]",'
            '"0","0","freeze-immovable"\n'
        )
    )
    (directory / "baseline.csv").write_text(baseline, encoding="utf-8")
    (directory / "freeze-immovable.csv").write_text(frozen, encoding="utf-8")


def test_loader_preserves_cell_identity_and_derives_macro_features(tmp_path: Path) -> None:
    _write_fixture(tmp_path)
    dataset = load_x02_dataset(tmp_path)

    assert len(dataset.runs) == 2
    assert len(dataset.macros) == 3
    assert len(dataset.cells) == 9
    assert dataset.run("baseline:1")["reached_goal"]
    assert not dataset.run("freeze-immovable:1")["reached_goal"]
    assert dataset.run("freeze-immovable:1")["matched_baseline_id"] == "baseline:1"

    baseline_end = dataset.trajectory("baseline:1").iloc[-1]
    assert baseline_end["inversions"] == 0
    assert baseline_end["sorted_prefix"] == 3
    assert baseline_end["longest_ascending_run"] == 3

    identities = dataset.cell_history("baseline:1")
    assert identities.loc[identities["tick"] == 1, "cell_id"].tolist() == [1, 2, 0]
    frozen = dataset.trajectory("freeze-immovable:1").iloc[0]
    assert frozen["active_fraction"] == pytest.approx(2 / 3)
    assert frozen["traversable_edge_fraction"] == pytest.approx(0.5)


def test_static_evidence_export(tmp_path: Path) -> None:
    _write_fixture(tmp_path)
    dataset = load_x02_dataset(tmp_path)
    output = render_evidence_png(dataset, "freeze-immovable:1", tmp_path / "evidence.png")
    assert output.exists()
    assert output.stat().st_size > 10_000


def test_existing_x02_representation_screen_if_artifacts_are_present() -> None:
    data_dir = Path("results/x02-netlogo")
    if not data_dir.exists():
        pytest.skip("X02 generated artifacts are intentionally not source-controlled")
    scores = evaluate_representations(load_x02_dataset(data_dir))
    assert set(scores["representation"]) == {
        "Boundary only",
        "Ordering geometry",
        "Capability state",
        "Geometry + capability",
    }
    assert scores["held_out_balanced_accuracy"].between(0, 1).all()
    assert pd.notna(scores["discovery_score"]).all()
