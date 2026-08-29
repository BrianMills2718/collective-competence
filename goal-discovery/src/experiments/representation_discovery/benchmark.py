"""Shared adapters and scoring for the frozen P5-000 benchmark."""

from __future__ import annotations

import csv
import json
import warnings
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, log_loss
from sklearn.preprocessing import StandardScaler

SORTING_TICKS = frozenset(range(5))
THERMOSTAT_TICKS = frozenset(range(20, 36))
THERMOSTAT_LATE_TICKS = frozenset(range(140, 161))
THERMOSTAT_ARMS = (
    "feedback",
    "passive",
    "sensor-blocked",
    "actuator-disabled",
)


@dataclass(frozen=True)
class TaskData:
    """One frozen binary prediction task in the shared benchmark schema."""

    name: str
    series: pd.DataFrame
    metadata: pd.DataFrame
    endpoint: pd.DataFrame
    labels: pd.Series
    groups: pd.Series

    @property
    def run_ids(self) -> pd.Index:
        return self.labels.index


@dataclass(frozen=True)
class ModelScore:
    log_loss: float
    balanced_accuracy: float
    predictions: pd.Series
    selected_counts: Counter[str]


def _indexed(frame: pd.DataFrame, run_ids: pd.Index) -> pd.DataFrame:
    result = frame.reindex(run_ids)
    if result.isna().all(axis=1).any():
        raise ValueError("feature table is missing one or more benchmark runs")
    return result


def _encode_sorting_metadata(runs: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "meta_schedule_shuffled": (runs["activation_schedule"] == "shuffled").astype(float),
            "meta_freeze_moveable": (runs["freeze_mode"] == "moveable").astype(float),
            "meta_freeze_count": runs["freeze_count"].astype(float),
        },
        index=runs["run_id"],
    )


def load_sorting_task(root: Path) -> TaskData:
    """Load the 72 pre-intervention sorting histories frozen for Task S."""

    source = root / "results" / "p2-002-crossed"
    runs = pd.read_csv(source / "discovery_runs.csv")
    trajectories = pd.read_csv(source / "discovery_trajectories.csv")
    runs = runs.loc[runs["branch_tick"] == 4].copy().sort_values("run_id")
    if len(runs) != 72 or runs["run_id"].nunique() != 72:
        raise ValueError("Task S requires exactly 72 unique tick-4 branches")
    if set(runs["seed"]) != set(range(101, 107)):
        raise ValueError("Task S seed groups do not match the frozen design")
    if runs.groupby("seed")["reached_goal"].nunique().min() != 2:
        raise ValueError("every Task S seed must contain both outcomes")

    observed = trajectories.loc[
        trajectories["run_id"].isin(runs["run_id"])
        & (trajectories["phase"] == "pre_branch")
        & trajectories["tick"].isin(SORTING_TICKS)
    ].copy()
    counts = observed.groupby("run_id").size()
    ticks = observed.groupby("run_id")["tick"].agg(lambda values: frozenset(values))
    if len(counts) != 72 or not counts.eq(5).all() or not ticks.eq(SORTING_TICKS).all():
        raise ValueError("Task S does not have one complete tick 0–4 history per run")
    expected_events = observed["tick"].map(lambda tick: "setup" if tick == 0 else "step")
    if not observed["event"].eq(expected_events).all():
        raise ValueError("Task S boundary includes a non-pre-intervention event")
    if observed["freeze_modes_json"].map(json.loads).map(set).ne({"none"}).any():
        raise ValueError("Task S boundary contains a frozen-cell state")

    series = observed.melt(
        id_vars=["run_id", "tick"],
        value_vars=["boundary_norm", "inversions_norm"],
        var_name="kind",
        value_name="value",
    ).rename(columns={"tick": "time"})
    series = series[["run_id", "time", "kind", "value"]].sort_values(["run_id", "kind", "time"])

    runs = runs.set_index("run_id", drop=False)
    run_ids = pd.Index(runs.index, name="run_id")
    metadata = _encode_sorting_metadata(runs).reindex(run_ids)
    last = (
        observed.loc[observed["tick"] == 4]
        .set_index("run_id")[["boundary_norm", "inversions_norm"]]
        .rename(
            columns={
                "boundary_norm": "endpoint_boundary_norm",
                "inversions_norm": "endpoint_inversions_norm",
            }
        )
    )
    labels = runs["reached_goal"].astype(int).rename("outcome")
    groups = runs["seed"].astype(int).rename("group")
    return TaskData(
        name="sorting_recovery",
        series=series.reset_index(drop=True),
        metadata=_indexed(metadata, run_ids),
        endpoint=_indexed(pd.concat([metadata, last], axis=1), run_ids),
        labels=labels,
        groups=groups,
    )


