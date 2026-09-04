"""Q1-005: does the idiosyncratic fraction measure coordination or differentiation?

Three arms on the C2-001 contended channel. The detector's estimator is imported
unchanged; only the reading of its output changes -- idiosyncratic fraction is
1 - shared_variance_fraction.

`random_attempt` is the sufficiency control both prior runs lacked: differentiated
but uncoordinated, matched to `derived_phase` on duty cycle so the arms differ
only in whether the acting is structured.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.experiments.contended_channel.run import SEEDS, load_config

from .latent_shared import report_dict

G1_COORD_MIN, G1_UNIFORM_MAX, G2_MARGIN = 0.30, 0.10, 0.20


def _trace(cfg, seed: int, arm: str) -> list[dict]:
    rng = np.random.default_rng(seed)
    needs = np.maximum(
        1,
        np.round(rng.uniform(cfg.mean_need * 0.25, cfg.mean_need * 1.75,
                             size=cfg.n_subunits)),
    ).astype(int)
    period = cfg.n_subunits
    # Matched duty cycle: under a phase rule each subunit acts once per period.
    duty = 1.0 / period
    act_rng = np.random.default_rng(seed + 777)

    if arm == "derived_phase":
        phases = np.array([int(n) % period for n in needs])
    elif arm == "constant_phase":
        phases = np.zeros(cfg.n_subunits, dtype=int)
    elif arm == "random_attempt":
        phases = None
    else:
        raise ValueError(f"unknown arm: {arm!r}")

    obtained = np.zeros(cfg.n_subunits, dtype=float)
    frames = []
    for tick in range(cfg.horizon):
        remaining = np.maximum(needs - obtained, 0.0)
        if phases is None:
            attempts = (remaining > 0) & (act_rng.random(cfg.n_subunits) < duty)
        else:
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
    return frames, float((obtained >= needs - 1e-9).mean())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    cfg = load_config()

    rows = []
    for arm in ("derived_phase", "constant_phase", "random_attempt"):
        units, perf = [], []
        for i, s in enumerate(SEEDS):
            frames, p = _trace(cfg, s, arm)
            units.append({"unit_id": f"u{i:03d}", "frames": frames})
            perf.append(p)
        package = {
            "schema_version": 1, "contract_version": 1,
            "case_id": "case-" + f"{abs(hash(arm)):012x}"[:12],
            "shape": "repeated_entity_dynamics",
            "fields": [
                {"field_id": "f000", "type": "continuous", "group": "g000", "units": "unknown"},
                {"field_id": "f001", "type": "continuous", "group": "g000", "units": "unknown"},
            ],
            "units": units,
        }
        rep = report_dict(package)
        rows.append({
            "arm": arm,
            "idiosyncratic_fraction": 1.0 - rep["shared_variance_fraction"],
            "shared_variance_fraction": rep["shared_variance_fraction"],
            "persistence": rep["persistence"],
            "need_satisfaction": float(np.mean(perf)),
        })

    by = {r["arm"]: r for r in rows}
    g1 = (by["derived_phase"]["idiosyncratic_fraction"] >= G1_COORD_MIN
          and by["constant_phase"]["idiosyncratic_fraction"] <= G1_UNIFORM_MAX)
    margin = by["derived_phase"]["idiosyncratic_fraction"] - by["random_attempt"]["idiosyncratic_fraction"]
    g2 = margin >= G2_MARGIN
    payload = {
        "rows": rows,
        "gates": {
            "G1_necessity": {"pass": bool(g1), "coord_min": G1_COORD_MIN, "uniform_max": G1_UNIFORM_MAX},
            "G2_sufficiency": {"pass": bool(g2), "margin": margin, "required": G2_MARGIN},
        },
        "disposition": (
            "reinterpretation_wrong_on_its_own_terms" if not g1 else
            "measures_differentiation_not_coordination_clause_2_fails" if not g2 else
            "marginal_do_not_round_up" if margin < G2_MARGIN + 0.05 else
            "instrument_qualified_separates_coordination_from_uniformity_and_independence"
        ),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "result.json").write_text(json.dumps(payload, indent=2) + "\n")

    print(f"{'arm':<18}{'idiosyncratic':<16}{'persistence':<14}{'need_satisfaction'}")
    print("-" * 68)
    for r in rows:
        print(f"{r['arm']:<18}{r['idiosyncratic_fraction']:<16.4f}"
              f"{r['persistence']:<14.4f}{r['need_satisfaction']:.3f}")
    print()
    print(json.dumps({"gates": payload["gates"], "disposition": payload["disposition"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
