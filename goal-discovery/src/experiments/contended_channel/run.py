"""Execute C1-002's validity gate. Reports nothing about any detector."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from .model import Config, feasible, simulate

SEEDS = tuple(range(8))


def load_config(path: Path | None = None) -> Config:
    target = path or Path(__file__).parent / "config.json"
    return Config(**json.loads(target.read_text()))


def execute(cfg: Config) -> dict:
    if not feasible(cfg):
        raise ValueError("Infeasible: total need exceeds one slot per tick over the horizon.")
    rows = []
    for seed in SEEDS:
        live = simulate(cfg, seed, signal="live")
        none = simulate(cfg, seed, signal="none")
        rows.append({
            "seed": seed,
            "live": live.need_satisfaction, "none": none.need_satisfaction,
            "live_collisions": live.collisions, "none_collisions": none.collisions,
            "live_idle": live.idle_ticks, "none_idle": none.idle_ticks,
            "live_served": live.served_total, "none_served": none.served_total,
        })
    wins = sum(
        1 for r in rows
        if (r["none"] <= 0 and r["live"] > 0)
        or (r["none"] > 0 and (r["live"] - r["none"]) / r["none"] >= 0.20)
    )
    return {
        "config": cfg.__dict__,
        "per_seed": rows,
        "means": {"live": float(np.mean([r["live"] for r in rows])),
                  "none": float(np.mean([r["none"] for r in rows]))},
        "validity_gate": {"wins": wins, "of": len(SEEDS), "pass": wins >= 6},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    payload = execute(load_config())
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in ("means", "validity_gate")}, indent=2))
    print("collisions live/none:",
          [(r["live_collisions"], r["none_collisions"]) for r in payload["per_seed"]][:4])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
