"""Characterize endogenous size recovery, positional ambiguity, and noise limits."""
from __future__ import annotations

import json
import random
from pathlib import Path

from model import (
    TARGET_SIZE, Tissue, add_right, amputate_right, discrimination_margin,
    inhibitor, reference_tissue, relax, step,
)

HERE = Path(__file__).resolve().parent
TRIALS = 2000
WIDTHS = (1, 2, 4, 8, 12, 18)


def recovery_matrix() -> list[dict]:
    rows = []
    reference = reference_tissue()
    for challenge, maker in (("amputation", amputate_right), ("addition", add_right)):
        for width in WIDTHS:
            size_ok = exact = 0
            for seed in range(TRIALS):
                final, operations = relax(maker(width), random.Random(seed))
                size_ok += final.size == TARGET_SIZE
                exact += final == reference
            rows.append({
                "challenge": challenge,
                "width": width,
                "trials": TRIALS,
                "size_recovered": size_ok,
                "exact_reference_position": exact,
                "expected_exact_position_probability": 0.5**width,
                "operations_to_size_recovery": width,
            })
    return rows


def causal_controls() -> dict:
    amputated = amputate_right(8)
    reference_signal = inhibitor(TARGET_SIZE)
    clamped, clamped_steps = relax(
        amputated, random.Random(0), clamp_signal=reference_signal,
    )
    ablated, ablated_steps = relax(
        amputated, random.Random(0), secretion=0.0, max_steps=50,
    )
    return {
        "amputated_start_size": amputated.size,
        "target_signal_clamp": {
            "final_size": clamped.size,
            "operations": clamped_steps,
            "interpretation": "holding the pre-damage signal prevents loss-triggered regrowth",
        },
        "secretion_ablation": {
            "final_size_after_50_operations": ablated.size,
            "operations": ablated_steps,
            "interpretation": "without inhibitor production, the growth stop is lost",
        },
    }


def noise_sweep(noise_sigma: float = 0.02) -> list[dict]:
    rows = []
    for decay_length in (4.0, 6.0, 8.0, 12.0, 18.0):
        sizes = []
        for seed in range(20):
            rng = random.Random(seed)
            tissue = amputate_right(8)
            for tick in range(2000):
                tissue = step(tissue, rng, decay_length=decay_length, noise_sigma=noise_sigma)
                if tick >= 200:
                    sizes.append(tissue.size)
        rows.append({
            "decay_length": decay_length,
            "noise_sigma": noise_sigma,
            "discrimination_margin": discrimination_margin(decay_length),
            "target_fraction": sum(n == TARGET_SIZE for n in sizes) / len(sizes),
            "mean_absolute_size_error": sum(abs(n - TARGET_SIZE) for n in sizes) / len(sizes),
            "min_size": min(sizes),
            "max_size": max(sizes),
        })
    return rows


def characterize() -> dict:
    reference = reference_tissue()
    formed, formation_ops = relax(Tissue(100, 100), random.Random(0))
    return {
        "system": {
            "arena_size": 200,
            "target_size": TARGET_SIZE,
            "reference_interval": [reference.left, reference.right],
            "baseline_decay_length": 12.0,
        },
        "formation": {
            "start_size": 1,
            "final_size": formed.size,
            "final_interval": [formed.left, formed.right],
            "operations": formation_ops,
        },
        "recovery": recovery_matrix(),
        "causal_controls": causal_controls(),
        "noise_sweep": noise_sweep(),
    }


def main() -> None:
    result = characterize()
    path = HERE / "results" / "characterization.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
