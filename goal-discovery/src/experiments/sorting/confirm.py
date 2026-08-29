"""Experiment 001, confirmation phase.

Runs the five pre-registered predictions in
docs/hypotheses/001_sorting_confirmation.md on held-out intervention types and
held-out seeds. Thresholds and predictions live in that document and in the
suite config; nothing is decided here.

    uv run python -m src.experiments.sorting.confirm
"""

from __future__ import annotations

import argparse
import statistics
from pathlib import Path

import yaml

from src.common import io
from src.common.seeds import derive
from src.common.seeds import rng as seeded_rng
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import RULE_VERSION, Freeze, SortingWorld
from src.experiments.sorting.observe import observe
from src.experiments.sorting.representations import (
    REPRESENTATION_SET_VERSION,
    boundary_length,
    evaluate,
    sorted_prefix_fraction,
)
from src.experiments.sorting.run import git_commit

SUITE = Path(__file__).resolve().parents[3] / "configs" / "suites" / "confirmation.yaml"


def world_for(n: int, arm: str, seed: int, order: str) -> SortingWorld:
    r = seeded_rng("initial_condition", seed, n)
    values = list(range(n))
    r.shuffle(values)
    return SortingWorld.from_values(values, arm, order=order, seed=seed)


# ---------------------------------------------------------------------------
# C1 -- replicate the paper's moveable/immovable ranking inversion
# ---------------------------------------------------------------------------


def run_c1(cfg: dict, seeds: list[int]) -> list[dict]:
    c = cfg["c1_replication"]
    rows: list[dict] = []
    budgets: dict[int, int] = {}
    for arm in cfg["arms"]:
        for kind in c["freeze_kinds"]:
            for k in c["freeze_counts"]:
                for seed in seeds:
                    w = world_for(c["n"], arm, seed, c["order"])
                    if k:
                        apply(
                            w,
                            Intervention("freeze_cells", {"count": k, "mode": kind}),
                            seed=derive("c1_freeze", seed, k, kind),
                        )
                    cap = c["max_ticks"]
                    if arm in cfg["null_arms"]:
                        cap = budgets.get((seed, kind, k), cap)
                    w.run(cap)
                    if arm == cfg["null_schedule_matched_to"]:
                        budgets[(seed, kind, k)] = max(w.tick, 1)
                    rows.append(
                        {
                            "test": "C1",
                            "arm": arm,
                            "freeze_kind": kind,
                            "freeze_count": k,
                            "seed": seed,
                            "n": c["n"],
                            "ticks": w.tick,
                            "steps": w.steps,
                            "monotonicity_error": boundary_length(observe(w)),
                        }
                    )
    return rows


def judge_c1(cfg: dict, rows: list[dict]) -> list[dict]:
    """C1 passes only if the ranking inverts at every non-zero frozen count."""
    c = cfg["c1_replication"]
    out: list[dict] = []
    for kind in c["freeze_kinds"]:
        for k in c["freeze_counts"]:
            if k == 0:
                continue
            means = {}
            for arm in ("bubble", "selection"):
                vals = [
                    r["monotonicity_error"]
                    for r in rows
                    if r["arm"] == arm and r["freeze_kind"] == kind and r["freeze_count"] == k
                ]
                means[arm] = statistics.fmean(vals) if vals else float("nan")
            expected_bubble_lower = kind == "moveable"
            observed_bubble_lower = means["bubble"] < means["selection"]
            pub = c["published"][kind]
            out.append(
                {
                    "rule": "C1_rank_inversion",
                    "freeze_kind": kind,
                    "freeze_count": k,
                    "mean_bubble": means["bubble"],
                    "mean_selection": means["selection"],
                    "published_bubble": pub["bubble"][k - 1],
                    "published_selection": pub["selection"][k - 1],
                    "expected_bubble_lower": expected_bubble_lower,
                    "passed": observed_bubble_lower == expected_bubble_lower,
                }
            )
    return out


# ---------------------------------------------------------------------------
# C2 -- mechanism damage, invisible to every state measure at the instant it fires
# ---------------------------------------------------------------------------


