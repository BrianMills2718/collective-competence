"""Score frozen select-or-abstain decisions from existing compact evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "results" / "p7-001-representation-tournament"
INPUTS = {
    "temporal": Path("results/p5-000-representation-discovery/scores.csv"),
    "relational": Path("results/p2-002c-relational-screen/representation_scores.csv"),
    "identity-conditioned": Path(
        "results/p4-002-heatbugs-blind-target-inference-001/held_out_seed_scores.csv"
    ),
    "network": Path("results/p5-001-slime-mold-network-001/summary.json"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def score_decision(
    *, candidate: float, null: float, threshold: float, metric_direction: str
) -> tuple[float, str]:
    """Return frozen improvement statistic and select/abstain action."""

    if metric_direction == "lower":
        if null <= 0:
            raise ValueError("Loss/error null must be positive")
        improvement = (null - candidate) / null
    elif metric_direction == "higher":
        improvement = candidate - null
    else:
        raise ValueError(f"Unknown metric direction: {metric_direction}")
    clears = improvement >= threshold or math.isclose(improvement, threshold, abs_tol=1e-12)
    return improvement, "select" if clears else "abstain"


def classify_tournament(n_correct: int, n_tasks: int = 4) -> str:
    if not 0 <= n_correct <= n_tasks:
        raise ValueError("Correct count must fall within the task count")
    if n_correct == n_tasks:
        return "pass"
    if n_correct >= 2:
        return "partial"
    return "fail"


def _temporal(path: Path) -> dict[str, Any]:
    frame = pd.read_csv(path)
    rows = frame[frame["task"] == "thermostat_preservation"]
    if len(rows) != 1:
        raise ValueError("Expected one thermostat_preservation row")
    row = rows.iloc[0]
    if int(row["n_runs"]) != 16 or int(row["n_groups"]) != 2:
        raise ValueError("Thermostat compact evidence has unexpected run/group structure")
    return _row(
        task="thermostat preservation",
        family="temporal",
        metric="log loss",
        candidate=float(row["automated_log_loss"]),
        null=float(row["null_intervention_log_loss"]),
        threshold=0.20,
        direction="lower",
        expected="select",
        source=path,
    )


def _relational(path: Path) -> dict[str, Any]:
    frame = pd.read_csv(path)
    candidate = frame[frame["representation"] == "Relational capability"]
    null = frame[frame["representation"] == "Intervention-only null"]
    if len(candidate) != 1 or len(null) != 1:
        raise ValueError("Sorting evidence is missing the relational candidate or primary null")
    if int(candidate.iloc[0]["n_runs"]) != 72 or int(null.iloc[0]["n_runs"]) != 72:
        raise ValueError("Sorting compact evidence must contain 72 runs")
    return _row(
        task="sorting recovery",
        family="relational",
        metric="log loss",
        candidate=float(candidate.iloc[0]["log_loss"]),
        null=float(null.iloc[0]["log_loss"]),
        threshold=0.10,
        direction="lower",
        expected="select",
        source=path,
    )


def _identity(path: Path) -> dict[str, Any]:
    frame = pd.read_csv(path)
    if set(frame.columns) != {"seed", "accuracy", "null_accuracy"}:
        raise ValueError("Heatbugs score table has an unexpected schema")
    if set(frame["seed"]) != set(range(5, 13)) or len(frame) != 8:
        raise ValueError("Heatbugs compact evidence must contain held-out seeds 5–12")
    return _row(
        task="Heatbugs target inference",
        family="identity-conditioned",
        metric="accuracy",
        candidate=float(frame["accuracy"].mean()),
        null=float(frame["null_accuracy"].mean()),
        threshold=0.10,
        direction="higher",
        expected="select",
        source=path,
    )


def _network(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("experiment") != "P5-001" or "prediction" not in payload:
        raise ValueError("Slime summary is not the expected P5-001 prediction artifact")
    prediction = payload["prediction"]
    simple_null = min(float(prediction["intervention_mae"]), float(prediction["density_mae"]))
    return _row(
        task="Slime recovery",
        family="network",
        metric="MAE",
        candidate=float(prediction["network_mae"]),
        null=simple_null,
        threshold=0.10,
        direction="lower",
        expected="abstain",
        source=path,
    )


def _row(
    *, task: str, family: str, metric: str, candidate: float, null: float,
    threshold: float, direction: str, expected: str, source: Path
) -> dict[str, Any]:
    improvement, action = score_decision(
        candidate=candidate, null=null, threshold=threshold, metric_direction=direction
    )
    return {
        "task": task,
        "family": family,
        "metric": metric,
        "candidate_score": candidate,
        "primary_null_score": null,
        "improvement": improvement,
        "threshold": threshold,
        "action": action,
        "expected_action": expected,
        "calibration_correct": action == expected,
        "source": str(source.relative_to(REPOSITORY_ROOT)),
    }


def load_scores(root: Path = REPOSITORY_ROOT) -> tuple[pd.DataFrame, dict[str, str]]:
    paths = {name: root / relative for name, relative in INPUTS.items()}
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing compact evidence:\n" + "\n".join(missing))
    rows = [
        _temporal(paths["temporal"]),
        _relational(paths["relational"]),
        _identity(paths["identity-conditioned"]),
        _network(paths["network"]),
    ]
    return pd.DataFrame(rows), {str(path.relative_to(root)): sha256(path) for path in paths.values()}


def _plot(scores: pd.DataFrame, path: Path) -> None:
    labels = [f"{row.task}\n{row.family}" for row in scores.itertuples()]
    colors = ["#16826c" if correct else "#c0392b" for correct in scores["calibration_correct"]]
    figure, axis = plt.subplots(figsize=(9, 4.8))
    bars = axis.bar(labels, scores["improvement"], color=colors)
    axis.scatter(range(len(scores)), scores["threshold"], marker="_", s=700, color="#17202a")
    axis.axhline(0, color="#7f8c8d", linewidth=1)
    axis.set_ylabel("Improvement over primary null")
    axis.set_title("P7-001 frozen select-or-abstain decisions")
    axis.text(0.99, 0.98, "black marker = selection threshold", transform=axis.transAxes,
              ha="right", va="top", fontsize=9)
    for bar, action in zip(bars, scores["action"], strict=True):
        y = bar.get_height()
        axis.text(bar.get_x() + bar.get_width() / 2, y, action.upper(), ha="center",
                  va="bottom" if y >= 0 else "top", fontsize=9, fontweight="bold")
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def run(output: Path = DEFAULT_OUTPUT, root: Path = REPOSITORY_ROOT) -> dict[str, Any]:
    scores, hashes = load_scores(root)
    output.mkdir(parents=True, exist_ok=True)
    n_correct = int(scores["calibration_correct"].sum())
    classification = classify_tournament(n_correct, len(scores))
    summary = {
        "experiment": "P7-001",
        "evidence_level": 1,
        "n_tasks": len(scores),
        "n_correct": n_correct,
        "classification": classification,
        "next_investment": {
            "pass": "freeze a prospective Level 2 selector test",
            "partial": "repair only the failed selection rule or observation family",
            "fail": "stop the generic selector line and reassess task-specific priors",
        }[classification],
        "input_sha256": hashes,
    }
    scores.to_csv(output / "scores.csv", index=False)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _plot(scores, output / "decision.png")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))


if __name__ == "__main__":
    main()
