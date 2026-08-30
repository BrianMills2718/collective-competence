from pathlib import Path

import numpy as np
import pandas as pd

from src.experiments.representation_discovery.benchmark import (
    SORTING_TICKS,
    THERMOSTAT_TICKS,
    grouped_score,
    load_sorting_task,
    load_thermostat_task,
)

ROOT = Path(__file__).resolve().parents[1]


def test_sorting_adapter_enforces_pre_intervention_boundary() -> None:
    task = load_sorting_task(ROOT)

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


def test_thermostat_adapter_excludes_mechanism_and_future_fields() -> None:
    task = load_thermostat_task(ROOT)

    assert len(task.labels) == 16
    assert task.labels.sum() == 4
    assert set(task.groups) == {0.2, 0.4}
    assert set(task.series["time"]) == THERMOSTAT_TICKS
    assert set(task.series["kind"]) == {"temperature"}
    assert task.series.groupby("run_id").size().eq(16).all()
    assert list(task.metadata) == ["meta_signed_load"]
    assert list(task.endpoint) == ["meta_signed_load", "endpoint_temperature"]


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
