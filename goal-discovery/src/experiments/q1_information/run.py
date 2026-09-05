"""Execute the frozen Q1-009 protocol. Reads its thresholds from the protocol only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.experiments.contended_channel.run import load_config as slot_config
from src.experiments.q1_information import commons as cm
from src.experiments.q1_information.calibrate import OBSERVED, ei_pair
from src.experiments.q1_information.measures import blahut_arimoto
from src.experiments.q1_information.traces import ARMS as SLOT_ARMS
from src.experiments.q1_information.traces import (
    action_trace as slot_trace,
)
from src.experiments.q1_information.traces import (
    forced_action_outcome_pair,
    shuffle_null,
)

SEEDS = 1600
NULL_REPLICATES = 5
EMP_SEEDS = 200
EMP_SAMPLES = 40
EMP_AHEAD = 5
# A single forced tick moved a commons subunit's own need by at most
# draw_cap/quota = 1.9%, which three buckets could not resolve, so the measured
# capacity was ~0 for reasons of instrumentation rather than of the system. A
# contiguous block and finer buckets put the intervention above the resolution.
EMP_BLOCK = 10
EMP_BUCKETS = 8
G1_MIN, G2_MIN, G3_MIN = 0.10, 0.05, 0.05


def ei_block(traces: list[np.ndarray], rng: np.random.Generator) -> dict:
    obs = ei_pair(traces, OBSERVED)
    nulls = [ei_pair([shuffle_null(t, rng) for t in traces], OBSERVED)
             for _ in range(NULL_REPLICATES)]
    null_micro = [n["ei_micro"] for n in nulls]
    null_em = [n["emergence"] for n in nulls]
    return {
        "ei_micro": obs["ei_micro"],
        "ei_macro": obs["ei_macro"],
        "emergence": obs["emergence"],
        "transitions_per_seen_row": obs["transitions_per_seen_row"],
        "null_ei_micro_mean": float(np.mean(null_micro)),
        "null_ei_micro_sd": float(np.std(null_micro, ddof=1)),
        "null_emergence_mean": float(np.mean(null_em)),
        "null_emergence_sd": float(np.std(null_em, ddof=1)),
        "ei_micro_above_null": obs["ei_micro"] - float(np.mean(null_micro)),
        "emergence_above_null": obs["emergence"] - float(np.mean(null_em)),
    }


def empowerment(kind: str, cfg, arm: str) -> dict:
    # Not hash(): Python salts it per process, so the original seeding made every
    # empowerment number unreproducible across runs. SeedSequence over the bytes
    # is stable.
    rng = np.random.default_rng(
        np.random.SeedSequence(list(f"{kind}/{arm}".encode()))
    )
    counts = np.zeros((2, EMP_BUCKETS))
    inadmissible = 0
    n_units = cfg.n_subunits
    for seed in range(EMP_SEEDS):
        for _ in range(EMP_SAMPLES):
            unit = int(rng.integers(n_units))
            tick = int(rng.integers(0, cfg.horizon - EMP_BLOCK - EMP_AHEAD - 1))
            if kind == "slot":
                # Bucket against the unit's OWN need, absolutely. The original code
                # divided by the larger of the counterfactual pair, which made the
                # code for do(act) depend on what happened under do(not act) and
                # forced the larger outcome into the top bucket every time -- p(middle
                # bucket | do not act) was structurally 0.000 in all three arms. It
                # also put the slot on a different scale from the commons, so the two
                # could not be compared. Same absolute rule as commons.empowerment_channel.
                pair = forced_action_outcome_pair(cfg, seed, arm, unit, tick, EMP_AHEAD,
                                                  n_buckets=EMP_BUCKETS, block=EMP_BLOCK)
                if pair is None:
                    inadmissible += 1
                    continue
                on, off = pair
            else:
                on, off = cm.empowerment_channel(cfg, seed, arm, unit, tick,
                                                 EMP_AHEAD, EMP_BUCKETS,
                                                 block=EMP_BLOCK)
            counts[0, on] += 1
            counts[1, off] += 1
    totals = counts.sum(axis=1, keepdims=True)
    channel = np.divide(counts, totals, out=np.zeros_like(counts), where=totals > 0)
    used = (channel > 0).any(axis=1)
    if not used.all():
        raise ValueError(f"{kind}/{arm}: an action was never sampled; cannot take capacity")
    return {"capacity_bits": blahut_arimoto(channel),
            "channel": channel.tolist(),
            "samples": int(counts.sum()),
            "inadmissible_samples": int(inadmissible)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    rng = np.random.default_rng(90920260905)
    report: dict = {"seeds": SEEDS, "null_replicates": NULL_REPLICATES,
                    "observed_units": OBSERVED, "commons": {}, "slot": {},
                    "empowerment": {"slot": {}, "commons": {}}}

    ccfg = cm.load()
    for arm in cm.ARMS:
        traces = [cm.action_trace(ccfg, s, arm)[0] for s in range(SEEDS)]
        report["commons"][arm] = ei_block(traces, rng)

    scfg = slot_config()
    for arm in SLOT_ARMS:
        traces = [slot_trace(scfg, s, arm)[0] for s in range(SEEDS)]
        report["slot"][arm] = ei_block(traces, rng)

    for arm in SLOT_ARMS:
        report["empowerment"]["slot"][arm] = empowerment("slot", scfg, arm)
    for arm in cm.ARMS:
        report["empowerment"]["commons"][arm] = empowerment("commons", ccfg, arm)

    live = report["commons"]["live"]["ei_micro_above_null"]
    none = report["commons"]["none"]["ei_micro_above_null"]
    caps = [report["empowerment"]["slot"][a]["capacity_bits"] for a in SLOT_ARMS]
    report["gates"] = {
        "G1_structure_above_null": {"value": live, "min": G1_MIN, "pass": live >= G1_MIN},
        "G2_discrimination": {"value": live - none, "min": G2_MIN, "pass": (live - none) >= G2_MIN},
        "G3_empowerment_not_vacuous": {"value": max(caps) - min(caps), "min": G3_MIN,
                                       "pass": (max(caps) - min(caps)) >= G3_MIN},
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    print(f"{'commons arm':<14}{'EI_micro':>10}{'null':>9}{'above':>9}{'emerg':>9}{'em_above':>10}")
    for arm, r in report["commons"].items():
        print(f"{arm:<14}{r['ei_micro']:>10.3f}{r['null_ei_micro_mean']:>9.3f}"
              f"{r['ei_micro_above_null']:>9.3f}{r['emergence']:>9.3f}{r['emergence_above_null']:>10.3f}")
    print(f"\n{'slot arm':<16}{'EI_micro':>10}{'null':>9}{'above':>9}{'emerg':>9}{'em_above':>10}")
    for arm, r in report["slot"].items():
        print(f"{arm:<16}{r['ei_micro']:>10.3f}{r['null_ei_micro_mean']:>9.3f}"
              f"{r['ei_micro_above_null']:>9.3f}{r['emergence']:>9.3f}{r['emergence_above_null']:>10.3f}")
    print("\nempowerment (bits)")
    for kind in ("slot", "commons"):
        for arm, r in report["empowerment"][kind].items():
            print(f"  {kind:<8}{arm:<16}{r['capacity_bits']:.4f}")
    print("\ngates")
    for g, r in report["gates"].items():
        print(f"  {g:<28}{r['value']:+.4f}  min {r['min']:.2f}  {'PASS' if r['pass'] else 'FAIL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
