"""Compute the single frozen P7-005 degree-versus-random causal contrast."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.experiments.prospective_network_selector.analyze import ARM_FILES
from src.experiments.prospective_network_selector.data import (
    load_dataset,
    parse_nodes,
    read_behaviorspace,
    validate_matched_preintervention,
)

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "results" / "p7-002-network-level2"
OUTPUT = ROOT / "results" / "p7-005-network-intervention-value"
PROTOCOL = ROOT / "docs" / "plans" / "p7_005_network_intervention_value_preregistration.md"
RUNS = tuple(range(1, 9)) + tuple(range(14, 22))
SPLITS = {run: "discovery" if run <= 8 else "confirmation" for run in RUNS}
INTERVENTION_ARMS = {
    "random-10": ("random", 10),
    "degree-10": ("degree", 10),
    "random-20": ("random", 20),
    "degree-20": ("degree", 20),
}


def _complete_infected(group: pd.DataFrame) -> np.ndarray:
    ordered = group.sort_values("tick").set_index("tick")["infected"]
    if ordered.index.min() != 0 or ordered.index.max() > 100:
        raise ValueError("trajectory has an invalid horizon")
    missing = sorted(set(range(101)) - set(ordered.index))
    if missing and (int(ordered.iloc[-1]) != 0 or min(missing) <= int(ordered.index.max())):
        raise ValueError("trajectory is incomplete before extinction")
    return ordered.reindex(range(101), fill_value=0).to_numpy(dtype=int)


def build_arm_summary(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for arm, frame in frames.items():
        for run, group in frame.groupby("seed_index"):
            if int(run) not in RUNS:
                continue
            infected = _complete_infected(group)
            rows.append(
                {
                    "arm": arm,
                    "run": int(run),
                    "seed": 10000 + int(run),
                    "split": SPLITS[int(run)],
                    "burden": int(infected[21:101].sum()),
                    "endpoint_infected": int(infected[100]),
                    "extinct": bool(infected[100] == 0),
                }
            )
    return pd.DataFrame(rows)


def build_pairs(arms: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for budget in (10, 20):
        random = arms.loc[arms["arm"] == f"random-{budget}"].set_index("run")
        degree = arms.loc[arms["arm"] == f"degree-{budget}"].set_index("run")
        for run in RUNS:
            random_row = random.loc[run]
            degree_row = degree.loc[run]
            rows.append(
                {
                    "run": run,
                    "seed": 10000 + run,
                    "split": SPLITS[run],
                    "budget": budget,
                    "random_burden": int(random_row["burden"]),
                    "degree_burden": int(degree_row["burden"]),
                    "paired_effect": int(random_row["burden"] - degree_row["burden"]),
                    "random_endpoint_infected": int(random_row["endpoint_infected"]),
                    "degree_endpoint_infected": int(degree_row["endpoint_infected"]),
                    "random_extinct": bool(random_row["extinct"]),
                    "degree_extinct": bool(degree_row["extinct"]),
                }
            )
    return pd.DataFrame(rows)


def evaluate(pairs: pd.DataFrame, integrity_gates: dict[str, bool]) -> dict[str, Any]:
    integrity_gates = {name: bool(value) for name, value in integrity_gates.items()}
    pooled_random = float(pairs["random_burden"].mean())
    pooled_degree = float(pairs["degree_burden"].mean())
    pooled_reduction = (pooled_random - pooled_degree) / pooled_random if pooled_random else 0.0
    wins = {
        str(budget): int((pairs.loc[pairs["budget"] == budget, "paired_effect"] > 0).sum())
        for budget in (10, 20)
    }
    split_effects = {
        f"{split}_{budget}": float(
            pairs.loc[
                (pairs["split"] == split) & (pairs["budget"] == budget), "paired_effect"
            ].mean()
        )
        for split in ("discovery", "confirmation")
        for budget in (10, 20)
    }
    integrity_pass = all(integrity_gates.values())
    causal_pass = bool(
        pooled_reduction >= 0.15
        and all(value >= 11 for value in wins.values())
        and all(value > 0 for value in split_effects.values())
    )
    decision = (
        "integrity-stop"
        if not integrity_pass
        else "measured-retrospective-pass"
        if causal_pass
        else "evidence-closed-no-go"
    )
    secondary = {
        f"{policy}_{budget}_extinction_rate": float(
            pairs.loc[pairs["budget"] == budget, f"{policy}_extinct"].mean()
        )
        for policy in ("random", "degree")
        for budget in (10, 20)
    }
    return {
        "decision": decision,
        "integrity_pass": integrity_pass,
        "integrity_gates": integrity_gates,
        "causal_gate": causal_pass,
        "pooled_random_mean_burden": pooled_random,
        "pooled_degree_mean_burden": pooled_degree,
        "pooled_reduction_fraction": pooled_reduction,
        "degree_seed_wins": wins,
        "mean_paired_effects": split_effects,
        "secondary": secondary,
    }


def _integrity(
    frames: dict[str, pd.DataFrame], pairs: pd.DataFrame, source_metadata: dict[str, Any]
) -> dict[str, bool]:
    dataset = load_dataset(SOURCE, ARM_FILES, run_indices=list(RUNS), snapshot_stride=20)
    validate_matched_preintervention(dataset)
    exact_rows = len(pairs) == 32 and pairs.groupby(["run", "budget"]).size().eq(1).all()
    complete_or_extinct = True
    node_count = True
    for frame in frames.values():
        for run, group in frame.loc[frame["seed_index"].isin(RUNS)].groupby("seed_index"):
            try:
                _complete_infected(group)
            except ValueError:
                complete_or_extinct = False
            tick_20 = group.loc[group["tick"] == 20]
            if len(tick_20) != 1 or len(parse_nodes(str(tick_20.iloc[0]["node_state"]))) != 150:
                node_count = False
    setup = ROOT / source_metadata["behaviorspace_setup"]
    policy_text = setup.read_text(encoding="utf-8")
    fixed_actions = all(
        token in policy_text
        for token in (
            "ask n-of 15 turtles",
            "max-n-of 15 turtles [count link-neighbors]",
            "ask n-of 30 turtles",
            "max-n-of 30 turtles [count link-neighbors]",
        )
    )
    hashes = bool(
        hashlib.sha256(setup.read_bytes()).hexdigest()
        == source_metadata["behaviorspace_setup_sha256"]
        and hashlib.sha256(Path(source_metadata["source_model"]).read_bytes()).hexdigest()
        == source_metadata["source_model_sha256"]
    )
    return {
        "exactly_16_seeds_and_four_intervention_rows": exact_rows,
        "matched_through_tick_20": True,
        "complete_or_extinct_trajectories": complete_or_extinct,
        "node_count_150": node_count,
        "fixed_15_and_30_node_public_actions": fixed_actions,
        "both_budgets_have_16_pairs": bool(pairs.groupby("budget").size().eq(16).all()),
        "stored_source_and_setup_hashes_match": hashes,
    }


def analyze(source: Path = SOURCE, output: Path = OUTPUT) -> dict[str, Any]:
    if source.resolve() != SOURCE.resolve():
        raise ValueError("P7-005 may analyze only the frozen P7-002 result directory")
    if (output / "summary.json").exists():
        raise FileExistsError("P7-005 is already finalized; the frozen contrast may run only once")
    run_summary = json.loads((source / "run_summary.json").read_text(encoding="utf-8"))
    source_metadata = run_summary["metadata"]
    frames = {arm: read_behaviorspace(source / filename, arm) for arm, filename in ARM_FILES.items()}
    arm_summary = build_arm_summary(frames)
    pairs = build_pairs(arm_summary)
    gates = _integrity(frames, pairs, source_metadata)
    summary = evaluate(pairs, gates)
    output.mkdir(parents=True, exist_ok=True)
    arm_summary.to_csv(output / "arm_outcomes.csv", index=False)
    pairs.to_csv(output / "paired_effects.csv", index=False)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    metadata = {
        "experiment_id": "P7-005",
        "evidence_level": 1,
        "retrospective": True,
        "source": str(source.relative_to(ROOT)),
        "source_run_summary_sha256": hashlib.sha256(
            (source / "run_summary.json").read_bytes()
        ).hexdigest(),
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "new_netlogo_outcomes_generated": False,
        "analysis_recovery": "A JSON bool normalization fixed finalization after the frozen paired tables were written; no source trajectory, contrast, outcome, or gate changed.",
        "decision": summary["decision"],
    }
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (output / "result.md").write_text(_result_markdown(summary), encoding="utf-8")
    return summary


def _result_markdown(summary: dict[str, Any]) -> str:
    gates = "\n".join(
        f"- {name}: {'PASS' if value else 'FAIL'}"
        for name, value in summary["integrity_gates"].items()
    )
    effects = "\n".join(
        f"| {key} | {value:.3f} |" for key, value in summary["mean_paired_effects"].items()
    )
    return f"""# P7-005 network-informed intervention value — results

**Decision: {summary['decision']}.**

## Integrity

{gates}

## Frozen causal gate

- Random mean burden: {summary['pooled_random_mean_burden']:.3f}
- Degree mean burden: {summary['pooled_degree_mean_burden']:.3f}
- Pooled reduction: {summary['pooled_reduction_fraction']:.1%}
- Degree wins at 10%: {summary['degree_seed_wins']['10']}/16
- Degree wins at 20%: {summary['degree_seed_wins']['20']}/16
- Gate: {'PASS' if summary['causal_gate'] else 'FAIL'}

| Split and budget | Mean random-minus-degree burden |
|---|---:|
{effects}

This is retrospective Level 1 evidence on already-open P7-002 trajectories. It
cannot rescue the representation selector or establish prospective/general
control value.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    print(json.dumps(analyze(output=args.output), indent=2))


if __name__ == "__main__":
    main()
