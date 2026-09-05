"""Measure Q1-010's nulls before any Q1-010 threshold is chosen.

This is the stricter form of the freeze discipline Q1-009 adopted. Q1-009's own
`calibrate.py` printed the observed statistic alongside the null, so the number
the gate would be compared against was on screen while the gate was being
written. This script **does not compute the observed effective information for
any arm.** It computes only:

  * the shuffle null's mean and standard deviation, at the exact seed count,
    horizon, unit count and micro-state dimension the run will use; and
  * per-arm duty cycle and schedule structure, which are properties of the
    trace rather than of the statistic and cannot reveal the outcome.

`assert_no_observed_ei` documents that refusal in code so a later reader can see
it was structural rather than promised.
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
    schedule_for,
    shared_cycle_length,
)
from src.experiments.q1_information.calibrate import OBSERVED, ei_pair
from src.experiments.q1_information.traces import needs_for, shuffle_null

SEEDS = 1600
NULL_REPLICATES = 8


def null_block(traces: list[np.ndarray], rng: np.random.Generator) -> dict:
    """Shuffle null only. The observed statistic is deliberately not computed."""
    nulls = [ei_pair([shuffle_null(t, rng) for t in traces], OBSERVED)
             for _ in range(NULL_REPLICATES)]
    micro = [n["ei_micro"] for n in nulls]
    return {
        "null_ei_micro_mean": float(np.mean(micro)),
        "null_ei_micro_sd": float(np.std(micro, ddof=1)),
        "null_ei_micro_replicates": [float(x) for x in micro],
        "replicates": NULL_REPLICATES,
    }


def structure_block(cfg, arm: str, traces: list[np.ndarray]) -> dict:
    """Trace-level structure. Says nothing about the statistic's value."""
    needs = needs_for(cfg, 0)
    periods, offsets = schedule_for(arm, needs, cfg.n_subunits)
    duty = float(np.mean([t.mean() for t in traces]))
    return {
        "mean_duty_cycle": duty,
        "distinct_periods_seed0": len(set(periods.tolist())),
        "periods_seed0": periods.tolist(),
        "offsets_seed0": offsets.tolist(),
        "shared_cycle_length_seed0": shared_cycle_length(periods),
        "horizon": cfg.horizon,
        "shared_cycle_exceeds_horizon": bool(
            shared_cycle_length(periods) > cfg.horizon),
    }


# Keys that can only exist if the observed (unshuffled) statistic was computed.
# Exact key names, not substrings: the first version of this guard matched the
# substring "observed" and fired on its own `observed_units` dimension field,
# which is a configuration constant. A guard that cries wolf gets deleted, and a
# deleted guard is how Q1-006's gate was frozen below its own null.
BANNED_KEYS = frozenset({
    "ei_micro", "ei_macro", "emergence",
    "ei_micro_above_null", "emergence_above_null",
})


def assert_no_observed_ei(report: object, path: str = "") -> None:
    """Fail loudly if a future edit lets an observed value into the freeze.

    `tests/test_q1_010_control.py::test_freeze_guard_fires_on_observed_value`
    feeds it a report carrying one, and asserts it raises -- the guard is checked
    against a negative control rather than assumed to work.
    """
    if isinstance(report, dict):
        for key, value in report.items():
            if key in BANNED_KEYS:
                raise AssertionError(
                    f"calibration report carries observed statistic {path}{key!r}; "
                    "the freeze must hold the null only, or the threshold is chosen "
                    "while looking at the answer"
                )
            assert_no_observed_ei(value, f"{path}{key}.")
    elif isinstance(report, list):
        for item in report:
            assert_no_observed_ei(item, path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    cfg = load_config()
    rng = np.random.default_rng(10100260905)
    report: dict = {
        "purpose": "null and trace structure only; no observed statistic is computed here",
        "seeds": SEEDS, "observed_units": OBSERVED, "micro_states": 1 << OBSERVED,
        "horizon": cfg.horizon, "n_subunits": cfg.n_subunits, "arms": {},
    }

    seeds = admissible_seeds(cfg, SEEDS)
    report["seed_pool"] = SEEDS
    report["admissible_seeds"] = len(seeds)
    report["excluded_seeds"] = [s for s in range(SEEDS) if s not in set(seeds)]

    for arm in ARMS:
        traces = [action_trace(cfg, s, arm)[0] for s in seeds]
        report["arms"][arm] = {
            "shuffle_null": null_block(traces, rng),
            "trace_structure": structure_block(cfg, arm, traces),
        }

    assert_no_observed_ei(report)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    print(f"{'arm':<22}{'null_EI':>10}{'null_sd':>10}{'2sd gate':>10}"
          f"{'duty':>8}{'periods':>9}{'cycle':>8}")
    for arm, row in report["arms"].items():
        n, s = row["shuffle_null"], row["trace_structure"]
        print(f"{arm:<22}{n['null_ei_micro_mean']:>10.4f}{n['null_ei_micro_sd']:>10.4f}"
              f"{2 * n['null_ei_micro_sd']:>10.4f}{s['mean_duty_cycle']:>8.4f}"
              f"{s['distinct_periods_seed0']:>9d}{s['shared_cycle_length_seed0']:>8d}")
    print(f"\nseed pool {SEEDS}; admissible {report['admissible_seeds']}; "
          f"excluded {report['excluded_seeds']}")
    print("No observed effective information was computed by this script.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
