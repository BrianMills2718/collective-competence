from __future__ import annotations

import json
from pathlib import Path

from model import (
    A_TARGET,
    B_TARGET,
    DECAY_LENGTH,
    TARGET,
    damage,
    growth_threshold,
    inhibitor,
    repair,
)

PARTIAL_CASES = [
    ("left4", 4, 0),
    ("right8", 0, 8),
    ("bilateral_2_6", 2, 6),
    ("bilateral_4_4", 4, 4),
    ("bilateral_4_8", 4, 8),
    ("bilateral_7_8", 7, 8),
]

EXTINCTION_CASES = [
    ("A_extinct", 8, 0),
    ("B_extinct", 0, 16),
    ("A_extinct_plus_B4", 8, 4),
    ("A4_plus_B_extinct", 4, 16),
]


def row(label: str, left: int, right: int, *, plastic: bool = False, **kwargs) -> dict:
    start = damage(left, right)
    final, operations = repair(start, plastic=plastic, **kwargs)
    return {
        "case": label,
        "removed_left": left,
        "removed_right": right,
        "start_counts": list(start.counts),
        "final_counts": list(final.counts),
        "exact": final.cells == TARGET,
        "operations": operations,
    }


def main() -> dict:
    partial = [row(*case) for case in PARTIAL_CASES]
    lineage_extinction = [row(*case) for case in EXTINCTION_CASES]
    plastic_extinction = [row(*case, plastic=True) for case in EXTINCTION_CASES]

    target_a_signal = inhibitor(A_TARGET)
    target_b_signal = inhibitor(B_TARGET)
    signal_controls = {
        "A_partial_signal_clamped_high": row(
            "A_clamp",
            4,
            0,
            clamp_a=target_a_signal,
        ),
        "A_partial_secretion_removed": row(
            "A_no_secretion",
            4,
            0,
            secretion_a=0.0,
            max_steps=40,
        ),
        "A_extinct_plastic_signal_clamped_high": row(
            "A_extinct_clamp",
            8,
            0,
            plastic=True,
            clamp_a=target_a_signal,
        ),
        "A_extinct_plastic_secretion_removed": row(
            "A_extinct_no_secretion",
            8,
            0,
            plastic=True,
            secretion_a=0.0,
            max_steps=40,
        ),
    }

    empty = damage(8, 16)
    empty_final, empty_operations = repair(empty, plastic=True)

    return {
        "target": {
            "A": A_TARGET,
            "B": B_TARGET,
            "criterion": "A^8 B^16 modulo translation",
        },
        "signal": {
            "decay_length": DECAY_LENGTH,
            "A_target_signal": target_a_signal,
            "B_target_signal": target_b_signal,
            "A_growth_threshold": growth_threshold(A_TARGET),
            "B_growth_threshold": growth_threshold(B_TARGET),
        },
        "partial": partial,
        "lineage_extinction": lineage_extinction,
        "plastic_extinction": plastic_extinction,
        "signal_controls": signal_controls,
        "complete_extinction": {
            "final_counts": list(empty_final.counts),
            "operations": empty_operations,
            "exact": empty_final.cells == TARGET,
        },
        "summary": {
            "partial_exact": sum(item["exact"] for item in partial),
            "partial_cases": len(partial),
            "lineage_extinction_exact": sum(item["exact"] for item in lineage_extinction),
            "lineage_extinction_cases": len(lineage_extinction),
            "plastic_extinction_exact": sum(item["exact"] for item in plastic_extinction),
            "plastic_extinction_cases": len(plastic_extinction),
        },
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).parent / "results" / "characterization.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
