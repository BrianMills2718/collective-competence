"""Characterize structural regeneration and its positional-information boundary."""
from __future__ import annotations

import json
from pathlib import Path

from model import (
    TARGET, TARGET_LEFT, TARGET_RIGHT, TARGET_SIZE,
    amputate, edge_signature, grow, morphology_metrics, policy_gate, seed_state,
)

HERE = Path(__file__).resolve().parent
COMMON_AMPLITUDES = (0.75, 1.0, 1.25)
DAMAGE_KINDS = ("left", "right", "middle")
DAMAGE_WIDTHS = (4, 8, 12)
POLICIES = ("ratio", "single", "ungated")


def characterize() -> dict:
    formation = []
    for amplitude in COMMON_AMPLITUDES:
        for policy in POLICIES:
            final, births = grow(seed_state(), policy_gate(policy, amplitude, amplitude))
            formation.append({
                "common_amplitude": amplitude,
                "policy": policy,
                "births": births,
                **morphology_metrics(final),
            })

    repair = []
    for amplitude in COMMON_AMPLITUDES:
        for kind in DAMAGE_KINDS:
            for width in DAMAGE_WIDTHS:
                initial = amputate(kind, width)
                for policy in POLICIES:
                    final, births = grow(initial, policy_gate(policy, amplitude, amplitude))
                    repair.append({
                        "common_amplitude": amplitude, "kind": kind, "width": width,
                        "policy": policy, "births": births, **morphology_metrics(final),
                    })

    imbalance = []
    for right_amp in (0.5, 0.75, 1.0, 1.5, 2.0):
        final, births = grow(amputate("right", 8), policy_gate("ratio", 1.0, right_amp))
        imbalance.append({
            "left_amplitude": 1.0,
            "right_amplitude": right_amp,
            "births": births,
            **morphology_metrics(final),
        })

    ablations = []
    for left_amp, right_amp, label in (
        (1.0, 0.0, "right_source_absent"),
        (0.0, 1.0, "left_source_absent"),
    ):
        final, births = grow(amputate("right", 8), policy_gate("ratio", left_amp, right_amp))
        ablations.append({
            "condition": label,
            "births": births,
            **morphology_metrics(final),
        })

    repair_summary = {
        "declared_cases_per_policy": len(COMMON_AMPLITUDES) * len(DAMAGE_KINDS) * len(DAMAGE_WIDTHS),
        "exact_recoveries": {
            policy: sum(row["exact_target"] for row in repair if row["policy"] == policy)
            for policy in POLICIES
        },
        "ratio_births_equal_removed": all(
            row["births"] == row["width"] for row in repair if row["policy"] == "ratio"
        ),
        "examples": [
            row for row in repair
            if (row["policy"], row["common_amplitude"], row["kind"], row["width"]) in {
                ("single", 0.75, "right", 8),
                ("single", 1.25, "right", 8),
                ("ungated", 1.0, "right", 8),
            }
        ],
    }

    intact = set(TARGET)
    normal_edge = edge_signature(intact, TARGET_RIGHT)
    wound = amputate("right", 8)
    wound_edge = edge_signature(wound, TARGET_RIGHT - 8)

    return {
        "system": {
            "arena_size": 64,
            "target_left": TARGET_LEFT,
            "target_right": TARGET_RIGHT,
            "target_size": TARGET_SIZE,
            "target_sites": sorted(TARGET),
        },
        "local_edge_symmetry": {
            "normal_boundary_signature": normal_edge,
            "wound_boundary_signature": wound_edge,
            "identical": normal_edge == wound_edge,
        },
        "formation": formation,
        "repair_summary": repair_summary,
        "relative_source_imbalance": imbalance,
        "source_ablations": ablations,
    }


def main() -> None:
    result = characterize()
    path = HERE / "results" / "characterization.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
