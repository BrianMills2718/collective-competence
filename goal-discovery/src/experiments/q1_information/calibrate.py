"""Measure the nulls before any Q1-009 threshold is chosen.

Q1-008's finding was that a gate had been frozen below its statistic's own
finite-sample floor, so no independent process could have passed it, and that
the same error was then repeated inside the experiment designed to catch it.
This script exists so that cannot happen a third time: it reports what each
statistic reads on structureless input at the exact dimensions and sample sizes
the experiment will use, and its output is committed before the protocol names a
number.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.experiments.contended_channel.run import load_config
from src.experiments.q1_information.measures import (
    coarse_grain,
    effective_information,
    tpm_from_transitions,
)
from src.experiments.q1_information.traces import (
    ARMS,
    action_trace,
    micro_macro_codes,
    micro_state_groups,
    shuffle_null,
)

OBSERVED = 5


def ei_pair(actions_list: list[np.ndarray], observed: int) -> dict:
    n_micro = 1 << observed
    groups = micro_state_groups(observed)
    pairs = []
    for actions in actions_list:
        micro, _ = micro_macro_codes(actions, observed)
        pairs.extend(zip(micro[:-1], micro[1:]))
    pairs = np.asarray(pairs)
    tpm, seen, totals = tpm_from_transitions(pairs, n_micro)
    ei_micro = effective_information(tpm, rows_seen=seen)
    macro, macro_seen = coarse_grain(tpm, groups, rows_seen=seen)
    ei_macro = effective_information(macro, rows_seen=macro_seen)
    return {
        "ei_micro": ei_micro,
        "ei_macro": ei_macro,
        "emergence": ei_macro - ei_micro,
        "transitions": int(pairs.shape[0]),
        "micro_rows_seen": int(seen.sum()),
        "transitions_per_seen_row": float(pairs.shape[0] / max(1, seen.sum())),
        "min_row_count": float(totals[seen].min()) if seen.any() else 0.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--seeds", type=int, default=400)
    args = ap.parse_args()

    cfg = load_config()
    rng = np.random.default_rng(20260905)
    report: dict = {"observed_units": OBSERVED, "micro_states": 1 << OBSERVED,
                    "macro_states": OBSERVED + 1, "horizon": cfg.horizon, "arms": {},
                    "seed_sweep": {}}

    for arm in ARMS:
        traces = [action_trace(cfg, s, arm)[0] for s in range(args.seeds)]
        observed = ei_pair(traces, OBSERVED)
        nulls = [shuffle_null(t, rng) for t in traces]
        null = ei_pair(nulls, OBSERVED)
        report["arms"][arm] = {"observed": observed, "shuffle_null": null,
                               "emergence_above_null": observed["emergence"] - null["emergence"]}

    for n_seeds in (25, 50, 100, 200, 400):
        traces = [action_trace(cfg, s, "derived_phase")[0] for s in range(n_seeds)]
        nulls = [shuffle_null(t, rng) for t in traces]
        report["seed_sweep"][str(n_seeds)] = {
            "observed": ei_pair(traces, OBSERVED),
            "shuffle_null": ei_pair(nulls, OBSERVED),
        }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"{'arm':<17}{'EI_micro':>10}{'EI_macro':>10}{'emerg':>9}{'null_em':>10}{'diff':>9}{'per_row':>10}")
    for arm, row in report["arms"].items():
        o, n = row["observed"], row["shuffle_null"]
        print(f"{arm:<17}{o['ei_micro']:>10.3f}{o['ei_macro']:>10.3f}{o['emergence']:>9.3f}"
              f"{n['emergence']:>10.3f}{row['emergence_above_null']:>9.3f}"
              f"{o['transitions_per_seen_row']:>10.0f}")
    print("\nseed sweep (derived_phase): emergence observed vs shuffle null")
    for k, v in report["seed_sweep"].items():
        print(f"  {k:>4} seeds  obs {v['observed']['emergence']:+.3f}   "
              f"null {v['shuffle_null']['emergence']:+.3f}   "
              f"diff {v['observed']['emergence'] - v['shuffle_null']['emergence']:+.3f}   "
              f"({v['observed']['transitions_per_seen_row']:.0f}/row)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
