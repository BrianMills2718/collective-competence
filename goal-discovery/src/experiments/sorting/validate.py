"""Experiment 001, validation phase.

Runs the pre-registered suite in docs/hypotheses/001_sorting_validation.md
against held-out seeds and reports each decision rule as pass or fail. It does
not choose thresholds, pick representations, or decide what counts as damage --
all of that is fixed in the pre-registration and read from the suite config.

    uv run python -m src.experiments.sorting.validate
"""

from __future__ import annotations

import argparse
import statistics
from pathlib import Path
from typing import Any

import yaml

from src.common import io
from src.common.seeds import derive
from src.common.seeds import rng as seeded_rng
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import RULE_VERSION, SortingWorld
from src.experiments.sorting.observe import observe
from src.experiments.sorting.representations import (
    REPRESENTATION_SET_VERSION,
    REPRESENTATIONS,
    boundary_length,
    evaluate,
    sorted_prefix_fraction,
)
from src.experiments.sorting.run import git_commit

SUITE = Path(__file__).resolve().parents[3] / "configs" / "suites" / "validation.yaml"


def make_world(cfg: dict, arm: str, seed: int) -> SortingWorld:
    n = cfg["system"]["n"]
    r = seeded_rng("initial_condition", seed, n)
    values = list(range(n))
    r.shuffle(values)
    return SortingWorld.from_values(values, arm, order=cfg["system"]["order"], seed=seed)


def run_baseline(cfg: dict, arm: str, seed: int, tick_budget: int | None) -> dict[str, Any]:
    """Unperturbed run. Returns approach, quiescence and maintenance evidence."""
    w = make_world(cfg, arm, seed)
    start = evaluate(observe(w))
    cap = tick_budget if tick_budget is not None else cfg["system"]["max_ticks"]

    first_zero: int | None = None
    quiesce_tick: int | None = None
    trace: list[float] = [boundary_length(observe(w))]
    prefix_trace: list[float] = [sorted_prefix_fraction(observe(w))]
    for _ in range(cap):
        if w.quiescent():
            quiesce_tick = w.tick
            break
        w.step_tick()
        bl = boundary_length(observe(w))
        trace.append(bl)
        prefix_trace.append(sorted_prefix_fraction(observe(w)))
        if first_zero is None and bl == 0:
            first_zero = w.tick
    if quiesce_tick is None:
        quiesce_tick = w.tick

    end = evaluate(observe(w))

    # Maintenance: once at zero, does it stay there?
    escaped = None
    if first_zero is not None:
        probe = make_world(cfg, arm, seed)
        for _ in range(first_zero):
            probe.step_tick()
        escaped = False
        for _ in range(cfg["maintenance_probe_ticks"]):
            probe.step_tick()
            if boundary_length(observe(probe)) != 0:
                escaped = True
                break

    return {
        "arm": arm,
        "seed": seed,
        "quiesce_tick": quiesce_tick,
        "first_zero_tick": first_zero,
        "reached_zero": first_zero is not None,
        "escaped_zero": escaped,
        "steps": w.steps,
        "swaps": w.swaps,
        "boundary_min": min(trace),
        "boundary_max": max(trace),
        "boundary_trace": trace,
        "prefix_trace": prefix_trace,
        **{f"start_{k}": v for k, v in start.items()},
        **{f"end_{k}": v for k, v in end.items()},
    }


def matched_last_crossing(trace: list[float], b: float, higher_is_better: bool) -> int | None:
    """C4's tighter comparator, declared in 001_sorting_confirmation.md.

    The *last* tick before the baseline first reached the goal at which it was
    still scoring at least as badly as b. `matched_baseline_cost` takes the
    first such tick instead, and because these measures oscillate that tick can
    be one scoring far better than b, understating the matched cost and
    inflating the ratio. Both are computed so the size of that bias is visible
    rather than asserted.
    """
    try:
        goal_tick = next(i for i, v in enumerate(trace) if v == 0)
    except StopIteration:
        return None
    worse_or_equal = [
        i for i, v in enumerate(trace[:goal_tick]) if (v <= b if higher_is_better else v >= b)
    ]
    if not worse_or_equal:
        return None
    return goal_tick - worse_or_equal[-1]


def matched_prefix_crossing(
    prefix_trace: list[float], boundary_trace: list[float], p: float
) -> int | None:
    """C3: match on sorted-prefix length instead of boundary length.

    Validation found boundary_length blind to the quantity that governs the
    insertion algotype's rate. If the prefix is what matters, matching on it
    should bring insertion's ratio toward 1.
    """
    try:
        goal_tick = next(i for i, v in enumerate(boundary_trace) if v == 0)
    except StopIteration:
        return None
    worse = [i for i, v in enumerate(prefix_trace[:goal_tick]) if v <= p]
    if not worse:
        return None
    return goal_tick - worse[-1]


