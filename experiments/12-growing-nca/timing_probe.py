"""Test whether regenerative competence depends on developmental timing in fixed ex3 NCA."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from fetch_upstream import MANIFEST, ensure_assets
from nca_numpy import NCA, visible_rgb
from run import GRID, RNG_SEED, target_mse, target_rgb

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "timing_probe.json"
CHECKPOINTS = (48, 72, 96)
LIVE_FRACTION_TO_REMOVE = 0.25
RADIUS_CANDIDATES = tuple(range(1, 33))
FOLLOW = 96
FUTURE_SEEDS = (100, 101, 102, 103)
PREDICTION = (
    "If ongoing developmental dynamics provide additional corrective routes, damage removing approximately 25% "
    "of currently live cells at steps 48 and 72 should recover at least as close to each checkpoint's matched "
    "undamaged branch as the corresponding mature step-96 damage."
)
REFUTER = (
    "If mature step-96 damage is consistently closer to its matched undamaged branch than both earlier checkpoints, "
    "reject the simple earlier-development-is-more-correctable prediction and treat competence as phase/state dependent "
    "in the opposite direction."
)


def circle_mask(radius: float) -> np.ndarray:
    yy, xx = np.mgrid[:GRID, :GRID]
    cy = cx = GRID // 2
    return np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2) < radius


def choose_mask(state: np.ndarray) -> tuple[np.ndarray, dict]:
    live = state[..., 3] > 0.1
    live_total = int(np.count_nonzero(live))
    if live_total == 0:
        raise ValueError("checkpoint has no live cells")
    candidates = []
    for radius in RADIUS_CANDIDATES:
        m = circle_mask(radius)
        removed = int(np.count_nonzero(m & live))
        fraction = removed / live_total
        candidates.append((abs(fraction - LIVE_FRACTION_TO_REMOVE), radius, fraction, removed, m))
    error, radius, fraction, removed, m = min(candidates, key=lambda x: (x[0], x[1]))
    return m, {
        "radius": int(radius),
        "mask_pixel_count": int(m.sum()),
        "live_cells_total": live_total,
        "live_cells_removed": int(removed),
        "live_fraction_removed": float(fraction),
        "fraction_target": LIVE_FRACTION_TO_REMOVE,
        "absolute_fraction_error": float(error),
    }


def apply_mask(state: np.ndarray, m: np.ndarray) -> np.ndarray:
    out = state.copy()
    out[m, :] = 0.0
    return out


def branch(state: np.ndarray, model_path: Path, checkpoint: int, future_seed: int, m: np.ndarray | None) -> NCA:
    out = NCA(model_path, size=GRID, seed=future_seed)
    out.state = state.copy() if m is None else apply_mask(state, m)
    out.rng = np.random.default_rng(future_seed)
    out.steps = checkpoint
    return out


def rgb_mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((visible_rgb(a) - visible_rgb(b)) ** 2))


def checkpoint_states(model_path: Path) -> dict[int, np.ndarray]:
    model = NCA(model_path, size=GRID, seed=RNG_SEED)
    states: dict[int, np.ndarray] = {}
    prior = 0
    for checkpoint in CHECKPOINTS:
        model.run(checkpoint - prior)
        prior = checkpoint
        states[checkpoint] = model.state.copy()
    return states


def characterize() -> dict:
    assets = ensure_assets()
    target = target_rgb(assets["emoji.png"])
    model_path = assets["ex3_lizard.json"]
    states = checkpoint_states(model_path)

    masks: dict[int, np.ndarray] = {}
    metadata: dict[str, dict] = {}
    for checkpoint, state in states.items():
        m, row = choose_mask(state)
        masks[checkpoint] = m
        damaged = apply_mask(state, m)
        metadata[str(checkpoint)] = {
            **row,
            "undamaged_target_mse_at_checkpoint": target_mse(state, target),
            "immediate_damaged_target_mse": target_mse(damaged, target),
        }

    prereg = {
        "status": "preregistered_before_recovery",
        "upstream": {"repository": MANIFEST["upstream"]["repository"], "commit": MANIFEST["upstream"]["commit"]},
        "prediction": PREDICTION,
        "refuter": REFUTER,
        "protocol": {
            "model": "ex3_lizard.json",
            "grid": GRID,
            "formation_history_seed": RNG_SEED,
            "checkpoints": list(CHECKPOINTS),
            "live_fraction_to_remove": LIVE_FRACTION_TO_REMOVE,
            "radius_candidates": list(RADIUS_CANDIDATES),
            "follow_steps": FOLLOW,
            "future_seeds": list(FUTURE_SEEDS),
            "matched_future_update_stream_within_checkpoint": True,
            "primary_metric": "damaged_vs_undamaged_rgb_mse_after_96",
        },
        "checkpoint_metadata": metadata,
        "replications": [],
        "summary": None,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(prereg, indent=2, sort_keys=True) + "\n")

    replications = []
    for seed in FUTURE_SEEDS:
        checkpoints = {}
        for checkpoint in CHECKPOINTS:
            none = branch(states[checkpoint], model_path, checkpoint, seed, None)
            damaged = branch(states[checkpoint], model_path, checkpoint, seed, masks[checkpoint])
            none.run(FOLLOW)
            damaged.run(FOLLOW)
            checkpoints[str(checkpoint)] = {
                "damaged_vs_undamaged_rgb_mse_after_96": rgb_mse(damaged.state, none.state),
                "undamaged_target_mse_after_96": target_mse(none.state, target),
                "damaged_target_mse_after_96": target_mse(damaged.state, target),
            }
        replications.append({"future_seed": seed, "checkpoints": checkpoints})

    primary = {
        checkpoint: np.array([
            r["checkpoints"][str(checkpoint)]["damaged_vs_undamaged_rgb_mse_after_96"]
            for r in replications
        ])
        for checkpoint in CHECKPOINTS
    }
    mature = primary[96]
    comparisons = {}
    supported = True
    contradicted = True
    for checkpoint in (48, 72):
        vals = primary[checkpoint]
        no_worse = int(np.count_nonzero(vals <= mature))
        worse = int(np.count_nonzero(vals > mature))
        comparisons[str(checkpoint)] = {
            "no_worse_than_96_count": no_worse,
            "worse_than_96_count": worse,
            "mean_primary_mse": float(vals.mean()),
            "mature_96_mean_primary_mse": float(mature.mean()),
        }
        supported &= no_worse >= 3 and vals.mean() <= mature.mean()
        contradicted &= worse >= 3 and vals.mean() > mature.mean()
    disposition = "supported" if supported else "contradicted" if contradicted else "mixed"

    final = prereg | {
        "status": "complete",
        "replications": replications,
        "summary": {
            "disposition": disposition,
            "mean_primary_mse_by_checkpoint": {str(k): float(v.mean()) for k, v in primary.items()},
            "earlier_vs_mature": comparisons,
            "replication_count": len(replications),
        },
    }
    RESULT.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    return final


def main() -> None:
    print(json.dumps(characterize(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
