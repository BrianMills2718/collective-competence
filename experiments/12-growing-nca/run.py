"""Reproduce the published growing/persistent/regenerating NCA hierarchy."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
from matplotlib.image import imread

from fetch_upstream import MANIFEST, ensure_assets
from nca_numpy import NCA, visible_rgb

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "characterization.json"
GRID = 96
FORMATION_STEPS = 96
FOLLOW_STEPS = 96
DAMAGE_RADIUS = 8.0
RNG_SEED = 7
MODEL_FILES = {
    "growing": "ex1_lizard.json",
    "persistent": "ex2_lizard.json",
    "regenerating": "ex3_lizard.json",
}


def target_rgb(sprite_path: Path) -> np.ndarray:
    """Return the official 40x40 lizard target, white-composited and centered."""
    rgba = np.asarray(imread(sprite_path), dtype=np.float32)[:, :40]
    if rgba.max() > 1.0:
        rgba /= 255.0
    rgb = rgba[..., :3] * rgba[..., 3:4] + (1.0 - rgba[..., 3:4])
    canvas = np.ones((GRID, GRID, 3), dtype=np.float32)
    offset = (GRID - 40) // 2
    canvas[offset : offset + 40, offset : offset + 40] = rgb
    return canvas


def target_mse(state: np.ndarray, target: np.ndarray) -> float:
    return float(np.mean((visible_rgb(state) - target) ** 2))


def exact_branch(nca: NCA) -> NCA:
    """Branch state and future stochastic update stream exactly."""
    out = NCA.__new__(NCA)
    out.layer1 = nca.layer1
    out.layer2 = nca.layer2
    out.state = nca.state.copy()
    out.rng = np.random.default_rng()
    out.rng.bit_generator.state = copy.deepcopy(nca.rng.bit_generator.state)
    out.steps = nca.steps
    return out


def characterize_model(name: str, model_path: Path, target: np.ndarray) -> dict:
    base = NCA(model_path, size=GRID, seed=RNG_SEED)
    base.run(FORMATION_STEPS)
    formed = base.state.copy()

    undamaged = exact_branch(base)
    damaged = exact_branch(base)
    damaged.damage(GRID // 2, GRID // 2, DAMAGE_RADIUS)
    immediately_damaged = damaged.state.copy()

    undamaged.run(FOLLOW_STEPS)
    damaged.run(FOLLOW_STEPS)

    return {
        "model": name,
        "formed_target_mse": target_mse(formed, target),
        "damage_target_mse": target_mse(immediately_damaged, target),
        "undamaged_target_mse_after_follow": target_mse(undamaged.state, target),
        "damaged_target_mse_after_follow": target_mse(damaged.state, target),
        "damaged_vs_undamaged_rgb_mse_after_follow": float(
            np.mean((visible_rgb(damaged.state) - visible_rgb(undamaged.state)) ** 2)
        ),
    }


def characterize() -> dict:
    assets = ensure_assets()
    target = target_rgb(assets["emoji.png"])
    rows = [
        characterize_model(name, assets[filename], target)
        for name, filename in MODEL_FILES.items()
    ]
    return {
        "upstream": {
            "repository": MANIFEST["upstream"]["repository"],
            "commit": MANIFEST["upstream"]["commit"],
            "doi": MANIFEST["article"]["doi"],
        },
        "protocol": {
            "grid": GRID,
            "formation_steps": FORMATION_STEPS,
            "follow_steps": FOLLOW_STEPS,
            "damage": {"kind": "central_clear_circle", "radius": DAMAGE_RADIUS},
            "rng_seed": RNG_SEED,
            "matched_future_update_stream": True,
        },
        "models": rows,
    }


def main() -> None:
    result = characterize()
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
