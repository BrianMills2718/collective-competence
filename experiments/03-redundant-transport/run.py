"""Characterize compensation and its capacity boundary in redundant transport."""
from __future__ import annotations

import json
from pathlib import Path

from model import Config, run

HERE = Path(__file__).resolve().parent


def summarize(rows: list[dict], cfg: Config) -> dict:
    post = rows[cfg.fault_tick:]
    return {
        "final_backlog": rows[-1]["backlog"],
        "post_fault_mean_flow_a": sum(r["flow_a"] for r in post) / len(post),
        "post_fault_mean_flow_b": sum(r["flow_b"] for r in post) / len(post),
        "post_fault_delivery_rate": sum(r["flow_a"] + r["flow_b"] for r in post) / len(post),
        "criterion_zero_backlog": rows[-1]["backlog"] == 0,
    }


def characterize() -> dict:
    cases = []
    for demand in (2, 4):
        cfg = Config(demand=demand)
        for policy in ("reroute", "fixed"):
            for fail in ("none", "a", "b", "both"):
                rows = run(policy, cfg, fail=fail)
                cases.append({
                    "demand": demand,
                    "policy": policy,
                    "failure": fail,
                    **summarize(rows, cfg),
                })
    return {
        "system": {"routes": 2, "capacity_each": 2, "fault_tick": 20, "horizon": 60},
        "criterion": "zero backlog",
        "cases": cases,
    }


def main() -> None:
    result = characterize()
    out = HERE / "results" / "characterization.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
