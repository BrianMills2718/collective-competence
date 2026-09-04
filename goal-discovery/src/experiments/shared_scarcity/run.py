"""Execute C1-001 and write its result package.

Order matters and is enforced: each seed's `live` run is executed first, because
the `frozen` condition's constant is that seed's own live time-average. Any other
source for that constant is a protocol violation (see the stop conditions).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from .model import Config, feasible, simulate

ALPHAS = (0.0, 0.25, 0.5, 0.75, 1.0)
SEEDS = tuple(range(8))


def load_config(path: Path | None = None) -> Config:
    target = path or Path(__file__).parent / "config.json"
    return Config(**json.loads(target.read_text()))


def _relative_gain(better: float, worse: float) -> float:
    if worse <= 0.0:
        return float("inf") if better > 0.0 else 0.0
    return (better - worse) / worse


def execute(cfg: Config) -> dict[str, Any]:
    if not feasible(cfg):
        raise ValueError(
            "Configuration is infeasible: total quota exceeds the resource ceiling. "
            "Failure here would be an opportunity limit, not a coordination failure."
        )

    per_seed: list[dict[str, Any]] = []
    for seed in SEEDS:
        live = simulate(cfg, seed, signal="live")
        p_bar = live.mean_signal
        frozen = simulate(cfg, seed, signal="frozen", frozen_level=p_bar)
        none = simulate(cfg, seed, signal="none")
        sweep = {
            f"{a:.2f}": simulate(
                cfg, seed, signal="live", frozen_level=p_bar, alpha=a
            ).quota_satisfaction
            for a in ALPHAS
        }
        per_seed.append(
            {
                "seed": seed,
                "p_bar": p_bar,
                "live": live.quota_satisfaction,
                "frozen": frozen.quota_satisfaction,
                "none": none.quota_satisfaction,
                "live_final_stock": live.final_stock,
                "none_final_stock": none.final_stock,
                "none_collapse_tick": none.collapse_tick,
                "sweep": sweep,
            }
        )

    live_v = np.array([s["live"] for s in per_seed])
    frozen_v = np.array([s["frozen"] for s in per_seed])
    none_v = np.array([s["none"] for s in per_seed])

    g1_wins = int(
        sum(_relative_gain(l, n) >= 0.20 for l, n in zip(live_v, none_v, strict=True))
    )
    g2_wins = int(
        sum(_relative_gain(l, f) >= 0.10 for l, f in zip(live_v, frozen_v, strict=True))
    )
    sweep_means = [
        float(np.mean([s["sweep"][f"{a:.2f}"] for s in per_seed])) for a in ALPHAS
    ]
    g3 = all(
        sweep_means[i] <= sweep_means[i + 1] + 1e-9 for i in range(len(sweep_means) - 1)
    )

    g1 = g1_wins >= 6
    g2 = g2_wins >= 6
    if not g1:
        disposition = "invalid_configuration_c1_untested"
    elif not g2:
        disposition = "negative_for_c1_on_this_family"
    elif not g3:
        disposition = "partial_endpoint_effect_without_monotonic_scaling"
    else:
        disposition = "c1_supported_on_this_family_only"

    return {
        "schema_version": 1,
        "protocol": "goal-discovery/docs/hypotheses/c1_001_shared_scarcity_signal.md",
        "config": cfg.__dict__,
        "per_seed": per_seed,
        "means": {
            "live": float(live_v.mean()),
            "frozen": float(frozen_v.mean()),
            "none": float(none_v.mean()),
        },
        "sweep_means": dict(zip([f"{a:.2f}" for a in ALPHAS], sweep_means, strict=True)),
        "gates": {
            "G1_live_beats_none_20pct": {"wins": g1_wins, "of": len(SEEDS), "pass": g1},
            "G2_live_beats_frozen_10pct": {"wins": g2_wins, "of": len(SEEDS), "pass": g2},
            "G3_monotonic_in_alpha": {"pass": bool(g3)},
        },
        "disposition": disposition,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument(
        "--g1-only",
        action="store_true",
        help="Report only the live/none comparison, for authored parameter selection. "
        "The protocol permits tuning against G1 and forbids seeing G2 first.",
    )
    args = parser.parse_args()
    cfg = load_config()
    payload = execute(cfg)
    if args.g1_only:
        print(json.dumps({
            "means_live": payload["means"]["live"],
            "means_none": payload["means"]["none"],
            "G1": payload["gates"]["G1_live_beats_none_20pct"],
            "none_collapse_ticks": [s["none_collapse_tick"] for s in payload["per_seed"]],
            "live_final_stock": [round(s["live_final_stock"], 2) for s in payload["per_seed"]],
        }, indent=2))
        return 0
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in ("means", "sweep_means", "gates", "disposition")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
