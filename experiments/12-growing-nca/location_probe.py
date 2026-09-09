"""Test whether objective lesion location predicts ex3 NCA recovery at matched immediate severity."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from fetch_upstream import MANIFEST, ensure_assets
from geometry_probe import target_axes
from nca_numpy import NCA, visible_rgb
from run import FORMATION_STEPS, GRID, RNG_SEED, target_mse, target_rgb

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "location_probe.json"
FOLLOW = 96
BASELINE_RADIUS = 16
SEVERITY_TOLERANCE = 0.05
AXIS_QUANTILE = 0.20
RADIUS_CANDIDATES = tuple(range(4, 33))
FUTURE_SEEDS = (100, 101, 102, 103)
ANNULUS_WIDTH = 3


def circle_mask(center_yx: tuple[int, int], radius: float) -> np.ndarray:
    yy, xx = np.mgrid[:GRID, :GRID]
    cy, cx = center_yx
    return np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2) < radius


def apply_mask(state: np.ndarray, m: np.ndarray) -> np.ndarray:
    out = state.copy()
    out[m, :] = 0.0
    return out


def candidate_centers(target: np.ndarray) -> tuple[dict[str, tuple[int, int]], dict]:
    foreground, centroid, axes = target_axes(target)
    coords = np.column_stack(np.nonzero(foreground)).astype(np.float64)
    centered = coords - centroid
    out: dict[str, tuple[int, int]] = {}

    nearest_centroid = coords[np.argmin(np.sum((coords - centroid) ** 2, axis=1))]
    out["centroid"] = tuple(int(v) for v in nearest_centroid)

    for i, axis in enumerate(axes, start=1):
        projection = centered @ axis
        for sign, q in (("neg", AXIS_QUANTILE), ("pos", 1.0 - AXIS_QUANTILE)):
            target_projection = float(np.quantile(projection, q))
            desired = centroid + axis * target_projection
            nearest = coords[np.argmin(np.sum((coords - desired) ** 2, axis=1))]
            out[f"pc{i}_{sign}"] = tuple(int(v) for v in nearest)

    metadata = {
        "foreground_pixel_count": int(foreground.sum()),
        "centroid_yx": centroid.tolist(),
        "principal_axes_yx": axes.tolist(),
        "axis_quantile": AXIS_QUANTILE,
    }
    return out, metadata


def annulus_support(formed: np.ndarray, center_yx: tuple[int, int], radius: float) -> dict:
    outer = circle_mask(center_yx, radius + ANNULUS_WIDTH)
    inner = circle_mask(center_yx, radius)
    annulus = outer & ~inner
    live = formed[..., 3] > 0.1
    count = int(annulus.sum())
    live_count = int(np.count_nonzero(annulus & live))
    return {
        "annulus_width": ANNULUS_WIDTH,
        "annulus_pixel_count": count,
        "annulus_live_count": live_count,
        "annulus_live_fraction": float(live_count / count) if count else 0.0,
    }


def choose_radius(
    formed: np.ndarray,
    target: np.ndarray,
    center_yx: tuple[int, int],
    baseline_mse: float,
) -> dict:
    live = formed[..., 3] > 0.1
    candidates = []
    for radius in RADIUS_CANDIDATES:
        m = circle_mask(center_yx, radius)
        immediate = target_mse(apply_mask(formed, m), target)
        rel_error = abs(immediate - baseline_mse) / baseline_mse
        candidates.append((rel_error, radius, immediate, m))
    rel_error, radius, immediate, m = min(candidates, key=lambda x: (x[0], x[1]))
    return {
        "radius": int(radius),
        "mask_pixel_count": int(m.sum()),
        "live_cells_removed": int(np.count_nonzero(m & live)),
        "immediate_target_mse": float(immediate),
        "relative_severity_error": float(rel_error),
        "within_tolerance": bool(rel_error <= SEVERITY_TOLERANCE),
        **annulus_support(formed, center_yx, radius),
    }


def branch(formed: np.ndarray, model_path: Path, future_seed: int, m: np.ndarray | None) -> NCA:
    out = NCA(model_path, size=GRID, seed=future_seed)
    out.state = formed.copy() if m is None else apply_mask(formed, m)
    out.rng = np.random.default_rng(future_seed)
    out.steps = FORMATION_STEPS
    return out


def rgb_mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((visible_rgb(a) - visible_rgb(b)) ** 2))


def characterize() -> dict:
    assets = ensure_assets()
    target = target_rgb(assets["emoji.png"])
    model_path = assets["ex3_lizard.json"]
    base = NCA(model_path, size=GRID, seed=RNG_SEED)
    base.run(FORMATION_STEPS)
    formed = base.state.copy()

    baseline_mask = circle_mask((GRID // 2, GRID // 2), BASELINE_RADIUS)
    baseline_mse = target_mse(apply_mask(formed, baseline_mask), target)
    centers, target_meta = candidate_centers(target)
    candidates = {
        name: {"center_yx": list(center), **choose_radius(formed, target, center, baseline_mse)}
        for name, center in centers.items()
    }
    matched = {name: row for name, row in candidates.items() if row["within_tolerance"]}

    if len(matched) >= 2:
        ordered = sorted(matched.items(), key=lambda kv: kv[1]["annulus_live_fraction"])
        low_name, low_row = ordered[0]
        high_name, high_row = ordered[-1]
        pair_status = "matched"
    else:
        ordered = sorted(candidates.items(), key=lambda kv: kv[1]["relative_severity_error"])
        best_two = dict(ordered[:2])
        support_ordered = sorted(best_two.items(), key=lambda kv: kv[1]["annulus_live_fraction"])
        low_name, low_row = support_ordered[0]
        high_name, high_row = support_ordered[-1]
        pair_status = "insufficient_tolerance"

    prediction = (
        f"Among severity-matched target-derived locations, {low_name} has lower intact live-cell "
        f"support in the {ANNULUS_WIDTH}-pixel annulus ({low_row['annulus_live_fraction']:.4f}) than "
        f"{high_name} ({high_row['annulus_live_fraction']:.4f}) and should therefore recover worse at 96 steps."
    )
    refuter = (
        f"If {low_name} is not worse than {high_name} in most matched future streams, reject local annulus "
        "live-cell support as a sufficient directional predictor of location-dependent recovery."
    )

    prereg = {
        "status": "preregistered_before_recovery",
        "upstream": {"repository": MANIFEST["upstream"]["repository"], "commit": MANIFEST["upstream"]["commit"]},
        "prediction": prediction,
        "refuter": refuter,
        "protocol": {
            "model": "ex3_lizard.json",
            "grid": GRID,
            "formation_steps": FORMATION_STEPS,
            "formed_state_seed": RNG_SEED,
            "follow_steps": FOLLOW,
            "baseline_center_yx": [GRID // 2, GRID // 2],
            "baseline_radius": BASELINE_RADIUS,
            "baseline_immediate_target_mse": float(baseline_mse),
            "severity_tolerance_relative": SEVERITY_TOLERANCE,
            "radius_candidates": list(RADIUS_CANDIDATES),
            "future_seeds": list(FUTURE_SEEDS),
            "matched_future_update_stream": True,
            "annulus_width": ANNULUS_WIDTH,
            "primary_pair_status": pair_status,
            "primary_pair": {"lower_support": low_name, "higher_support": high_name},
            **target_meta,
        },
        "candidate_locations": candidates,
        "replications": [],
        "summary": None,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(prereg, indent=2, sort_keys=True) + "\n")

    masks = {
        low_name: circle_mask(tuple(low_row["center_yx"]), low_row["radius"]),
        high_name: circle_mask(tuple(high_row["center_yx"]), high_row["radius"]),
    }
    replications = []
    for seed in FUTURE_SEEDS:
        none = branch(formed, model_path, seed, None)
        low = branch(formed, model_path, seed, masks[low_name])
        high = branch(formed, model_path, seed, masks[high_name])
        none.run(FOLLOW)
        low.run(FOLLOW)
        high.run(FOLLOW)
        replications.append({
            "future_seed": seed,
            "target_mse_after_96": {
                "none": target_mse(none.state, target),
                low_name: target_mse(low.state, target),
                high_name: target_mse(high.state, target),
            },
            "vs_undamaged_rgb_mse_after_96": {
                low_name: rgb_mse(low.state, none.state),
                high_name: rgb_mse(high.state, none.state),
            },
        })

    low_vals = np.array([r["target_mse_after_96"][low_name] for r in replications])
    high_vals = np.array([r["target_mse_after_96"][high_name] for r in replications])
    low_worse = int(np.count_nonzero(low_vals > high_vals))
    if low_worse >= 3 and low_vals.mean() > high_vals.mean():
        disposition = "supported"
    elif low_worse <= 1 and low_vals.mean() < high_vals.mean():
        disposition = "contradicted"
    else:
        disposition = "mixed"

    final = prereg | {
        "status": "complete",
        "replications": replications,
        "summary": {
            "disposition": disposition,
            "lower_support_location": low_name,
            "higher_support_location": high_name,
            "lower_support_worse_count": low_worse,
            "replication_count": len(replications),
            "mean_target_mse_after_96": {
                low_name: float(low_vals.mean()),
                high_name: float(high_vals.mean()),
            },
        },
    }
    RESULT.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    return final


def main() -> None:
    print(json.dumps(characterize(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