def matched_baseline_cost(trace: list[float], b: float) -> int | None:
    """R7's comparator: how many further ticks the *unperturbed* run needed to
    reach the goal, counted from the first tick at which it scored b or better.

    None when the baseline never reached the goal, or never scored as poorly as
    b after the start -- in either case there is nothing to match against and
    the branch is excluded from R7 rather than given a fabricated denominator.
    """
    try:
        goal_tick = next(i for i, v in enumerate(trace) if v == 0)
    except StopIteration:
        return None
    match = next((i for i, v in enumerate(trace) if v <= b), None)
    if match is None or match > goal_tick:
        return None
    return goal_tick - match


def run_branch(
    cfg: dict,
    arm: str,
    seed: int,
    branch_tick: int,
    magnitude: float,
    horizon: int,
    goal_at_most: float,
    baseline_trace: list[float],
    baseline_prefix: list[float],
) -> dict[str, Any]:
    w = make_world(cfg, arm, seed)
    for _ in range(branch_tick):
        w.step_tick()
    pre = evaluate(observe(w))
    snap = w.snapshot()

    w.restore(snap)
    iv = Intervention(cfg["branch"]["intervention_kind"], {"fraction": magnitude})
    apply(w, iv, seed=derive("intervention", seed, magnitude, branch_tick))
    post = evaluate(observe(w))

    damaged = post["boundary_length"] > pre["boundary_length"]
    recovered_at: int | None = None
    if boundary_length(observe(w)) <= goal_at_most:
        recovered_at = w.tick
    else:
        for _ in range(horizon):
            if w.quiescent():
                break
            w.step_tick()
            if boundary_length(observe(w)) <= goal_at_most:
                recovered_at = w.tick
                break

    final = evaluate(observe(w))
    return {
        "arm": arm,
        "seed": seed,
        "branch_tick": branch_tick,
        "magnitude": magnitude,
        "horizon": horizon,
        "snapshot_id": snap["snapshot_id"],
        "damaged": damaged,
        "pre_boundary": pre["boundary_length"],
        "post_boundary": post["boundary_length"],
        "final_boundary": final["boundary_length"],
        "recovered": recovered_at is not None,
        "ticks_to_recover": (recovered_at - branch_tick) if recovered_at is not None else None,
        "matched_baseline_ticks": matched_baseline_cost(baseline_trace, post["boundary_length"]),
        "matched_last_crossing_ticks": matched_last_crossing(
            baseline_trace, post["boundary_length"], higher_is_better=False
        ),
        "matched_prefix_ticks": matched_prefix_crossing(
            baseline_prefix, baseline_trace, post["sorted_prefix_fraction"]
        ),
        **{f"pre_{k}": v for k, v in pre.items()},
        **{f"post_{k}": v for k, v in post.items()},
        **{f"final_{k}": v for k, v in final.items()},
    }


def _rate(xs: list[bool]) -> float:
    return (sum(xs) / len(xs)) if xs else float("nan")