def run_c2(cfg: dict, seeds: list[int]) -> list[dict]:
    c = cfg["c2_mechanism"]
    conditions: list[tuple[str, Intervention]] = [("none", Intervention("none", {}))]
    for kind in c["freeze_kinds"]:
        for k in c["freeze_counts"]:
            conditions.append(
                (f"freeze_{kind}_{k}", Intervention("freeze_cells", {"count": k, "mode": kind}))
            )
    conditions.append(
        (
            "block_swap",
            Intervention(c["state_damage_control"]["kind"], c["state_damage_control"]["params"]),
        )
    )
    conditions.append(
        ("randomize", Intervention(c["extra_control"]["kind"], c["extra_control"]["params"]))
    )

    rows: list[dict] = []
    for arm in cfg["arms"]:
        for seed in seeds:
            base = world_for(c["n"], arm, seed, c["order"])
            base.run(c["max_ticks"])
            q = max(base.tick, 1)
            branch_tick = max(1, round(c["branch_timing"] * q))
            horizon = max(c["horizon_minimum"], c["horizon_multiplier"] * q)

            for label, iv in conditions:
                w = world_for(c["n"], arm, seed, c["order"])
                for _ in range(branch_tick):
                    w.step_tick()
                pre = evaluate(observe(w))
                snap = w.snapshot()
                w.restore(snap)
                apply(w, iv, seed=derive("c2", seed, label))
                post = evaluate(observe(w))

                reached = boundary_length(observe(w)) == 0
                for _ in range(horizon):
                    if reached or w.quiescent():
                        break
                    w.step_tick()
                    reached = boundary_length(observe(w)) == 0
                rows.append(
                    {
                        "test": "C2",
                        "arm": arm,
                        "condition": label,
                        "seed": seed,
                        "branch_tick": branch_tick,
                        "horizon": horizon,
                        "snapshot_id": snap["snapshot_id"],
                        "state_visible_change": any(post[k] != pre[k] for k in pre),
                        "pre_boundary": pre["boundary_length"],
                        "post_boundary": post["boundary_length"],
                        "reached_goal": reached,
                        "final_boundary": boundary_length(observe(w)),
                    }
                )
    return rows


