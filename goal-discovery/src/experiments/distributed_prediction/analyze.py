"""Off-the-shelf representation comparisons for P2-002."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import balanced_accuracy_score, brier_score_loss, log_loss, mean_absolute_error
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

VALUE_FEATURES = [
    "value_boundary_norm",
    "value_inversions_norm",
    "value_ascending_run_norm",
    "value_sorted_prefix_norm",
]
INTERVENTION_FEATURES = [
    "intervention_system_size",
    "intervention_schedule_shuffled",
    "intervention_branch_time_norm",
    "intervention_freeze_fraction",
    "intervention_moveable",
    "intervention_immovable",
]
CAPABILITY_FEATURES = VALUE_FEATURES + [
    "cap_active_fraction",
    "cap_moveable_fraction",
    "cap_immovable_fraction",
    "cap_barrier_groups_norm",
    "cap_resolvable_inversion_fraction",
]
HISTORY_FEATURES = CAPABILITY_FEATURES + [
    "history_boundary_rate",
    "history_inversion_rate",
    "history_boundary_volatility",
]
MICRO_FEATURES = [
    f"micro_{channel}_{index:02d}"
    for channel in ("value", "moveable", "immovable")
    for index in range(12)
]
ABLATION_FEATURES = [
    feature for feature in CAPABILITY_FEATURES if feature != "cap_resolvable_inversion_fraction"
]

MODEL_FAMILIES: dict[str, list[str]] = {
    "Value-only macro": VALUE_FEATURES,
    "Intervention-only null": INTERVENTION_FEATURES,
    "Capability-aware macro": CAPABILITY_FEATURES,
    "History-aware macro": HISTORY_FEATURES,
    "Observable-micro baseline": MICRO_FEATURES,
    "Capability ablation": ABLATION_FEATURES,
}


def _classifier() -> Any:
    return make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2_000, solver="liblinear", random_state=0),
    )


def _time_regressor() -> Any:
    return make_pipeline(StandardScaler(), Ridge(alpha=1.0))


def _metrics(
    frame: pd.DataFrame,
    family: str,
    features: Sequence[str],
    probabilities: np.ndarray,
    predicted_time: np.ndarray,
    *,
    scope: str,
) -> dict[str, Any]:
    actual = frame["reached_goal"].astype(bool).to_numpy()
    predicted = probabilities >= 0.5
    success_mask = actual & np.isfinite(predicted_time)
    return {
        "scope": scope,
        "representation": family,
        "n_features": len(features),
        "n_runs": len(frame),
        "success_rate": float(actual.mean()),
        "log_loss": float(log_loss(actual, probabilities, labels=[False, True])),
        "brier_loss": float(brier_score_loss(actual, probabilities)),
        "balanced_accuracy": float(balanced_accuracy_score(actual, predicted)),
        "time_to_goal_mae_per_cell": (
            float(
                mean_absolute_error(
                    frame.loc[success_mask, "time_to_goal_per_cell"],
                    predicted_time[success_mask],
                )
            )
            if success_mask.any()
            else np.nan
        ),
    }


def _cross_validated_family(
    frame: pd.DataFrame, features: Sequence[str]
) -> tuple[np.ndarray, np.ndarray]:
    actual = frame["reached_goal"].astype(bool).to_numpy()
    groups = frame["seed"].to_numpy()
    splitter = LeaveOneGroupOut()
    x = frame[list(features)].to_numpy(dtype=float)
    probabilities = np.full(len(frame), np.nan)
    predicted_time = np.full(len(frame), np.nan)
    for train, test in splitter.split(x, actual, groups=groups):
        classifier = _classifier()
        classifier.fit(x[train], actual[train])
        probabilities[test] = classifier.predict_proba(x[test])[:, 1]

        successful_train = train[actual[train]]
        successful_test = test[actual[test]]
        if len(successful_train) >= 2 and len(successful_test):
            regressor = _time_regressor()
            regressor.fit(
                x[successful_train],
                frame.iloc[successful_train]["time_to_goal_per_cell"].to_numpy(dtype=float),
            )
            predicted_time[successful_test] = regressor.predict(x[successful_test])
    if not np.isfinite(probabilities).all():
        raise AssertionError("cross-validation did not predict every row")
    return probabilities, predicted_time


def cross_validated_scores(frame: pd.DataFrame) -> pd.DataFrame:
    """Leave one initial-condition seed out for every discovery prediction."""

    records: list[dict[str, Any]] = []
    for family, features in MODEL_FAMILIES.items():
        probabilities, predicted_time = _cross_validated_family(frame, features)
        records.append(
            _metrics(
                frame,
                family,
                features,
                probabilities,
                predicted_time,
                scope="discovery: leave-one-seed-out",
            )
        )
    return pd.DataFrame(records).sort_values("log_loss").reset_index(drop=True)


def score_feature_family(
    frame: pd.DataFrame, family: str, features: Sequence[str]
) -> dict[str, Any]:
    """Score one frozen feature family with the standard grouped evaluator."""

    probabilities, predicted_time = _cross_validated_family(frame, features)
    return _metrics(
        frame,
        family,
        features,
        probabilities,
        predicted_time,
        scope="discovery: leave-one-seed-out",
    )


def cross_validated_predictions(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the held-out probability and row loss used by the error audit."""

    columns = [
        "run_id",
        "seed",
        "activation_schedule",
        "branch_tick",
        "freeze_mode",
        "freeze_count",
        "reached_goal",
    ]
    records: list[pd.DataFrame] = []
    for family, features in MODEL_FAMILIES.items():
        probabilities, predicted_time = _cross_validated_family(frame, features)
        actual = frame["reached_goal"].astype(bool).to_numpy()
        clipped = np.clip(probabilities, 1e-12, 1 - 1e-12)
        row_loss = -(actual * np.log(clipped) + (~actual) * np.log(1 - clipped))
        result = frame[columns].copy()
        result["representation"] = family
        result["predicted_probability"] = probabilities
        result["predicted_goal"] = probabilities >= 0.5
        result["row_log_loss"] = row_loss
        result["predicted_time_to_goal_per_cell"] = predicted_time
        records.append(result)
    return pd.concat(records, ignore_index=True)


