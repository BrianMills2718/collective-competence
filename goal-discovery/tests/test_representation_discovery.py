from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.experiments.representation_discovery.benchmark import (
    SORTING_TICKS,
    THERMOSTAT_ARMS,
    THERMOSTAT_TICKS,
    grouped_score,
    load_sorting_task,
    load_thermostat_task,
)

ROOT = Path(__file__).resolve().parents[1]


def _write_sorting_unit_fixture(root: Path) -> None:
    """Synthetic adapter input only; never research evidence or a replication."""
    source = root / "results" / "p2-002-crossed"
    source.mkdir(parents=True)
    runs, trajectories = [], []
    for seed in range(101, 107):
        for variant in range(12):
            run_id = f"unit-only-{seed}-{variant:02d}"
            runs.append({
                "run_id": run_id, "seed": seed, "branch_tick": 4,
                "reached_goal": variant % 2, "activation_schedule": "shuffled",
                "freeze_mode": "moveable", "freeze_count": variant % 3,
                "final_inversions": 99999,
            })
            for tick in range(6):
                trajectories.append({
                    "run_id": run_id, "tick": tick,
                    "phase": "pre_branch" if tick < 5 else "post_branch",
                    "event": "setup" if tick == 0 else "step",
                    "freeze_modes_json": '["none"]' if tick < 5 else '["moveable"]',
                    "boundary_norm": tick / 10 if tick < 5 else 99999,
                    "inversions_norm": 1 - tick / 10 if tick < 5 else 99999,
                    "hidden_goal": 99999,
                })
            # Same timestamp, wrong phase: time filtering alone must not admit it.
            trajectories.append({**trajectories[-1], "tick": 4})
    pd.DataFrame(runs).to_csv(source / "discovery_runs.csv", index=False)
    pd.DataFrame(trajectories).to_csv(source / "discovery_trajectories.csv", index=False)


def _write_thermostat_unit_fixture(root: Path) -> None:
    """Minimal rectangular BehaviorSpace-shaped fixture, not simulator output."""
    source = root / "results" / "003-thermostat"
    source.mkdir(parents=True)
    for arm in THERMOSTAT_ARMS:
        rows = []
        for run_number, load in enumerate((-0.4, -0.2, 0.2, 0.4), start=1):
            for tick in range(161):
                temperature = 20 + load if tick in THERMOSTAT_TICKS else 99999
                if tick >= 140:
                    temperature = 20 if arm == "feedback" else 20 + 10 * load
                rows.append({
                    "[run number]": run_number, "arm": arm, "load-magnitude": load,
                    "ticks": tick, "temperature": temperature, "setpoint": 20,
                    "controller-gain": 99999, "future-outcome": 99999,
                })
        pd.DataFrame(rows).to_csv(source / f"003-load-{arm}.csv", index=False)


@pytest.fixture(params=["synthetic-unit", "optional-repository-data"])
def sorting_root(request: pytest.FixtureRequest, tmp_path: Path) -> Path:
    if request.param == "optional-repository-data":
        source = ROOT / "results" / "p2-002-crossed"
        missing = [name for name in ("discovery_runs.csv", "discovery_trajectories.csv")
                   if not (source / name).is_file()]
        if missing:
            pytest.skip(f"Optional recorded sorting adapter inputs absent: {missing}")
        return ROOT
    _write_sorting_unit_fixture(tmp_path)
    return tmp_path


@pytest.fixture(params=["synthetic-unit", "optional-repository-data"])
def thermostat_root(request: pytest.FixtureRequest, tmp_path: Path) -> Path:
    if request.param == "optional-repository-data":
        source = ROOT / "results" / "003-thermostat"
        missing = [f"003-load-{arm}.csv" for arm in THERMOSTAT_ARMS
                   if not (source / f"003-load-{arm}.csv").is_file()]
        if missing:
            pytest.skip(f"Optional recorded thermostat adapter inputs absent: {missing}")
        return ROOT
    _write_thermostat_unit_fixture(tmp_path)
    return tmp_path


def test_sorting_adapter_enforces_pre_intervention_boundary(sorting_root: Path) -> None:
    task = load_sorting_task(sorting_root)

    assert len(task.labels) == 72
    assert task.groups.nunique() == 6
    assert set(task.series["time"]) == SORTING_TICKS
    assert set(task.series["kind"]) == {"boundary_norm", "inversions_norm"}
    assert task.series.groupby(["run_id", "kind"]).size().eq(5).all()
    assert set(task.metadata) == {
        "meta_schedule_shuffled",
        "meta_freeze_moveable",
        "meta_freeze_count",
    }
    assert not any("seed" in column or "final" in column for column in task.metadata)
    assert task.series["value"].lt(99999).all()
    assert set(task.endpoint) == {
        *task.metadata.columns, "endpoint_boundary_norm", "endpoint_inversions_norm",
    }


def test_thermostat_adapter_excludes_mechanism_and_future_fields(thermostat_root: Path) -> None:
    task = load_thermostat_task(thermostat_root)

    assert len(task.labels) == 16
    assert task.labels.sum() == 4
    assert set(task.groups) == {0.2, 0.4}
    assert set(task.series["time"]) == THERMOSTAT_TICKS
    assert set(task.series["kind"]) == {"temperature"}
    assert task.series.groupby("run_id").size().eq(16).all()
    assert list(task.metadata) == ["meta_signed_load"]
    assert list(task.endpoint) == ["meta_signed_load", "endpoint_temperature"]
    assert task.series["value"].lt(99999).all()


def test_sorting_adapter_rejects_contaminated_pre_intervention_state(tmp_path: Path) -> None:
    _write_sorting_unit_fixture(tmp_path)
    path = tmp_path / "results" / "p2-002-crossed" / "discovery_trajectories.csv"
    frame = pd.read_csv(path)
    frame.loc[0, "freeze_modes_json"] = '["moveable"]'
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError, match="frozen-cell state"):
        load_sorting_task(tmp_path)


def test_grouped_score_predicts_each_run_once() -> None:
    index = pd.Index([f"run-{value}" for value in range(12)], name="run_id")
    groups = pd.Series(np.repeat([1, 2, 3], 4), index=index)
    labels = pd.Series(np.tile([0, 0, 1, 1], 3), index=index)
    features = pd.DataFrame(
        {
            "signal": labels.astype(float) + np.linspace(0.0, 0.01, len(index)),
            "constant": 1.0,
        },
        index=index,
    )

    result = grouped_score(features, labels, groups)

    assert result.predictions.index.equals(index)
    assert result.predictions.between(0.0, 1.0).all()
    assert result.balanced_accuracy == 1.0
    assert "constant" not in result.selected_counts
