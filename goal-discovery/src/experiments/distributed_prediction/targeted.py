"""Run the frozen P2-002b within-intervention study."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

from src.common import io

from .analyze import (
    condition_summary,
    cross_validated_predictions,
    cross_validated_scores,
    discovery_decision,
    error_audit,
    final_decision,
    render_evidence,
    write_decisions,
)
from .analyze import holdout_scores as score_holdout
from .batch import BatchDesign, write_batch

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p2_002b_within_intervention_prediction.md"
DAMAGE_CONDITIONS = (("moveable", 2), ("moveable", 3), ("immovable", 1))
TARGETED_DISCOVERY = BatchDesign(
    "discovery",
    12,
    tuple(range(201, 213)),
    branch_fractions=(1.0 / 3.0,),
    damage_conditions=DAMAGE_CONDITIONS,
)
TARGETED_HOLDOUT = BatchDesign(
    "holdout",
    24,
    tuple(range(501, 513)),
    branch_fractions=(1.0 / 3.0,),
    damage_conditions=DAMAGE_CONDITIONS,
)


def eligibility(frame: pd.DataFrame) -> dict[str, Any]:
    strata = (
        frame.groupby(["activation_schedule", "freeze_mode", "freeze_count"])["reached_goal"]
        .agg(["size", "mean", "nunique"])
        .reset_index()
        .rename(columns={"size": "runs", "mean": "goal_rate", "nunique": "outcomes"})
    )
    criteria = {
        "all_six_strata_present": len(strata) == 6,
        "all_six_strata_mixed": len(strata) == 6 and bool(strata["outcomes"].eq(2).all()),
        "no_pre_sorted_branches": not bool(frame["pre_sorted"].any()),
    }
    return {
        "passed": all(criteria.values()),
        "criteria": criteria,
        "strata": strata.to_dict(orient="records"),
    }


def targeted_discovery_decision(frame: pd.DataFrame, scores: pd.DataFrame) -> dict[str, Any]:
    model_result = discovery_decision(scores)
    eligibility_result = eligibility(frame)
    criteria = {
        **eligibility_result["criteria"],
        **model_result["criteria"],
    }
    return {
        **model_result,
        "study": "p2-002b-within-intervention",
        "promoted": all(bool(value) for value in criteria.values()),
        "criteria": criteria,
        "eligibility": eligibility_result,
    }


def _score_table(scores: pd.DataFrame, scope: str) -> str:
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
    rows = [[str(value) for value in row] for row in selected.itertuples(index=False)]
    return "\n".join(
        [
            "| " + " | ".join(headings) + " |",
            "| " + " | ".join("---" for _ in headings) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def _strata_table(frame: pd.DataFrame) -> str:
    summary = (
        frame.groupby(["activation_schedule", "freeze_mode", "freeze_count"])["reached_goal"]
        .agg(["size", "sum", "mean"])
        .reset_index()
    )
    lines = [
        "| Schedule | Damage | Successes | Goal rate |",
        "| --- | --- | ---: | ---: |",
    ]
    for row in summary.itertuples(index=False):
        lines.append(
            f"| {row.activation_schedule} | {row.freeze_mode} × {row.freeze_count} | "
            f"{int(row.sum)} / {int(row.size)} | {row.mean:.1%} |"
        )
    return "\n".join(lines)


def write_targeted_report(
    output: Path,
    discovery: pd.DataFrame,
    scores: pd.DataFrame,
    discovery_result: dict[str, Any],
    holdout: pd.DataFrame | None,
    heldout_scores: pd.DataFrame | None,
    heldout_result: dict[str, Any] | None,
) -> Path:
    lines = [
        "# P2-002b within-intervention prediction — results",
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
            f"The new-seed size-12 study contains {len(discovery)} branches and has an overall "
            f"goal rate of {discovery['reached_goal'].mean():.1%}."
        ),
        "",
        "### Outcome eligibility",
        "",
        _strata_table(discovery),
        "",
        "### Representation comparison",
        "",
        _score_table(scores, "discovery: leave-one-seed-out"),
        "",
        "### Frozen criteria",
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
                    "**LEVEL 2 PASS.** The within-intervention signal survived size 24."
                    if heldout_result["passed"]
                    else "**NO-GO.** The promoted signal did not satisfy the size-24 gate."
                ),
                "",
                _strata_table(holdout),
                "",
                _score_table(heldout_scores, "holdout: all"),
                "",
                "### Held-out criteria",
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
                "This study tests whether observable retained capability adds predictive "
                "information inside nominally matched damage classes. It does not test agency, "
                "goal possession, or causal emergence."
            ),
            "",
        ]
    )
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def execute(run_id: str = "p2-002b-within-intervention", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    discovery_path, _, _ = write_batch(
        TARGETED_DISCOVERY,
        output,
        protocol_path=PROTOCOL,
        experiment_id="p2-002b-within-intervention-prediction",
    )
    discovery = pd.read_csv(discovery_path)
    scores = cross_validated_scores(discovery)
    scores.to_csv(output / "discovery_scores.csv", index=False)
    predictions = cross_validated_predictions(discovery)
    predictions.to_csv(output / "discovery_predictions.csv", index=False)
    error_audit(predictions).to_csv(output / "error_audit.csv", index=False)
    discovery_result = targeted_discovery_decision(discovery, scores)

    holdout: pd.DataFrame | None = None
    heldout_score_table: pd.DataFrame | None = None
    heldout_result = None
    if discovery_result["promoted"]:
        holdout_path, _, _ = write_batch(
            TARGETED_HOLDOUT,
            output,
            protocol_path=PROTOCOL,
            experiment_id="p2-002b-within-intervention-prediction",
        )
        holdout = pd.read_csv(holdout_path)
        heldout_score_table = score_holdout(discovery, holdout)
        heldout_score_table.to_csv(output / "holdout_scores.csv", index=False)
        heldout_result = final_decision(heldout_score_table)

    frames = [discovery] + ([] if holdout is None else [holdout])
    condition_summary(pd.concat(frames, ignore_index=True)).to_csv(
        output / "condition_summary.csv", index=False
    )
    write_decisions(output, discovery_result, heldout_result)
    write_targeted_report(
        output,
        discovery,
        scores,
        discovery_result,
        holdout,
        heldout_score_table,
        heldout_result,
    )
    render_evidence(output, discovery, scores, holdout, heldout_score_table)
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(args.run_id or "p2-002b-within-intervention", exact=args.run_id is not None)
    print(output)
    print((output / "result.md").read_text())


if __name__ == "__main__":
    main()