def judge_c2(cfg: dict, rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for arm in cfg["arms"]:
        sub = [r for r in rows if r["arm"] == arm]
        conds = []
        for r in sub:
            if r["condition"] not in conds:
                conds.append(r["condition"])
        control = [r["reached_goal"] for r in sub if r["condition"] == "none"]
        base_rate = statistics.fmean(control) if control else float("nan")
        for cond in conds:
            vals = [r["reached_goal"] for r in sub if r["condition"] == cond]
            visible = [r["state_visible_change"] for r in sub if r["condition"] == cond]
            out.append(
                {
                    "rule": "C2_goal_rate",
                    "arm": arm,
                    "condition": cond,
                    "goal_rate": statistics.fmean(vals) if vals else float("nan"),
                    "drop_from_control": base_rate
                    - (statistics.fmean(vals) if vals else float("nan")),
                    "changed_any_representation": statistics.fmean(visible)
                    if visible
                    else float("nan"),
                    "n": len(vals),
                    "passed": None,
                }
            )
    return out


# ---------------------------------------------------------------------------
# C5 -- do conclusions survive a changed activation order?
# ---------------------------------------------------------------------------


def run_c5(cfg: dict, seeds: list[int]) -> list[dict]:
    c = cfg["c5_order"]
    rows: list[dict] = []
    for order in c["orders"]:
        for arm in cfg["arms"]:
            for seed in seeds:
                w = world_for(c["n"], arm, seed, order)
                w.run(c["max_ticks"])
                rows.append(
                    {
                        "test": "C5",
                        "arm": arm,
                        "order": order,
                        "seed": seed,
                        "ticks": w.tick,
                        "steps": w.steps,
                        "reached_goal": boundary_length(observe(w)) == 0,
                        "final_prefix": sorted_prefix_fraction(observe(w)),
                    }
                )
    return rows


def judge_c5(cfg: dict, rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for arm in cfg["arms"]:
        rates, ticks = {}, {}
        for order in cfg["c5_order"]["orders"]:
            sub = [r for r in rows if r["arm"] == arm and r["order"] == order]
            rates[order] = statistics.fmean([r["reached_goal"] for r in sub])
            ticks[order] = statistics.median([r["ticks"] for r in sub])
        a, b = cfg["c5_order"]["orders"]
        out.append(
            {
                "rule": "C5_order_robustness",
                "arm": arm,
                f"goal_rate_{a}": rates[a],
                f"goal_rate_{b}": rates[b],
                f"median_ticks_{a}": ticks[a],
                f"median_ticks_{b}": ticks[b],
                "qualitative_match": (rates[a] > 0.5) == (rates[b] > 0.5),
                "passed": (rates[a] > 0.5) == (rates[b] > 0.5),
            }
        )
    return out


# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--suite", type=Path, default=SUITE)
    ap.add_argument("--run-id", default="001-confirmation")
    ap.add_argument("--seeds", type=int, default=None)
    ap.add_argument("--only", default=None, help="C1 | C2 | C5")
    args = ap.parse_args()

    cfg = yaml.safe_load(args.suite.read_text())
    count = args.seeds or cfg["seeds"]["count"]
    seeds = [cfg["seeds"]["start"] + i for i in range(count)]
    d = io.run_dir(args.run_id, exact=False)
    print(f"[{d.name}] confirmation, {len(seeds)} held-out seeds")

    verdicts: list[dict] = []
    if args.only in (None, "C1"):
        c1 = run_c1(cfg, seeds)
        io.write_rows(d, "c1_replication.csv", c1)
        v = judge_c1(cfg, c1)
        verdicts += v
        print("\n  C1 -- paper's ranking inversion (mean final monotonicity error)")
        print("    kind        k   bubble  selection   published b/s      verdict")
        for r in v:
            print(
                f"    {r['freeze_kind']:<10} {r['freeze_count']}  "
                f"{r['mean_bubble']:>7.2f} {r['mean_selection']:>10.2f}   "
                f"{r['published_bubble']:>5.2f}/{r['published_selection']:<6.2f}  "
                f"{'PASS' if r['passed'] else 'FAIL'}"
            )

    if args.only in (None, "C2"):
        c2 = run_c2(cfg, seeds)
        io.write_rows(d, "c2_mechanism.csv", c2)
        v = judge_c2(cfg, c2)
        verdicts += v
        print("\n  C2 -- mechanism damage vs state damage (rate of reaching the goal)")
        print("    arm          condition             rate   drop   changed a representation?")
        for r in v:
            print(
                f"    {r['arm']:<12} {r['condition']:<20} {r['goal_rate']:>6.2f}"
                f" {r['drop_from_control']:>6.2f}   {r['changed_any_representation']:.2f}"
            )

    if args.only in (None, "C5"):
        c5 = run_c5(cfg, seeds)
        io.write_rows(d, "c5_order.csv", c5)
        v = judge_c5(cfg, c5)
        verdicts += v
        print("\n  C5 -- conclusions under a changed activation order")
        for r in v:
            print(
                f"    {r['arm']:<12} goal rate {r['goal_rate_shuffled']:.2f} -> "
                f"{r['goal_rate_index']:.2f}   median ticks "
                f"{r['median_ticks_shuffled']:.0f} -> {r['median_ticks_index']:.0f}   "
                f"{'PASS' if r['passed'] else 'FAIL'}"
            )

    io.write_rows(d, "verdicts.csv", verdicts)
    io.write_metadata(
        d,
        {
            "run_id": d.name,
            "phase": "confirmation",
            "git_commit": git_commit(),
            "rule_version": RULE_VERSION,
            "representation_set_version": REPRESENTATION_SET_VERSION,
            "suite": str(args.suite),
            "seeds": seeds,
            "config": cfg,
            "preregistration": "docs/hypotheses/001_sorting_confirmation.md",
            "freeze_kinds": [f.value for f in Freeze],
        },
    )
    io.point_at_latest(d.name)
    print(f"\n  {d}")


if __name__ == "__main__":
    main()