def error_audit(predictions: pd.DataFrame) -> pd.DataFrame:
    """Locate conditions where capability adds information beyond intervention."""

    selected = predictions.loc[
        predictions["representation"].isin(["Capability-aware macro", "Intervention-only null"])
    ]
    grouped = selected.groupby(
        [
            "activation_schedule",
            "branch_tick",
            "freeze_mode",
            "freeze_count",
            "representation",
        ],
        as_index=False,
    ).agg(
        runs=("run_id", "size"),
        goal_rate=("reached_goal", "mean"),
        mean_log_loss=("row_log_loss", "mean"),
    )
    pivot = grouped.pivot(
        index=["activation_schedule", "branch_tick", "freeze_mode", "freeze_count"],
        columns="representation",
        values="mean_log_loss",
    ).reset_index()
    pivot.columns.name = None
    pivot["capability_gain"] = pivot["Intervention-only null"] - pivot["Capability-aware macro"]
    context = grouped.drop_duplicates(
        ["activation_schedule", "branch_tick", "freeze_mode", "freeze_count"]
    )[["activation_schedule", "branch_tick", "freeze_mode", "freeze_count", "runs", "goal_rate"]]
    return context.merge(
        pivot,
        on=["activation_schedule", "branch_tick", "freeze_mode", "freeze_count"],
        validate="one_to_one",
    ).sort_values("capability_gain", ascending=False)


def _score_lookup(scores: pd.DataFrame, family: str, scope: str | None = None) -> pd.Series:
    rows = scores.loc[scores["representation"] == family]
    if scope is not None:
        rows = rows.loc[rows["scope"] == scope]
    if len(rows) != 1:
        raise ValueError(f"Expected one score for {family!r} in {scope!r}; found {len(rows)}")
    return rows.iloc[0]