def _read_behaviorspace(path: Path) -> pd.DataFrame:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise ValueError(f"{path} has no BehaviorSpace table header") from error
    raw_headers = rows[header_index]
    seen: Counter[str] = Counter()
    headers: list[str] = []
    for header in raw_headers:
        seen[header] += 1
        headers.append(header if seen[header] == 1 else f"{header}__{seen[header]}")
    data = [row for row in rows[header_index + 1 :] if row and any(value.strip() for value in row)]
    if not data or any(len(row) != len(headers) for row in data):
        raise ValueError(f"{path} has no rectangular BehaviorSpace data")
    return pd.DataFrame(data, columns=headers)


def load_thermostat_task(root: Path) -> TaskData:
    """Load early temperature responses and frozen late-regulation labels."""

    source = root / "results" / "003-thermostat"
    frames: list[pd.DataFrame] = []
    for arm in THERMOSTAT_ARMS:
        frame = _read_behaviorspace(source / f"003-load-{arm}.csv")
        required = {"[run number]", "arm", "load-magnitude", "ticks", "temperature", "setpoint"}
        if missing := required - set(frame):
            raise ValueError(f"Task T arm {arm} lacks columns: {sorted(missing)}")
        frame = frame[list(required)].copy()
        frame["arm"] = arm
        for column in ("load-magnitude", "ticks", "temperature", "setpoint"):
            frame[column] = pd.to_numeric(frame[column])
        frame["tick"] = frame["ticks"].round().astype(int)
        frame["run_id"] = arm + ":load" + frame["load-magnitude"].map(lambda value: f"{value:+.1f}")
        frames.append(frame)
    full = pd.concat(frames, ignore_index=True)
    magnitudes = {-0.4, -0.2, 0.2, 0.4}
    if set(full["load-magnitude"].round(10)) != magnitudes:
        raise ValueError("Task T load magnitudes do not match the frozen design")
    run_ticks = full.groupby("run_id")["tick"].agg(lambda values: frozenset(values))
    if len(run_ticks) != 16 or not run_ticks.eq(frozenset(range(161))).all():
        raise ValueError("Task T requires 16 complete tick 0–160 runs")

    late = full.loc[full["tick"].isin(THERMOSTAT_LATE_TICKS)].copy()
    late["absolute_error"] = (late["temperature"] - late["setpoint"]).abs()
    late_error = late.groupby("run_id")["absolute_error"].mean()
    run_info = full.groupby("run_id", sort=True).agg(
        arm=("arm", "first"), load_magnitude=("load-magnitude", "first")
    )
    passive_error = {
        float(row.load_magnitude): float(late_error.loc[run_id])
        for run_id, row in run_info.loc[run_info["arm"] == "passive"].iterrows()
    }
    labels = pd.Series(
        {
            run_id: int(late_error.loc[run_id] <= 0.25 * passive_error[float(row.load_magnitude)])
            for run_id, row in run_info.iterrows()
        },
        name="outcome",
        dtype=int,
    )
    if labels.sum() == 0 or labels.sum() == len(labels):
        raise ValueError("Task T frozen outcome is not discriminating")

    observed = full.loc[full["tick"].isin(THERMOSTAT_TICKS)].copy()
    counts = observed.groupby("run_id").size()
    ticks = observed.groupby("run_id")["tick"].agg(lambda values: frozenset(values))
    if not counts.eq(16).all() or not ticks.eq(THERMOSTAT_TICKS).all():
        raise ValueError("Task T does not have one complete tick 20–35 history per run")
    series = pd.DataFrame(
        {
            "run_id": observed["run_id"],
            "time": observed["tick"],
            "kind": "temperature",
            "value": observed["temperature"].astype(float),
        }
    ).sort_values(["run_id", "time"])

    run_ids = labels.index.rename("run_id")
    signed_load = run_info["load_magnitude"].astype(float).rename("meta_signed_load")
    metadata = signed_load.to_frame().reindex(run_ids)
    first = (
        observed.loc[observed["tick"] == 20]
        .set_index("run_id")["temperature"]
        .astype(float)
        .rename("endpoint_temperature")
    )
    groups = run_info["load_magnitude"].abs().round(1).rename("group").reindex(run_ids)
    return TaskData(
        name="thermostat_preservation",
        series=series.reset_index(drop=True),
        metadata=_indexed(metadata, run_ids),
        endpoint=_indexed(pd.concat([metadata, first], axis=1), run_ids),
        labels=labels.reindex(run_ids),
        groups=groups,
    )


