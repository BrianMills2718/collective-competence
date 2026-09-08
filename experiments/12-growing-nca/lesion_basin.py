"""Map the central circular-lesion response of the fixed published NCA models."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from fetch_upstream import ensure_assets
from nca_numpy import NCA, visible_rgb
from run import FORMATION_STEPS, GRID, RNG_SEED, exact_branch, target_mse, target_rgb

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "lesion_basin.json"
FOLLOW_STEPS = 96
RADIUS_SWEEP = {
    "growing": (2, 4, 8, 12),
    "persistent": (2, 4, 8, 12),
    "regenerating": (2, 4, 8, 12, 14, 16, 18, 20),
}
MODEL_FILES = {
    "growing": "ex1_lizard.json",
    "persistent": "ex2_lizard.json",
    "regenerating": "ex3_lizard.json",
}
LONG_CHECKPOINTS = (32, 64, 96, 128, 192, 256, 384, 512)
LONG_RADII = (16, 18, 20)


def rgb_mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((visible_rgb(a) - visible_rgb(b)) ** 2))


def run_to_checkpoints(nca: NCA, checkpoints: tuple[int, ...], target: np.ndarray) -> list[dict]:
    rows = []
    previous = 0
    for step in checkpoints:
        nca.run(step - previous)
        previous = step
        rows.append({"step": step, "target_mse": target_mse(nca.state, target)})
    return rows


def characterize() -> dict:
    assets = ensure_assets()
    target = target_rgb(assets["emoji.png"])
    fixed_horizon = []
    long_horizon = {}

    for model, filename in MODEL_FILES.items():
        base = NCA(assets[filename], size=GRID, seed=RNG_SEED)
        base.run(FORMATION_STEPS)

        undamaged = exact_branch(base)
        undamaged.run(FOLLOW_STEPS)
        undamaged_state = undamaged.state.copy()
        undamaged_mse = target_mse(undamaged_state, target)

        for radius in RADIUS_SWEEP[model]:
            damaged = exact_branch(base)
            damaged.damage(GRID // 2, GRID // 2, radius)
            immediate = target_mse(damaged.state, target)
            damaged.run(FOLLOW_STEPS)
            fixed_horizon.append({
                "model": model,
                "radius": radius,
                "immediate_target_mse": immediate,
                "target_mse_after_96": target_mse(damaged.state, target),
                "undamaged_target_mse_after_96": undamaged_mse,
                "damaged_vs_undamaged_rgb_mse_after_96": rgb_mse(
                    damaged.state, undamaged_state
                ),
            })

        if model == "regenerating":
            undamaged_long = exact_branch(base)
            long_horizon["undamaged"] = run_to_checkpoints(
                undamaged_long, LONG_CHECKPOINTS, target
            )
            for radius in LONG_RADII:
                damaged = exact_branch(base)
                damaged.damage(GRID // 2, GRID // 2, radius)
                long_horizon[f"radius_{radius}"] = run_to_checkpoints(
                    damaged, LONG_CHECKPOINTS, target
                )

    return {
        "protocol": {
            "grid": GRID,
            "formation_steps": FORMATION_STEPS,
            "fixed_follow_steps": FOLLOW_STEPS,
            "rng_seed": RNG_SEED,
            "damage": "central clear circle",
            "matched_future_update_stream": True,
            "radius_sweep": {key: list(value) for key, value in RADIUS_SWEEP.items()},
            "long_checkpoints": list(LONG_CHECKPOINTS),
        },
        "fixed_horizon": fixed_horizon,
        "regenerating_long_horizon": long_horizon,
    }


def main() -> None:
    result = characterize()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
