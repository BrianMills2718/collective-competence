"""Test visible/latent consistency by shuffling intact hidden vectors in fixed ex3 NCA."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from fetch_upstream import MANIFEST, ensure_assets
from hidden_state_probe import REPLICATION_SEEDS, mask
from nca_numpy import NCA, visible_rgb
from run import FORMATION_STEPS, GRID, RNG_SEED, target_mse, target_rgb

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "hidden_shuffle_probe.json"
PRIOR_RESULT = HERE / "results" / "hidden_state_probe.json"
FOLLOW = 96
RADIUS = 16
PREDICTION = (
    "If the hidden-zero result is driven by visible/latent inconsistency rather than merely "
    "loss of hidden content, spatially shuffling intact 12-channel hidden vectors among "
    "radius-16 cells should also be damaging and should be worse than full deletion in most matched streams."
)
REFUTER = (
    "If hidden-vector shuffle is close to undamaged while hidden-zero remains damaging, weaken "
    "the visible/latent inconsistency account and investigate zeroing or loss of specific hidden content instead."
)


def apply_hidden_shuffle(state: np.ndarray, radius: int, permutation_seed: int) -> np.ndarray:
    """Preserve RGBA and the hidden-vector multiset, but destroy hidden spatial assignment."""
    out = state.copy()
    m = mask(radius)
    hidden = out[m, 4:].copy()
    permutation = np.random.default_rng(permutation_seed).permutation(len(hidden))
    out[m, 4:] = hidden[permutation]
    return out


def branch_with_future_seed(formed: np.ndarray, model_path: Path, future_seed: int, shuffled: bool) -> NCA:
    branch = NCA(model_path, size=GRID, seed=future_seed)
    branch.state = (
        apply_hidden_shuffle(formed, RADIUS, 20_000 + future_seed)
        if shuffled
        else formed.copy()
    )
    branch.rng = np.random.default_rng(future_seed)
    branch.steps = FORMATION_STEPS
    return branch


def rgb_mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((visible_rgb(a) - visible_rgb(b)) ** 2))


def load_prior_controls() -> dict[int, dict]:
    prior = json.loads(PRIOR_RESULT.read_text())
    protocol = prior["protocol"]
    expected = {
        "grid": GRID,
        "formation_steps": FORMATION_STEPS,
        "follow_steps": FOLLOW,
        "formed_state_seed": RNG_SEED,
        "replication_radius": RADIUS,
        "replication_future_seeds": list(REPLICATION_SEEDS),
    }
    for key, value in expected.items():
        if protocol.get(key) != value:
            raise ValueError(f"prior hidden-state control mismatch for {key}: {protocol.get(key)!r} != {value!r}")
    return {row["future_seed"]: row for row in prior["replications"]}


def characterize() -> dict:
    assets = ensure_assets()
    target = target_rgb(assets["emoji.png"])
    model_path = assets["ex3_lizard.json"]
    base = NCA(model_path, size=GRID, seed=RNG_SEED)
    base.run(FORMATION_STEPS)
    formed = base.state.copy()
    prior = load_prior_controls()

    m = mask(RADIUS)
    hidden_before = formed[m, 4:].copy()
    example_shuffle = apply_hidden_shuffle(formed, RADIUS, 20_000 + REPLICATION_SEEDS[0])
    hidden_after = example_shuffle[m, 4:]

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
            "follow_steps": FOLLOW,
            "radius": RADIUS,
            "future_seeds": list(REPLICATION_SEEDS),
            "permutation_seed_rule": "20000 + future_seed",
            "shuffle_unit": "whole 12-channel hidden vector within lesion mask",
            "matched_future_update_stream": True,
            "reused_control_artifact": "hidden_state_probe.json",
        },
        "invariants": {
            "masked_cell_count": int(m.sum()),
            "visible_rgba_preserved_exactly": bool(np.array_equal(example_shuffle[..., :4], formed[..., :4])),
            "hidden_vector_multiset_preserved": bool(
                np.array_equal(
                    np.sort(hidden_before.view(np.dtype((np.void, hidden_before.dtype.itemsize * hidden_before.shape[1]))).ravel()),
                    np.sort(hidden_after.copy().view(np.dtype((np.void, hidden_after.dtype.itemsize * hidden_after.shape[1]))).ravel()),
                )
            ),
        },
        "replications": [],
        "summary": None,
    }
    RESULT.write_text(json.dumps(preregistration, indent=2, sort_keys=True) + "\n")

    replications = []
    for seed in REPLICATION_SEEDS:
        none = branch_with_future_seed(formed, model_path, seed, shuffled=False)
        shuffled = branch_with_future_seed(formed, model_path, seed, shuffled=True)
        none.run(FOLLOW)
        shuffled.run(FOLLOW)

        prior_row = prior[seed]
        prior_none = prior_row["target_mse_after_96"]["none"]
        reproduced_none = target_mse(none.state, target)
        if not np.isclose(reproduced_none, prior_none, rtol=0.0, atol=1e-12):
            raise ValueError(f"reused control did not reproduce for seed {seed}: {reproduced_none} != {prior_none}")

        replications.append({
            "future_seed": seed,
            "permutation_seed": 20_000 + seed,
            "target_mse_after_96": {
                "none": reproduced_none,
                "hidden_zero": prior_row["target_mse_after_96"]["hidden_only"],
                "hidden_shuffle": target_mse(shuffled.state, target),
                "full": prior_row["target_mse_after_96"]["full"],
            },
            "vs_undamaged_rgb_mse_after_96": {
                "hidden_zero": prior_row["vs_undamaged_rgb_mse_after_96"]["hidden_only"],
                "hidden_shuffle": rgb_mse(shuffled.state, none.state),
                "full": prior_row["vs_undamaged_rgb_mse_after_96"]["full"],
            },
        })

    shuffle = np.array([r["target_mse_after_96"]["hidden_shuffle"] for r in replications])
    full = np.array([r["target_mse_after_96"]["full"] for r in replications])
    zero = np.array([r["target_mse_after_96"]["hidden_zero"] for r in replications])
    none = np.array([r["target_mse_after_96"]["none"] for r in replications])
    worse_full = int(np.count_nonzero(shuffle > full))
    damaging = int(np.count_nonzero(shuffle > none))
    if damaging >= 3 and worse_full >= 3:
        disposition = "supported"
    elif damaging <= 1:
        disposition = "contradicted"
    else:
        disposition = "mixed"

    final = preregistration | {
        "status": "complete",
        "replications": replications,
        "summary": {
            "disposition": disposition,
            "shuffle_worse_than_full_count": worse_full,
            "shuffle_worse_than_undamaged_count": damaging,
            "replication_count": len(replications),
            "mean_target_mse": {
                "none": float(none.mean()),
                "hidden_zero": float(zero.mean()),
                "hidden_shuffle": float(shuffle.mean()),
                "full": float(full.mean()),
            },
        },
    }
    RESULT.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    return final


def main() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    result = characterize()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
