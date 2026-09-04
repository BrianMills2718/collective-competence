"""C2-002: how load-bearing is the derivation rule?

Sweeps a generic affine-then-modulo family. The C2-001 rule is the single point
(a=1, b=0) and receives no special handling: it is scored by the same code path
as every other member and is only identified when the distribution is reported.

Degenerate members (a=0, constant phase) are included on purpose as the
discrimination check.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from .model import Config
from .run import SEEDS, load_config

SPREAD = 0.75
A_GRID = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0)
B_GRID = (0.0, 1.0, 2.0, 3.0, 5.0)


def _score(cfg: Config, seed: int, a: float, b: float) -> float:
    """One run under phase(need) = int(a*need + b) mod P. Substrate unchanged."""
    rng = np.random.default_rng(seed)
    needs = np.maximum(
        1,
        np.round(rng.uniform(cfg.mean_need * (1 - SPREAD),
                             cfg.mean_need * (1 + SPREAD),
                             size=cfg.n_subunits)),
    ).astype(int)
    period = cfg.n_subunits
    phases = np.array([int(a * n + b) % period for n in needs])
    obtained = np.zeros(cfg.n_subunits, dtype=float)
    for tick in range(cfg.horizon):
        remaining = np.maximum(needs - obtained, 0.0)
        attempts = (remaining > 0) & (phases == (tick % period))
        n = int(attempts.sum())
        if n:
            obtained[attempts] += 1.0 / (n * n)
    return float((obtained >= needs - 1e-9).mean())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    cfg = load_config()

    rows = []
    for a in A_GRID:
        for b in B_GRID:
            mean = float(np.mean([_score(cfg, s, a, b) for s in SEEDS]))
            rows.append({"a": a, "b": b, "mean": mean, "degenerate": a == 0.0})

    authored = next(r["mean"] for r in rows if r["a"] == 1.0 and r["b"] == 0.0)
    nondegen = [r for r in rows if not r["degenerate"]]
    degen = [r for r in rows if r["degenerate"]]
    within90 = [r for r in nondegen if r["mean"] >= 0.9 * authored]
    best = max(rows, key=lambda r: r["mean"])
    frac = len(within90) / len(nondegen)

    separated = max(r["mean"] for r in degen) < 0.5 * authored
    payload = {
        "spread": SPREAD, "authored_rule_mean": authored,
        "n_members": len(rows), "n_nondegenerate": len(nondegen),
        "fraction_within_90pct": frac,
        "best": best,
        "best_beats_authored_by": best["mean"] - authored,
        "degenerate_max": max(r["mean"] for r in degen),
        "discrimination_check_passed": bool(separated),
        "rows": rows,
    }
    payload["disposition"] = (
        "void_measurement_insensitive" if not separated else
        "rule_not_load_bearing_broad_plateau" if frac >= 0.5 else
        "rule_strongly_load_bearing_narrow_ridge" if frac < 0.1 else
        "partial_report_the_distribution"
    )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "rule-sweep.json").write_text(json.dumps(payload, indent=2) + "\n")

    print(f"authored rule (a=1,b=0): {authored:.3f}")
    print(f"degenerate (a=0) max:    {payload['degenerate_max']:.3f}   "
          f"discrimination check passed: {separated}")
    print(f"non-degenerate members:  {len(nondegen)}")
    print(f"fraction within 90% of authored: {frac:.3f}")
    print(f"best member: a={best['a']} b={best['b']} -> {best['mean']:.3f} "
          f"({payload['best_beats_authored_by']:+.3f} vs authored)")
    print(f"disposition: {payload['disposition']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
