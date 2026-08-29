"""Exhaustively test the frozen P2-003 immovable-barrier invariant."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

import pandas as pd

from src.common import io
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import SortingWorld

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p2_003_barrier_reachability.md"
DEFAULT_N = 5
DEFAULT_HORIZON_PER_CELL = 30
SCHEDULES = ("index", "shuffled")
FREEZE_MODES = ("immovable", "moveable")


def inversion_intervals(values: Sequence[int]) -> list[tuple[int, int]]:
    """Return every inverted pair as its inclusive positional interval."""

    return [
        (left, right)
        for left in range(len(values))
        for right in range(left + 1, len(values))
        if values[left] > values[right]
    ]


def barrier_feasible(values: Sequence[int], freeze_modes: Sequence[str]) -> bool:
    """Whether no inversion would need to cross an immovable position."""

    if len(values) != len(freeze_modes):
        raise ValueError("values and freeze modes must have the same length")
    barriers = {index for index, mode in enumerate(freeze_modes) if mode == "immovable"}
    return not any(
        any(left <= barrier <= right for barrier in barriers)
        for left, right in inversion_intervals(values)
    )


def selected_positions_cross_an_inversion(
    values: Sequence[int], selected_positions: Iterable[int]
) -> bool:
    """Whether the selected mask intersects at least one required crossing path."""

    selected = set(selected_positions)
    return any(
        any(left <= position <= right for position in selected)
        for left, right in inversion_intervals(values)
    )


def moveable_order_feasible(values: Sequence[int], selected_positions: Iterable[int]) -> bool:
    """Whether the passive-cell value subsequence is already ascending."""

    selected_values = [values[position] for position in sorted(selected_positions)]
    return selected_values == sorted(selected_values)


def _positions(mask: int, n: int) -> tuple[int, ...]:
    return tuple(index for index in range(n) if mask & (1 << index))


def _seed(permutation_index: int, mask: int, schedule_index: int) -> int:
    return permutation_index * 100 + mask * 2 + schedule_index


def run_case(
    values: Sequence[int],
    selected_positions: Sequence[int],
    schedule: str,
    freeze_mode: str,
    seed: int,
    *,
    horizon_ticks: int,
) -> dict[str, Any]:
    """Run one fully specified branch and return its observable terminal record."""

    world = SortingWorld.from_values(list(values), "bubble", order=schedule, seed=seed)
    apply(
        world,
        Intervention(
            "freeze_cells",
            {"positions": list(selected_positions), "mode": freeze_mode},
        ),
        seed=seed,
    )
    immovable_prediction = barrier_feasible(
        values,
        ["immovable" if index in selected_positions else "none" for index in range(len(values))],
    )
    moveable_prediction = moveable_order_feasible(values, selected_positions)
    predicted = immovable_prediction if freeze_mode == "immovable" else moveable_prediction
    world.run(horizon_ticks)
    reached_goal = world.values == sorted(world.values)
    quiescent = world.quiescent()
    return {
        "values_json": json.dumps(list(values), separators=(",", ":")),
        "selected_positions_json": json.dumps(list(selected_positions), separators=(",", ":")),
        "activation_schedule": schedule,
        "freeze_mode": freeze_mode,
        "seed": seed,
        "selected_crosses_inversion": selected_positions_cross_an_inversion(
            values, selected_positions
        ),
        "barrier_feasible": immovable_prediction,
        "moveable_order_feasible": moveable_prediction,
        "predicted_reachable": predicted,
        "reached_goal": reached_goal,
        "correct": predicted == reached_goal,
        "quiescent": quiescent,
        "time_limit_exit": not quiescent,
        "final_tick": world.tick,
        "final_values_json": json.dumps(world.values, separators=(",", ":")),
        "swaps": world.swaps,
        "steps": world.steps,
    }


def generate_cases(
    n: int = DEFAULT_N,
    *,
    schedules: Sequence[str] = SCHEDULES,
    freeze_modes: Sequence[str] = FREEZE_MODES,
    horizon_per_cell: int = DEFAULT_HORIZON_PER_CELL,
) -> pd.DataFrame:
    """Enumerate all states, nonempty masks, schedules, and requested modes."""

    records: list[dict[str, Any]] = []
    for permutation_index, values in enumerate(itertools.permutations(range(n))):
        for mask in range(1, 1 << n):
            positions = _positions(mask, n)
            for schedule_index, schedule in enumerate(schedules):
                seed = _seed(permutation_index, mask, schedule_index)
                pair_id = f"p{permutation_index:03d}-m{mask:02d}-{schedule}"
                for freeze_mode in freeze_modes:
                    record = run_case(
                        values,
                        positions,
                        schedule,
                        freeze_mode,
                        seed,
                        horizon_ticks=horizon_per_cell * n,
                    )
                    record.update(
                        {
                            "case_id": f"{pair_id}-{freeze_mode}",
                            "pair_id": pair_id,
                            "permutation_index": permutation_index,
                            "mask": mask,
                            "system_size": n,
                        }
                    )
                    records.append(record)
    return pd.DataFrame(records)


def decide(frame: pd.DataFrame) -> dict[str, Any]:
    immovable = frame.loc[frame["freeze_mode"] == "immovable"].copy()
    false_feasible = int((immovable["barrier_feasible"] & ~immovable["reached_goal"]).sum())
    false_infeasible = int((~immovable["barrier_feasible"] & immovable["reached_goal"]).sum())
    schedule_accuracy = {
        str(schedule): float(group["correct"].mean())
        for schedule, group in immovable.groupby("activation_schedule")
    }

    paired = frame.pivot(
        index=["pair_id", "selected_crosses_inversion"],
        columns="freeze_mode",
        values="reached_goal",
    ).reset_index()
    specificity_cases = paired.loc[
        paired["selected_crosses_inversion"]
        & ~paired["immovable"].astype(bool)
        & paired["moveable"].astype(bool)
    ]
    criteria = {
        "immovable_accuracy_is_100_percent": bool(immovable["correct"].all()),
        "zero_false_feasible": false_feasible == 0,
        "zero_false_infeasible": false_infeasible == 0,
        "every_schedule_is_100_percent": bool(
            schedule_accuracy and all(value == 1.0 for value in schedule_accuracy.values())
        ),
        "zero_immovable_time_limit_exits": not bool(immovable["time_limit_exit"].any()),
        "moveable_specificity_case_exists": len(specificity_cases) > 0,
    }
    return {
        "study": "p2-003-barrier-reachability",
        "passed": all(criteria.values()),
        "criteria": criteria,
        "immovable_cases": len(immovable),
        "moveable_cases": int((frame["freeze_mode"] == "moveable").sum()),
        "immovable_accuracy": float(immovable["correct"].mean()),
        "false_feasible": false_feasible,
        "false_infeasible": false_infeasible,
        "schedule_accuracy": schedule_accuracy,
        "immovable_time_limit_exits": int(immovable["time_limit_exit"].sum()),
        "moveable_specificity_cases": len(specificity_cases),
        "outcomes_by_mode": {
            str(mode): dict(Counter(group["reached_goal"].map(bool)))
            for mode, group in frame.groupby("freeze_mode")
        },
    }


def write_report(output: Path, frame: pd.DataFrame, decision: dict[str, Any]) -> Path:
    immovable = frame.loc[frame["freeze_mode"] == "immovable"]
    schedule_lines = [
        f"| {schedule} | {len(group):,} | {group['correct'].mean():.1%} | "
        f"{int(group['time_limit_exit'].sum())} |"
        for schedule, group in immovable.groupby("activation_schedule")
    ]
    lines = [
        "# P2-003 immovable-barrier reachability — results",
        "",
        (
            "**PASS — the barrier rule exactly classified the exhaustive size-5 cases.**"
            if decision["passed"]
            else "**NO-GO — the frozen barrier rule was not exact.**"
        ),
        "",
        (
            f"The experiment evaluated {len(frame):,} branches: "
            f"{decision['immovable_cases']:,} immovable cases and "
            f"{decision['moveable_cases']:,} matched moveable controls."
        ),
        "",
        "| Schedule | Immovable cases | Accuracy | Time-limit exits |",
        "| --- | ---: | ---: | ---: |",
        *schedule_lines,
        "",
        (
            f"False feasible: **{decision['false_feasible']}**. "
            f"False infeasible: **{decision['false_infeasible']}**. "
            f"Matched moveable specificity cases: "
            f"**{decision['moveable_specificity_cases']:,}**."
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
            "This establishes an exact size-5 reachability invariant for this implementation of "
            "cell-view bubble sorting under immovable damage. It identifies a mechanistic "
            "boundary on collective recovery; it does not establish agency, goal possession, "
            "or emergence."
        ),
        "",
    ]
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def execute(run_id: str = "p2-003-barrier-reachability", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    frame = generate_cases()
    frame.to_csv(output / "cases.csv", index=False)
    decision = decide(frame)
    (output / "decision.json").write_text(
        json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8"
    )
    write_report(output, frame, decision)
    protocol_bytes = PROTOCOL.read_bytes()
    io.write_metadata(
        output,
        {
            "experiment_id": "p2-003-barrier-reachability",
            "protocol": str(PROTOCOL.relative_to(ROOT)),
            "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
            "system_size": DEFAULT_N,
            "horizon_ticks": DEFAULT_HORIZON_PER_CELL * DEFAULT_N,
            "schedules": list(SCHEDULES),
            "freeze_modes": list(FREEZE_MODES),
            "cases": len(frame),
        },
    )
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(args.run_id or "p2-003-barrier-reachability", exact=args.run_id is not None)
    print(output)


if __name__ == "__main__":
    main()
