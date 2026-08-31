"""Frozen discovery/evaluation stages for P10; simulator access stays here.

Run from goal-discovery with ``python -m src.experiments.candidate_relations.run
discover``; commit discovery.json before the separate ``evaluate`` command.
Research output writes are intentional artifacts; existing outputs are never
overwritten. An honest failed gate is an outcome, not an exception.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sklearn

from src.experiments.candidate_relations.proposal import (
    candidate_hash,
    fit_candidate,
    predict_pairs,
    validate_observation,
)
from src.experiments.sorting.model import Freeze, SortingWorld

LAB = Path(__file__).resolve().parents[3]
REPO = LAB.parent
PROTOCOL = LAB / "docs/hypotheses/p10_candidate_relations.md"
DEFAULT_OUTPUT = LAB / "results/p10-candidate-relations"
RELEVANT = [
    PROTOCOL,
    Path(__file__).parent,
    LAB / "src/experiments/sorting",
    LAB / "src/common/snapshots.py",
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_inputs(extra: list[Path] | None = None) -> dict[str, Any]:
    """Refuse dirty or uncommitted scientific inputs, including untracked code."""
    paths = [*RELEVANT, *(extra or [])]
    relative = [str(p.resolve().relative_to(REPO)) for p in paths]
    dirty = git("status", "--porcelain", "--untracked-files=all", "--", *relative)
    if dirty:
        raise RuntimeError(f"Commit relevant protocol, code and model before running:\n{dirty}")
    tracked = git("ls-files", "--", *relative).splitlines()
    if not PROTOCOL.is_file() or str(PROTOCOL.relative_to(REPO)) not in tracked:
        raise RuntimeError("Frozen protocol must be committed")
    for path in extra or []:
        if str(path.resolve().relative_to(REPO)) not in tracked:
            raise RuntimeError(f"Frozen artifact must be committed: {path}")
    files = [p for p in tracked if p.endswith((".py", ".md", ".json"))]
    return {
        "revision": git("rev-parse", "HEAD"),
        "utc": datetime.now(UTC).isoformat(),
        "files_sha256": {p: sha256(REPO / p) for p in files},
        "sklearn_version": sklearn.__version__,
    }


def observe(world: SortingWorld) -> dict[str, Any]:
    frame = {
        "tick": world.tick,
        "cells": [
            {"id": f"cell-{c.cell_id:03d}", "position": pos, "value": c.value}
            for pos, c in enumerate(world.cells)
        ],
    }
    validate_observation(frame)
    return frame


def trajectory(world: SortingWorld, ticks: int) -> list[dict[str, Any]]:
    frames = [observe(world)]
    for _ in range(ticks):
        world.step_tick()  # Never stop early based on privileged quiescence.
        frames.append(observe(world))
    return frames


def make_world(seed: int, size: int, order: str) -> SortingWorld:
    values = [v for v in range(size // 2) for _ in range(2)]
    random.Random(seed).shuffle(values)
    return SortingWorld.from_values(values, "bubble", order=order, seed=seed)


def positions(frame: dict[str, Any]) -> dict[str, int]:
    return {c["id"]: c["position"] for c in frame["cells"]}


def orientation(frame: dict[str, Any], pair: list[str]) -> bool:
    pos = positions(frame)
    return pos[pair[0]] < pos[pair[1]]


def sustained(frames: list[dict[str, Any]], pair: list[str], before: bool) -> bool:
    return len(frames) >= 8 and all(orientation(f, pair) == before for f in frames[-8:])


def probe(
    world: SortingWorld,
    baseline_frames: list[dict[str, Any]],
    predictions: dict[tuple[str, str], bool],
    kind: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Matched descendants of one complete snapshot, with explicit mechanism damage."""
    end = baseline_frames[-1]
    cells = sorted(end["cells"], key=lambda c: c["position"])
    if kind == "unequal":
        selected = (0, len(cells) - 1)
    else:
        selected = next(
            (
                (i, j)
                for i in range(len(cells))
                for j in range(i + 1, len(cells))
                if cells[i]["value"] == cells[j]["value"]
            ),
            None,
        )
    if selected is None:
        return {
            "eligible": False,
            "failure": "no matching pair",
            "active_recovers": False,
            "disabled_recovers": False,
            "baseline_recovers": False,
            "integrity": False,
            "value_multiset_conserved": False,
        }, {}
    i, j = selected
    pair = [cells[i]["id"], cells[j]["id"]]
    expected = predictions[tuple(pair)]
    stable = len(baseline_frames) >= 8 and all(
        positions(f) == positions(end) for f in baseline_frames[-8:]
    )
    correct = orientation(end, pair) == expected
    kind_valid = (cells[i]["value"] != cells[j]["value"]) if kind == "unequal" else True
    snapshot = world.snapshot()
    traces, branch_hashes, branch_integrity = {}, {}, {}
    multiset = sorted(c["value"] for c in end["cells"])
    identities = {c["id"] for c in end["cells"]}
    for arm in ("baseline", "active", "disabled"):
        descendant = SortingWorld.from_values([0, 0])
        descendant.restore(snapshot)
        restored_exactly = descendant.snapshot() == snapshot
        if arm != "baseline":
            descendant.cells[i], descendant.cells[j] = descendant.cells[j], descendant.cells[i]
        if arm == "disabled":
            for cell in descendant.cells:
                cell.freeze = Freeze.IMMOVABLE
        branch_snapshot = descendant.snapshot()
        branch_hashes[arm] = branch_snapshot["snapshot_id"]
        expected_cells = [dict(c) for c in snapshot["cells"]]
        if arm != "baseline":
            expected_cells[i], expected_cells[j] = expected_cells[j], expected_cells[i]
        if arm == "disabled":
            for cell in expected_cells:
                cell["freeze"] = Freeze.IMMOVABLE.value
        branch_integrity[arm] = {
            "exact_snapshot_restore": restored_exactly,
            "rng_origin_preserved": branch_snapshot["rng_state"] == snapshot["rng_state"],
            "cell_attributes_match_declared_operation": branch_snapshot["cells"] == expected_cells,
            "other_state_unchanged": all(
                branch_snapshot[k] == snapshot[k]
                for k in snapshot
                if k not in {"cells", "snapshot_id"}
            ),
        }
        traces[arm] = trajectory(descendant, 64)
    flipped = orientation(traces["active"][0], pair) != orientation(end, pair)
    eligible = stable and correct and kind_valid and flipped
    conserved = all(
        sorted(c["value"] for c in f["cells"]) == multiset
        for frames in traces.values()
        for f in frames
    )
    identity_conserved = all(
        {c["id"] for c in f["cells"]} == identities for frames in traces.values() for f in frames
    )
    integrity = (
        conserved
        and identity_conserved
        and all(all(checks.values()) for checks in branch_integrity.values())
    )
    record = {
        "eligible": eligible,
        "selected_pair": pair,
        "target_before": expected,
        "baseline_stable_last8": stable,
        "candidate_correct_before": correct,
        "displacement_flipped": flipped,
        "kind_valid": kind_valid,
        "value_multiset_conserved": conserved,
        "identity_set_conserved": identity_conserved,
        "branch_integrity": branch_integrity,
        "integrity": integrity,
        "source_snapshot_id": snapshot["snapshot_id"],
        "branch_snapshot_ids": branch_hashes,
        "rng_lineage": "All arms restored the identical complete baseline snapshot before intervention",
    }
    for arm, frames in traces.items():
        record[f"{arm}_recovers"] = eligible and integrity and sustained(frames, pair, expected)
        record[f"{arm}_orientation_last8"] = [orientation(f, pair) for f in frames[-8:]]
    demo = {
        "initial": baseline_frames[0],
        "selected_pair": pair,
        "target_before": expected,
        "traces": traces,
        "baseline_observation": end,
        "eligible": eligible,
    }
    return record, demo


