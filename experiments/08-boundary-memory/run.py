"""Characterize composition of endogenous size control and boundary memory."""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

from model import TARGET_SIZE, Tissue, amputate, inhibitor, reference_tissue, relax

HERE = Path(__file__).resolve().parent
UNILATERAL_TRIALS = 2000
BILATERAL_TRIALS = 5000


def unilateral_matrix() -> list[dict]:
    reference = reference_tissue()
    rows = []
    for side in ("left", "right"):
        for width in (1, 4, 8, 12, 18):
            exact = size_ok = 0
            for seed in range(UNILATERAL_TRIALS):
                damaged = amputate(reference, **{side: width})
                final, operations = relax(damaged, random.Random(seed))
                exact += final == reference
                size_ok += final.size == TARGET_SIZE
            rows.append({
                "side": side, "width": width, "trials": UNILATERAL_TRIALS,
                "size_recovered": size_ok, "exact_reference_position": exact,
                "operations": width,
            })
    return rows


def memory_ablation() -> dict:
    reference = reference_tissue()
    exact = size_ok = 0
    for seed in range(UNILATERAL_TRIALS):
        final, _ = relax(
            amputate(reference, right=8), random.Random(seed), use_boundary_memory=False,
        )
        exact += final == reference
        size_ok += final.size == TARGET_SIZE
    return {
        "challenge": "right_amputation_width_8",
        "trials": UNILATERAL_TRIALS,
        "size_recovered": size_ok,
        "exact_reference_position": exact,
        "interpretation": "size signal intact; side information removed",
    }


def signal_controls() -> dict:
    damaged = amputate(reference_tissue(), right=8)
    clamped, clamp_ops = relax(
        damaged, random.Random(0), clamp_signal=inhibitor(TARGET_SIZE),
    )
    ablated, ablated_ops = relax(
        damaged, random.Random(0), secretion=0.0, max_steps=50,
    )
    return {
        "target_signal_clamp": {
            "final_size": clamped.size, "operations": clamp_ops,
            "left_sealed": clamped.left_sealed, "right_sealed": clamped.right_sealed,
        },
        "secretion_ablation": {
            "final_size_after_50_operations": ablated.size,
            "operations": ablated_ops,
            "interval": [ablated.left, ablated.right],
        },
    }


def bilateral_matrix() -> list[dict]:
    reference = reference_tissue()
    rows = []
    for left_width, right_width in ((2, 6), (4, 4), (4, 8), (8, 8)):
        exact = size_ok = 0
        total = left_width + right_width
        for seed in range(BILATERAL_TRIALS):
            final, _ = relax(
                amputate(reference, left=left_width, right=right_width), random.Random(seed),
            )
            exact += final == reference
            size_ok += final.size == TARGET_SIZE
        rows.append({
            "left_width": left_width,
            "right_width": right_width,
            "trials": BILATERAL_TRIALS,
            "size_recovered": size_ok,
            "exact_reference_position": exact,
            "expected_exact_probability": math.comb(total, left_width) / 2**total,
        })
    return rows


def repeated_unilateral_sequence() -> dict:
    tissue = reference_tissue()
    trace = []
    for side, width in (("right", 8), ("left", 6), ("right", 12), ("left", 4)):
        tissue = amputate(tissue, **{side: width})
        tissue, operations = relax(tissue, random.Random(1))
        trace.append({
            "side": side, "width": width, "operations": operations,
            "exact_reference_position": tissue == reference_tissue(),
            "left_sealed": tissue.left_sealed, "right_sealed": tissue.right_sealed,
        })
    return {"trace": trace, "all_exact": all(row["exact_reference_position"] for row in trace)}


def translation_control() -> list[dict]:
    rows = []
    for left in (40, 120):
        reference = Tissue(left, left + TARGET_SIZE - 1)
        for side in ("left", "right"):
            exact = 0
            for seed in range(1000):
                final, _ = relax(amputate(reference, **{side: 8}), random.Random(seed))
                exact += final == reference
            rows.append({"reference_interval": [reference.left, reference.right], "side": side, "exact": exact, "trials": 1000})
    return rows


def characterize() -> dict:
    return {
        "system": {
            "target_size": TARGET_SIZE,
            "reference_interval": [reference_tissue().left, reference_tissue().right],
            "boundary_memory": "one sealed/unsealed bit at each current tissue edge",
        },
        "unilateral": unilateral_matrix(),
        "boundary_memory_ablation": memory_ablation(),
        "size_signal_controls": signal_controls(),
        "bilateral": bilateral_matrix(),
        "repeated_unilateral": repeated_unilateral_sequence(),
        "translation_control": translation_control(),
    }


def main() -> None:
    result = characterize()
    path = HERE / "results" / "characterization.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
