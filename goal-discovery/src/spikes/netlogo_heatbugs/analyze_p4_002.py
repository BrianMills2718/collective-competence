"""Blind per-agent target inference for the P4-002 Heatbugs probes."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

POSITION_LIST = "map [t -> [(list who xcor ycor)] of t] sort turtles"
TRUTH_LIST = "map [t -> [list who ideal-temp] of t] sort turtles"
POPULATION = "count turtles"
PROBES = (10, 15, 20, 25, 30, 35, 40)
DISCOVERY_PROBES = frozenset({10, 20, 30, 40})
HELD_OUT_PROBES = frozenset({15, 25, 35})
FILES = {probe: f"p4-002-probe-{probe}.csv" for probe in PROBES}


def _parse_list(value: str, width: int) -> list[list[float]]:
    parsed = [
        [float(token) for token in match.split()] for match in re.findall(r"\[([^\[\]]+)\]", value)
    ]
    if not parsed or any(len(item) != width for item in parsed):
        raise ValueError(f"NetLogo list metric does not contain width-{width} rows")
    return parsed


def read_probe(path: Path, probe: int) -> pd.DataFrame:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise ValueError(f"{path} has no BehaviorSpace table header") from error
    headers = rows[header_index]
    data = [row for row in rows[header_index + 1 :] if row and any(value.strip() for value in row)]
    frame = pd.DataFrame(data, columns=headers)
    required = {"[run number]", "ticks", POSITION_LIST, TRUTH_LIST, POPULATION}
    if missing := required - set(frame):
        raise ValueError(f"{path} lacks required metrics: {sorted(missing)}")
    records: list[dict[str, Any]] = []
    for run_number, run in frame.groupby(frame["[run number]"].astype(int)):
        by_tick = {int(float(row["ticks"])): row for _, row in run.iterrows()}
        if set(by_tick) != {0, 1}:
            continue
        positions = {
            tick: {
                int(item[0]): (float(item[1]), float(item[2]))
                for item in _parse_list(row[POSITION_LIST], 3)
            }
            for tick, row in by_tick.items()
        }
        truths = {
            tick: {int(item[0]): float(item[1]) for item in _parse_list(row[TRUTH_LIST], 2)}
            for tick, row in by_tick.items()
        }
        identities = sorted(set(positions[0]) & set(positions[1]) & set(truths[0]) & set(truths[1]))
        for who in identities:
            x0, y0 = positions[0][who]
            x1, y1 = positions[1][who]
            records.append(
                {
                    "probe": probe,
                    "run_number": int(run_number),
                    "seed": int(run_number) + 4,
                    "who": who,
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "dx": x1 - x0,
                    "dy": y1 - y0,
                    "ideal_temp_truth": truths[0][who],
                    "truth_unchanged": truths[0][who] == truths[1][who],
                    "population": int(float(by_tick[0][POPULATION])),
                }
            )
    return pd.DataFrame(records)


def infer_targets(observations: pd.DataFrame) -> pd.DataFrame:
    """Infer targets from identity, probe, and movement only."""
    discovery = observations.loc[observations["probe"].isin(DISCOVERY_PROBES)]
    records: list[dict[str, Any]] = []
    for (seed, who), group in discovery.groupby(["seed", "who"]):
        exact = group.loc[group["direction"] == 0, "probe"]
        if not exact.empty:
            estimate = float(exact.iloc[0])
            lower = estimate
            upper = estimate
        else:
            hotter = group.loc[group["direction"] > 0, "probe"]
            cooler = group.loc[group["direction"] < 0, "probe"]
            lower = float(hotter.max()) if not hotter.empty else 10.0
            upper = float(cooler.min()) if not cooler.empty else 40.0
            estimate = (lower + upper) / 2
        records.append(
            {
                "seed": int(seed),
                "who": int(who),
                "lower_bound": lower,
                "upper_bound": upper,
                "target_estimate": estimate,
            }
        )
    return pd.DataFrame(records)


def evaluate(observations: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    observations = observations.copy()
    observations["direction"] = np.sign(observations["dx"]).astype(int)
    observations["interpretable"] = np.isclose(observations["dx"].abs(), 1) | np.isclose(
        observations["dx"], 0
    )
    expected_rows = len(PROBES) * 8 * 25
    complete = len(observations) == expected_rows and all(
        len(group) == len(PROBES) for _, group in observations.groupby(["seed", "who"])
    )
    paired_truth = bool(
        observations.groupby(["seed", "who"])["ideal_temp_truth"].nunique().eq(1).all()
        and observations["truth_unchanged"].all()
    )
    paired_positions = bool(
        observations.groupby(["seed", "who"])[["x0", "y0"]].nunique().eq(1).all().all()
    )
    estimates = infer_targets(observations.drop(columns=["ideal_temp_truth", "truth_unchanged"]))
    truth = (
        observations.groupby(["seed", "who"], as_index=False)
        .agg(ideal_temp_truth=("ideal_temp_truth", "first"))
        .sort_values(["seed", "who"])
    )
    estimates = estimates.merge(truth, on=["seed", "who"], validate="one_to_one")
    estimates["absolute_error"] = (
        estimates["target_estimate"] - estimates["ideal_temp_truth"]
    ).abs()
    held_out = observations.loc[observations["probe"].isin(HELD_OUT_PROBES)].merge(
        estimates[["seed", "who", "target_estimate"]],
        on=["seed", "who"],
        validate="many_to_one",
    )
    held_out["predicted_direction"] = np.sign(
        held_out["target_estimate"] - held_out["probe"]
    ).astype(int)
    held_out["null_direction"] = np.sign(25 - held_out["probe"]).astype(int)
    held_out["correct"] = held_out["predicted_direction"] == held_out["direction"]
    held_out["null_correct"] = held_out["null_direction"] == held_out["direction"]
    per_seed = (
        held_out.groupby("seed", as_index=False)
        .agg(accuracy=("correct", "mean"), null_accuracy=("null_correct", "mean"))
        .sort_values("seed")
    )
    accuracy = float(held_out["correct"].mean())
    null_accuracy = float(held_out["null_correct"].mean())
    criteria = {
        "all_probe_agent_pairs_complete": complete,
        "paired_hidden_targets_agree": paired_truth,
        "paired_initial_positions_agree": paired_positions,
        "population_preserved": bool(observations["population"].eq(25).all()),
        "interpretable_response_rate_at_least_95pct": bool(
            observations["interpretable"].mean() >= 0.95
        ),
        "median_absolute_target_error_at_most_5": bool(estimates["absolute_error"].median() <= 5),
        "held_out_accuracy_at_least_70pct": accuracy >= 0.70,
        "seven_seeds_at_least_65pct": bool((per_seed["accuracy"] >= 0.65).sum() >= 7),
        "beats_midpoint_null_by_15_points": accuracy - null_accuracy >= 0.15,
    }
    decision = {
        "study": "p4-002-heatbugs-blind-target-inference",
        "promoted": all(criteria.values()),
        "criteria": criteria,
        "agents": len(estimates),
        "median_absolute_target_error": float(estimates["absolute_error"].median()),
        "mean_absolute_target_error": float(estimates["absolute_error"].mean()),
        "held_out_accuracy": accuracy,
        "midpoint_null_accuracy": null_accuracy,
        "accuracy_advantage": accuracy - null_accuracy,
        "interpretable_response_rate": float(observations["interpretable"].mean()),
    }
    return estimates, per_seed, decision


def render_evidence(output: Path, estimates: pd.DataFrame, decision: dict[str, Any]) -> Path:
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.8), constrained_layout=True)
    axes[0].scatter(
        estimates["ideal_temp_truth"],
        estimates["target_estimate"],
        s=18,
        alpha=0.55,
        color="#38bdf8",
    )
    axes[0].plot([10, 40], [10, 40], color="#64748b", linestyle="--")
    axes[0].set(
        xlabel="Hidden ideal temperature", ylabel="Blind estimate", xlim=(8, 42), ylim=(8, 42)
    )
    axes[0].grid(alpha=0.2)
    axes[0].set_title("Per-agent target recovery")
    axes[1].bar(
        ["Inferred target", "Midpoint null"],
        [decision["held_out_accuracy"], decision["midpoint_null_accuracy"]],
        color=["#38bdf8", "#f97316"],
    )
    axes[1].axhline(0.70, color="#64748b", linestyle="--", label="Frozen gate")
    axes[1].set_ylim(0, 1)
    axes[1].set_ylabel("Held-out direction accuracy")
    axes[1].set_title("Unseen thermal probes")
    axes[1].legend(frameon=False)
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_report(
    output: Path,
    estimates: pd.DataFrame,
    per_seed: pd.DataFrame,
    decision: dict[str, Any],
) -> Path:
    verdict = (
        "**PROMOTE — blind per-agent target inference passed every frozen gate.**"
        if decision["promoted"]
        else "**STOP — blind per-agent target inference missed the frozen gate.**"
    )
    lines = [
        "# P4-002 blind heterogeneous Heatbugs target inference — results",
        "",
        verdict,
        "",
        (
            f"Median target error: **{decision['median_absolute_target_error']:.2f}°**. "
            f"Held-out direction accuracy: **{decision['held_out_accuracy']:.1%}** "
            f"versus **{decision['midpoint_null_accuracy']:.1%}** for the midpoint null."
        ),
        "",
        "| Seed | Inferred accuracy | Midpoint-null accuracy |",
        "| ---: | ---: | ---: |",
        *[
            f"| {row.seed} | {row.accuracy:.1%} | {row.null_accuracy:.1%} |"
            for row in per_seed.itertuples(index=False)
        ],
        "",
        "## Frozen criteria",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in decision["criteria"].items()
        ],
        "",
        "## Interpretation boundary",
        "",
        (
            "Inference used identity, controlled probe temperature, and observed movement "
            "only. Truth was joined after estimates were fixed for scoring. The targets "
            "remain explicitly authored micro targets, not an emergent collective goal."
        ),
        "",
        f"Scored agents: {len(estimates)}.",
        "",
    ]
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def analyze(output: Path) -> dict[str, Any]:
    observations = pd.concat(
        [read_probe(output / filename, probe) for probe, filename in FILES.items()],
        ignore_index=True,
    )
    observations.to_csv(output / "sealed_probe_records.csv", index=False)
    estimates, per_seed, decision = evaluate(observations)
    estimates.to_csv(output / "target_estimates.csv", index=False)
    per_seed.to_csv(output / "held_out_seed_scores.csv", index=False)
    (output / "decision.json").write_text(
        json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8"
    )
    render_evidence(output, estimates, decision)
    write_report(output, estimates, per_seed, decision)
    return decision
