"""Probe visible versus hidden-state damage in the fixed regenerating NCA."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from fetch_upstream import ensure_assets
from nca_numpy import NCA, visible_rgb
from run import FORMATION_STEPS, GRID, RNG_SEED, exact_branch, target_mse, target_rgb

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "hidden_state_probe.json"
FOLLOW = 96
RADII = (8, 16)
REPLICATION_SEEDS = (100, 101, 102, 103)


def mask(radius: int) -> np.ndarray:
    yy, xx = np.mgrid[:GRID, :GRID]
    return np.sqrt((yy - GRID // 2) ** 2 + (xx - GRID // 2) ** 2) < radius


def apply(state: np.ndarray, radius: int, arm: str) -> np.ndarray:
    out = state.copy()
    m = mask(radius)
    if arm == "visible_only":
        out[m, :4] = 0.0
    elif arm == "hidden_only":
        out[m, 4:] = 0.0
    elif arm == "full":
        out[m, :] = 0.0
    elif arm != "none":
        raise ValueError(arm)
    return out


def branch_with_seed(formed: np.ndarray, model_path: Path, seed: int, arm: str, radius: int) -> NCA:
    out = NCA(model_path, size=GRID, seed=seed)
    out.state = apply(formed, radius, arm)
    out.rng = np.random.default_rng(seed)
    out.steps = FORMATION_STEPS
    return out


def rgb_mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((visible_rgb(a) - visible_rgb(b)) ** 2))


def characterize() -> dict:
    assets = ensure_assets()
    target = target_rgb(assets["emoji.png"])
    path = assets["ex3_lizard.json"]
    base = NCA(path, size=GRID, seed=RNG_SEED)
    base.run(FORMATION_STEPS)
    formed = base.state.copy()

    matched_curves = []
    for radius in RADII:
        branches = {}
        for arm in ("none", "visible_only", "hidden_only", "full"):
            b = exact_branch(base)
            b.state = apply(formed, radius, arm)
            b.run(FOLLOW)
            branches[arm] = b.state.copy()
        matched_curves.append({
            "radius": radius,
            "target_mse_after_96": {
                arm: target_mse(state, target) for arm, state in branches.items()
            },
            "vs_undamaged_rgb_mse_after_96": {
                arm: rgb_mse(state, branches["none"])
                for arm, state in branches.items() if arm != "none"
            },
        })

    replications = []
    for seed in REPLICATION_SEEDS:
        branches = {}
        for arm in ("none", "hidden_only", "full"):
            b = branch_with_seed(formed, path, seed, arm, 16)
            b.run(FOLLOW)
            branches[arm] = b.state.copy()
        replications.append({
            "future_seed": seed,
            "target_mse_after_96": {
                arm: target_mse(state, target) for arm, state in branches.items()
            },
            "vs_undamaged_rgb_mse_after_96": {
                arm: rgb_mse(state, branches["none"])
                for arm, state in branches.items() if arm != "none"
            },
        })

    hidden = [r["target_mse_after_96"]["hidden_only"] for r in replications]
    full = [r["target_mse_after_96"]["full"] for r in replications]
    return {
        "protocol": {
            "grid": GRID,
            "formation_steps": FORMATION_STEPS,
            "follow_steps": FOLLOW,
            "formed_state_seed": RNG_SEED,
            "matched_curve_radii": list(RADII),
            "replication_radius": 16,
            "replication_future_seeds": list(REPLICATION_SEEDS),
        },
        "matched_curves": matched_curves,
        "replications": replications,
        "summary": {
            "hidden_worse_than_full_count": sum(h > f for h, f in zip(hidden, full)),
            "replication_count": len(replications),
            "mean_hidden_target_mse": float(np.mean(hidden)),
            "mean_full_target_mse": float(np.mean(full)),
        },
    }


def main() -> None:
    result = characterize()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