def extract_tsfresh_features(task: TaskData) -> pd.DataFrame:
    """Run the frozen label-free off-the-shelf extractor."""

    try:
        from tsfresh import extract_features
        from tsfresh.feature_extraction import EfficientFCParameters
    except ImportError as error:
        raise RuntimeError("P5-000 requires `uv sync --extra representation-discovery`") from error

    features = extract_features(
        task.series,
        column_id="run_id",
        column_sort="time",
        column_kind="kind",
        column_value="value",
        default_fc_parameters=EfficientFCParameters(),
        disable_progressbar=True,
        n_jobs=0,
    )
    features.index.name = "run_id"
    return features.replace([np.inf, -np.inf], np.nan).reindex(task.run_ids)


def _finite_training_columns(frame: pd.DataFrame) -> list[str]:
    keep: list[str] = []
    for column in frame:
        finite = frame[column].replace([np.inf, -np.inf], np.nan).dropna()
        if not finite.empty and finite.nunique() > 1:
            keep.append(column)
    return keep


def grouped_score(
    features: pd.DataFrame,
    labels: pd.Series,
    groups: pd.Series,
    *,
    k: int = 12,
) -> ModelScore:
    """Apply the frozen fold-local feature selection and estimator."""

    features = features.reindex(labels.index)
    groups = groups.reindex(labels.index)
    probabilities = pd.Series(index=labels.index, dtype=float, name="probability")
    selections: Counter[str] = Counter()
    for group in sorted(groups.unique()):
        train = groups != group
        test = ~train
        y_train = labels.loc[train]
        if y_train.nunique() != 2:
            raise ValueError(f"training fold without both classes when holding out {group}")
        columns = _finite_training_columns(features.loc[train])
        if not columns:
            raise ValueError(f"no usable training features when holding out {group}")
        train_frame = features.loc[train, columns].replace([np.inf, -np.inf], np.nan)
        test_frame = features.loc[test, columns].replace([np.inf, -np.inf], np.nan)
        medians = train_frame.median()
        train_values = train_frame.fillna(medians).fillna(0.0)
        test_values = test_frame.fillna(medians).fillna(0.0)
        variable = train_values.nunique(dropna=False) > 1
        columns = list(variable.index[variable])
        if not columns:
            raise ValueError(f"no nonconstant training features when holding out {group}")
        train_values = train_values[columns]
        test_values = test_values[columns]
        selector = SelectKBest(f_classif, k=min(k, len(columns)))
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=r"Features .* are constant\.")
            warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*divide.*")
            selected_train = selector.fit_transform(train_values, y_train)
        selected_test = selector.transform(test_values)
        selected_names = [name for name, chosen in zip(columns, selector.get_support()) if chosen]
        selections.update(selected_names)
        scaler = StandardScaler().fit(selected_train)
        model = LogisticRegression(
            C=1,
            solver="liblinear",
            max_iter=2000,
            random_state=0,
        ).fit(scaler.transform(selected_train), y_train)
        probabilities.loc[test] = model.predict_proba(scaler.transform(selected_test))[:, 1]
    if probabilities.isna().any():
        raise ValueError("grouped validation did not predict every run")
    clipped = probabilities.clip(1e-6, 1 - 1e-6)
    predictions = (clipped >= 0.5).astype(int)
    return ModelScore(
        log_loss=float(log_loss(labels, clipped, labels=[0, 1])),
        balanced_accuracy=float(balanced_accuracy_score(labels, predictions)),
        predictions=clipped,
        selected_counts=selections,
    )


