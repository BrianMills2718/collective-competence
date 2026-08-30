"""Exhaustively test the frozen P2-004 moveable-cell order invariant."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from src.common import io

from .reachability import generate_cases

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p2_004_moveable_order_reachability.md"
SYSTEM_SIZE = 6
HORIZON_PER_CELL = 30
SCHEDULES = ("index", "shuffled")


def decide(frame: pd.DataFrame) -> dict[str, Any]:
    false_feasible = int((frame["moveable_order_feasible"] & ~frame["reached_goal"]).sum())
    false_infeasible = int((~frame["moveable_order_feasible"] & frame["reached_goal"]).sum())
    schedule_accuracy = {
        str(schedule): float(group["correct"].mean())
        for schedule, group in frame.groupby("activation_schedule")
    }
    mode_specific_cases = int(
        (
            ~frame["barrier_feasible"] & frame["moveable_order_feasible"] & frame["reached_goal"]
        ).sum()
    )
    outcomes = Counter(frame["reached_goal"].map(bool))
    criteria = {
        "accuracy_is_100_percent": bool(frame["correct"].all()),
        "zero_false_feasible": false_feasible == 0,
        "zero_false_infeasible": false_infeasible == 0,
        "every_schedule_is_100_percent": bool(
            schedule_accuracy and all(value == 1.0 for value in schedule_accuracy.values())
        ),
        "zero_time_limit_exits": not bool(frame["time_limit_exit"].any()),
        "both_outcomes_present": len(outcomes) == 2,
        "mode_specific_success_exists": mode_specific_cases > 0,
    }
    return {
        "study": "p2-004-moveable-order-reachability",
        "passed": all(criteria.values()),
        "criteria": criteria,
        "cases": len(frame),
        "accuracy": float(frame["correct"].mean()),
        "false_feasible": false_feasible,
        "false_infeasible": false_infeasible,
        "schedule_accuracy": schedule_accuracy,
        "time_limit_exits": int(frame["time_limit_exit"].sum()),
        "mode_specific_successes": mode_specific_cases,
        "outcomes": {str(key).lower(): value for key, value in outcomes.items()},
    }


def write_report(output: Path, frame: pd.DataFrame, decision: dict[str, Any]) -> Path:
    schedule_lines = [
        f"| {schedule} | {len(group):,} | {group['correct'].mean():.1%} | "
        f"{int(group['time_limit_exit'].sum())} |"
        for schedule, group in frame.groupby("activation_schedule")
    ]
    lines = [
        "# P2-004 moveable-cell order reachability — results",
        "",
        (
            "**PASS — the passive-order rule exactly classified the exhaustive size-6 cases.**"
            if decision["passed"]
            else "**NO-GO — the frozen passive-order rule was not exact.**"
        ),
        "",
        f"The new-size experiment evaluated {len(frame):,} moveable-damage branches.",
        "",
        "| Schedule | Cases | Accuracy | Time-limit exits |",
        "| --- | ---: | ---: | ---: |",
        *schedule_lines,
        "",
        (
            f"False feasible: **{decision['false_feasible']}**. "
            f"False infeasible: **{decision['false_infeasible']}**. "
            f"Mode-specific successful controls: **{decision['mode_specific_successes']:,}**."
        ),
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
            "This establishes an exact size-6 reachability invariant for this implementation "
            "of cell-view bubble sorting under moveable damage. It identifies preserved "
            "relative order among passive cells; it does not establish agency or goal possession."
        ),
        "",
    ]
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def execute(run_id: str = "p2-004-moveable-order-reachability", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    frame = generate_cases(
        n=SYSTEM_SIZE,
        schedules=SCHEDULES,
        freeze_modes=("moveable",),
        horizon_per_cell=HORIZON_PER_CELL,
    )
    frame.to_csv(output / "cases.csv", index=False)
    decision = decide(frame)
    (output / "decision.json").write_text(
        json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8"
    )
    write_report(output, frame, decision)
    io.write_metadata(
        output,
        {
            "experiment_id": "p2-004-moveable-order-reachability",
            "protocol": str(PROTOCOL.relative_to(ROOT)),
            "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            "system_size": SYSTEM_SIZE,
            "horizon_ticks": HORIZON_PER_CELL * SYSTEM_SIZE,
            "schedules": list(SCHEDULES),
            "freeze_modes": ["moveable"],
            "cases": len(frame),
        },
    )
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(
        args.run_id or "p2-004-moveable-order-reachability", exact=args.run_id is not None
    )
    print(output)


if __name__ == "__main__":
    main()
