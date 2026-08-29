"""Load NetLogo BehaviorSpace trajectories into analysis-friendly tables.

The workbench deliberately consumes exported experiment artifacts rather than
reimplementing the generator.  NetLogo remains the source of trajectories;
this module only normalizes those trajectories for linked visual analysis.
"""

from __future__ import annotations

import csv
import itertools
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

CONDITION_LABELS = {
    "baseline": "Baseline",
    "block-swap": "Block swap",
    "freeze-immovable": "Freeze: immovable",
    "freeze-moveable": "Freeze: moveable",
}


@dataclass(frozen=True)
class ExperimentDataset:
    """Normalized experiment data used by every workbench view."""

    runs: pd.DataFrame
    macros: pd.DataFrame
    cells: pd.DataFrame
    source_paths: tuple[Path, ...]

    def run(self, run_id: str) -> pd.Series:
        match = self.runs.loc[self.runs["run_id"] == run_id]
        if match.empty:
            raise KeyError(f"Unknown run_id: {run_id}")
        return match.iloc[0]

    def trajectory(self, run_id: str) -> pd.DataFrame:
        return self.macros.loc[self.macros["run_id"] == run_id].sort_values("tick")

    def cell_history(self, run_id: str) -> pd.DataFrame:
        return self.cells.loc[self.cells["run_id"] == run_id].sort_values(["tick", "position"])


def _netlogo_rows(path: Path) -> list[dict[str, str]]:
    """Read a BehaviorSpace table while tolerating its six-line preamble."""

    with path.open(newline="", encoding="utf-8-sig") as handle:
        lines = handle.readlines()
    header_index = next((index for index, line in enumerate(lines) if "[run number]" in line), None)
    if header_index is None:
        raise ValueError(f"No BehaviorSpace table header found in {path}")
    return list(csv.DictReader(lines[header_index:]))


def _atoms(text: str) -> list[str]:
    value = str(text).strip()
    if not (value.startswith("[") and value.endswith("]")):
        raise ValueError(f"Expected a NetLogo list, got {text!r}")
    body = value[1:-1].strip()
    return [] if not body else body.split()


def _as_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def _longest_ascending_run(values: list[int]) -> int:
    if not values:
        return 0
    best = current = 1
    for left, right in itertools.pairwise(values):
        current = current + 1 if left <= right else 1
        best = max(best, current)
    return best


def _sorted_prefix(values: list[int]) -> int:
    """Number of leading positions already equal to the sorted target."""

    target = sorted(values)
    prefix = 0
    for observed, expected in zip(values, target, strict=False):
        if observed != expected:
            break
        prefix += 1
    return prefix


def _inversions(values: list[int]) -> int:
    return sum(left > right for index, left in enumerate(values) for right in values[index + 1 :])


def _capability_features(modes: list[str]) -> tuple[float, float, float, float]:
    n = len(modes)
    if n == 0:
        return 0.0, 0.0, 0.0, 0.0
    active = np.asarray([mode == "none" for mode in modes], dtype=bool)
    immovable = np.asarray([mode == "immovable" for mode in modes], dtype=bool)
    movable = np.asarray([mode == "moveable" for mode in modes], dtype=bool)
    if n == 1:
        traversable = float(not immovable[0])
    else:
        traversable = float(np.mean(~(immovable[:-1] | immovable[1:])))
    return float(active.mean()), float(immovable.mean()), float(movable.mean()), traversable


