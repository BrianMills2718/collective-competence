"""Generate the smallest saved visual-evidence package for the Experiment 12 workbench.

This replays already-frozen comparisons from the pinned ex3 model. It does not
create new scientific claims, tune the model, or recompute dispositions.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from matplotlib.image import imsave

from action_gate_probe import blackout_gate, run_recovery
from fetch_upstream import MANIFEST, ensure_assets
from geometry_probe import apply_mask as apply_geometry_mask
from geometry_probe import circle_mask as geometry_circle_mask
from geometry_probe import ranked_ellipse_mask, target_axes
from hidden_shuffle_probe import apply_hidden_shuffle
from location_probe import circle_mask as location_circle_mask
from location_probe import apply_mask as apply_location_mask
from nca_numpy import NCA, visible_rgb
from run import FORMATION_STEPS, GRID, RNG_SEED, exact_branch, target_mse, target_rgb
from timing_probe import apply_mask as apply_timing_mask
from timing_probe import checkpoint_states, circle_mask as timing_circle_mask

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
OUT = RESULTS / "workbench"
SEED = 100
FOLLOW = 96


def load_result(name: str) -> dict:
    return json.loads((RESULTS / f"{name}.json").read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def branch_from_state(state: np.ndarray, model_path: Path, seed: int, steps: int) -> NCA:
    nca = NCA(model_path, size=GRID, seed=seed)
    nca.state = state.copy()
    nca.rng = np.random.default_rng(seed)
    nca.steps = steps
    return nca


def save_state(name: str, state: np.ndarray) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.png"
    imsave(path, visible_rgb(state))
    return path.name


def save_pair(prefix: str, baseline_initial: np.ndarray, intervention_initial: np.ndarray,
              baseline_final: np.ndarray, intervention_final: np.ndarray) -> dict:
    return {
        "immediate": {
            "baseline": save_state(f"{prefix}-baseline-immediate", baseline_initial),
            "intervention": save_state(f"{prefix}-intervention-immediate", intervention_initial),
        },
        "after_96": {
            "baseline": save_state(f"{prefix}-baseline-after96", baseline_final),
            "intervention": save_state(f"{prefix}-intervention-after96", intervention_final),
        },
    }


def run96(initial: np.ndarray, model_path: Path, steps: int = FORMATION_STEPS) -> np.ndarray:
    branch = branch_from_state(initial, model_path, SEED, steps)
    branch.run(FOLLOW)
    return branch.state.copy()


def assert_metric(label: str, state: np.ndarray, target: np.ndarray, expected: float) -> None:
    actual = target_mse(state, target)
    if not np.isclose(actual, expected, rtol=0.0, atol=1e-9):
        raise ValueError(f"visual replay mismatch for {label}: {actual} != {expected}")


def geometry_rows(result: dict) -> list[dict]:
    rows = []
    for rep in result["replications"]:
        row = {"seed": rep["future_seed"]}
        for arm in ("circle", "ellipse_pc1", "ellipse_pc2"):
            row[arm] = rep["outcomes"][arm]["target_mse_after_96"]
        rows.append(row)
    return rows


def location_rows(result: dict) -> list[dict]:
    low = result["summary"]["lower_support_location"]
    high = result["summary"]["higher_support_location"]
    return [
        {"seed": rep["future_seed"], high: rep["target_mse_after_96"][high],
         low: rep["target_mse_after_96"][low]}
        for rep in result["replications"]
    ]


def timing_rows(result: dict) -> list[dict]:
    return [
        {"seed": rep["future_seed"], **{
            f"t{cp}": rep["checkpoints"][cp]["damaged_vs_undamaged_rgb_mse_after_96"]
            for cp in ("48", "72", "96")
        }}
        for rep in result["replications"]
    ]


def hidden_rows(result: dict) -> list[dict]:
    return [
        {"seed": rep["future_seed"], **rep["target_mse_after_96"]}
        for rep in result["replications"]
    ]


def action_rows(result: dict) -> list[dict]:
    return [
        {"seed": rep["future_seed"], **{
            f"blackout_{duration}": rep["after_96"]["arms"][str(duration)]["target_mse"]
            for duration in (0, 16, 32, 64)
        }}
        for rep in result["replications"]
    ]


def build() -> dict:
    assets = ensure_assets()
    model_path = assets["ex3_lizard.json"]
    target = target_rgb(assets["emoji.png"])
    base = NCA(model_path, size=GRID, seed=RNG_SEED)
    base.run(FORMATION_STEPS)
    formed = base.state.copy()

    lesion = load_result("lesion_basin")
    geometry = load_result("geometry_probe")
    location = load_result("location_probe")
    timing = load_result("timing_probe")
    hidden = load_result("hidden_shuffle_probe")
    action = load_result("action_gate_probe")

    # Shared future-seed-100 radius-16 branch: G1 baseline, H2 full-deletion comparator, and A1 normal recovery.
    r16_mask = geometry_circle_mask(16)
    r16_initial = apply_geometry_mask(formed, r16_mask)
    r16_final = run96(r16_initial, model_path)

    # Lesion basin used the original formed-seed-7 RNG continuation, not the later confirmation seeds.
    basin_r16 = exact_branch(base)
    basin_r16.damage(GRID // 2, GRID // 2, 16)
    basin_r16_initial = basin_r16.state.copy()
    basin_r16.run(FOLLOW)
    basin_r16_final = basin_r16.state.copy()
    basin_r18 = exact_branch(base)
    basin_r18.damage(GRID // 2, GRID // 2, 18)
    basin_r18_initial = basin_r18.state.copy()
    basin_r18.run(FOLLOW)
    basin_r18_final = basin_r18.state.copy()

    # G1: equal-area PC1 ellipse versus radius-16 circle.
    _, _, axes = target_axes(target)
    pc1_mask = ranked_ellipse_mask(axes[0], int(r16_mask.sum()))
    pc1_initial = apply_geometry_mask(formed, pc1_mask)
    pc1_final = run96(pc1_initial, model_path)

    # H2: intact hidden vectors spatially shuffled; comparison is full deletion.
    shuffle_initial = apply_hidden_shuffle(formed, 16, 20_000 + SEED)
    shuffle_final = run96(shuffle_initial, model_path)

    # L1: exact committed target-derived centers/radii.
    loc_rows = location["candidate_locations"]
    centroid_meta = loc_rows["centroid"]
    low_name = location["summary"]["lower_support_location"]
    low_meta = loc_rows[low_name]
    centroid_mask = location_circle_mask(tuple(centroid_meta["center_yx"]), centroid_meta["radius"])
    low_mask = location_circle_mask(tuple(low_meta["center_yx"]), low_meta["radius"])
    centroid_initial = apply_location_mask(formed, centroid_mask)
    low_initial = apply_location_mask(formed, low_mask)
    centroid_final = run96(centroid_initial, model_path)
    low_final = run96(low_initial, model_path)

    # T1 representative: step-48 damaged branch against its same-checkpoint control.
    states = checkpoint_states(model_path)
    t48_state = states[48]
    t48_radius = timing["checkpoint_metadata"]["48"]["radius"]
    t48_damaged_initial = apply_timing_mask(t48_state, timing_circle_mask(t48_radius))
    t48_control_final = run96(t48_state, model_path, steps=48)
    t48_damaged_final = run96(t48_damaged_initial, model_path, steps=48)

    # A1 representative: same r16 damage, updates withheld in the original footprint for 64 steps.
    blackout64 = branch_from_state(r16_initial, model_path, SEED, FORMATION_STEPS)
    run_recovery(blackout64, FOLLOW, 64, blackout_gate(r16_mask))
    blackout64_final = blackout64.state.copy()

    target_file = "authored-target-reference.png"
    OUT.mkdir(parents=True, exist_ok=True)
    imsave(OUT / target_file, target)

    # Fail if any replayed morphology is not the exact branch represented by its frozen artifact.
    basin_rows = {row["radius"]: row for row in lesion["fixed_horizon"] if row["model"] == "regenerating"}
    assert_metric("basin r16", basin_r16_final, target, basin_rows[16]["target_mse_after_96"])
    assert_metric("basin r18", basin_r18_final, target, basin_rows[18]["target_mse_after_96"])
    g1_100 = next(row for row in geometry["replications"] if row["future_seed"] == SEED)
    assert_metric("G1 circle", r16_final, target, g1_100["outcomes"]["circle"]["target_mse_after_96"])
    assert_metric("G1 PC1", pc1_final, target, g1_100["outcomes"]["ellipse_pc1"]["target_mse_after_96"])
    h2_100 = next(row for row in hidden["replications"] if row["future_seed"] == SEED)
    assert_metric("H2 full", r16_final, target, h2_100["target_mse_after_96"]["full"])
    assert_metric("H2 shuffle", shuffle_final, target, h2_100["target_mse_after_96"]["hidden_shuffle"])
    l1_100 = next(row for row in location["replications"] if row["future_seed"] == SEED)
    assert_metric("L1 centroid", centroid_final, target, l1_100["target_mse_after_96"]["centroid"])
    assert_metric("L1 lower support", low_final, target, l1_100["target_mse_after_96"][low_name])
    t1_100 = next(row for row in timing["replications"] if row["future_seed"] == SEED)["checkpoints"]["48"]
    assert_metric("T1 control", t48_control_final, target, t1_100["undamaged_target_mse_after_96"])
    assert_metric("T1 damage", t48_damaged_final, target, t1_100["damaged_target_mse_after_96"])
    a1_100 = next(row for row in action["replications"] if row["future_seed"] == SEED)["after_96"]["arms"]
    assert_metric("A1 normal", r16_final, target, a1_100["0"]["target_mse"])
    assert_metric("A1 blackout64", blackout64_final, target, a1_100["64"]["target_mse"])

    source_names = [
        "lesion_basin.json", "geometry_probe.json", "location_probe.json",
        "timing_probe.json", "hidden_shuffle_probe.json", "action_gate_probe.json",
    ]
    manifest = {
        "schema_version": 1,
        "evidence_mode": "saved replay for owner review; no new scientific inference",
        "representative_seed": SEED,
        "upstream": MANIFEST["upstream"],
        "target_reference": target_file,
        "source_hashes": {name: sha256(RESULTS / name) for name in source_names},
        "default_family": "h2",
        "families": [
            {
                "id": "basin", "label": "Lesion basin", "prospective": False,
                "artifact": "lesion_basin.json", "disposition": "descriptive baseline",
                "prediction": "Calibration map: characterize the tested central-lesion recovery boundary.",
                "refuter": "Not a directional preregistration; interpret only within the tested radii, state, geometry, and stochastic stream.",
                "changed": "Increase a central circular lesion from radius 16 to radius 18.",
                "observed": "Radius 16 returns to the low-error regime; radius 18 stalls at substantially higher error.",
                "warranted": "Recovery has a finite tested basin for this central-circle challenge family.",
                "not_established": "A universal maximum lesion size.",
                "baseline_label": "radius 16 · repairing", "intervention_label": "radius 18 · stalled",
                "visual_stream": "formed seed 7 continuation",
                "match_note": "Same formed state and native seed-7 continuation stream; challenge amount differs by design.",
                "visual": save_pair("basin", basin_r16_initial, basin_r18_initial, basin_r16_final, basin_r18_final),
                "plot": {"kind": "line", "title": "Central lesion response", "x_label": "lesion radius",
                         "y_label": "target MSE after 96", "points": [
                    {"x": row["radius"], "y": row["target_mse_after_96"]}
                    for row in lesion["fixed_horizon"] if row["model"] == "regenerating"
                ]},
                "replications": [
                    {"radius": row["radius"], "target_mse_after_96": row["target_mse_after_96"],
                     "vs_undamaged_rgb_mse": row["damaged_vs_undamaged_rgb_mse_after_96"]}
                    for row in lesion["fixed_horizon"] if row["model"] == "regenerating"
                ],
            },
            {
                "id": "g1", "label": "G1 · Geometry", "prospective": True,
                "artifact": "geometry_probe.json", "disposition": geometry["summary"]["disposition"],
                "prediction": geometry["prediction"], "refuter": geometry["refuter"],
                "changed": "Replace the 793-pixel radius-16 circle with an equal-area 4:1 ellipse aligned to target PC1.",
                "observed": "The PC1 ellipse is worse than the circle in 4/4 confirmation streams despite closely matched immediate severity.",
                "warranted": "Geometry/orientation can move the recovery boundary beyond lesion pixel count; exposed boundary length alone is insufficient.",
                "not_established": "Pure anatomical anisotropy or a universal shape law.",
                "baseline_label": "circle · r16", "intervention_label": "PC1 ellipse · 4:1",
                "visual_stream": "future seed 100",
                "match_note": "Equal 793-pixel masks; immediate target error and live-cell removal are closely matched.",
                "visual": save_pair("g1", r16_initial, pc1_initial, r16_final, pc1_final),
                "plot": {"kind": "bar", "title": "Mean target error by geometry", "x_label": "geometry",
                         "y_label": "mean target MSE after 96", "points": [
                    {"x": "circle", "y": geometry["summary"]["orientation_comparisons"]["ellipse_pc1"]["circle_mean_target_mse_after_96"]},
                    {"x": "PC1 ellipse", "y": geometry["summary"]["orientation_comparisons"]["ellipse_pc1"]["mean_target_mse_after_96"]},
                    {"x": "PC2 ellipse", "y": geometry["summary"]["orientation_comparisons"]["ellipse_pc2"]["mean_target_mse_after_96"]},
                ]}, "replications": geometry_rows(geometry),
            },
            {
                "id": "l1", "label": "L1 · Location / support", "prospective": True,
                "artifact": "location_probe.json", "disposition": location["summary"]["disposition"],
                "prediction": location["prediction"], "refuter": location["refuter"],
                "changed": "Move the lesion from the target-derived centroid to the preregistered lower-annulus-support PC1-negative location while matching immediate target error.",
                "observed": "The lower-support location is worse in 4/4 future streams (mean target MSE 0.00477 vs 0.00299).",
                "warranted": "Where damage occurs and local intact-cell support can matter for recovery in this specimen.",
                "not_established": "A universal annulus-support law or a geometry-free pure location effect.",
                "baseline_label": "centroid · higher support", "intervention_label": f"{low_name} · lower support",
                "visual_stream": "future seed 100",
                "match_note": "Immediate target error is matched within 5%; radii/areas differ, so geometry remains a caveat.",
                "visual": save_pair("l1", centroid_initial, low_initial, centroid_final, low_final),
                "plot": {"kind": "bar", "title": "Matched-severity location outcome", "x_label": "location",
                         "y_label": "mean target MSE after 96", "points": [
                    {"x": "centroid", "y": location["summary"]["mean_target_mse_after_96"]["centroid"]},
                    {"x": low_name, "y": location["summary"]["mean_target_mse_after_96"][low_name]},
                ]}, "replications": location_rows(location),
            },
            {
                "id": "t1", "label": "T1 · Developmental timing", "prospective": True,
                "artifact": "timing_probe.json", "disposition": timing["summary"]["disposition"],
                "prediction": timing["prediction"], "refuter": timing["refuter"],
                "changed": "Apply the same radius-8 challenge at developmental step 48 rather than only after the mature step-96 state.",
                "observed": "Step 48 is farther from its same-checkpoint control than step 96 in 4/4 streams; step 72 is mixed.",
                "warranted": "Regenerative performance depends on developmental state/timing.",
                "not_established": "A monotonic younger-is-more-plastic rule or an isolated hidden-history effect.",
                "baseline_label": "step 48 · undamaged control", "intervention_label": "step 48 · radius-8 damage",
                "visual_stream": "future seed 100",
                "match_note": "Visual pair is same checkpoint/state history; cross-checkpoint summary uses the same radius-8 geometry and ~25% live-cell burden.",
                "visual": save_pair("t1", t48_state, t48_damaged_initial, t48_control_final, t48_damaged_final),
                "plot": {"kind": "line", "title": "Damage/control divergence by checkpoint", "x_label": "developmental checkpoint",
                         "y_label": "mean RGB MSE vs matched control after 96", "points": [
                    {"x": int(cp), "y": value}
                    for cp, value in timing["summary"]["mean_primary_mse_by_checkpoint"].items()
                ]}, "replications": timing_rows(timing),
            },
            {
                "id": "h2", "label": "H2 · Latent consistency", "prospective": True,
                "artifact": "hidden_shuffle_probe.json", "disposition": hidden["summary"]["disposition"],
                "prediction": hidden["prediction"], "refuter": hidden["refuter"],
                "changed": "Preserve visible RGBA and the full multiset of 12-channel hidden vectors, but spatially reassign those hidden vectors inside the radius-16 region.",
                "observed": "Hidden-vector shuffle is worse than full deletion in 4/4 streams (mean target MSE 0.06216 vs 0.00316).",
                "warranted": "Visible/latent spatial compatibility is causally load-bearing, not merely the presence of hidden values.",
                "not_established": "Memory, a semantic goal, or an explicit target map in the hidden channels.",
                "baseline_label": "full local deletion", "intervention_label": "hidden-vector shuffle",
                "visual_stream": "future seed 100",
                "match_note": "Same formed state and future update stream; shuffle preserves visible RGBA and the hidden-vector multiset.",
                "visual": save_pair("h2", r16_initial, shuffle_initial, r16_final, shuffle_final),
                "plot": {"kind": "bar", "title": "Latent-state intervention outcome", "x_label": "intervention",
                         "y_label": "mean target MSE after 96", "points": [
                    {"x": key.replace("_", " "), "y": value}
                    for key, value in hidden["summary"]["mean_target_mse"].items()
                ]}, "replications": hidden_rows(hidden),
            },
            {
                "id": "a1", "label": "A1 · Action availability", "prospective": True,
                "artifact": "action_gate_probe.json", "disposition": action["summary"]["disposition"],
                "prediction": action["prediction"], "refuter": action["refuter"],
                "changed": "Begin from identical radius-16 damage, then suppress updates only inside the original lesion footprint for the first 64 recovery steps.",
                "observed": "Every blackout hurts; 64 steps is clearly worst. The strict 0<16<32<64 dose ordering is mixed, and divergence persists after release through +256.",
                "warranted": "Timely local action availability is load-bearing; temporary restriction can leave persistent path-dependent consequences over the tested horizon.",
                "not_established": "Formal unreachability or a theorem about all longer futures.",
                "baseline_label": "normal damaged recovery", "intervention_label": "64-step update blackout",
                "visual_stream": "future seed 100",
                "match_note": "Initial damaged state and future RNG are identical; the gate changes action availability without overwriting state.",
                "visual": save_pair("a1", r16_initial, r16_initial, r16_final, blackout64_final),
                "plot": {"kind": "line", "title": "Recovery versus action blackout", "x_label": "blackout steps",
                         "y_label": "mean target MSE after 96", "points": [
                    {"x": int(duration), "y": value}
                    for duration, value in action["summary"]["mean_target_mse_after_96"].items()
                ]}, "replications": action_rows(action),
            },
        ],
    }
    path = OUT / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    built = build()
    print(json.dumps({"families": [x["id"] for x in built["families"]], "out": str(OUT)}, indent=2))
