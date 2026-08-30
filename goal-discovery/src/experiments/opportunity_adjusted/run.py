"""Run the frozen P2-005 opportunity-adjusted discovery experiment."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.common import io
from src.experiments.distributed_prediction.reachability import (
    barrier_feasible,
    moveable_order_feasible,
)
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import ALGOTYPES, SortingWorld

from .graph import opportunity

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p2_005_opportunity_adjusted_performance.md"
SYSTEM_SIZE = 4
HORIZON_PER_CELL = 30
SCHEDULES = ("index", "shuffled")
FREEZE_MODES = ("moveable", "immovable")
REPLICATES = tuple(range(4))


def _positions(mask: int, n: int) -> tuple[int, ...]:
    return tuple(index for index in range(n) if mask & (1 << index))


def _world(
    values: tuple[int, ...],
    algotype: str,
    positions: tuple[int, ...],
    freeze_mode: str,
    *,
    schedule: str = "index",
    seed: int = 0,
) -> SortingWorld:
    world = SortingWorld.from_values(list(values), algotype, order=schedule, seed=seed)
    apply(
        world,
        Intervention(
            "freeze_cells",
            {"positions": list(positions), "mode": freeze_mode},
        ),
        seed=seed,
    )
    return world


def generate_discovery(
    n: int = SYSTEM_SIZE,
    *,
    schedules: tuple[str, ...] = SCHEDULES,
    replicates: tuple[int, ...] = REPLICATES,
    horizon_per_cell: int = HORIZON_PER_CELL,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    oracle_records: list[dict[str, Any]] = []
    run_records: list[dict[str, Any]] = []
    case_index = 0
    for permutation_index, values in enumerate(itertools.permutations(range(n))):
        for mask in range(1, 1 << n):
            positions = _positions(mask, n)
            for freeze_mode in FREEZE_MODES:
                modes = [freeze_mode if index in positions else "none" for index in range(n)]
                for algotype in ALGOTYPES:
                    case_id = f"{algotype}-{freeze_mode}-p{permutation_index:02d}-m{mask:02d}"
                    graph_result = opportunity(_world(values, algotype, positions, freeze_mode))
                    oracle_records.append(
                        {
                            "case_id": case_id,
                            "case_index": case_index,
                            "system_size": n,
                            "permutation_index": permutation_index,
                            "values_json": json.dumps(values, separators=(",", ":")),
                            "mask": mask,
                            "positions_json": json.dumps(positions, separators=(",", ":")),
                            "freeze_mode": freeze_mode,
                            "algotype": algotype,
                            "graph_reachable": graph_result.reachable,
                            "shortest_activations": graph_result.shortest_activations,
                            "graph_nodes": graph_result.graph_nodes,
                            "graph_edges": graph_result.graph_edges,
                            "bubble_invariant": (
                                barrier_feasible(values, modes)
                                if freeze_mode == "immovable"
                                else moveable_order_feasible(values, positions)
                            ),
                        }
                    )
                    for schedule_index, schedule in enumerate(schedules):
                        for replicate in replicates:
                            seed = case_index * 100 + schedule_index * 10 + replicate
                            world = _world(
                                values,
                                algotype,
                                positions,
                                freeze_mode,
                                schedule=schedule,
                                seed=seed,
                            )
                            world.run(horizon_per_cell * n)
                            quiescent = world.quiescent()
                            run_records.append(
                                {
                                    "run_id": f"{case_id}-{schedule}-r{replicate}",
                                    "case_id": case_id,
                                    "case_index": case_index,
                                    "algotype": algotype,
                                    "freeze_mode": freeze_mode,
                                    "activation_schedule": schedule,
                                    "replicate": replicate,
                                    "seed": seed,
                                    "graph_reachable": graph_result.reachable,
                                    "reached_goal": world.values == sorted(world.values),
                                    "quiescent": quiescent,
                                    "time_limit_exit": not quiescent,
                                    "final_tick": world.tick,
                                    "final_values_json": json.dumps(
                                        world.values, separators=(",", ":")
                                    ),
                                }
                            )
                    case_index += 1
    return pd.DataFrame(oracle_records), pd.DataFrame(run_records)


def summarize(oracle: pd.DataFrame, runs: pd.DataFrame) -> pd.DataFrame:
    case_schedule = runs.groupby(
        ["case_id", "algotype", "freeze_mode", "activation_schedule"],
        as_index=False,
    ).agg(
        graph_reachable=("graph_reachable", "first"),
        successes=("reached_goal", "sum"),
        run_count=("run_id", "size"),
    )
    case_schedule["realized"] = case_schedule["successes"] > 0
    case_schedule["robust"] = case_schedule["successes"] == case_schedule["run_count"]

    records: list[dict[str, Any]] = []
    for (algotype, mode, schedule), cases in case_schedule.groupby(
        ["algotype", "freeze_mode", "activation_schedule"]
    ):
        reachable = cases.loc[cases["graph_reachable"]]
        matching_runs = runs.loc[
            (runs["algotype"] == algotype)
            & (runs["freeze_mode"] == mode)
            & (runs["activation_schedule"] == schedule)
            & runs["graph_reachable"]
        ]
        opportunity_cases = oracle.loc[
            (oracle["algotype"] == algotype) & (oracle["freeze_mode"] == mode)
        ]
        records.append(
            {
                "algotype": algotype,
                "freeze_mode": mode,
                "activation_schedule": schedule,
                "cases": len(cases),
                "reachable_cases": len(reachable),
                "opportunity_rate": float(opportunity_cases["graph_reachable"].mean()),
                "realization_rate": float(matching_runs["reached_goal"].mean()),
                "realized_case_rate": float(reachable["realized"].mean()),
                "robust_case_rate": float(reachable["robust"].mean()),
            }
        )
    return pd.DataFrame(records).sort_values(["freeze_mode", "activation_schedule", "algotype"])


def _unique_extreme(group: pd.DataFrame, kind: str) -> str | None:
    extreme = group["robust_case_rate"].max() if kind == "best" else group["robust_case_rate"].min()
    matching = group.loc[group["robust_case_rate"] == extreme, "algotype"]
    return str(matching.iloc[0]) if len(matching) == 1 else None


def decide(oracle: pd.DataFrame, runs: pd.DataFrame, summary: pd.DataFrame) -> dict[str, Any]:
    bubble = oracle.loc[oracle["algotype"] == "bubble"]
    integrity = {
        "bubble_immovable_oracle_matches_invariant": bool(
            bubble.loc[bubble["freeze_mode"] == "immovable", "graph_reachable"].equals(
                bubble.loc[bubble["freeze_mode"] == "immovable", "bubble_invariant"]
            )
        ),
        "bubble_moveable_oracle_matches_invariant": bool(
            bubble.loc[bubble["freeze_mode"] == "moveable", "graph_reachable"].equals(
                bubble.loc[bubble["freeze_mode"] == "moveable", "bubble_invariant"]
            )
        ),
        "zero_unreachable_successes": not bool(
            (~runs["graph_reachable"] & runs["reached_goal"]).any()
        ),
        "zero_time_limit_exits": not bool(runs["time_limit_exit"].any()),
        "at_least_30_reachable_cases_per_cell": bool(summary["reachable_cases"].ge(30).all()),
    }

    candidates: list[dict[str, Any]] = []
    for mode in FREEZE_MODES:
        schedule_groups = {
            str(schedule): group
            for schedule, group in summary.loc[summary["freeze_mode"] == mode].groupby(
                "activation_schedule"
            )
        }
        if set(schedule_groups) != set(SCHEDULES):
            continue
        best = {
            schedule: _unique_extreme(group, "best") for schedule, group in schedule_groups.items()
        }
        worst = {
            schedule: _unique_extreme(group, "worst") for schedule, group in schedule_groups.items()
        }
        gaps = {
            schedule: float(group["robust_case_rate"].max() - group["robust_case_rate"].min())
            for schedule, group in schedule_groups.items()
        }
        passed = (
            len(set(best.values())) == 1
            and None not in best.values()
            and len(set(worst.values())) == 1
            and None not in worst.values()
            and all(gap >= 0.20 for gap in gaps.values())
        )
        candidates.append(
            {
                "freeze_mode": mode,
                "best_by_schedule": best,
                "worst_by_schedule": worst,
                "robust_rate_gap_by_schedule": gaps,
                "passed": passed,
            }
        )

    return {
        "study": "p2-005-opportunity-adjusted-performance",
        "integrity_passed": all(integrity.values()),
        "promoted": all(integrity.values()) and any(item["passed"] for item in candidates),
        "integrity_criteria": integrity,
        "promotion_candidates": candidates,
        "oracle_cases": len(oracle),
        "actual_runs": len(runs),
    }


def _summary_table(summary: pd.DataFrame) -> str:
    lines = [
        "| Damage | Schedule | Algotype | Reachable | Opportunity | Realization | Any seed | All seeds |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary.itertuples(index=False):
        lines.append(
            f"| {row.freeze_mode} | {row.activation_schedule} | {row.algotype} | "
            f"{row.reachable_cases} | {row.opportunity_rate:.1%} | "
            f"{row.realization_rate:.1%} | {row.realized_case_rate:.1%} | "
            f"{row.robust_case_rate:.1%} |"
        )
    return "\n".join(lines)


def write_report(
    output: Path,
    oracle: pd.DataFrame,
    runs: pd.DataFrame,
    summary: pd.DataFrame,
    decision: dict[str, Any],
) -> Path:
    lines = [
        "# P2-005 opportunity-adjusted performance — discovery results",
        "",
        (
            "**PROMOTE — freeze a new size-5 confirmation batch.**"
            if decision["promoted"]
            else "**STOP — the frozen opportunity-adjusted promotion gate did not pass.**"
        ),
        "",
        (
            f"The discovery contains {len(oracle):,} graph-oracle cases and "
            f"{len(runs):,} scheduled branches."
        ),
        "",
        _summary_table(summary),
        "",
        "## Integrity gates",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in decision["integrity_criteria"].items()
        ],
        "",
        "## Promotion comparisons",
        "",
        *[
            (
                f"- {item['freeze_mode']}: {'pass' if item['passed'] else 'fail'}; "
                f"best {item['best_by_schedule']}; worst {item['worst_by_schedule']}; "
                f"gaps {item['robust_rate_gap_by_schedule']}"
            )
            for item in decision["promotion_candidates"]
        ],
        "",
        "## Interpretation boundary",
        "",
        (
            "The graph labels whether some allowed local-action sequence can reach sorted order. "
            "The scheduled runs measure whether the implemented rule realizes that opportunity. "
            "Neither quantity alone establishes agency or an autonomous goal."
        ),
        "",
    ]
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def execute(
    run_id: str = "p2-005-opportunity-adjusted-performance", *, exact: bool = False
) -> Path:
    output = io.run_dir(run_id, exact=exact)
    oracle, runs = generate_discovery()
    summary = summarize(oracle, runs)
    decision = decide(oracle, runs, summary)
    oracle.to_csv(output / "oracle_cases.csv", index=False)
    runs.to_csv(output / "scheduled_runs.csv", index=False)
    summary.to_csv(output / "summary.csv", index=False)
    (output / "decision.json").write_text(
        json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8"
    )
    write_report(output, oracle, runs, summary, decision)
    io.write_metadata(
        output,
        {
            "experiment_id": "p2-005-opportunity-adjusted-performance",
            "protocol": str(PROTOCOL.relative_to(ROOT)),
            "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            "system_size": SYSTEM_SIZE,
            "horizon_ticks": HORIZON_PER_CELL * SYSTEM_SIZE,
            "schedules": list(SCHEDULES),
            "freeze_modes": list(FREEZE_MODES),
            "replicates": list(REPLICATES),
            "oracle_cases": len(oracle),
            "actual_runs": len(runs),
        },
    )
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(
        args.run_id or "p2-005-opportunity-adjusted-performance",
        exact=args.run_id is not None,
    )
    print(output)


if __name__ == "__main__":
    main()