def discovery_decision(scores: pd.DataFrame) -> dict[str, Any]:
    capability = _score_lookup(scores, "Capability-aware macro")
    value = _score_lookup(scores, "Value-only macro")
    intervention = _score_lookup(scores, "Intervention-only null")
    micro = _score_lookup(scores, "Observable-micro baseline")
    ablation = _score_lookup(scores, "Capability ablation")
    criteria = {
        "20pct_better_than_value": capability["log_loss"] <= 0.8 * value["log_loss"],
        "20pct_better_than_intervention": (
            capability["log_loss"] <= 0.8 * intervention["log_loss"]
        ),
        "within_10pct_of_micro": capability["log_loss"] <= 1.1 * micro["log_loss"],
        "quarter_micro_features": capability["n_features"] <= 0.25 * micro["n_features"],
        "brier_below_0_25": capability["brier_loss"] < 0.25,
        "ablation_beats_both_nulls": ablation["log_loss"]
        < min(value["log_loss"], intervention["log_loss"]),
    }
    return {
        "stage": "discovery",
        "promoted": all(bool(value) for value in criteria.values()),
        "criteria": {key: bool(value) for key, value in criteria.items()},
        "capability_log_loss": float(capability["log_loss"]),
        "value_log_loss": float(value["log_loss"]),
        "intervention_log_loss": float(intervention["log_loss"]),
        "micro_log_loss": float(micro["log_loss"]),
        "capability_brier_loss": float(capability["brier_loss"]),
    }


def holdout_scores(discovery: pd.DataFrame, holdout: pd.DataFrame) -> pd.DataFrame:
    """Fit once on discovery and score the frozen size-24 batch without tuning."""

    train_actual = discovery["reached_goal"].astype(bool).to_numpy()
    test_actual = holdout["reached_goal"].astype(bool).to_numpy()
    records: list[dict[str, Any]] = []
    for family, features in MODEL_FAMILIES.items():
        train_x = discovery[features].to_numpy(dtype=float)
        test_x = holdout[features].to_numpy(dtype=float)
        classifier = _classifier()
        classifier.fit(train_x, train_actual)
        probabilities = classifier.predict_proba(test_x)[:, 1]

        predicted_time = np.full(len(holdout), np.nan)
        successful_train = np.flatnonzero(train_actual)
        successful_test = np.flatnonzero(test_actual)
        if len(successful_train) >= 2 and len(successful_test):
            regressor = _time_regressor()
            regressor.fit(
                train_x[successful_train],
                discovery.iloc[successful_train]["time_to_goal_per_cell"].to_numpy(dtype=float),
            )
            predicted_time[successful_test] = regressor.predict(test_x[successful_test])

        records.append(
            _metrics(
                holdout,
                family,
                features,
                probabilities,
                predicted_time,
                scope="holdout: all",
            )
        )
        for schedule in sorted(holdout["activation_schedule"].unique()):
            mask = holdout["activation_schedule"].eq(schedule).to_numpy()
            records.append(
                _metrics(
                    holdout.loc[mask].reset_index(drop=True),
                    family,
                    features,
                    probabilities[mask],
                    predicted_time[mask],
                    scope=f"holdout: {schedule}",
                )
            )
    return pd.DataFrame(records).sort_values(["scope", "log_loss"]).reset_index(drop=True)


