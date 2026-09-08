from __future__ import annotations

import json
from pathlib import Path

from model import State, damage, inhibitor, repair, train_memory

TARGETS = [(6, 18), (8, 16), (10, 14)]
RETENTIONS = [1.0, 0.9995, 0.999, 0.998, 0.995]


def challenge_rows() -> list[dict]:
    rows = []
    for a, b in TARGETS:
        healthy = State(a, b)
        memory = train_memory(healthy)
        challenges = [
            ("partial", 2, 4),
            ("A_extinct", a, 0),
            ("B_extinct", 0, b),
            ("bilateral_half", max(1, a // 2), max(1, b // 2)),
        ]
        for label, remove_a, remove_b in challenges:
            start = damage(healthy, remove_a, remove_b)
            for retention in RETENTIONS:
                final, _, operations = repair(
                    start,
                    memory,
                    plastic=True,
                    retention=retention,
                )
                rows.append(
                    {
                        "target": [a, b],
                        "challenge": label,
                        "removed": [remove_a, remove_b],
                        "retention_per_birth": retention,
                        "final": [final.a, final.b],
                        "exact": (final.a, final.b) == (a, b),
                        "operations": operations,
                    }
                )
    return rows


def main() -> dict:
    rows = challenge_rows()
    retention_summary = {
        str(retention): sum(
            row["exact"]
            for row in rows
            if row["retention_per_birth"] == retention
        )
        for retention in RETENTIONS
    }

    training = []
    for a, b in TARGETS:
        memory = train_memory(State(a, b))
        training.append(
            {
                "healthy": [a, b],
                "memory": [memory.a_signal, memory.b_signal],
                "true_signals": [inhibitor(a), inhibitor(b)],
                "relative_errors": [
                    abs(memory.a_signal - inhibitor(a)) / inhibitor(a),
                    abs(memory.b_signal - inhibitor(b)) / inhibitor(b),
                ],
            }
        )

    healthy = State(8, 16)
    memory = train_memory(healthy)
    no_wound, _, no_wound_ops = repair(
        healthy,
        memory,
        secretion_a=0.0,
        max_steps=40,
    )
    wound_failure, _, wound_failure_ops = repair(
        damage(healthy, 4, 0),
        memory,
        secretion_a=0.0,
        max_steps=40,
    )
    extinction_failure, _, extinction_failure_ops = repair(
        damage(healthy, 8, 0),
        memory,
        plastic=True,
        secretion_a=0.0,
        max_steps=40,
    )

    no_plastic = []
    for a, b in TARGETS:
        healthy_target = State(a, b)
        target_memory = train_memory(healthy_target)
        for label, remove_a, remove_b in (
            ("A_extinct", a, 0),
            ("B_extinct", 0, b),
        ):
            final, _, operations = repair(
                damage(healthy_target, remove_a, remove_b),
                target_memory,
                plastic=False,
            )
            no_plastic.append(
                {
                    "target": [a, b],
                    "challenge": label,
                    "final": [final.a, final.b],
                    "exact": (final.a, final.b) == (a, b),
                    "operations": operations,
                }
            )

    return {
        "controller": {
            "memory_training_alpha": 0.2,
            "memory_training_steps": 100,
            "match_fraction": 0.99,
            "target_counts_supplied_to_repair": False,
        },
        "training": training,
        "challenge_rows": rows,
        "retention_exact_of_12": retention_summary,
        "no_plastic_extinction": no_plastic,
        "reporter_failure_controls": {
            "healthy_no_wound_A_secretion_loss": {
                "final": [no_wound.a, no_wound.b],
                "operations": no_wound_ops,
            },
            "A_partial_wound_plus_secretion_loss": {
                "final": [wound_failure.a, wound_failure.b],
                "operations": wound_failure_ops,
            },
            "A_extinction_plus_secretion_loss": {
                "final": [extinction_failure.a, extinction_failure.b],
                "operations": extinction_failure_ops,
            },
        },
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).parent / "results" / "characterization.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