def write_new(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")


def discover(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    provenance = frozen_inputs()
    episodes = []
    for seed in range(100, 112):
        frames = trajectory(make_world(seed, 12, "shuffled"), 96)
        episodes.append({"seed": seed, "initial": frames[0], "terminal": frames[-1]})
    candidate = fit_candidate(episodes)
    payload = {
        "schema_version": 1,
        "protocol": str(PROTOCOL.relative_to(REPO)),
        "provenance": provenance,
        "candidate": candidate,
        "candidate_sha256": candidate_hash(candidate),
        "summary": {"stage": "discovery", "episodes": 12, "confirmation_used": False},
        "cases": episodes,
        "demo": {},
    }
    write_new(output / "discovery.json", payload)
    return payload


def evaluate(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    model_path = output / "discovery.json"
    provenance = frozen_inputs([model_path])
    discovery = json.loads(model_path.read_text())
    candidate = discovery["candidate"]
    if candidate_hash(candidate) != discovery["candidate_sha256"]:
        raise RuntimeError("Frozen candidate content hash mismatch")
    for path, digest in discovery["provenance"]["files_sha256"].items():
        if sha256(REPO / path) != digest:
            raise RuntimeError(f"Scientific input changed after candidate discovery: {path}")
    cases, demo = [], {}
    for seed in range(1000, 1024):
        order = "index" if seed % 2 == 0 else "reverse_index"
        world = make_world(seed, 16, order)
        frames = trajectory(world, 128)
        predictions = predict_pairs(candidate, frames[0])
        expected = {(p["first"], p["second"]): p["before"] for p in predictions}
        id_map = {
            c["id"]: f"opaque-{len(frames[0]['cells']) - k:04d}"
            for k, c in enumerate(frames[0]["cells"])
        }
        relabeled = {
            "tick": frames[0]["tick"],
            "cells": [{**c, "id": id_map[c["id"]]} for c in frames[0]["cells"]],
        }
        relabeled_predictions = {
            (p["first"], p["second"]): p["before"] for p in predict_pairs(candidate, relabeled)
        }
        invariant = all(
            relabeled_predictions[(id_map[a], id_map[b])] == before
            for (a, b), before in expected.items()
        )
        terminal, initial = positions(frames[-1]), positions(frames[0])
        accuracy = sum(
            (terminal[a] < terminal[b]) == before for (a, b), before in expected.items()
        ) / len(expected)
        naive = sum(
            (terminal[a] < terminal[b]) == (initial[a] < initial[b]) for a, b in expected
        ) / len(expected)
        case = {
            "seed": seed,
            "order": order,
            "accuracy": accuracy,
            "initial_order_accuracy": naive,
            "pair_count": len(expected),
            "observation_id_relabel_invariant": invariant,
            "probes": {},
        }
        for kind in ("unequal", "equal"):
            record, display = probe(world, frames, expected, kind)
            case["probes"][kind] = record
            if seed == 1000:
                demo[kind] = display
        case["integrity"] = invariant and all(p["integrity"] for p in case["probes"].values())
        cases.append(case)
    counts = {
        kind: {
            field: sum(bool(c["probes"][kind][field]) for c in cases)
            for field in ("eligible", "active_recovers", "disabled_recovers", "baseline_recovers")
        }
        for kind in ("unequal", "equal")
    }
    predictive = sum(
        c["integrity"] and c["accuracy"] >= 0.95 and c["accuracy"] > c["initial_order_accuracy"]
        for c in cases
    )
    gates = {
        "predictive": predictive >= 20,
        "unequal_active": counts["unequal"]["active_recovers"] >= 20,
        "unequal_disabled": counts["unequal"]["disabled_recovers"] <= 4,
        "equal_not_defended": sum(
            c["probes"]["equal"]["eligible"]
            and c["probes"]["equal"]["integrity"]
            and not c["probes"]["equal"]["active_recovers"]
            for c in cases
        )
        >= 20,
        "integrity": all(c["integrity"] for c in cases),
    }
    payload = {
        "schema_version": 1,
        "protocol": str(PROTOCOL.relative_to(REPO)),
        "provenance": {
            **provenance,
            "discovery_file_sha256": sha256(model_path),
            "discovery_revision": discovery["provenance"]["revision"],
        },
        "candidate": candidate,
        "candidate_sha256": candidate_hash(candidate),
        "summary": {
            "stage": "confirmation",
            "runs": 24,
            "predictive_runs": predictive,
            "probes": counts,
            "gates": gates,
            "passed": all(gates.values()),
            "interpretation": "Endpoint prediction and selective recovery are distinct. This is bounded calibration, not unexpected-goal discovery.",
        },
        "cases": cases,
        "demo": demo,
    }
    write_new(output / "evaluation.json", payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("discover", "evaluate"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = (
        discover(args.output.resolve())
        if args.stage == "discover"
        else evaluate(args.output.resolve())
    )
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