def final_decision(scores: pd.DataFrame) -> dict[str, Any]:
    criteria: dict[str, bool] = {}
    for scope in ("holdout: all", "holdout: index", "holdout: shuffled"):
        capability = _score_lookup(scores, "Capability-aware macro", scope)
        value = _score_lookup(scores, "Value-only macro", scope)
        intervention = _score_lookup(scores, "Intervention-only null", scope)
        criteria[f"20pct_better_than_both_nulls__{scope.removeprefix('holdout: ')}"] = bool(
            capability["log_loss"] <= 0.8 * value["log_loss"]
            and capability["log_loss"] <= 0.8 * intervention["log_loss"]
        )
    capability = _score_lookup(scores, "Capability-aware macro", "holdout: all")
    micro = _score_lookup(scores, "Observable-micro baseline", "holdout: all")
    ablation = _score_lookup(scores, "Capability ablation", "holdout: all")
    value = _score_lookup(scores, "Value-only macro", "holdout: all")
    intervention = _score_lookup(scores, "Intervention-only null", "holdout: all")
    criteria.update(
        {
            "within_10pct_of_micro": bool(capability["log_loss"] <= 1.1 * micro["log_loss"]),
            "quarter_micro_features": bool(capability["n_features"] <= 0.25 * micro["n_features"]),
            "brier_below_0_25": bool(capability["brier_loss"] < 0.25),
            "ablation_beats_both_nulls": bool(
                ablation["log_loss"] < min(value["log_loss"], intervention["log_loss"])
            ),
        }
    )
    return {
        "stage": "heldout",
        "passed": all(criteria.values()),
        "criteria": criteria,
        "capability_log_loss": float(capability["log_loss"]),
        "value_log_loss": float(value["log_loss"]),
        "intervention_log_loss": float(intervention["log_loss"]),
        "micro_log_loss": float(micro["log_loss"]),
        "capability_brier_loss": float(capability["brier_loss"]),
    }


def condition_summary(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame.groupby(
            ["batch", "activation_schedule", "branch_tick", "freeze_mode", "freeze_count"],
            as_index=False,
        )
        .agg(
            runs=("run_id", "size"),
            goal_rate=("reached_goal", "mean"),
            median_time_to_goal=("time_to_goal", "median"),
            mean_final_boundary=("final_boundary_norm", "mean"),
        )
        .sort_values(["batch", "activation_schedule", "branch_tick", "freeze_mode", "freeze_count"])
    )


