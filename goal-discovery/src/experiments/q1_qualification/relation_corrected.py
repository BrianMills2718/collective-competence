"""Q1-007: pairwise relation after removing the substrate's congestion coupling.

Reuses the Q1-005 arms and the Q1-003 common-component estimator unchanged. The
only new thing is how what remains after removing the common component is read:
pairwise correlation across entities, which is zero in expectation for an
independent population and strongly negative for one taking turns.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.experiments.contended_channel.run import SEEDS, load_config

from .idiosyncratic import _trace

G1_SIGNAL, G2_MARGIN, G3_RANDOM_MAX = 0.15, 0.10, 0.10


def _residual_correlation(frames_per_unit: list[list[dict]]) -> float:
    """Mean |off-diagonal correlation| of post-common-component residuals."""
    per_unit = []
    for frames in frames_per_unit:
        rows = []
        for frame in frames:
            ents = sorted(frame["entities"], key=lambda e: e["entity_id"])
            rows.append([[e["values"]["f000"], e["values"]["f001"]] for e in ents])
        arr = np.asarray(rows, dtype=float)          # (time, entity, field)
        cur, nxt = arr[:-1], arr[1:]
        n_ent, n_f = cur.shape[1], cur.shape[2]
        x = cur.reshape(-1, n_f)
        y = nxt.reshape(-1, n_f)
        design = np.hstack([x, np.ones((x.shape[0], 1))])
        coef, *_ = np.linalg.lstsq(design, y, rcond=None)
        resid = (y - design @ coef).reshape(cur.shape[0], n_ent, n_f)
        resid = resid - resid.mean(axis=1, keepdims=True)   # remove common component

        # Q1-007: remove the substrate's own coupling. k simultaneous attempters
        # each receive 1/k**2, so independent entities still share an outcome
        # term. The acting count is recovered from the observations themselves --
        # entities with non-zero gain this tick -- so nothing privileged is used.
        acting = (np.abs(nxt[:, :, 1]) > 1e-12).sum(axis=1).astype(float)
        ctrl = np.column_stack([acting, np.ones_like(acting)])
        for e in range(n_ent):
            for f in range(n_f):
                beta, *_ = np.linalg.lstsq(ctrl, resid[:, e, f], rcond=None)
                resid[:, e, f] -= ctrl @ beta
        # One series per entity: the field-summed residual over time.
        series = resid.sum(axis=2).T                        # (entity, time)
        sd = series.std(axis=1)
        keep = sd > 1e-12
        if keep.sum() < 2:
            continue
        c = np.corrcoef(series[keep])
        off = c[~np.eye(c.shape[0], dtype=bool)]
        per_unit.append(float(np.mean(np.abs(off))))
    return float(np.mean(per_unit)) if per_unit else 0.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    cfg = load_config()

    rows = []
    for arm in ("derived_phase", "constant_phase", "random_attempt"):
        frames_per_unit = [_trace(cfg, s, arm)[0] for s in SEEDS]
        rows.append({"arm": arm, "mean_abs_offdiag_corr": _residual_correlation(frames_per_unit)})

    by = {r["arm"]: r["mean_abs_offdiag_corr"] for r in rows}
    margin = by["derived_phase"] - by["random_attempt"]
    g1, g2, g3 = by["derived_phase"] >= G1_SIGNAL, margin >= G2_MARGIN, by["random_attempt"] <= G3_RANDOM_MAX
    payload = {
        "rows": rows,
        "gates": {
            "G1_signal": {"pass": bool(g1), "value": by["derived_phase"], "required": G1_SIGNAL},
            "G2_sufficiency": {"pass": bool(g2), "margin": margin, "required": G2_MARGIN},
            "G3_clause2_random_low": {"pass": bool(g3), "value": by["random_attempt"], "max": G3_RANDOM_MAX},
        },
        "disposition": (
            "no_signal_discard" if not g1 else
            "relation_not_measured_line_exhausted" if not g2 else
            "contaminated_by_congestion_coupling" if not g3 else
            "separates_coordination_from_uniformity_and_independence"
        ),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "result.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(f"{'arm':<18}mean |off-diagonal correlation|")
    print("-" * 50)
    for r in rows:
        print(f"{r['arm']:<18}{r['mean_abs_offdiag_corr']:.4f}")
    print()
    print(json.dumps({"gates": payload["gates"], "disposition": payload["disposition"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