def judge(cfg: dict, base: list[dict], branches: list[dict]) -> list[dict]:
    """Apply the pre-registered decision rules. No thresholds live here."""
    t = cfg["thresholds"]
    nulls = set(cfg["null_arms"])
    out: list[dict] = []

    for arm in cfg["arms"]:
        b = [r for r in base if r["arm"] == arm]
        br = [r for r in branches if r["arm"] == arm]
        damaged = [r for r in br if r["damaged"]]

        approach = _rate([r["end_boundary_length"] < r["start_boundary_length"] for r in b])
        out.append(
            {
                "rule": "R1_approach",
                "arm": arm,
                "value": approach,
                "threshold": t["R1_approach_rate"],
                "n": len(b),
                "passed": approach >= t["R1_approach_rate"],
            }
        )

        reached = [r for r in b if r["reached_zero"]]
        if arm in nulls:
            out.append(
                {
                    "rule": "R2_maintenance",
                    "arm": arm,
                    "value": float("nan"),
                    "threshold": 1.0,
                    "n": len(reached),
                    "passed": None,
                    "note": "not applicable: the null has no absorbing state",
                }
            )
        else:
            held = _rate([not r["escaped_zero"] for r in reached])
            out.append(
                {
                    "rule": "R2_maintenance",
                    "arm": arm,
                    "value": held,
                    "threshold": 1.0,
                    "n": len(reached),
                    "passed": (len(reached) > 0 and held == 1.0),
                }
            )

        rec = _rate([r["recovered"] for r in damaged])
        out.append(
            {
                "rule": "R3_recovery",
                "arm": arm,
                "value": rec,
                "threshold": t["R3_recovery_rate"],
                "n": len(damaged),
                "passed": rec >= t["R3_recovery_rate"],
            }
        )

        out.append(
            {
                "rule": "R4_damage_rate",
                "arm": arm,
                "value": _rate([r["damaged"] for r in br]),
                "threshold": None,
                "n": len(br),
                "passed": None,
                "note": "reported, not a pass/fail rule",
            }
        )

    null_arm = cfg["null_arms"][0]
    null_rec = next(r["value"] for r in out if r["rule"] == "R3_recovery" and r["arm"] == null_arm)
    out.append(
        {
            "rule": "R5_null_ceiling",
            "arm": null_arm,
            "value": null_rec,
            "threshold": t["R5_null_recovery_ceiling"],
            "n": len([r for r in branches if r["arm"] == null_arm and r["damaged"]]),
            "passed": null_rec < t["R5_null_recovery_ceiling"],
        }
    )
    for arm in cfg["arms"]:
        if arm in nulls:
            continue
        arm_rec = next(r["value"] for r in out if r["rule"] == "R3_recovery" and r["arm"] == arm)
        margin = arm_rec - null_rec
        out.append(
            {
                "rule": "R5_margin_over_null",
                "arm": arm,
                "value": margin,
                "threshold": t["R5_margin_over_null"],
                "n": None,
                "passed": margin >= t["R5_margin_over_null"],
            }
        )

    comparators = {
        "boundary_first_crossing": "matched_baseline_ticks",  # v2, biased upward
        "boundary_last_crossing": "matched_last_crossing_ticks",  # C4, tighter
        "prefix_last_crossing": "matched_prefix_ticks",  # C3
    }
    for arm in cfg["arms"]:
        for label, field in comparators.items():
            ratios = [
                r["ticks_to_recover"] / r[field]
                for r in branches
                if r["arm"] == arm and r["damaged"] and r["recovered"] and r[field] not in (None, 0)
            ]
            out.append(
                {
                    "rule": "R7_sufficiency",
                    "arm": arm,
                    "comparator": label,
                    "value": statistics.median(ratios) if ratios else float("nan"),
                    "threshold": None,
                    "n": len(ratios),
                    "passed": None,
                    "faster_than_matched": (
                        sum(1 for x in ratios if x < 1) / len(ratios) if ratios else float("nan")
                    ),
                    "note": "measured, not judged",
                }
            )

    for arm in cfg["arms"]:
        b = [r for r in base if r["arm"] == arm]
        damaged = [r for r in branches if r["arm"] == arm and r["damaged"]]
        for rep in REPRESENTATIONS:
            signs = [_sign(r[f"end_{rep}"] - r[f"start_{rep}"]) for r in b]
            cons_b = _dominant(signs)
            signs_d = [_sign(r[f"final_{rep}"] - r[f"post_{rep}"]) for r in damaged]
            cons_d = _dominant(signs_d)
            out.append(
                {
                    "rule": "R6_consistency",
                    "arm": arm,
                    "representation": rep,
                    "value": min(cons_b, cons_d),
                    "threshold": t["R6_sign_consistency_damaged"],
                    "baseline_consistency": cons_b,
                    "damaged_consistency": cons_d,
                    "n": len(b),
                    "passed": (
                        cons_b >= t["R6_sign_consistency_baseline"]
                        and cons_d >= t["R6_sign_consistency_damaged"]
                    ),
                }
            )
    return out


def _sign(x: float) -> int:
    return (x > 0) - (x < 0)