def write_report(
    output_dir: Path,
    discovery: pd.DataFrame,
    discovery_scores: pd.DataFrame,
    discovery_result: dict[str, Any],
    holdout: pd.DataFrame | None = None,
    heldout_scores: pd.DataFrame | None = None,
    heldout_result: dict[str, Any] | None = None,
) -> Path:
    def table(scores: pd.DataFrame, scope: str) -> str:
        selected = scores.loc[
            scores["scope"] == scope,
            [
                "representation",
                "n_features",
                "log_loss",
                "brier_loss",
                "balanced_accuracy",
                "time_to_goal_mae_per_cell",
            ],
        ].copy()
        for column in selected.columns[2:]:
            selected[column] = selected[column].map(lambda value: f"{value:.3f}")
        headings = [str(column).replace("_", " ") for column in selected.columns]
        rows = [headings] + [
            [str(value) for value in row] for row in selected.itertuples(index=False)
        ]
        return "\n".join(
            [
                "| " + " | ".join(rows[0]) + " |",
                "| " + " | ".join("---" for _ in rows[0]) + " |",
                *["| " + " | ".join(row) + " |" for row in rows[1:]],
            ]
        )

    crossed = (
        discovery.groupby(["freeze_mode", "freeze_count"])["reached_goal"].nunique().eq(2).sum()
    )
    lines = [
        "# P2-002 crossed distributed prediction — results",
        "",
        "## Discovery decision",
        "",
        (
            "**PROMOTE to the frozen size-24 batch.**"
            if discovery_result["promoted"]
            else "**STOP before the size-24 batch.**"
        ),
        "",
        (
            f"The size-12 batch contains {len(discovery)} branches and an overall goal rate of "
            f"{discovery['reached_goal'].mean():.1%}. {crossed} of the six freeze mode/count "
            "classes contain both success and failure, so the original frozen-equals-failed "
            "confound is broken."
        ),
        "",
        table(discovery_scores, "discovery: leave-one-seed-out"),
        "",
        "Promotion criteria:",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in discovery_result["criteria"].items()
        ],
    ]
    if holdout is not None and heldout_scores is not None and heldout_result is not None:
        lines.extend(
            [
                "",
                "## Frozen size-24 result",
                "",
                (
                    "**LEVEL 2 PASS.** The macro signal survived the new size and both schedules."
                    if heldout_result["passed"]
                    else "**NO-GO.** The promoted signal did not satisfy the frozen held-out gate."
                ),
                "",
                (
                    f"The held-out batch contains {len(holdout)} branches on unseen seeds and "
                    f"has a goal rate of {holdout['reached_goal'].mean():.1%}."
                ),
                "",
                table(heldout_scores, "holdout: all"),
                "",
                "Held-out criteria:",
                "",
                *[
                    f"- {'pass' if passed else 'fail'} — `{name}`"
                    for name, passed in heldout_result["criteria"].items()
                ],
            ]
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            (
                "This test concerns predictive usefulness of an observable macro description. "
                "A pass would not establish agency, goal possession, or causal emergence. A "
                "failure is a decision to revise the observation/outcome before adding analysis "
                "machinery."
            ),
            "",
        ]
    )
    path = output_dir / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def render_evidence(
    output_dir: Path,
    discovery: pd.DataFrame,
    discovery_scores: pd.DataFrame,
    holdout: pd.DataFrame | None = None,
    heldout_scores: pd.DataFrame | None = None,
) -> Path:
    families = [
        "Value-only macro",
        "Intervention-only null",
        "Capability-aware macro",
        "History-aware macro",
        "Observable-micro baseline",
    ]
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)
    x = np.arange(len(families))
    discovery_lookup = discovery_scores.set_index("representation")
    axes[0].bar(
        x - (0.18 if heldout_scores is not None else 0),
        [discovery_lookup.loc[family, "log_loss"] for family in families],
        width=0.36 if heldout_scores is not None else 0.62,
        label="size 12 · grouped discovery",
        color="#2f81f7",
    )
    if heldout_scores is not None:
        heldout_lookup = heldout_scores.loc[heldout_scores["scope"] == "holdout: all"].set_index(
            "representation"
        )
        axes[0].bar(
            x + 0.18,
            [heldout_lookup.loc[family, "log_loss"] for family in families],
            width=0.36,
            label="size 24 · frozen holdout",
            color="#f0883e",
        )
    axes[0].set_xticks(x, [family.replace(" ", "\n", 1) for family in families])
    axes[0].set_ylabel("Attainment log loss · lower is better")
    axes[0].set_title("Representation comparison")
    axes[0].legend(frameon=False)
    axes[0].spines[["top", "right"]].set_visible(False)

    combined = discovery if holdout is None else pd.concat([discovery, holdout], ignore_index=True)
    summary = (
        combined.groupby(["batch", "freeze_mode", "freeze_count"])["reached_goal"]
        .mean()
        .reset_index()
    )
    mode_order = {"moveable": 0, "immovable": 1}
    conditions = sorted(
        {
            (str(row.freeze_mode), int(row.freeze_count))
            for row in summary[["freeze_mode", "freeze_count"]].itertuples(index=False)
        },
        key=lambda item: (mode_order.get(item[0], 2), item[1]),
    )
    labels = [f"{mode} {count}" for mode, count in conditions]
    positions = np.arange(len(labels))
    for index, batch in enumerate(summary["batch"].drop_duplicates()):
        subset = summary.loc[summary["batch"] == batch].set_index(["freeze_mode", "freeze_count"])
        rates = [subset.loc[(mode, count), "reached_goal"] for mode, count in conditions]
        offset = (index - (summary["batch"].nunique() - 1) / 2) * 0.36
        axes[1].bar(positions + offset, rates, width=0.34, label=batch)
    axes[1].set_xticks(positions, labels, rotation=25, ha="right")
    axes[1].set_ylim(0, 1)
    axes[1].set_ylabel("Goal attainment rate")
    axes[1].set_title("The crossed outcome surface")
    axes[1].legend(frameon=False)
    axes[1].spines[["top", "right"]].set_visible(False)
    path = output_dir / "evidence.png"
    figure.savefig(path, dpi=170)
    plt.close(figure)
    return path


def write_decisions(
    output_dir: Path, discovery: dict[str, Any], heldout: dict[str, Any] | None
) -> Path:
    path = output_dir / "decision.json"
    path.write_text(json.dumps({"discovery": discovery, "heldout": heldout}, indent=2) + "\n")
    return path
