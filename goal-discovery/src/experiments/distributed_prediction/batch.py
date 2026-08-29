"""Generate the frozen P2-002 crossed sorting batches.

The generator writes observations and outcomes.  It does not fit a model.  All
features are derived from the declared observation map at the branch or from
its pre-branch history.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.common.seeds import rng as seeded_rng
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import RULE_VERSION, SortingWorld
from src.experiments.sorting.observe import Observation, observe

PROTOCOL_PATH = (
    Path(__file__).resolve().parents[3]
    / "docs"
    / "hypotheses"
    / "p2_002_distributed_macro_prediction.md"
)
MICRO_BINS = 12
SCHEDULES = ("index", "shuffled")
FREEZE_MODES = ("moveable", "immovable")
FREEZE_COUNTS = (1, 2, 3)
BRANCH_FRACTIONS = (0.0, 1.0 / 3.0)


@dataclass(frozen=True)
class BatchDesign:
    name: str
    n: int
    seeds: tuple[int, ...]
    schedules: tuple[str, ...] = SCHEDULES
    branch_fractions: tuple[float, ...] = BRANCH_FRACTIONS
    freeze_modes: tuple[str, ...] = FREEZE_MODES
    freeze_counts: tuple[int, ...] = FREEZE_COUNTS
    damage_conditions: tuple[tuple[str, int], ...] = ()
    horizon_ticks: int | None = None

    @property
    def damage_pairs(self) -> tuple[tuple[str, int], ...]:
        if self.damage_conditions:
            return self.damage_conditions
        return tuple(itertools.product(self.freeze_modes, self.freeze_counts))

    @property
    def branches(self) -> int:
        return (
            len(self.seeds)
            * len(self.schedules)
            * len(self.branch_fractions)
            * len(self.damage_pairs)
        )

    @property
    def horizon(self) -> int:
        return self.horizon_ticks or 30 * self.n


DISCOVERY = BatchDesign("discovery", 12, tuple(range(101, 107)))
HOLDOUT = BatchDesign("holdout", 24, tuple(range(401, 407)))


def protocol_sha256(path: Path = PROTOCOL_PATH) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _make_world(n: int, schedule: str, seed: int) -> SortingWorld:
    values = list(range(n))
    seeded_rng("p2-002-initial-condition", seed, n).shuffle(values)
    return SortingWorld.from_values(values, "bubble", order=schedule, seed=seed)


def _inversions(values: Sequence[int]) -> int:
    return sum(left > right for index, left in enumerate(values) for right in values[index + 1 :])


def _longest_ascending_run(values: Sequence[int]) -> int:
    if not values:
        return 0
    best = current = 1
    for left, right in itertools.pairwise(values):
        current = current + 1 if left <= right else 1
        best = max(best, current)
    return best


def _sorted_prefix(values: Sequence[int]) -> int:
    target = sorted(values)
    prefix = 0
    for current, expected in zip(values, target, strict=True):
        if current != expected:
            break
        prefix += 1
    return prefix


def _value_features(observation: Observation) -> dict[str, float]:
    values = observation["values"]
    n = len(values)
    boundary = sum(left > right for left, right in itertools.pairwise(values))
    max_inversions = max(1, n * (n - 1) // 2)
    return {
        "value_boundary_norm": boundary / max(1, n - 1),
        "value_inversions_norm": _inversions(values) / max_inversions,
        "value_ascending_run_norm": _longest_ascending_run(values) / max(1, n),
        "value_sorted_prefix_norm": _sorted_prefix(values) / max(1, n),
    }


def _barrier_groups(modes: Sequence[str]) -> int:
    return sum(
        mode == "immovable" and (index == 0 or modes[index - 1] != "immovable")
        for index, mode in enumerate(modes)
    )


def _resolvable_inversion_fraction(observation: Observation) -> float:
    values = observation["values"]
    modes = observation["frozen"]
    inversion_edges = [
        index for index, (left, right) in enumerate(itertools.pairwise(values)) if left > right
    ]
    if not inversion_edges:
        return 1.0
    resolvable = 0
    for index in inversion_edges:
        left_can_move_right = modes[index] == "none" and modes[index + 1] != "immovable"
        right_can_move_left = modes[index + 1] == "none" and modes[index] != "immovable"
        resolvable += left_can_move_right or right_can_move_left
    return resolvable / len(inversion_edges)


def _capability_features(observation: Observation) -> dict[str, float]:
    modes = observation["frozen"]
    n = max(1, len(modes))
    return {
        "cap_active_fraction": sum(mode == "none" for mode in modes) / n,
        "cap_moveable_fraction": sum(mode == "moveable" for mode in modes) / n,
        "cap_immovable_fraction": sum(mode == "immovable" for mode in modes) / n,
        "cap_barrier_groups_norm": _barrier_groups(modes) / n,
        "cap_resolvable_inversion_fraction": _resolvable_inversion_fraction(observation),
    }


def _history_features(history: Sequence[Observation], n: int) -> dict[str, float]:
    values = [_value_features(item) for item in history]
    elapsed = max(1, len(history) - 1)
    boundary = np.asarray([item["value_boundary_norm"] for item in values], dtype=float)
    inversions = np.asarray([item["value_inversions_norm"] for item in values], dtype=float)
    return {
        "history_boundary_rate": float((boundary[-1] - boundary[0]) / elapsed),
        "history_inversion_rate": float((inversions[-1] - inversions[0]) / elapsed),
        "history_boundary_volatility": float(np.std(boundary[-min(4, len(boundary)) :])),
    }


def _resample(values: Sequence[float], bins: int = MICRO_BINS) -> np.ndarray:
    source = np.linspace(0.0, 1.0, num=len(values))
    target = np.linspace(0.0, 1.0, num=bins)
    return np.interp(target, source, np.asarray(values, dtype=float))


def _micro_features(observation: Observation) -> dict[str, float]:
    n = max(1, len(observation["values"]) - 1)
    values = _resample([value / n for value in observation["values"]])
    moveable = _resample([mode == "moveable" for mode in observation["frozen"]])
    immovable = _resample([mode == "immovable" for mode in observation["frozen"]])
    result: dict[str, float] = {}
    for prefix, vector in (
        ("micro_value", values),
        ("micro_moveable", moveable),
        ("micro_immovable", immovable),
    ):
        result.update({f"{prefix}_{index:02d}": float(value) for index, value in enumerate(vector)})
    return result


def _trajectory_row(run_id: str, phase: str, event: str, world: SortingWorld) -> dict[str, Any]:
    observation = observe(world)
    values = observation["values"]
    value_features = _value_features(observation)
    return {
        "run_id": run_id,
        "phase": phase,
        "event": event,
        "tick": observation["tick"],
        "steps": observation["steps"],
        "values_json": json.dumps(values),
        "freeze_modes_json": json.dumps(observation["frozen"]),
        "boundary_norm": value_features["value_boundary_norm"],
        "inversions_norm": value_features["value_inversions_norm"],
        "sorted": values == sorted(values),
        "quiescent": world.quiescent(),
    }


def _run_branch(
    design: BatchDesign,
    seed: int,
    schedule: str,
    branch_fraction: float,
    mode: str,
    count: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    branch_tick = round(design.n * branch_fraction)
    intervention_seed = seed + 10_000 + branch_tick * 101 + count * 17
    run_id = f"{design.name}:n{design.n}:seed{seed}:{schedule}:t{branch_tick}:{mode}:k{count}"
    world = _make_world(design.n, schedule, seed)
    history = [observe(world)]
    trajectory = [_trajectory_row(run_id, "pre_branch", "setup", world)]
    for _ in range(branch_tick):
        if world.quiescent():
            break
        world.step_tick()
        history.append(observe(world))
        trajectory.append(_trajectory_row(run_id, "pre_branch", "step", world))

    pre_sorted = world.values == sorted(world.values)
    apply(
        world,
        Intervention("freeze_cells", {"count": count, "mode": mode}),
        seed=intervention_seed,
    )
    branch_observation = observe(world)
    trajectory.append(_trajectory_row(run_id, "post_branch", f"freeze-{mode}", world))

    reached_goal = world.values == sorted(world.values)
    time_to_goal: int | None = 0 if reached_goal else None
    for elapsed in range(1, design.horizon + 1):
        if reached_goal or world.quiescent():
            break
        world.step_tick()
        trajectory.append(_trajectory_row(run_id, "post_branch", "step", world))
        reached_goal = world.values == sorted(world.values)
        if reached_goal:
            time_to_goal = elapsed

    final_observation = observe(world)
    final_value = _value_features(final_observation)
    row: dict[str, Any] = {
        "run_id": run_id,
        "batch": design.name,
        "seed": seed,
        "n_cells": design.n,
        "activation_schedule": schedule,
        "branch_tick": branch_tick,
        "branch_time_norm": branch_tick / design.n,
        "freeze_mode": mode,
        "freeze_count": count,
        "freeze_count_norm": count / design.n,
        "intervention_seed": intervention_seed,
        "pre_sorted": pre_sorted,
        "reached_goal": reached_goal,
        "time_to_goal": time_to_goal,
        "time_to_goal_per_cell": (time_to_goal / design.n if time_to_goal is not None else np.nan),
        "final_tick": final_observation["tick"],
        "final_boundary_norm": final_value["value_boundary_norm"],
        "ended_quiescent": world.quiescent(),
        "values_json": json.dumps(branch_observation["values"]),
        "freeze_modes_json": json.dumps(branch_observation["frozen"]),
        "algotypes_json": json.dumps(branch_observation["algotypes"]),
        "intervention_system_size": float(design.n),
        "intervention_schedule_shuffled": float(schedule == "shuffled"),
        "intervention_branch_time_norm": branch_tick / design.n,
        "intervention_freeze_fraction": count / design.n,
        "intervention_moveable": float(mode == "moveable"),
        "intervention_immovable": float(mode == "immovable"),
        **_value_features(branch_observation),
        **_capability_features(branch_observation),
        **_history_features(history, design.n),
        **_micro_features(branch_observation),
    }
    return row, trajectory


def generate_batch(design: BatchDesign) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate every frozen branch in deterministic product order."""

    rows: list[dict[str, Any]] = []
    trajectories: list[dict[str, Any]] = []
    combinations: Iterable[tuple[int, str, float, tuple[str, int]]] = itertools.product(
        design.seeds,
        design.schedules,
        design.branch_fractions,
        design.damage_pairs,
    )
    for seed, schedule, branch_fraction, (mode, count) in combinations:
        row, trajectory = _run_branch(design, seed, schedule, branch_fraction, mode, count)
        rows.append(row)
        trajectories.extend(trajectory)
    frame = pd.DataFrame(rows)
    trace = pd.DataFrame(trajectories)
    if len(frame) != design.branches:
        raise AssertionError(f"generated {len(frame)} branches; expected {design.branches}")
    return frame, trace


def write_batch(
    design: BatchDesign,
    output_dir: Path,
    *,
    protocol_path: Path = PROTOCOL_PATH,
    experiment_id: str = "p2-002-distributed-macro-prediction",
) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    runs, trajectories = generate_batch(design)
    runs_path = output_dir / f"{design.name}_runs.csv"
    trajectories_path = output_dir / f"{design.name}_trajectories.csv"
    metadata_path = output_dir / f"{design.name}_metadata.json"
    runs.to_csv(runs_path, index=False)
    trajectories.to_csv(trajectories_path, index=False)
    metadata = {
        "experiment_id": experiment_id,
        "phase": design.name,
        "rule_version": RULE_VERSION,
        "protocol_path": str(protocol_path.relative_to(Path(__file__).resolve().parents[3])),
        "protocol_sha256": protocol_sha256(protocol_path),
        "observation_boundary": "src.experiments.sorting.observe.observe",
        "design": asdict(design),
        "branches": len(runs),
        "trajectory_rows": len(trajectories),
        "goal_rate": float(runs["reached_goal"].mean()),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    return runs_path, trajectories_path, metadata_path