def _normalize_file(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    condition = path.stem
    macro_records: list[dict[str, object]] = []
    cell_records: list[dict[str, object]] = []

    for row in _netlogo_rows(path):
        run_number = int(float(row["[run number]"]))
        run_id = f"{condition}:{run_number}"
        values = [int(float(value)) for value in _atoms(row["values"])]
        cell_ids = [int(float(value)) for value in _atoms(row["cell-ids-by-position"])]
        modes = _atoms(row["freeze-modes-by-position"])
        if not (len(values) == len(cell_ids) == len(modes)):
            raise ValueError(f"Mismatched cell lists in {path}, run {run_number}")

        tick = round(float(row["ticks"]))
        boundary = float(row["boundary-length"])
        n_cells = len(values)
        max_inversions = max(1, n_cells * (n_cells - 1) // 2)
        inversion_count = _inversions(values)
        ascending_run = _longest_ascending_run(values)
        sorted_prefix = _sorted_prefix(values)
        active_fraction, immovable_fraction, movable_fraction, traversable_edges = (
            _capability_features(modes)
        )

        common = {
            "run_id": run_id,
            "condition": condition,
            "condition_label": CONDITION_LABELS.get(condition, condition.replace("-", " ").title()),
            "run_number": run_number,
            "seed": int(float(row["seed-number"])),
            "activation_order": row["activation-order"],
            "tick": tick,
        }
        macro_records.append(
            {
                **common,
                "step": int(float(row["[step]"])),
                "boundary": boundary,
                "boundary_norm": boundary / max(1, n_cells - 1),
                "inversions": inversion_count,
                "inversions_norm": inversion_count / max_inversions,
                "longest_ascending_run": ascending_run,
                "ascending_run_norm": ascending_run / max(1, n_cells),
                "sorted_prefix": sorted_prefix,
                "sorted_prefix_norm": sorted_prefix / max(1, n_cells),
                "active_fraction": active_fraction,
                "immovable_fraction": immovable_fraction,
                "moveable_fraction": movable_fraction,
                "traversable_edge_fraction": traversable_edges,
                "sorted": _as_bool(row["sorted?"]),
                "quiescent": _as_bool(row["quiescent?"]),
                "swap_count": int(float(row["swap-count"])),
                "comparison_count": int(float(row["comparison-count"])),
                "last_event": row["last-event"],
                "n_cells": n_cells,
                "perturb_fraction": float(row["perturb-fraction"]),
                "intervention_seed": int(float(row["intervention-seed"])),
                "freeze_count": int(float(row["freeze-count"])),
                "freeze_mode": row["freeze-mode-choice"],
                "max_ticks": int(float(row["max-ticks"])),
            }
        )
        for position, (value, cell_id, mode) in enumerate(
            zip(values, cell_ids, modes, strict=True)
        ):
            cell_records.append(
                {
                    **common,
                    "position": position,
                    "value": value,
                    "value_norm": value / max(1, n_cells - 1),
                    "cell_id": cell_id,
                    "cell_id_norm": cell_id / max(1, n_cells - 1),
                    "freeze_mode": mode,
                    "freeze_code": {"none": 0, "moveable": 1, "immovable": 2}.get(mode, 3),
                }
            )

    return pd.DataFrame(macro_records), pd.DataFrame(cell_records)


def _build_run_table(macros: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for run_id, group in macros.groupby("run_id", sort=False):
        group = group.sort_values("tick")
        first = group.iloc[0]
        last = group.iloc[-1]
        condition = str(first["condition"])
        intervention_tick = int(first["tick"]) if condition != "baseline" else np.nan
        records.append(
            {
                "run_id": run_id,
                "condition": condition,
                "condition_label": first["condition_label"],
                "run_number": int(first["run_number"]),
                "seed": int(first["seed"]),
                "activation_order": first["activation_order"],
                "intervention_tick": intervention_tick,
                "start_tick": int(first["tick"]),
                "end_tick": int(last["tick"]),
                "observations": len(group),
                "n_cells": int(first["n_cells"]),
                "start_boundary": float(first["boundary"]),
                "final_boundary": float(last["boundary"]),
                "best_boundary": float(group["boundary"].min()),
                "start_inversions": int(first["inversions"]),
                "final_inversions": int(last["inversions"]),
                "final_prefix": int(last["sorted_prefix"]),
                "final_ascending_run": int(last["longest_ascending_run"]),
                "reached_goal": bool(group["sorted"].any()),
                "ended_quiescent": bool(last["quiescent"]),
                "final_swaps": int(last["swap_count"]),
                "final_comparisons": int(last["comparison_count"]),
                "freeze_count": int(first["freeze_count"]),
                "freeze_mode": first["freeze_mode"],
                "perturb_fraction": float(first["perturb_fraction"]),
                "intervention_seed": int(first["intervention_seed"]),
            }
        )
    runs = pd.DataFrame(records)
    runs["run_label"] = runs.apply(
        lambda row: (
            f"{row['condition_label']} · seed {row['seed']} · "
            f"{row['activation_order']} · run {row['run_number']}"
        ),
        axis=1,
    )

    baseline = runs.loc[runs["condition"] == "baseline"].copy()
    baseline = baseline.sort_values("run_number").drop_duplicates(["seed", "activation_order"])
    baseline_lookup = baseline.set_index(["seed", "activation_order"])["run_id"].to_dict()
    runs["matched_baseline_id"] = runs.apply(
        lambda row: (
            row["run_id"]
            if row["condition"] == "baseline"
            else baseline_lookup.get((row["seed"], row["activation_order"]), "")
        ),
        axis=1,
    )
    return runs.sort_values(["condition", "seed", "activation_order", "run_number"]).reset_index(
        drop=True
    )


def load_x02_dataset(paths: str | Path | Iterable[str | Path]) -> ExperimentDataset:
    """Load one file, a directory, or an explicit list of X02 CSV files."""

    if isinstance(paths, (str, Path)):
        candidate = Path(paths)
        source_paths = sorted(candidate.glob("*.csv")) if candidate.is_dir() else [candidate]
    else:
        source_paths = [Path(path) for path in paths]
    source_paths = [path.resolve() for path in source_paths if path.exists()]
    if not source_paths:
        raise FileNotFoundError(f"No BehaviorSpace CSV files found at {paths}")

    macro_frames: list[pd.DataFrame] = []
    cell_frames: list[pd.DataFrame] = []
    for path in source_paths:
        macros, cells = _normalize_file(path)
        macro_frames.append(macros)
        cell_frames.append(cells)
    macro_table = pd.concat(macro_frames, ignore_index=True)
    cell_table = pd.concat(cell_frames, ignore_index=True)
    return ExperimentDataset(
        runs=_build_run_table(macro_table),
        macros=macro_table.sort_values(["run_id", "tick"]).reset_index(drop=True),
        cells=cell_table.sort_values(["run_id", "tick", "position"]).reset_index(drop=True),
        source_paths=tuple(source_paths),
    )
