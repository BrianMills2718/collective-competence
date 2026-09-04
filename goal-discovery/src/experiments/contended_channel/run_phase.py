"""Execute C2-001: precondition P0, then refuter-2 gates G1 and G2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from .phase import simulate_phase
from .run import SEEDS, load_config

SPREADS = (0.0, 0.1, 0.25, 0.5, 0.75)
MODES = ("level_only", "authored_phase", "derived_phase")


def _wins(better, worse, threshold=0.20):
    return sum(1 for b, w in zip(better, worse, strict=True)
               if (w <= 0 and b > 0) or (w > 0 and (b - w) / w >= threshold))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    cfg = load_config()

    cells = {}
    for spread in SPREADS:
        for mode in MODES:
            cells[(spread, mode)] = [
                simulate_phase(cfg, s, mode=mode, spread=spread).need_satisfaction
                for s in SEEDS
            ]

    widest = SPREADS[-1]
    p0 = _wins(cells[(widest, "authored_phase")], cells[(widest, "level_only")])
    g1 = _wins(cells[(widest, "derived_phase")], cells[(widest, "level_only")])
    derived_means = [float(np.mean(cells[(s, "derived_phase")])) for s in SPREADS]
    g2 = all(derived_means[i] <= derived_means[i + 1] + 1e-9 for i in range(len(SPREADS) - 1))

    payload = {
        "means": {f"{s}": {m: float(np.mean(cells[(s, m)])) for m in MODES} for s in SPREADS},
        "distinct_phases_at_widest": {
            m: simulate_phase(cfg, 0, mode=m, spread=widest).distinct_phases
            for m in ("authored_phase", "derived_phase")
        },
        "gates": {
            "P0_authored_beats_level": {"wins": p0, "of": len(SEEDS), "pass": p0 >= 6},
            "G1_derived_beats_level": {"wins": g1, "of": len(SEEDS), "pass": g1 >= 6},
            "G2_derived_monotonic_in_spread": {"pass": bool(g2), "means": derived_means},
        },
    }
    payload["disposition"] = (
        "invalid_substrate_p0_failed" if p0 < 6 else
        "refuter_2_fires_environmental_heterogeneity_insufficient" if g1 < 6 else
        "derived_works_but_not_by_the_stated_scaling" if not g2 else
        "c2_sharper_half_supported_on_this_family"
    )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "result.json").write_text(json.dumps(payload, indent=2) + "\n")

    print(f"{'spread':<9}{'level_only':<13}{'authored':<13}{'derived'}")
    for s in SPREADS:
        m = payload["means"][f"{s}"]
        print(f"{s:<9}{m['level_only']:<13.3f}{m['authored_phase']:<13.3f}{m['derived_phase']:.3f}")
    print()
    print(json.dumps({"distinct_phases": payload["distinct_phases_at_widest"],
                      "gates": payload["gates"], "disposition": payload["disposition"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
