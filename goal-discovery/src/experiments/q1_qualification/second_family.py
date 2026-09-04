"""Q1-004: the frozen Q1-003 detector on the C2-001 contended-channel family.

The detector is imported unchanged from .latent_shared. Nothing here modifies
its estimator or its persistence threshold -- that is what clause 4 requires and
what the protocol's stop conditions forbid touching.

Positive arm: derived phase (coprime multiplier), entities differentiated.
Negative arm: constant phase (a = 0), entities ACTIVE but undifferentiated --
chosen because Q1-001's negative arm was degenerate and any separation there
would only have measured activity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.experiments.contended_channel.run import SEEDS, load_config

from .latent_shared import report_dict


def _trace(cfg, seed: int, multiplier: float) -> list[dict]:
    """Replay one arm, recording per-entity observables only.

    Phase, rule and period are never written into the record.
    """
    rng = np.random.default_rng(seed)
    needs = np.maximum(
        1,
        np.round(rng.uniform(cfg.mean_need * (1 - 0.75),
                             cfg.mean_need * (1 + 0.75),
                             size=cfg.n_subunits)),
    ).astype(int)
    period = cfg.n_subunits
    phases = np.array([int(multiplier * n) % period for n in needs])
    obtained = np.zeros(cfg.n_subunits, dtype=float)
    frames = []
    for tick in range(cfg.horizon):
        remaining = np.maximum(needs - obtained, 0.0)
        attempts = (remaining > 0) & (phases == (tick % period))
        n = int(attempts.sum())
        gain = np.zeros(cfg.n_subunits)
        if n:
            gain[attempts] = 1.0 / (n * n)
            obtained += gain
        frames.append({
            "time": tick,
            "entities": [
                {"entity_id": f"e{i:03d}",
                 "values": {"f000": float(obtained[i]), "f001": float(gain[i])}}
                for i in range(cfg.n_subunits)
            ],
        })
    return frames


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    cfg = load_config()

    arms = {"derived_phase": 1.0, "constant_phase": 0.0}
    rows = []
    for arm, multiplier in arms.items():
        package = {
            "schema_version": 1, "contract_version": 1,
            "case_id": "case-" + f"{abs(hash(arm)):012x}"[:12],
            "shape": "repeated_entity_dynamics",
            "fields": [
                {"field_id": "f000", "type": "continuous", "group": "g000", "units": "unknown"},
                {"field_id": "f001", "type": "continuous", "group": "g000", "units": "unknown"},
            ],
            "units": [{"unit_id": f"u{i:03d}", "frames": _trace(cfg, s, multiplier)}
                      for i, s in enumerate(SEEDS)],
        }
        rows.append({"arm": arm, **report_dict(package)})

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "second-family-report.json").write_text(json.dumps({"rows": rows}, indent=2) + "\n")

    print(f"{'arm':<18}{'shared_var_frac':<18}{'persistence':<14}local_resid_var")
    print("-" * 68)
    for r in rows:
        print(f"{r['arm']:<18}{r['shared_variance_fraction']:<18.4f}"
              f"{r['persistence']:<14.4f}{r['local_residual_variance']:.6f}")
    d = abs(rows[0]["persistence"] - rows[1]["persistence"])
    direction = "predicted" if rows[0]["persistence"] > rows[1]["persistence"] else "OPPOSITE"
    print(f"\npersistence gap: {d:.4f}   direction: {direction}")
    print(f"distinguishes (gap > 0.1): {d > 0.1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
