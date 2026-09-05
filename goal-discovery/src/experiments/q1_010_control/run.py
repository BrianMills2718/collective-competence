"""Execute the frozen Q1-010 protocol. Reads its thresholds from the protocol only.

G-A = 0.1217 bits is two standard deviations of `private_period`'s own shuffle
null, measured in `results/q1-010-determinism-control/null_calibration.json` and
committed in 4f09f00 before the protocol named it. G-B = 0.80 is the frozen
relative performance ceiling. Neither is recomputed here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.experiments.contended_channel.run import load_config
from src.experiments.q1_010_control.traces import (
    ARMS,
    action_trace,
    admissible_seeds,
)
from src.experiments.q1_information.calibrate import OBSERVED, ei_pair
from src.experiments.q1_information.traces import shuffle_null

SEED_POOL = 1600
NULL_REPLICATES = 8

# Frozen in docs/hypotheses/q1_010_determinism_control.md. Do not recompute.
G_A_MIN_ABOVE_NULL = 0.1217      # two sd of private_period's measured null
G_B_MAX_RELATIVE = 0.80          # private_period satisfaction / derived_phase


def ei_block(traces: list[np.ndarray], rng: np.random.Generator) -> dict:
    obs = ei_pair(traces, OBSERVED)
    nulls = [ei_pair([shuffle_null(t, rng) for t in traces], OBSERVED)
             for _ in range(NULL_REPLICATES)]
    micro = [n["ei_micro"] for n in nulls]
    return {
        "ei_micro": obs["ei_micro"],
        "transitions": obs["transitions"],
        "micro_rows_seen": obs["micro_rows_seen"],
        "transitions_per_seen_row": obs["transitions_per_seen_row"],
        "null_ei_micro_mean": float(np.mean(micro)),
        "null_ei_micro_sd": float(np.std(micro, ddof=1)),
        "ei_micro_above_null": obs["ei_micro"] - float(np.mean(micro)),
        "above_null_in_null_sd": (obs["ei_micro"] - float(np.mean(micro)))
        / float(np.std(micro, ddof=1)),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    cfg = load_config()
    seeds = admissible_seeds(cfg, SEED_POOL)
    rng = np.random.default_rng(10102260905)
    report: dict = {
        "seed_pool": SEED_POOL, "admissible_seeds": len(seeds),
        "excluded_seeds": [s for s in range(SEED_POOL) if s not in set(seeds)],
        "null_replicates": NULL_REPLICATES, "observed_units": OBSERVED,
        "frozen_gates": {"G_A_min_above_null": G_A_MIN_ABOVE_NULL,
                         "G_B_max_relative_satisfaction": G_B_MAX_RELATIVE},
        "arms": {},
    }

    for arm in ARMS:
        traces, sats = [], []
        for s in seeds:
            actions, _, sat = action_trace(cfg, s, arm)
            traces.append(actions)
            sats.append(sat)
        report["arms"][arm] = {
            **ei_block(traces, rng),
            "mean_satisfaction": float(np.mean(sats)),
            "sd_satisfaction": float(np.std(sats, ddof=1)),
            "mean_duty_cycle": float(np.mean([t.mean() for t in traces])),
        }

    pp = report["arms"]["private_period"]
    dp = report["arms"]["derived_phase"]
    relative = pp["mean_satisfaction"] / dp["mean_satisfaction"]
    g_a = pp["ei_micro_above_null"] >= G_A_MIN_ABOVE_NULL
    g_b = relative <= G_B_MAX_RELATIVE
    report["gates"] = {
        "G_A_statistic_reports_structure": {
            "pass": bool(g_a), "value": pp["ei_micro_above_null"],
            "required": G_A_MIN_ABOVE_NULL},
        "G_B_coordination_performance_absent": {
            "pass": bool(g_b), "value": relative, "required_at_most": G_B_MAX_RELATIVE},
    }
    report["disposition"] = {
        (True, True): "statistic is not a coordination detector on this family",
        (False, True): "statistic separates shared-period coordination here; critique narrows to the commons",
        (True, False): "INVALID: private_period is not an uncoordinated control",
        (False, False): "INVALID: private_period is not an uncoordinated control",
    }[(g_a, g_b)]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    print(f"{'arm':<24}{'EI':>9}{'null':>9}{'above':>9}{'in sd':>8}"
          f"{'satisf':>9}{'duty':>8}")
    for arm, r in report["arms"].items():
        print(f"{arm:<24}{r['ei_micro']:>9.4f}{r['null_ei_micro_mean']:>9.4f}"
              f"{r['ei_micro_above_null']:>+9.4f}{r['above_null_in_null_sd']:>+8.1f}"
              f"{r['mean_satisfaction']:>9.4f}{r['mean_duty_cycle']:>8.4f}")
    print(f"\nG-A  private_period above its null >= {G_A_MIN_ABOVE_NULL}: "
          f"{pp['ei_micro_above_null']:+.4f}  -> {'PASS' if g_a else 'FAIL'}")
    print(f"G-B  satisfaction relative to derived_phase <= {G_B_MAX_RELATIVE}: "
          f"{relative:.4f}  -> {'PASS' if g_b else 'FAIL'}")
    print(f"\nDisposition: {report['disposition']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
