"""Three-stage P13 runner: discover, freeze probes, then reveal outcomes.

Each stage refuses overwrite. ``plan`` requires the candidate file to match the
current Git revision; ``evaluate`` applies the same rule to the frozen probes.
This makes the prospective chronology executable rather than conventional prose.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import random
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from src.experiments.bowl.model import BowlWorld
from src.experiments.vector_dynamics.model import discover, predict, state_vector

DISCOVERY_SEEDS = tuple(range(6100, 6108))
EVALUATION_SEEDS = tuple(range(6200, 6208))
CONDITIONS = ("none", "displace", "kick", "freeze")
N_COORDINATES = 8
SPREAD = 10.0
PREFIX_TICK = 40
FINAL_TICK = 400
FINAL_WINDOW = 32
RESULT_DIRECTORY = Path("results/p13-vector-dynamics")
PROTOCOL = Path("docs/hypotheses/p13_vector_dynamics.md")
SCIENTIFIC_INPUT_SCOPES = (
    "goal-discovery/docs/hypotheses/p13_vector_dynamics.md",
    "goal-discovery/src/experiments/vector_dynamics",
    "goal-discovery/src/experiments/bowl",
)


def observe(world: BowlWorld, run_id: str) -> dict[str, Any]:
    """The entire learner-visible boundary; IDs carry no simulator meaning."""

    return {
        "tick": world.tick,
        "run_id": run_id,
        "coordinates": [
            {"id": f"c{coordinate.coord_id:03d}", "x": coordinate.x, "v": coordinate.v}
            for coordinate in world.coords
        ],
    }


def _episode(seed: int, last_tick: int, run_id: str) -> tuple[BowlWorld, list[dict[str, Any]]]:
    world = BowlWorld.from_seed(N_COORDINATES, seed, spread=SPREAD)
    frames = [observe(world, run_id)]
    while world.tick < last_tick:
        world.step_tick()
        frames.append(observe(world, run_id))
    return world, frames


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def _write_jsonl_new(path: Path, frames: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        for frame in frames:
            handle.write(json.dumps(frame, separators=(",", ":"), allow_nan=False) + "\n")


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=_repository_root(), check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def _revision() -> str:
    return _git("rev-parse", "HEAD")


def _require_revision_ancestor(revision: str) -> None:
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise RuntimeError("Scientific lineage has an invalid source revision")
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", revision, "HEAD"],
        cwd=_repository_root(),
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        raise RuntimeError(f"Scientific source revision {revision} is not an ancestor of HEAD")


def _tracked_scientific_inputs() -> list[str]:
    paths = _git("ls-files", "--", *SCIENTIFIC_INPUT_SCOPES).splitlines()
    if not paths:
        raise RuntimeError("P13 scientific input scopes contain no tracked files")
    return sorted(paths)


def _require_clean_scientific_inputs() -> None:
    status = _git(
        "status", "--porcelain=v1", "--untracked-files=all", "--", *SCIENTIFIC_INPUT_SCOPES
    )
    if status:
        raise RuntimeError(f"P13 scientific inputs must be clean before execution:\n{status}")


def _committed_bytes(revision: str, relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{relative}"],
        cwd=_repository_root(),
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        raise RuntimeError(f"Scientific input {relative} is absent at revision {revision}")
    return completed.stdout


def _capture_scientific_lineage() -> dict[str, Any]:
    """Freeze every tracked simulator/learner/runner/protocol input before execution."""

    _require_clean_scientific_inputs()
    revision = _revision()
    return {
        "source_revision": revision,
        "scopes": list(SCIENTIFIC_INPUT_SCOPES),
        "files": {
            relative: _sha(_committed_bytes(revision, relative))
            for relative in _tracked_scientific_inputs()
        },
    }


def _verify_scientific_lineage(lineage: object) -> None:
    """Fail closed unless frozen P13 scientific inputs still match byte-for-byte."""

    if not isinstance(lineage, dict):
        raise TypeError("P13 scientific lineage must be an object")
    if lineage.get("scopes") != list(SCIENTIFIC_INPUT_SCOPES):
        raise RuntimeError("P13 scientific lineage scopes do not match the frozen contract")
    revision = lineage.get("source_revision")
    _require_revision_ancestor(revision)
    _require_clean_scientific_inputs()
    recorded = lineage.get("files")
    if not isinstance(recorded, dict) or sorted(recorded) != _tracked_scientific_inputs():
        raise RuntimeError("P13 scientific lineage file set changed across stages")
    for relative, expected_sha in recorded.items():
        committed = _committed_bytes(revision, relative)
        working = (_repository_root() / relative).read_bytes()
        if _sha(committed) != expected_sha or _sha(working) != expected_sha:
            raise RuntimeError(f"P13 scientific input changed across stages: {relative}")


def _require_committed(path: Path) -> str:
    absolute = path.resolve()
    relative = absolute.relative_to(_repository_root()).as_posix()
    committed = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=_repository_root(),
        check=False,
        capture_output=True,
    )
    if committed.returncode or committed.stdout != absolute.read_bytes():
        raise RuntimeError(f"{relative} must exactly match the current committed revision")
    return _sha(committed.stdout)


def discover_stage(directory: Path = RESULT_DIRECTORY) -> dict[str, Any]:
    lineage = _capture_scientific_lineage()
    episodes: list[list[dict[str, Any]]] = []
    all_frames: list[dict[str, Any]] = []
    for seed in DISCOVERY_SEEDS:
        _, frames = _episode(seed, PREFIX_TICK, f"discovery-{seed}")
        episodes.append(frames)
        all_frames.extend(frames)
    discovery_path = directory / "discovery.jsonl"
    _write_jsonl_new(discovery_path, all_frames)
    raw_sha = _sha(discovery_path.read_bytes())
    result = discover(episodes)
    if result["status"] != "stable_fixed_relation":
        raise RuntimeError(f"P13 abstained before challenges: {result['reason']}")
    candidate = {
        "schema_version": 1,
        "experiment": "P13",
        "stage": "candidate_frozen_before_evaluation",
        "source_revision": lineage["source_revision"],
        "scientific_inputs": lineage,
        "protocol": str(PROTOCOL),
        "discovery_observations": {
            "path": discovery_path.name,
            "sha256": raw_sha,
            "runs": len(episodes),
            "frames": len(all_frames),
            "allowed_fields": ["tick", "run_id", "coordinates[id,x,v]"],
        },
        "proposal": result,
        "limitations": [
            "candidate grammar and observables were supplied",
            "this is a passive-system calibration, not evidence of agency",
            "challenge outcomes have not been observed at this stage",
        ],
    }
    _write_new(directory / "candidate.json", _json_bytes(candidate))
    return candidate


def _apply_challenge(
    world: BowlWorld, condition: str, intervention_seed: int, fixed_point: list[float]
) -> list[str]:
    """Evaluator-only operation; target identities never enter the learner."""

    rng = random.Random(intervention_seed)
    if condition == "none":
        return []
    if condition in {"displace", "kick"}:
        selected = rng.sample(range(len(world.coords)), 2)
        for index in selected:
            sign = rng.choice((-1.0, 1.0))
            if condition == "displace":
                world.coords[index].x += sign * 6.0
            else:
                world.coords[index].v += sign * 2.0
        return [f"c{index:03d}" for index in selected]
    if condition == "freeze":
        eligible = [
            index
            for index, coordinate in enumerate(world.coords)
            if float(np.hypot(coordinate.x - fixed_point[0], coordinate.v - fixed_point[1])) > 0.5
        ]
        if not eligible:
            raise RuntimeError("freeze challenge has no coordinate farther than 0.5")
        selected = rng.choice(eligible)
        world.coords[selected].frozen = True
        return [f"c{selected:03d}"]
    raise ValueError(f"Unknown challenge {condition!r}")


def _forecast_frames(
    candidate: dict[str, Any], post: dict[str, Any], run_id: str
) -> list[dict[str, Any]]:
    coordinate_ids = [coordinate["id"] for coordinate in post["coordinates"]]
    states = predict(candidate, state_vector(post), FINAL_TICK - PREFIX_TICK)
    frames = []
    for tick, state in enumerate(states, PREFIX_TICK + 1):
        frames.append(
            {
                "tick": tick,
                "run_id": run_id,
                "coordinates": [
                    {"id": coordinate_id, "x": state[2 * i], "v": state[2 * i + 1]}
                    for i, coordinate_id in enumerate(coordinate_ids)
                ],
            }
        )
    return frames


def plan_stage(directory: Path = RESULT_DIRECTORY) -> dict[str, Any]:
    candidate_path = directory / "candidate.json"
    candidate_sha = _require_committed(candidate_path)
    candidate = json.loads(candidate_path.read_bytes())
    _verify_scientific_lineage(candidate.get("scientific_inputs"))
    proposal = candidate["proposal"]
    if proposal["status"] != "stable_fixed_relation":
        raise RuntimeError("Cannot plan outcome probes for an abstained candidate")
    selected = proposal["selected"]
    fixed_point = selected["local_fixed_point"]
    if fixed_point is None:
        raise RuntimeError("P13 challenge contract requires the selected shared local model")
    probes: list[dict[str, Any]] = []
    prefix_frames: list[dict[str, Any]] = []
    for seed in EVALUATION_SEEDS:
        base, prefix = _episode(seed, PREFIX_TICK, f"evaluation-{seed}-prefix")
        prefix_frames.extend(prefix)
        snapshot = base.snapshot()
        for condition_index, condition in enumerate(CONDITIONS):
            run_id = f"evaluation-{seed}-{condition}"
            world = BowlWorld.from_seed(N_COORDINATES, seed, spread=SPREAD)
            world.restore(snapshot)
            intervention_seed = seed * 10 + condition_index
            targets = _apply_challenge(world, condition, intervention_seed, fixed_point)
            post = observe(world, run_id)
            probes.append(
                {
                    "run_id": run_id,
                    "seed": seed,
                    "condition": condition,
                    "intervention_seed": intervention_seed,
                    "target_ids": targets,
                    "prefix_snapshot_id": snapshot["snapshot_id"],
                    "post_observation": post,
                    "forecast": _forecast_frames(selected, post, run_id),
                }
            )
    prefix_path = directory / "evaluation-prefix.jsonl"
    _write_jsonl_new(prefix_path, prefix_frames)
    plan = {
        "schema_version": 1,
        "experiment": "P13",
        "stage": "forecasts_frozen_before_outcomes",
        "source_revision": _revision(),
        "candidate_source_revision": candidate["source_revision"],
        "scientific_inputs": candidate["scientific_inputs"],
        "candidate_sha256": candidate_sha,
        "evaluation_prefix_sha256": _sha(prefix_path.read_bytes()),
        "probes": probes,
        "outcomes_present": False,
    }
    _write_new(directory / "probes.json.gz", gzip.compress(_json_bytes(plan), mtime=0))
    return plan


def _same_observation(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left == right


def _rms(actual: list[dict[str, Any]], forecast: list[dict[str, Any]], ids: set[str] | None = None) -> float:
    errors: list[float] = []
    for observed, expected in zip(actual, forecast, strict=True):
        for left, right in zip(observed["coordinates"], expected["coordinates"], strict=True):
            if ids is None or left["id"] in ids:
                errors.extend((left["x"] - right["x"], left["v"] - right["v"]))
    return float(np.sqrt(np.mean(np.square(errors))))


def _final_distances(frames: list[dict[str, Any]], fixed_point: list[float]) -> dict[str, float]:
    values: dict[str, list[float]] = defaultdict(list)
    for frame in frames[-FINAL_WINDOW:]:
        for coordinate in frame["coordinates"]:
            values[coordinate["id"]].append(
                float(np.hypot(coordinate["x"] - fixed_point[0], coordinate["v"] - fixed_point[1]))
            )
    return {coordinate_id: max(distances) for coordinate_id, distances in values.items()}


def _assess(
    probe: dict[str, Any], actual: list[dict[str, Any]], fixed_point: list[float], integrity: bool
) -> dict[str, Any]:
    all_ids = {coordinate["id"] for coordinate in actual[0]["coordinates"]}
    target_ids = set(probe["target_ids"])
    unaffected = all_ids - target_ids
    whole_rms = _rms(actual, probe["forecast"])
    unaffected_rms = _rms(actual, probe["forecast"], unaffected) if unaffected else None
    distances = _final_distances(actual, fixed_point)
    condition = probe["condition"]
    if condition == "freeze":
        checks = {
            "whole_forecast_rms_gt_0_1": whole_rms > 0.1,
            "frozen_coordinate_remains_away": all(distances[item] > 0.01 for item in target_ids),
            "unaffected_coordinates_settle": all(distances[item] <= 0.01 for item in unaffected),
            "unaffected_forecast_rms_le_1e_8": unaffected_rms is not None and unaffected_rms <= 1e-8,
        }
    else:
        checks = {
            "whole_forecast_rms_le_1e_8": whole_rms <= 1e-8,
            "all_coordinates_settle": all(distance <= 0.01 for distance in distances.values()),
        }
    return {
        "integrity": integrity,
        "supported": integrity and all(checks.values()),
        "checks": checks,
        "whole_forecast_rms": whole_rms,
        "unaffected_forecast_rms": unaffected_rms,
        "final_window_max_distance": distances,
    }


def evaluate_stage(directory: Path = RESULT_DIRECTORY) -> dict[str, Any]:
    candidate_path = directory / "candidate.json"
    probes_path = directory / "probes.json.gz"
    candidate_sha = _require_committed(candidate_path)
    probes_sha = _require_committed(probes_path)
    candidate = json.loads(candidate_path.read_bytes())
    plan = json.loads(gzip.decompress(probes_path.read_bytes()))
    _verify_scientific_lineage(candidate.get("scientific_inputs"))
    _require_revision_ancestor(plan.get("source_revision"))
    if (
        plan["candidate_sha256"] != candidate_sha
        or plan.get("candidate_source_revision") != candidate.get("source_revision")
        or plan.get("scientific_inputs") != candidate.get("scientific_inputs")
        or plan["outcomes_present"] is not False
    ):
        raise RuntimeError("Frozen probe/candidate lineage is invalid")
    selected = candidate["proposal"]["selected"]
    fixed_point = selected["local_fixed_point"]
    outcomes: list[dict[str, Any]] = []
    raw_frames: list[dict[str, Any]] = []
    for probe in plan["probes"]:
        seed, condition = probe["seed"], probe["condition"]
        world, _ = _episode(seed, PREFIX_TICK, probe["run_id"])
        snapshot_matches = world.snapshot()["snapshot_id"] == probe["prefix_snapshot_id"]
        targets = _apply_challenge(world, condition, probe["intervention_seed"], fixed_point)
        post_matches = targets == probe["target_ids"] and _same_observation(
            observe(world, probe["run_id"]), probe["post_observation"]
        )
        actual = []
        while world.tick < FINAL_TICK:
            world.step_tick()
            actual.append(observe(world, probe["run_id"]))
        raw_frames.extend(actual)
        integrity = snapshot_matches and post_matches and len(actual) == len(probe["forecast"])
        outcomes.append(
            {
                "run_id": probe["run_id"],
                "seed": seed,
                "condition": condition,
                "target_ids": probe["target_ids"],
                "assessment": _assess(probe, actual, fixed_point, integrity),
            }
        )
    raw_path = directory / "evaluation.jsonl"
    _write_jsonl_new(raw_path, raw_frames)
    expected_block = np.asarray([[0.862, 0.92], [-0.138, 0.92]])
    learned_block = np.asarray(selected["matrix"], dtype=float)[:2, :2]
    hidden_diagnostic = {
        "coefficient_max_error": float(np.max(np.abs(expected_block - learned_block))),
        "coefficient_check": bool(np.max(np.abs(expected_block - learned_block)) <= 1e-8),
        "fixed_point_max_error": float(np.max(np.abs(np.asarray(fixed_point)))),
        "fixed_point_check": bool(np.max(np.abs(np.asarray(fixed_point))) <= 1e-8),
        "unlocked_after_forecast_freeze": True,
    }
    by_condition = {
        condition: {
            "supported_runs": sum(
                item["assessment"]["supported"] for item in outcomes if item["condition"] == condition
            ),
            "total_runs": sum(item["condition"] == condition for item in outcomes),
        }
        for condition in CONDITIONS
    }
    result = {
        "schema_version": 1,
        "experiment": "P13",
        "stage": "outcomes_revealed",
        "source_revision": _revision(),
        "candidate_sha256": candidate_sha,
        "probes_sha256": probes_sha,
        "evaluation_observations": {
            "path": raw_path.name,
            "sha256": _sha(raw_path.read_bytes()),
            "frames": len(raw_frames),
        },
        "outcomes": outcomes,
        "summary": {
            "by_condition": by_condition,
            "all_preregistered_checks_pass": all(
                item["assessment"]["supported"] for item in outcomes
            ) and all(hidden_diagnostic[key] for key in ("coefficient_check", "fixed_point_check")),
            "interpretation": (
                "The observation-only learner recovered the passive local law and predicted state damage, "
                "while persistent mechanism loss falsified whole-system restoration. This calibrates a "
                "proposal/falsification seam; it does not discover agency or an unexpected bowl goal."
            ),
        },
        "hidden_evaluator_diagnostic": hidden_diagnostic,
    }
    _write_new(directory / "evaluation.json", _json_bytes(result))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("discover", "plan", "evaluate"))
    parser.add_argument("--output", type=Path, default=RESULT_DIRECTORY)
    arguments = parser.parse_args()
    functions = {"discover": discover_stage, "plan": plan_stage, "evaluate": evaluate_stage}
    result = functions[arguments.stage](arguments.output)
    print(json.dumps({"stage": result["stage"], "output": str(arguments.output)}, indent=2))


if __name__ == "__main__":
    main()
