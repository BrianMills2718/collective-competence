"""Characterize adaptive, frozen, and reset policies across episode histories."""
from __future__ import annotations
import json
from pathlib import Path
from model import A_GOOD, B_GOOD, reversal, run, stationary

HERE = Path(__file__).resolve().parent
SEQUENCES = {
    "a_stationary": stationary(A_GOOD),
    "b_stationary": stationary(B_GOOD),
    "a_then_b": reversal(A_GOOD, B_GOOD),
    "b_then_a": reversal(B_GOOD, A_GOOD),
}


def characterize() -> dict:
    cases = {}
    for name, envs in SEQUENCES.items():
        cases[name] = {policy: run(policy, envs) for policy in ("adaptive", "frozen", "reset")}
    return {"batch": 100, "learning_rule": "p <- clip(p + 0.5*(quality_a-quality_b), 0.1, 0.9)", "cases": cases}

if __name__ == "__main__":
    value=characterize()
    out=HERE/'results/characterization.json'
    out.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    print(json.dumps(value, indent=2, sort_keys=True))
