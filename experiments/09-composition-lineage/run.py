from __future__ import annotations

import json
from pathlib import Path

from model import (
    TARGET,
    damage,
    oracle_lineage_repair,
    oracle_plastic_repair,
    total_only_exact_probability,
)

CASES = [
    ("left_partial", 4, 0),
    ("right_partial", 0, 8),
    ("bilateral_2_6", 2, 6),
    ("bilateral_4_4", 4, 4),
    ("bilateral_4_8", 4, 8),
    ("bilateral_7_8", 7, 8),
    ("A_extinct", 8, 0),
    ("B_extinct", 0, 16),
    ("A_extinct_plus_B_loss", 8, 4),
    ("B_extinct_plus_A_loss", 4, 16),
    ("all_cells_lost", 8, 16),
]


def row(label: str, left: int, right: int) -> dict:
    start = damage(left, right)
    lineage = oracle_lineage_repair(start)
    plastic = oracle_plastic_repair(start)
    return {
        "case": label,
        "removed_left": left,
        "removed_right": right,
        "start_counts": list(start.counts),
        "total_only_exact_probability": total_only_exact_probability(start),
        "oracle_lineage_final_counts": list(lineage.counts),
        "oracle_lineage_exact": lineage.cells == TARGET,
        "oracle_plastic_final_counts": list(plastic.counts),
        "oracle_plastic_exact": plastic.cells == TARGET,
    }


def main() -> dict:
    rows = [row(*case) for case in CASES]
    return {
        "target": {
            "A": 8,
            "B": 16,
            "criterion": "A^8 followed by B^16, modulo translation",
        },
        "rows": rows,
        "summary": {
            "partial_cases_lineage_exact": sum(r["oracle_lineage_exact"] for r in rows[:6]),
            "partial_cases": 6,
            "lineage_extinction_cases_exact": sum(
                r["oracle_lineage_exact"] for r in rows[6:10]
            ),
            "lineage_extinction_cases": 4,
            "plastic_extinction_cases_exact": sum(
                r["oracle_plastic_exact"] for r in rows[6:10]
            ),
            "plastic_extinction_cases": 4,
            "all_cells_lost_plastic_exact": rows[-1]["oracle_plastic_exact"],
        },
    }


if __name__ == "__main__":
    result = main()
    out = Path(__file__).parent / "results" / "characterization.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
