"""Analysis for the frozen P14 relational Flocking experiment."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

A_DX = "mean [dx] of turtles with [who mod 4 = 0]"
A_DY = "mean [dy] of turtles with [who mod 4 = 0]"
B_DX = "mean [dx] of turtles with [who mod 4 != 0]"
B_DY = "mean [dy] of turtles with [who mod 4 != 0]"
ALL_DX = "mean [dx] of turtles"
ALL_DY = "mean [dy] of turtles"
NEIGHBORS = "mean [count flockmates] of turtles"
DISAGREEMENT = (
    "ifelse-value any? turtles with [any? flockmates] "
    "[mean [abs (subtract-headings heading average-flockmate-heading)] "
    "of turtles with [any? flockmates]] [0]"
)
VECTOR_COLUMNS = ["a_dx", "a_dy", "b_dx", "b_dy"]
ARMS = {
    "sham": "sham.csv",
    "cohort_rotate": "cohort-rotate.csv",
    "cohort_rotate_vision_off": "cohort-rotate-vision-off.csv",
    "whole_rotate": "whole-rotate.csv",
}


def read_behaviorspace(path: Path, arm: str) -> pd.DataFrame:
    """Read one rectangular NetLogo BehaviorSpace table."""
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise ValueError(f"{path} has no BehaviorSpace header") from error
    headers = rows[header_index]
    values = [row for row in rows[header_index + 1 :] if row and any(v.strip() for v in row)]
    if not values or any(len(row) != len(headers) for row in values):
        raise ValueError(f"{path} has no rectangular BehaviorSpace data")
    raw = pd.DataFrame(values, columns=headers)

    def column(name: str, *, last: bool = False) -> pd.Series:
        selected = raw.loc[:, name]
        if isinstance(selected, pd.DataFrame):
            selected = selected.iloc[:, -1 if last else 0]
        return selected

    required = {
        "[run number]",
        "ticks",
        A_DX,
        A_DY,
        B_DX,
        B_DY,
        ALL_DX,
        ALL_DY,
        NEIGHBORS,
        DISAGREEMENT,
        "count turtles",
        "vision",
    }
    if missing := required - set(raw.columns):
        raise ValueError(f"{path} lacks required metrics: {sorted(missing)}")
    return pd.DataFrame(
        {
            "arm": arm,
            "run_number": column("[run number]").astype(int),
            "tick": column("ticks").astype(float).round().astype(int),
            "a_dx": column(A_DX).astype(float),
            "a_dy": column(A_DY).astype(float),
            "b_dx": column(B_DX).astype(float),
            "b_dy": column(B_DY).astype(float),
            "all_dx": column(ALL_DX).astype(float),
            "all_dy": column(ALL_DY).astype(float),
            "mean_neighbors": column(NEIGHBORS).astype(float),
            "local_disagreement": column(DISAGREEMENT).astype(float),
            "population": column("count turtles").astype(int),
            "vision": column("vision", last=True).astype(float),
        }
    ).sort_values(["run_number", "tick"], ignore_index=True)


def _pairs(frame: pd.DataFrame, runs: list[int]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    selected = frame.loc[
        frame["run_number"].isin(runs) & frame["tick"].between(50, 150)
    ].copy()
    selected["next_run"] = selected["run_number"].shift(-1)
    next_values = selected[VECTOR_COLUMNS].shift(-1)
    valid = (selected["tick"] < 150) & (selected["next_run"] == selected["run_number"])
    return (
        selected.loc[valid, VECTOR_COLUMNS].to_numpy(float),
        next_values.loc[valid].to_numpy(float),
        selected.loc[valid, "run_number"].to_numpy(int),
    )


def _fit_matrix(x: np.ndarray, y: np.ndarray, family: str) -> np.ndarray:
    matrix = np.zeros((4, 5), dtype=float)
    if family == "invariant":
        matrix[:, 1:] = np.eye(4)
        return matrix
    for output in range(4):
        indices = [0, 1] if output < 2 else [2, 3]
        if family == "relational_affine":
            indices = [0, 1, 2, 3]
        design = np.column_stack([np.ones(len(x)), x[:, indices]])
        coefficients, *_ = np.linalg.lstsq(design, y[:, output], rcond=None)
        matrix[output, 0] = coefficients[0]
        matrix[output, np.asarray(indices) + 1] = coefficients[1:]
    return matrix


def _predict(x: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return np.column_stack([np.ones(len(x)), x]) @ matrix.T


def _per_run_rmse(
    x: np.ndarray, y: np.ndarray, runs: np.ndarray, matrix: np.ndarray
) -> dict[str, float]:
    prediction = _predict(x, matrix)
    return {
        str(run): float(np.sqrt(np.mean((prediction[runs == run] - y[runs == run]) ** 2)))
        for run in sorted(set(runs))
    }


def discover(frame: pd.DataFrame) -> dict[str, Any]:
    """Fit the frozen families and decide from untouched per-seed holdout error."""
    if sorted(frame["run_number"].unique()) != list(range(1, 13)):
        raise ValueError("discovery requires exactly 12 runs")
    if any(set(group["tick"]) != set(range(201)) for _, group in frame.groupby("run_number")):
        raise ValueError("discovery runs must contain ticks 0..200")
    train_x, train_y, train_runs = _pairs(frame, list(range(1, 7)))
    hold_x, hold_y, hold_runs = _pairs(frame, list(range(7, 13)))
    families = ["invariant", "independent_affine", "relational_affine"]
    matrices = {family: _fit_matrix(train_x, train_y, family) for family in families}
    train_scores = {
        family: _per_run_rmse(train_x, train_y, train_runs, matrix)
        for family, matrix in matrices.items()
    }
    holdout_scores = {
        family: _per_run_rmse(hold_x, hold_y, hold_runs, matrix)
        for family, matrix in matrices.items()
    }
    wins = 0
    improvements: list[float] = []
    for run in range(7, 13):
        key = str(run)
        relational = holdout_scores["relational_affine"][key]
        rival = min(
            holdout_scores["invariant"][key], holdout_scores["independent_affine"][key]
        )
        wins += relational < rival
        improvements.append((rival - relational) / rival if rival > 0 else 0.0)
    median_improvement = float(np.median(improvements))
    adequate = wins >= 5 and median_improvement >= 0.05
    return {
        "schema_version": 1,
        "study": "p14-relational-flocking",
        "selected_family": "relational_affine" if adequate else "none",
        "proposal_adequate": adequate,
        "criteria": {
            "relational_wins_at_least_five_holdout_runs": wins >= 5,
            "median_improvement_at_least_five_percent": median_improvement >= 0.05,
        },
        "relational_holdout_wins": wins,
        "median_holdout_improvement": median_improvement,
        "median_relational_holdout_rmse": float(
            np.median(list(holdout_scores["relational_affine"].values()))
        ),
        "train_scores": train_scores,
        "holdout_scores": holdout_scores,
        "coefficients": {name: matrix.tolist() for name, matrix in matrices.items()},
        "non_claim": (
            "The cohort partition, observation grammar and candidate families are supplied; "
            "adequacy would not establish a goal or competency."
        ),
    }


def render_discovery(output: Path, candidate: dict[str, Any]) -> Path:
    """Show every untouched run rather than hiding the proposal gate in an average."""
    runs = [str(run) for run in range(7, 13)]
    families = ["invariant", "independent_affine", "relational_affine"]
    labels = ["Invariant", "Independent", "Relational"]
    colors = ["#64748b", "#38bdf8", "#f97316"]
    x = np.arange(len(runs))
    width = 0.24
    figure, axis = plt.subplots(figsize=(10, 5), constrained_layout=True)
    for index, (family, label, color) in enumerate(zip(families, labels, colors, strict=True)):
        values = [candidate["holdout_scores"][family][run] for run in runs]
        axis.bar(x + (index - 1) * width, values, width, label=label, color=color)
    axis.set_xticks(x, [f"Seed {31000 + int(run)}" for run in runs])
    axis.set_ylabel("Untouched next-step vector RMSE (lower is better)")
    axis.set_title(
        "P14 proposal gate failed: relational model won "
        f"{candidate['relational_holdout_wins']}/6 held-out runs"
    )
    axis.grid(axis="y", alpha=0.2)
    axis.legend(frameon=False, ncol=3)
    path = output / "proposal-evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_discovery_result(output: Path, candidate: dict[str, Any]) -> Path:
    verdict = "PROCEED" if candidate["proposal_adequate"] else "STOP BEFORE INTERVENTIONS"
    lines = [
        "# P14 relational Flocking proposal result",
        "",
        f"**{verdict}.**",
        "",
        (
            f"The relational family won {candidate['relational_holdout_wins']}/6 untouched runs. "
            f"Median improvement over the better simple rival was "
            f"{candidate['median_holdout_improvement']:.1%}; the frozen gate required at least "
            "5/6 wins and +5%."
        ),
        "",
        (
            "The arbitrary global identity-cohort relation did not earn an intervention test. "
            "This supports an artifact/over-capacity explanation at the proposal stage; it does "
            "not show that the locally interacting flock lacks useful relations or competencies."
        ),
        "",
        "No perturbation outcome was generated.",
        "",
    ]
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _direction(dx: float, dy: float) -> float:
    return math.degrees(math.atan2(dx, dy)) % 360


def _angular_distance(first: float, second: float) -> float:
    return abs((first - second + 180) % 360 - 180)


def add_readouts(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["cohort_gap"] = [
        _angular_distance(_direction(a_x, a_y), _direction(b_x, b_y))
        for a_x, a_y, b_x, b_y in result[VECTOR_COLUMNS].itertuples(index=False, name=None)
    ]
    result["absolute_heading"] = [
        _direction(dx, dy) for dx, dy in result[["all_dx", "all_dy"]].itertuples(index=False, name=None)
    ]
    return result


def _window(frame: pd.DataFrame, arm: str, run: int, start: int, end: int) -> pd.DataFrame:
    return frame.loc[
        (frame["arm"] == arm)
        & (frame["run_number"] == run)
        & frame["tick"].between(start, end)
    ]


def _recursive_rmse(frame: pd.DataFrame, run: int, matrix: np.ndarray) -> float:
    actual = _window(frame, "cohort_rotate", run, 151, 200)
    state = actual.iloc[0][VECTOR_COLUMNS].to_numpy(float)
    predictions = [state.copy()]
    for _ in range(1, len(actual)):
        state = _predict(state.reshape(1, -1), matrix)[0]
        predictions.append(state.copy())
    return float(np.sqrt(np.mean((np.asarray(predictions) - actual[VECTOR_COLUMNS].to_numpy()) ** 2)))


def evaluate(frame: pd.DataFrame, candidate: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    if not candidate.get("proposal_adequate"):
        raise ValueError("evaluation is forbidden because the relational proposal failed")
    expected_ticks = set(range(351))
    runs = list(range(1, 11))
    complete = sorted(frame["run_number"].unique()) == runs and all(
        set(group["tick"]) == expected_ticks for _, group in frame.groupby(["arm", "run_number"])
    )
    observation_columns = VECTOR_COLUMNS + [
        "all_dx",
        "all_dy",
        "mean_neighbors",
        "local_disagreement",
        "population",
        "vision",
    ]
    prebranch_identical = all(
        np.allclose(
            _window(frame, "sham", run, 0, 150)[observation_columns],
            _window(frame, arm, run, 0, 150)[observation_columns],
            rtol=0,
            atol=1e-12,
        )
        for run in runs
        for arm in ARMS
    )
    finite = bool(np.isfinite(frame[observation_columns].to_numpy(float)).all())
    population = bool(frame["population"].eq(100).all())
    matrix = np.asarray(candidate["coefficients"]["relational_affine"], dtype=float)
    envelope = 2 * float(candidate["median_relational_holdout_rmse"])
    rows: list[dict[str, Any]] = []
    for run in runs:
        sham_immediate = _window(frame, "sham", run, 151, 160)
        active_immediate = _window(frame, "cohort_rotate", run, 151, 160)
        whole_immediate = _window(frame, "whole_rotate", run, 151, 160)
        sham_late = _window(frame, "sham", run, 320, 350)
        active_late = _window(frame, "cohort_rotate", run, 320, 350)
        off_late = _window(frame, "cohort_rotate_vision_off", run, 320, 350)
        whole_late = _window(frame, "whole_rotate", run, 320, 350)
        pre = _window(frame, "sham", run, 140, 150)
        pre_heading = _direction(float(pre["all_dx"].mean()), float(pre["all_dy"].mean()))
        whole_now = _direction(
            float(whole_immediate["all_dx"].mean()), float(whole_immediate["all_dy"].mean())
        )
        whole_end = _direction(float(whole_late["all_dx"].mean()), float(whole_late["all_dy"].mean()))
        fixed_shock = float(active_immediate["cohort_gap"].mean() - sham_immediate["cohort_gap"].mean())
        dynamic_shock = float(
            active_immediate["local_disagreement"].mean()
            - sham_immediate["local_disagreement"].mean()
        )
        late_fixed_gap = float(active_late["cohort_gap"].mean() - sham_late["cohort_gap"].mean())
        late_dynamic_gap = float(
            active_late["local_disagreement"].mean() - sham_late["local_disagreement"].mean()
        )
        interaction_advantage = float(
            off_late["cohort_gap"].mean() - active_late["cohort_gap"].mean()
        )
        immediate_invariance_error = abs(
            float(whole_immediate["cohort_gap"].mean() - sham_immediate["cohort_gap"].mean())
        )
        recursive_rmse = _recursive_rmse(frame, run, matrix)
        rows.append(
            {
                "run_number": run,
                "fixed_cohort_shock": fixed_shock,
                "dynamic_neighbor_shock": dynamic_shock,
                "late_fixed_cohort_gap": late_fixed_gap,
                "late_dynamic_neighbor_gap": late_dynamic_gap,
                "interaction_fixed_gap_advantage": interaction_advantage,
                "whole_rotation_immediate_heading_error": _angular_distance(whole_now, pre_heading),
                "whole_rotation_relational_error": immediate_invariance_error,
                "whole_rotation_late_heading_error": _angular_distance(whole_end, pre_heading),
                "passive_recursive_vector_rmse": recursive_rmse,
                "shock_valid": fixed_shock >= 20 and dynamic_shock >= 20,
                "rotation_valid": _angular_distance(whole_now, pre_heading) >= 75
                and immediate_invariance_error <= 5,
                "fixed_relation_restored": abs(late_fixed_gap) <= 5,
                "dynamic_relation_restored": abs(late_dynamic_gap) <= 5,
                "interaction_required": interaction_advantage >= 20,
                "absolute_heading_not_defended": _angular_distance(whole_end, pre_heading) >= 60,
                "passive_forecast_adequate": recursive_rmse <= envelope,
            }
        )
    summary = pd.DataFrame(rows)
    integrity = {
        "ten_complete_runs_per_arm": complete,
        "prebranch_arms_identical": prebranch_identical,
        "population_and_readouts_valid": population and finite,
        "cohort_shock_valid_in_eight_runs": bool(summary["shock_valid"].sum() >= 8),
        "whole_rotation_valid_in_eight_runs": bool(summary["rotation_valid"].sum() >= 8),
    }
    integrity_passed = all(integrity.values())
    fixed_restored = bool(summary["fixed_relation_restored"].sum() >= 8)
    dynamic_restored = bool(summary["dynamic_relation_restored"].sum() >= 8)
    artifact_supported = dynamic_restored and not fixed_restored
    interaction_required = bool(summary["interaction_required"].sum() >= 8)
    heading_not_defended = bool(summary["absolute_heading_not_defended"].sum() >= 8)
    passive_adequate = bool(summary["passive_forecast_adequate"].sum() >= 8)
    competency_survives = (
        integrity_passed
        and fixed_restored
        and dynamic_restored
        and interaction_required
        and heading_not_defended
        and not passive_adequate
        and not artifact_supported
    )
    decision = {
        "schema_version": 1,
        "study": "p14-relational-flocking",
        "integrity_passed": integrity_passed,
        "integrity": integrity,
        "proposal_adequate": True,
        "relation_restored": fixed_restored and dynamic_restored,
        "fixed_relation_restored": fixed_restored,
        "dynamic_relation_restored": dynamic_restored,
        "interaction_required": interaction_required,
        "invariant_explanation_supported": heading_not_defended,
        "measurement_artifact_supported": artifact_supported,
        "passive_forecast_adequate": passive_adequate,
        "competency_survives": competency_survives,
        "verdict": (
            "invalid"
            if not integrity_passed
            else "competency_candidate_survives"
            if competency_survives
            else "rival_explanation_sufficient_or_relation_failed"
        ),
        "claim_limit": (
            "A surviving competency candidate would only reject the frozen simple rivals; "
            "it would not establish a goal, agency, or exhaust passive mechanisms."
        ),
    }
    return summary, decision


def render(output: Path, frame: pd.DataFrame, decision: dict[str, Any]) -> Path:
    colors = {
        "sham": "#38bdf8",
        "cohort_rotate": "#f97316",
        "cohort_rotate_vision_off": "#ef4444",
        "whole_rotate": "#8b5cf6",
    }
    labels = {
        "sham": "Sham",
        "cohort_rotate": "Rotate cohort",
        "cohort_rotate_vision_off": "Rotate + interactions off",
        "whole_rotate": "Rotate whole flock",
    }
    figure, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, constrained_layout=True)
    for arm in ARMS:
        aggregate = frame.loc[frame["arm"] == arm].groupby("tick", as_index=False).agg(
            cohort_gap=("cohort_gap", "mean"), disagreement=("local_disagreement", "mean")
        )
        axes[0].plot(aggregate["tick"], aggregate["cohort_gap"], color=colors[arm], label=labels[arm])
        axes[1].plot(aggregate["tick"], aggregate["disagreement"], color=colors[arm], label=labels[arm])
    for axis in axes:
        axis.axvline(150, color="#64748b", linestyle="--", linewidth=1)
        axis.grid(alpha=0.2)
        axis.legend(frameon=False, ncol=2)
    axes[0].set_ylabel("Fixed cohort heading gap (°)")
    axes[0].set_title(f"P14 rival explanations — {decision['verdict']}")
    axes[1].set_ylabel("Current-neighbor disagreement (°)")
    axes[1].set_xlabel("Tick")
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_result(output: Path, decision: dict[str, Any], summary: pd.DataFrame) -> Path:
    lines = [
        "# P14 relational Flocking result",
        "",
        f"**Verdict: `{decision['verdict']}`.**",
        "",
        "| Explanation/readout | Outcome |",
        "|---|---|",
        f"| Integrity | {'pass' if decision['integrity_passed'] else 'fail'} |",
        f"| Relation restored on fixed and dynamic readouts | {decision['relation_restored']} |",
        f"| Live interaction required | {decision['interaction_required']} |",
        f"| Rotational invariance / no absolute-heading defense | {decision['invariant_explanation_supported']} |",
        f"| Measurement artifact supported | {decision['measurement_artifact_supported']} |",
        f"| Frozen passive forecast adequate | {decision['passive_forecast_adequate']} |",
        f"| Competency candidate survives | {decision['competency_survives']} |",
        "",
        "## Seed counts",
        "",
        f"- fixed relation restored: {int(summary['fixed_relation_restored'].sum())}/10",
        f"- dynamic relation restored: {int(summary['dynamic_relation_restored'].sum())}/10",
        f"- interaction required: {int(summary['interaction_required'].sum())}/10",
        f"- passive forecast adequate: {int(summary['passive_forecast_adequate'].sum())}/10",
        "",
        "## Claim boundary",
        "",
        decision["claim_limit"],
        "",
    ]
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def dump_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
