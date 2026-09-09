"""Test whether lesion geometry shifts the fixed ex3 Growing NCA recovery boundary."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from fetch_upstream import MANIFEST, ensure_assets
from nca_numpy import NCA, visible_rgb
from run import FORMATION_STEPS, GRID, RNG_SEED, exact_branch, target_mse, target_rgb

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "geometry_probe.json"
FOLLOW_STEPS = 96
RADIUS = 16
ASPECT_RATIO = 4.0
CONFIRMATION_SEEDS = (100, 101, 102, 103)
PREDICTION = (
    "At matched removed pixel count, elongated lesions should recover better than the "
    "compact circle because a local CA has more intact boundary per removed cell from "
    "which corrective dynamics can propagate."
)
REFUTER = (
    "If both elongated orientations are consistently worse than the circle, reject the "
    "simple boundary-to-area explanation and treat shape/topological severing as "
    "load-bearing. A strong orientation split is evidence of anisotropy and must not be averaged away."
)


def circle_mask(radius: float = RADIUS) -> np.ndarray:
    yy, xx = np.mgrid[:GRID, :GRID]
    cy = cx = GRID // 2
    return np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2) < radius


def target_axes(target: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    foreground = np.max(np.abs(target - 1.0), axis=-1) > 1e-3
    yy, xx = np.nonzero(foreground)
    coords = np.column_stack([yy, xx]).astype(np.float64)
    center = coords.mean(axis=0)
    centered = coords - center
    cov = np.cov(centered, rowvar=False)
    values, vectors = np.linalg.eigh(cov)
    order = np.argsort(values)[::-1]
    axes = vectors[:, order].T
    return foreground, center, axes


def ranked_ellipse_mask(axis: np.ndarray, count: int, aspect_ratio: float = ASPECT_RATIO) -> np.ndarray:
    axis = np.asarray(axis, dtype=np.float64)
    axis = axis / np.linalg.norm(axis)
    perpendicular = np.array([-axis[1], axis[0]], dtype=np.float64)
    yy, xx = np.mgrid[:GRID, :GRID]
    coords = np.stack([yy - GRID // 2, xx - GRID // 2], axis=-1).astype(np.float64)
    along = coords @ axis
    across = coords @ perpendicular
    score = (along / aspect_ratio) ** 2 + across**2
    order = np.argsort(score.ravel(), kind="stable")
    mask = np.zeros(GRID * GRID, dtype=bool)
    mask[order[:count]] = True
    return mask.reshape(GRID, GRID)


def mask_boundary_edges(mask: np.ndarray) -> int:
    edges = 0
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        edges += int(np.count_nonzero(mask & ~np.roll(mask, shift=(dy, dx), axis=(0, 1))))
    return edges


def apply_mask(state: np.ndarray, mask: np.ndarray) -> np.ndarray:
    out = state.copy()
    out[mask, :] = 0.0
    return out


def branch_with_future_seed(formed: np.ndarray, model_path: Path, seed: int, mask: np.ndarray | None) -> NCA:
    branch = NCA(model_path, size=GRID, seed=seed)
    branch.state = formed.copy() if mask is None else apply_mask(formed, mask)
    branch.rng = np.random.default_rng(seed)
    branch.steps = FORMATION_STEPS
    return branch


def rgb_mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((visible_rgb(a) - visible_rgb(b)) ** 2))


def mask_metadata(mask: np.ndarray, formed: np.ndarray, target: np.ndarray) -> dict:
    damaged = apply_mask(formed, mask)
    live_before = formed[..., 3] > 0.1
    return {
        "pixel_count": int(mask.sum()),
        "boundary_edges_4_neighbor": mask_boundary_edges(mask),
        "live_cells_removed": int(np.count_nonzero(mask & live_before)),
        "immediate_target_mse": target_mse(damaged, target),
    }


def run_matched(branches: dict[str, NCA], target: np.ndarray) -> dict:
    for branch in branches.values():
        branch.run(FOLLOW_STEPS)
    undamaged = branches["none"].state
    return {
        name: {
            "target_mse_after_96": target_mse(branch.state, target),
            "vs_undamaged_rgb_mse_after_96": 0.0 if name == "none" else rgb_mse(branch.state, undamaged),
        }
        for name, branch in branches.items()
    }


def disposition(replications: list[dict]) -> tuple[str, dict]:
    orientation_names = ("ellipse_pc1", "ellipse_pc2")
    circle = np.array([r["outcomes"]["circle"]["target_mse_after_96"] for r in replications])
    details = {}
    supported = True
    contradicted = True
    for name in orientation_names:
        values = np.array([r["outcomes"][name]["target_mse_after_96"] for r in replications])
        better = int(np.count_nonzero(values < circle))
        worse = int(np.count_nonzero(values > circle))
        details[name] = {
            "better_than_circle_count": better,
            "worse_than_circle_count": worse,
            "mean_target_mse_after_96": float(values.mean()),
            "circle_mean_target_mse_after_96": float(circle.mean()),
        }
        supported &= better >= 3 and values.mean() < circle.mean()
        contradicted &= worse >= 3 and values.mean() > circle.mean()
    if supported:
        return "supported", details
    if contradicted:
        return "contradicted", details
    return "mixed", details


def characterize() -> dict:
    assets = ensure_assets()
    target = target_rgb(assets["emoji.png"])
    model_path = assets["ex3_lizard.json"]
    base = NCA(model_path, size=GRID, seed=RNG_SEED)
    base.run(FORMATION_STEPS)
    formed = base.state.copy()

    foreground, target_center, axes = target_axes(target)
    circle = circle_mask()
    count = int(circle.sum())
    masks = {
        "circle": circle,
        "ellipse_pc1": ranked_ellipse_mask(axes[0], count),
        "ellipse_pc2": ranked_ellipse_mask(axes[1], count),
    }
    metadata = {name: mask_metadata(mask, formed, target) for name, mask in masks.items()}

    preregistration = {
        "status": "preregistered_before_recovery",
        "upstream": {"repository": MANIFEST["upstream"]["repository"], "commit": MANIFEST["upstream"]["commit"]},
        "prediction": PREDICTION,
        "refuter": REFUTER,
        "protocol": {
            "model": "ex3_lizard.json",
            "grid": GRID,
            "formation_steps": FORMATION_STEPS,
            "formed_state_seed": RNG_SEED,
            "follow_steps": FOLLOW_STEPS,
            "circle_radius": RADIUS,
            "ellipse_aspect_ratio": ASPECT_RATIO,
            "confirmation_future_seeds": list(CONFIRMATION_SEEDS),
            "matched_future_update_stream": True,
            "target_foreground_pixel_count": int(foreground.sum()),
            "target_foreground_centroid_yx": target_center.tolist(),
            "target_principal_axes_yx": axes.tolist(),
        },
        "mask_metadata": metadata,
        "screening": None,
        "replications": [],
        "summary": None,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(preregistration, indent=2, sort_keys=True) + "\n")

    screen_branches = {"none": exact_branch(base)}
    for name, mask in masks.items():
        branch = exact_branch(base)
        branch.state = apply_mask(formed, mask)
        screen_branches[name] = branch
    screening = {"future_stream": "formed_seed_7_continuation", "outcomes": run_matched(screen_branches, target)}

    replications = []
    for seed in CONFIRMATION_SEEDS:
        branches = {"none": branch_with_future_seed(formed, model_path, seed, None)}
        for name, mask in masks.items():
            branches[name] = branch_with_future_seed(formed, model_path, seed, mask)
        replications.append({"future_seed": seed, "outcomes": run_matched(branches, target)})

    result_status, details = disposition(replications)
    final = preregistration | {
        "status": "complete",
        "screening": screening,
        "replications": replications,
        "summary": {
            "disposition": result_status,
            "orientation_comparisons": details,
        },
    }
    RESULT.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    return final


def main() -> None:
    result = characterize()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
