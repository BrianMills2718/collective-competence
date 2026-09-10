"""Test whether temporary loss of local update actions changes ex3 NCA recovery."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from fetch_upstream import MANIFEST, ensure_assets
from nca_numpy import NCA, visible_rgb
from run import FORMATION_STEPS, GRID, RNG_SEED, target_mse, target_rgb

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "action_gate_probe.json"
RADIUS = 16
FOLLOW = 96
LONG_HORIZON = 256
BLACKOUTS = (0, 16, 32, 64)
LONG_ARMS = (0, 32, 64)
FUTURE_SEEDS = (100, 101, 102, 103)
PREDICTION = (
    "With identical radius-16 damage, 96-step recovery error should worsen monotonically "
    "as updates inside the original lesion footprint are withheld for 0, 16, 32, or 64 steps."
)
REFUTER = (
    "If longer action blackouts do not produce a monotonic worsening in most matched future streams, "
    "reject blackout duration as a simple directional predictor in this regime. If 96-step differences "
    "substantially shrink after all actions are restored through step 256, interpret them primarily as "
    "time-budget/delay costs; persistent divergence motivates path-dependence analysis, not an automatic "
    "claim of formal unreachability."
)


def lesion_mask() -> np.ndarray:
    yy, xx = np.mgrid[:GRID, :GRID]
    return np.sqrt((yy - GRID // 2) ** 2 + (xx - GRID // 2) ** 2) < RADIUS


def apply_lesion(state: np.ndarray, mask: np.ndarray) -> np.ndarray:
    out = state.copy()
    out[mask, :] = 0.0
    return out


def branch(formed: np.ndarray, model_path: Path, future_seed: int, damaged: bool) -> NCA:
    out = NCA(model_path, size=GRID, seed=future_seed)
    out.state = formed.copy()
    if damaged:
        out.state = apply_lesion(out.state, lesion_mask())
    out.rng = np.random.default_rng(future_seed)
    out.steps = FORMATION_STEPS
    return out


def blackout_gate(mask: np.ndarray) -> np.ndarray:
    gate = np.ones((GRID, GRID), dtype=np.float32)
    gate[mask] = 0.0
    return gate


def run_recovery(nca: NCA, steps: int, blackout_steps: int, gate: np.ndarray) -> None:
    for recovery_step in range(steps):
        nca.step(gate if recovery_step < blackout_steps else None)


def rgb_mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((visible_rgb(a) - visible_rgb(b)) ** 2))


def characterize() -> dict:
    assets = ensure_assets()
    target = target_rgb(assets["emoji.png"])
    model_path = assets["ex3_lizard.json"]
    base = NCA(model_path, size=GRID, seed=RNG_SEED)
    base.run(FORMATION_STEPS)
    formed = base.state.copy()
    mask = lesion_mask()
    damaged_initial = apply_lesion(formed, mask)
    gate = blackout_gate(mask)

    prereg = {
        "status": "preregistered_before_recovery",
        "upstream": {
            "repository": MANIFEST["upstream"]["repository"],
            "commit": MANIFEST["upstream"]["commit"],
        },
        "prediction": PREDICTION,
        "refuter": REFUTER,
        "protocol": {
            "model": "ex3_lizard.json",
            "grid": GRID,
            "formation_steps": FORMATION_STEPS,
            "formed_state_seed": RNG_SEED,
            "lesion": {"kind": "central_clear_circle", "radius": RADIUS},
            "blackout_steps": list(BLACKOUTS),
            "primary_horizon": FOLLOW,
            "long_horizon": LONG_HORIZON,
            "long_horizon_arms": list(LONG_ARMS),
            "future_seeds": list(FUTURE_SEEDS),
            "gate_application": "after native stochastic update mask is drawn; state is not overwritten",
            "matched_future_update_stream": True,
            "primary_metrics": ["target_mse", "rgb_mse_vs_normal_damaged_branch"],
        },
        "initial_damage": {
            "lesion_pixel_count": int(mask.sum()),
            "live_cells_removed": int(np.count_nonzero(mask & (formed[..., 3] > 0.1))),
            "immediate_target_mse": target_mse(damaged_initial, target),
        },
        "replications": [],
        "summary": None,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(prereg, indent=2, sort_keys=True) + "\n")

    replications = []
    for seed in FUTURE_SEEDS:
        undamaged = branch(formed, model_path, seed, damaged=False)
        arms = {duration: branch(formed, model_path, seed, damaged=True) for duration in BLACKOUTS}
        undamaged.run(FOLLOW)
        for duration, arm in arms.items():
            run_recovery(arm, FOLLOW, duration, gate)

        normal_state_96 = arms[0].state.copy()
        row = {
            "future_seed": seed,
            "after_96": {
                "undamaged_target_mse": target_mse(undamaged.state, target),
                "arms": {
                    str(duration): {
                        "target_mse": target_mse(arm.state, target),
                        "rgb_mse_vs_normal_damaged": rgb_mse(arm.state, normal_state_96),
                        "rgb_mse_vs_undamaged": rgb_mse(arm.state, undamaged.state),
                    }
                    for duration, arm in arms.items()
                },
            },
        }

        long_normal = arms[0]
        long_selected = {duration: arms[duration] for duration in LONG_ARMS if duration != 0}
        for arm in [long_normal, *long_selected.values()]:
            arm.run(LONG_HORIZON - FOLLOW)
        normal_state_256 = long_normal.state.copy()
        row["after_256"] = {
            "arms": {
                "0": {
                    "target_mse": target_mse(long_normal.state, target),
                    "rgb_mse_vs_normal_damaged": 0.0,
                },
                **{
                    str(duration): {
                        "target_mse": target_mse(arm.state, target),
                        "rgb_mse_vs_normal_damaged": rgb_mse(arm.state, normal_state_256),
                    }
                    for duration, arm in long_selected.items()
                },
            }
        }
        replications.append(row)

    target_96 = {
        duration: np.array([
            row["after_96"]["arms"][str(duration)]["target_mse"]
            for row in replications
        ])
        for duration in BLACKOUTS
    }
    monotonic_count = sum(
        all(
            row["after_96"]["arms"][str(a)]["target_mse"]
            <= row["after_96"]["arms"][str(b)]["target_mse"]
            for a, b in zip(BLACKOUTS, BLACKOUTS[1:])
        )
        for row in replications
    )
    means_96 = {str(k): float(v.mean()) for k, v in target_96.items()}
    means_monotonic = all(means_96[str(a)] <= means_96[str(b)] for a, b in zip(BLACKOUTS, BLACKOUTS[1:]))
    disposition = "supported" if monotonic_count >= 3 and means_monotonic else "contradicted" if monotonic_count <= 1 and not means_monotonic else "mixed"

    long_summary = {}
    for duration in (32, 64):
        mse96 = np.array([
            row["after_96"]["arms"][str(duration)]["rgb_mse_vs_normal_damaged"]
            for row in replications
        ])
        mse256 = np.array([
            row["after_256"]["arms"][str(duration)]["rgb_mse_vs_normal_damaged"]
            for row in replications
        ])
        long_summary[str(duration)] = {
            "mean_rgb_mse_vs_normal_after_96": float(mse96.mean()),
            "mean_rgb_mse_vs_normal_after_256": float(mse256.mean()),
            "mean_256_to_96_ratio": float(mse256.mean() / mse96.mean()) if mse96.mean() else 0.0,
        }

    final = prereg | {
        "status": "complete",
        "replications": replications,
        "summary": {
            "disposition": disposition,
            "monotonic_target_mse_count": int(monotonic_count),
            "replication_count": len(replications),
            "mean_target_mse_after_96": means_96,
            "mean_order_is_monotonic": bool(means_monotonic),
            "post_release_divergence": long_summary,
        },
    }
    RESULT.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    return final


def main() -> None:
    print(json.dumps(characterize(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