def _permuted_within_groups(labels: pd.Series, groups: pd.Series, seed: int) -> pd.Series:
    rng = np.random.default_rng(seed)
    shuffled = labels.copy()
    for group in sorted(groups.unique()):
        index = groups.index[groups == group]
        shuffled.loc[index] = rng.permutation(labels.loc[index].to_numpy())
    return shuffled


def evaluate_task(task: TaskData, extracted: pd.DataFrame) -> dict[str, Any]:
    """Score both nulls, the extracted model, shuffle attack, and ablation."""

    extracted_columns = [f"tsfresh__{column}" for column in extracted.columns]
    extracted = extracted.copy()
    extracted.columns = extracted_columns
    combined = pd.concat([task.metadata, extracted], axis=1)
    null_intervention = grouped_score(task.metadata, task.labels, task.groups)
    null_endpoint = grouped_score(task.endpoint, task.labels, task.groups)
    automated = grouped_score(combined, task.labels, task.groups)
    feature_counts = Counter(
        {
            name: count
            for name, count in automated.selected_counts.items()
            if name.startswith("tsfresh__")
        }
    )
    if not feature_counts:
        raise ValueError(f"{task.name} selected no extracted feature")
    max_count = max(feature_counts.values())
    top_feature = min(name for name, count in feature_counts.items() if count == max_count)
    ablated = grouped_score(combined.drop(columns=[top_feature]), task.labels, task.groups)
    shuffled_losses = [
        grouped_score(
            combined,
            _permuted_within_groups(task.labels, task.groups, seed),
            task.groups,
        ).log_loss
        for seed in range(9000, 9099)
    ]
    shuffle_fifth = float(np.percentile(shuffled_losses, 5))
    if task.name == "sorting_recovery":
        score_gate = automated.log_loss <= 0.9 * min(
            null_intervention.log_loss, null_endpoint.log_loss
        )
        ablation_gate = ablated.log_loss <= 0.9 * min(
            null_intervention.log_loss, null_endpoint.log_loss
        )
    else:
        score_gate = automated.log_loss < min(null_intervention.log_loss, null_endpoint.log_loss)
        ablation_gate = ablated.log_loss < min(null_intervention.log_loss, null_endpoint.log_loss)
    robustness_gate = ablated.log_loss <= 1.2 * automated.log_loss and ablation_gate
    shuffle_gate = automated.log_loss < shuffle_fifth
    return {
        "task": task.name,
        "n_runs": len(task.labels),
        "n_groups": int(task.groups.nunique()),
        "positive_fraction": float(task.labels.mean()),
        "n_extracted_features": int(extracted.shape[1]),
        "null_intervention_log_loss": null_intervention.log_loss,
        "null_endpoint_log_loss": null_endpoint.log_loss,
        "automated_log_loss": automated.log_loss,
        "ablated_log_loss": ablated.log_loss,
        "null_intervention_balanced_accuracy": null_intervention.balanced_accuracy,
        "null_endpoint_balanced_accuracy": null_endpoint.balanced_accuracy,
        "automated_balanced_accuracy": automated.balanced_accuracy,
        "top_extracted_feature": top_feature.removeprefix("tsfresh__"),
        "top_feature_fold_count": int(max_count),
        "shuffle_fifth_percentile_log_loss": shuffle_fifth,
        "shuffle_median_log_loss": float(np.median(shuffled_losses)),
        "score_gate": bool(score_gate),
        "shuffle_gate": bool(shuffle_gate),
        "ablation_gate": bool(robustness_gate),
        "task_passed": bool(score_gate and shuffle_gate and robustness_gate),
        "selected_feature_counts": {
            name.removeprefix("tsfresh__"): int(count)
            for name, count in feature_counts.most_common()
        },
        "predictions": {
            str(run_id): float(value) for run_id, value in automated.predictions.items()
        },
        "shuffle_losses": shuffled_losses,
    }
