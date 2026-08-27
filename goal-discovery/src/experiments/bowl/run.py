"""Experiment 002 — the passive control, D1 through D5.

Predictions and thresholds live in docs/hypotheses/002_bowl.md and in the suite
config. Nothing is decided here.

    uv run python -m src.experiments.bowl.run
"""

from __future__ import annotations

import argparse
import statistics
from pathlib import Path
from typing import Any

import yaml

from src.common import io
from src.common.seeds import derive
from src.experiments.bowl.interventions import BowlIntervention, apply
from src.experiments.bowl.model import RULE_VERSION, BowlWorld
from src.experiments.bowl.observe import observe
from src.experiments.bowl.representations import (
    REPRESENTATION_SET_VERSION,
    evaluate,
    max_abs_position,
)
from src.experiments.sorting.run import git_commit

SUITE = Path(__file__).resolve().parents[3] / "configs" / "suites" / "bowl.yaml"


def make(cfg: dict, seed: int) -> BowlWorld:
    s = cfg["system"]
    return BowlWorld.from_seed(
        s["n"], seed, spread=s["spread"],
        stiffness=s["stiffness"], damping=s["damping"], eps=s["eps"],
    )


def first_crossing(trace: list[float], b: float, goal_tick: int) -> int | None:
    i = next((i for i, v in enumerate(trace[:goal_tick]) if v <= b), None)
    return None if i is None else goal_tick - i


def last_crossing(trace: list[float], b: float, goal_tick: int) -> int | None:
    idx = [i for i, v in enumerate(trace[:goal_tick]) if v >= b]
    return None if not idx else goal_tick - idx[-1]


def run_baseline(cfg: dict, seed: int) -> dict[str, Any]:
    w = make(cfg, seed)
    start = evaluate(observe(w))
    trace = [max_abs_position(observe(w))]
    goal_tick = None
    for _ in range(cfg["system"]["max_ticks"]):
        if w.at_goal():
            goal_tick = w.tick
            break
        w.step_tick()
        trace.append(max_abs_position(observe(w)))
    if goal_tick is None and w.at_goal():
        goal_tick = w.tick

    escaped = None
    if goal_tick is not None:
        probe = make(cfg, seed)
        probe.run(goal_tick, stop_at_goal=False)
        escaped = False
        for _ in range(500):
            probe.step_tick()
            if not probe.at_goal():
                escaped = True
                break

    return {
        "seed": seed, "goal_tick": goal_tick, "reached": goal_tick is not None,
        "escaped_goal": escaped, "ticks": w.tick, "trace": trace,
        **{f"start_{k}": v for k, v in start.items()},
        **{f"end_{k}": v for k, v in evaluate(observe(w)).items()},
    }


def run_branch(cfg: dict, seed: int, cond: dict, branch_tick: int, horizon: int,
               trace: list[float], goal_tick: int | None) -> dict[str, Any]:
    w = make(cfg, seed)
    w.run(branch_tick, stop_at_goal=False)
    pre = evaluate(observe(w))
    snap = w.snapshot()
    w.restore(snap)
    iv = BowlIntervention(cond["kind"], cond["params"])
    apply(w, iv, seed=derive("bowl", seed, cond["label"]))
    post = evaluate(observe(w))

    reached_at = None
    for _ in range(horizon):
        if w.at_goal():
            reached_at = w.tick
            break
        if w.quiescent():
            break
        w.step_tick()
    if reached_at is None and w.at_goal():
        reached_at = w.tick

    b = post["max_abs_position"]
    return {
        "seed": seed, "condition": cond["label"], "branch_tick": branch_tick,
        "snapshot_id": snap["snapshot_id"],
        "changed_any_representation": any(post[k] != pre[k] for k in pre),
        "pre_max_abs_position": pre["max_abs_position"],
        "post_max_abs_position": b,
        "reached_goal": reached_at is not None,
        "ticks_to_reach": (reached_at - branch_tick) if reached_at is not None else None,
        "matched_first": first_crossing(trace, b, goal_tick) if goal_tick else None,
        "matched_last": last_crossing(trace, b, goal_tick) if goal_tick else None,
    }