def _dominant(signs: list[int]) -> float:
    if not signs:
        return float("nan")
    return max(signs.count(s) for s in (-1, 0, 1)) / len(signs)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--suite", type=Path, default=SUITE)
    ap.add_argument("--run-id", default="001-validation")
    ap.add_argument("--seeds", type=int, default=None, help="override seed count (pilot only)")
    args = ap.parse_args()

    cfg = yaml.safe_load(args.suite.read_text())
    count = args.seeds or cfg["seeds"]["count"]
    seeds = [cfg["seeds"]["start"] + i for i in range(count)]
    d = io.run_dir(args.run_id, exact=False)

    print(
        f"[{d.name}] {len(seeds)} held-out seeds x {len(cfg['arms'])} arms "
        f"x {len(cfg['branch']['timings'])} timings x {len(cfg['branch']['magnitudes'])} "
        "magnitudes"
    )

    goal_at_most = cfg["goal_region"]["boundary_length_at_most"]
    base: list[dict] = []
    matched = cfg["null_schedule_matched_to"]
    budgets: dict[int, int] = {}
    for arm in [matched] + [a for a in cfg["arms"] if a != matched]:
        for seed in seeds:
            budget = budgets.get(seed) if arm in cfg["null_arms"] else None
            r = run_baseline(cfg, arm, seed, budget)
            if arm == matched:
                budgets[seed] = r["quiesce_tick"]
            base.append(r)
        done = [r for r in base if r["arm"] == arm]
        # Liveness. A null that fails to recover because it is inert would be a
        # broken probe, not a result, so its movement is reported beside its
        # outcome rather than assumed.
        print(
            f"  baseline {arm:<12} median quiesce tick "
            f"{statistics.median([r['quiesce_tick'] for r in done]):.0f}, "
            f"reached zero {_rate([r['reached_zero'] for r in done]):.2f}, "
            f"median swaps {statistics.median([r['swaps'] for r in done]):.0f}, "
            f"boundary range {statistics.median([r['boundary_min'] for r in done]):.0f}"
            f"-{statistics.median([r['boundary_max'] for r in done]):.0f}"
        )

    branches: list[dict] = []
    for arm in cfg["arms"]:
        for seed in seeds:
            brow = next(r for r in base if r["arm"] == arm and r["seed"] == seed)
            q, trace = brow["quiesce_tick"], brow["boundary_trace"]
            ptrace = brow["prefix_trace"]
            horizon = max(cfg["branch"]["horizon_minimum"], cfg["branch"]["horizon_multiplier"] * q)
            for label, frac in cfg["branch"]["timings"].items():
                tick = max(1, round(frac * q))
                for mag in cfg["branch"]["magnitudes"]:
                    row = run_branch(
                        cfg, arm, seed, tick, mag, horizon, goal_at_most, trace, ptrace
                    )
                    row["timing"] = label
                    branches.append(row)
        sub = [r for r in branches if r["arm"] == arm]
        dmg = [r for r in sub if r["damaged"]]
        print(
            f"  branches {arm:<12} {len(sub)} runs, damaged {_rate([r['damaged'] for r in sub]):.2f}"
            f", recovery among damaged {_rate([r['recovered'] for r in dmg]):.2f}"
        )

    verdicts = judge(cfg, base, branches)
    io.write_rows(
        d,
        "baselines.csv",
        [{k: v for k, v in r.items() if k not in ("boundary_trace", "prefix_trace")} for r in base],
    )
    io.write_rows(d, "branches.csv", branches)
    io.write_rows(d, "verdicts.csv", verdicts)
    io.write_metadata(
        d,
        {
            "run_id": d.name,
            "phase": "validation",
            "git_commit": git_commit(),
            "rule_version": RULE_VERSION,
            "representation_set_version": REPRESENTATION_SET_VERSION,
            "suite": str(args.suite),
            "seeds": seeds,
            "config": cfg,
            "preregistration": "docs/hypotheses/001_sorting_validation.md",
        },
    )
    io.point_at_latest(d.name)

    print("\n  RULE                  ARM            VALUE   THRESHOLD  VERDICT")
    for v in verdicts:
        if v["rule"] == "R6_consistency":
            continue
        val = "n/a" if v["value"] != v["value"] else f"{v['value']:.3f}"
        thr = "-" if v.get("threshold") is None else f"{v['threshold']:.2f}"
        mark = {True: "PASS", False: "FAIL", None: "----"}[v["passed"]]
        print(f"  {v['rule']:<21} {v['arm']:<14} {val:>6}  {thr:>9}  {mark}")
    print("\n  R7 sufficiency (median recovery ticks / matched baseline ticks):")
    print(f"    {'arm':<12} {'comparator':<24} {'ratio':>6} {'faster':>7}    n")
    for v in verdicts:
        if v["rule"] != "R7_sufficiency":
            continue
        val = "n/a" if v["value"] != v["value"] else f"{v['value']:.2f}"
        faster = (
            "n/a"
            if v["faster_than_matched"] != v["faster_than_matched"]
            else f"{v['faster_than_matched']:.2f}"
        )
        print(f"    {v['arm']:<12} {v['comparator']:<24} {val:>6} {faster:>7}  {v['n']:>4}")
    print("\n  R6 consistency, passing representations per arm:")
    for arm in cfg["arms"]:
        ok = [
            v["representation"]
            for v in verdicts
            if v["rule"] == "R6_consistency" and v["arm"] == arm and v["passed"]
        ]
        print(f"    {arm:<14} {', '.join(ok) if ok else '(none)'}")
    print(f"\n  {d}")


if __name__ == "__main__":
    main()