def run_adaptation(cfg: dict, seed: int) -> list[dict]:
    """D3: repeat the same episode and check nothing improves."""
    a = cfg["adaptation"]
    rows = []
    for ep in range(a["episodes"]):
        w = make(cfg, seed)
        apply(w, BowlIntervention(a["disturbance"]["kind"], a["disturbance"]["params"]),
              seed=derive("bowl_adapt", seed))
        t = None
        for _ in range(cfg["system"]["max_ticks"]):
            if w.at_goal():
                t = w.tick
                break
            w.step_tick()
        rows.append({"seed": seed, "episode": ep, "ticks_to_goal": t})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--suite", type=Path, default=SUITE)
    ap.add_argument("--run-id", default="002-bowl")
    ap.add_argument("--seeds", type=int, default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load(args.suite.read_text())
    count = args.seeds or cfg["seeds"]["count"]
    seeds = [cfg["seeds"]["start"] + i for i in range(count)]
    d = io.run_dir(args.run_id, exact=False)
    t = cfg["thresholds"]
    print(f"[{d.name}] passive control, {len(seeds)} seeds, n={cfg['system']['n']} coordinates")

    base = [run_baseline(cfg, s) for s in seeds]
    approach = statistics.fmean([r["reached"] for r in base])
    held = [r for r in base if r["reached"]]
    maintenance = statistics.fmean([not r["escaped_goal"] for r in held]) if held else float("nan")
    print(f"\n  D1  approach {approach:.3f} (>= {t['D1_approach_rate']}), "
          f"maintenance {maintenance:.3f}, median ticks "
          f"{statistics.median([r['goal_tick'] for r in held]):.0f}")

    branches: list[dict] = []
    for r in base:
        if not r["reached"]:
            continue
        bt = max(1, round(cfg["branch"]["timing"] * r["goal_tick"]))
        hz = max(cfg["branch"]["horizon_minimum"],
                 cfg["branch"]["horizon_multiplier"] * r["goal_tick"])
        for cond in cfg["branch"]["conditions"]:
            branches.append(run_branch(cfg, r["seed"], cond, bt, hz, r["trace"], r["goal_tick"]))

    print("\n  D2/D4  condition        goal rate   changed a representation?")
    summary = []
    for cond in cfg["branch"]["conditions"]:
        sub = [b for b in branches if b["condition"] == cond["label"]]
        rate = statistics.fmean([b["reached_goal"] for b in sub])
        vis = statistics.fmean([b["changed_any_representation"] for b in sub])
        summary.append({"condition": cond["label"], "goal_rate": rate, "visible": vis,
                        "n": len(sub)})
        print(f"         {cond['label']:<16} {rate:>8.3f}   {vis:>10.2f}")

    frozen = [s for s in summary if s["condition"].startswith("freeze")]
    d2_pass = all(s["goal_rate"] <= t["D2_frozen_goal_ceiling"] for s in frozen)
    state = [s for s in summary if s["condition"].startswith(("displace", "kick"))]
    d4a_pass = all(s["goal_rate"] >= 0.95 for s in state)
    print(f"\n  D2  frozen coordinates strand the system: "
          f"{'PASS' if d2_pass else 'FAIL'}")
    print(f"  D4a state damage is visible and costs nothing: "
          f"{'PASS' if d4a_pass else 'FAIL'}")
    print(f"  D4b mechanism damage is invisible and costs everything: "
          f"{'PASS' if d2_pass and all(s['visible'] == 0.0 for s in frozen) else 'FAIL'}")

    adapt = [row for s in seeds for row in run_adaptation(cfg, s)]
    per_ep = {}
    for row in adapt:
        per_ep.setdefault(row["episode"], []).append(row["ticks_to_goal"])
    means = {e: statistics.fmean(v) for e, v in sorted(per_ep.items())}
    d3_pass = len({round(m, 6) for m in means.values()}) == 1
    print(f"\n  D3  ticks to goal by episode: "
          f"{', '.join(f'{m:.0f}' for m in means.values())}  "
          f"{'PASS (no improvement)' if d3_pass else 'FAIL'}")

    ratios = {}
    for field in ("matched_first", "matched_last"):
        vals = [b["ticks_to_reach"] / b[field] for b in branches
                if b["reached_goal"] and b[field] not in (None, 0)
                and b["condition"].startswith(("displace", "kick"))]
        ratios[field] = statistics.median(vals) if vals else float("nan")
    spread = abs(ratios["matched_first"] - ratios["matched_last"])
    d5_pass = all(abs(v - 1.0) <= t["D5_ratio_tolerance"] for v in ratios.values())
    print(f"\n  D5  recovery / fresh convergence: first-crossing "
          f"{ratios['matched_first']:.2f}, last-crossing {ratios['matched_last']:.2f}, "
          f"spread {spread:.2f}  {'PASS' if d5_pass else 'FAIL'}")

    verdicts = [
        {"rule": "D1_approach", "value": approach, "threshold": t["D1_approach_rate"],
         "passed": approach >= t["D1_approach_rate"]},
        {"rule": "D1_maintenance", "value": maintenance, "threshold": 1.0,
         "passed": maintenance == 1.0},
        {"rule": "D2_no_compensation", "value": max(s["goal_rate"] for s in frozen),
         "threshold": t["D2_frozen_goal_ceiling"], "passed": d2_pass},
        {"rule": "D3_no_adaptation", "value": len({round(m, 6) for m in means.values()}),
         "threshold": 1, "passed": d3_pass},
        {"rule": "D4a_state_damage_free", "value": min(s["goal_rate"] for s in state),
         "threshold": 0.95, "passed": d4a_pass},
        {"rule": "D4b_mechanism_damage_invisible",
         "value": max(s["visible"] for s in frozen), "threshold": 0.0,
         "passed": all(s["visible"] == 0.0 for s in frozen)},
        {"rule": "D5_ratio_first", "value": ratios["matched_first"], "threshold": 1.0,
         "passed": abs(ratios["matched_first"] - 1.0) <= t["D5_ratio_tolerance"]},
        {"rule": "D5_ratio_last", "value": ratios["matched_last"], "threshold": 1.0,
         "passed": abs(ratios["matched_last"] - 1.0) <= t["D5_ratio_tolerance"]},
        {"rule": "D5_comparator_spread", "value": spread,
         "threshold": t["D5_ratio_tolerance"], "passed": spread <= t["D5_ratio_tolerance"]},
    ]
    io.write_rows(d, "baselines.csv", [{k: v for k, v in r.items() if k != "trace"} for r in base])
    io.write_rows(d, "branches.csv", branches)
    io.write_rows(d, "adaptation.csv", adapt)
    io.write_rows(d, "verdicts.csv", verdicts)
    io.write_metadata(d, {
        "run_id": d.name, "phase": "control", "git_commit": git_commit(),
        "rule_version": RULE_VERSION,
        "representation_set_version": REPRESENTATION_SET_VERSION,
        "suite": str(args.suite), "seeds": seeds, "config": cfg,
        "preregistration": "docs/hypotheses/002_bowl.md",
    })
    io.point_at_latest(d.name)
    print(f"\n  {d}")


if __name__ == "__main__":
    main()
