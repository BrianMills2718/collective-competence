"""Analyze P7-004 under its frozen scale, split, null, and decision gates."""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler

ARMS = {"sham": "p7-004-sham.csv", "trail_cut": "p7-004-trail-cut.csv"}
SEEDS = tuple(range(1101, 1109))
FIELD_METRIC = (
    "ifelse-value (ticks = 330) "
    "[[(list pxcor pycor chemical food nest? food-source-number)] of patches] [[]]"
)
FIELD_PATTERN = re.compile(
    r"\[\s*(-?\d+)\s+(-?\d+)\s+([^\s\]]+)\s+([^\s\]]+)\s+"
    r"(true|false)\s+([^\s\]]+)\s*\]"
)
RAW_COLUMNS = {
    "count turtles": "population",
    "count turtles with [color = orange + 1]": "carrying",
    "count turtles with [distancexy 0 0 < 5]": "in_nest",
    "count turtles with [distancexy 0 0 >= 8 and distancexy 0 0 < 13]": "in_annulus",
    (
        "ifelse-value any? turtles with [color != orange + 1] "
        "[mean [[chemical] of patch-here] of turtles with [color != orange + 1]] [0]"
    ): "noncarrier_patch_chemical",
    "sum [food] of patches": "food",
    "sum [chemical] of patches": "total_chemical",
    (
        "sum [chemical] of patches with "
        "[distancexy 0 0 >= 8 and distancexy 0 0 < 13]"
    ): "annulus_chemical",
}
BASE = ["arm_cut", "food_300"]
SCALE_FEATURES = {
    "local": [
        "carrying_fraction_330",
        "noncarrier_patch_chemical_330",
        "annulus_fraction_330",
        "carrying_slope_301_330",
    ],
    "colony": [
        "total_chemical_330",
        "mean_patch_chemical_330",
        "food_removal_slope_301_330",
        "nest_fraction_330",
    ],
    "trail": [
        "source_connection_fraction_330",
        "largest_component_fraction_330",
        "skeleton_fraction_330",
        "mean_source_path_330",
    ],
}


@dataclass(frozen=True)
class PatchField:
    chemical: np.ndarray
    food: np.ndarray
    nest: np.ndarray
    source: np.ndarray
    min_x: int
    max_y: int


def read_behaviorspace(path: Path, arm: str) -> pd.DataFrame:
    csv.field_size_limit(sys.maxsize)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise ValueError(f"{path} has no BehaviorSpace table header") from error
    headers = rows[header_index]
    data = [row for row in rows[header_index + 1 :] if row and any(value.strip() for value in row)]
    if any(len(row) != len(headers) for row in data):
        raise ValueError(f"{path} has ragged BehaviorSpace rows")
    frame = pd.DataFrame(data, columns=headers)
    required = {"[run number]", "ticks", FIELD_METRIC, *RAW_COLUMNS}
    if missing := required - set(frame):
        raise ValueError(f"{path} lacks fields: {sorted(missing)}")
    frame["run_number"] = frame["[run number]"].astype(int)
    frame["seed"] = 1101 + ((frame["run_number"] - 1) % 8)
    frame["tick"] = frame["ticks"].astype(float).round().astype(int)
    frame["arm"] = arm
    for source, target in RAW_COLUMNS.items():
        frame[target] = frame[source].astype(float)
    if set(frame["seed"]) != set(SEEDS):
        raise ValueError(f"{path} does not contain the frozen seeds")
    expected_ticks = set(range(601))
    for seed, group in frame.groupby("seed"):
        if set(group["tick"]) != expected_ticks or len(group) != 601:
            raise ValueError(f"{path} seed {seed} is not a complete tick 0–600 trajectory")
    return frame[["arm", "seed", "tick", *RAW_COLUMNS.values(), FIELD_METRIC]]


def parse_field(raw: str) -> PatchField:
    matches = FIELD_PATTERN.findall(raw)
    if not matches:
        raise ValueError("patch field is empty")
    xs = [int(row[0]) for row in matches]
    ys = [int(row[1]) for row in matches]
    min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
    shape = (max_y - min_y + 1, max_x - min_x + 1)
    if len(matches) != shape[0] * shape[1]:
        raise ValueError("patch field is not rectangular")
    chemical = np.zeros(shape, dtype=float)
    food = np.zeros(shape, dtype=float)
    nest = np.zeros(shape, dtype=bool)
    source = np.zeros(shape, dtype=int)
    for x_text, y_text, chemical_text, food_text, nest_text, source_text in matches:
        row = max_y - int(y_text)
        column = int(x_text) - min_x
        chemical[row, column] = float(chemical_text)
        food[row, column] = float(food_text)
        nest[row, column] = nest_text == "true"
        source[row, column] = int(float(source_text))
    return PatchField(chemical, food, nest, source, min_x, max_y)


def trail_metrics(field: PatchField) -> dict[str, float]:
    try:
        from skimage.measure import label
        from skimage.morphology import skeletonize
    except ImportError as error:
        raise RuntimeError("run `uv sync --extra network-analysis`") from error

    active = field.chemical >= 0.05
    skeleton = skeletonize(active)
    labels = label(active, connectivity=2)
    label_sizes = np.bincount(labels.ravel())[1:]
    largest = int(label_sizes.max()) if len(label_sizes) else 0
    pixels = {tuple(map(int, point)) for point in np.argwhere(skeleton)}
    graph = nx.Graph()
    for pixel in pixels:
        graph.add_node(pixel)
        row, column = pixel
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                neighbor = (row + dr, column + dc)
                if (dr or dc) and neighbor in pixels:
                    graph.add_edge(pixel, neighbor, weight=math.hypot(dr, dc))

    source_ids = [
        source_id
        for source_id in sorted(set(field.source.ravel()) - {0})
        if field.food[field.source == source_id].sum() > 0
    ]
    diagonal = math.hypot(*field.chemical.shape)
    nest_pixels = np.argwhere(field.nest)
    nest_nodes = _nearby_skeleton_nodes(nest_pixels, pixels)
    connected = 0
    paths: list[float] = []
    for source_id in source_ids:
        source_pixels = np.argwhere(field.source == source_id)
        source_nodes = _nearby_skeleton_nodes(source_pixels, pixels)
        lengths = [
            nx.shortest_path_length(graph, nest_node, source_node, weight="weight")
            for nest_node in nest_nodes
            for source_node in source_nodes
            if nx.has_path(graph, nest_node, source_node)
        ]
        if lengths:
            connected += 1
            paths.append(float(min(lengths)))
        else:
            paths.append(diagonal)
    return {
        "source_connection_fraction_330": connected / len(source_ids) if source_ids else 0.0,
        "largest_component_fraction_330": largest / field.chemical.size,
        "skeleton_fraction_330": len(pixels) / field.chemical.size,
        "mean_source_path_330": float(np.mean(paths)) if paths else diagonal,
    }


def _nearby_skeleton_nodes(regions: np.ndarray, pixels: set[tuple[int, int]]) -> list[tuple[int, int]]:
    if not pixels or not len(regions):
        return []
    candidates: set[tuple[int, int]] = set()
    for row, column in regions:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                point = (int(row + dr), int(column + dc))
                if point in pixels:
                    candidates.add(point)
    if candidates:
        return sorted(candidates)
    return []


def slope(group: pd.DataFrame, column: str, start: int, end: int) -> float:
    window = group.loc[group["tick"].between(start, end)]
    return float(np.polyfit(window["tick"], window[column], 1)[0])


def build_features(trajectories: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    for (arm, seed), group in trajectories.groupby(["arm", "seed"], sort=True):
        group = group.sort_values("tick")
        at = group.set_index("tick")
        field = parse_field(str(at.loc[330, FIELD_METRIC]))
        record = {
            "arm": arm,
            "seed": int(seed),
            "arm_cut": float(arm == "trail_cut"),
            "food_300": float(at.loc[300, "food"]),
            "food_330": float(at.loc[330, "food"]),
            "food_600": float(at.loc[600, "food"]),
            "future_collection": float(at.loc[330, "food"] - at.loc[600, "food"]),
            "persistence_prediction": float(
                np.clip(
                    (at.loc[271, "food"] - at.loc[300, "food"]) / 29 * 270,
                    0,
                    at.loc[330, "food"],
                )
            ),
            "carrying_fraction_330": float(at.loc[330, "carrying"] / 125),
            "noncarrier_patch_chemical_330": float(at.loc[330, "noncarrier_patch_chemical"]),
            "annulus_fraction_330": float(at.loc[330, "in_annulus"] / 125),
            "carrying_slope_301_330": slope(group, "carrying", 301, 330) / 125,
            "total_chemical_330": float(at.loc[330, "total_chemical"]),
            "mean_patch_chemical_330": float(at.loc[330, "total_chemical"] / field.chemical.size),
            "food_removal_slope_301_330": -slope(group, "food", 301, 330),
            "nest_fraction_330": float(at.loc[330, "in_nest"] / 125),
            **trail_metrics(field),
        }
        records.append(record)
    return pd.DataFrame(records)


def _loso_predictions(frame: pd.DataFrame, features: list[str]) -> pd.Series:
    predictions = pd.Series(index=frame.index, dtype=float)
    for seed in SEEDS:
        train = frame["seed"] != seed
        test = ~train
        scaler = StandardScaler().fit(frame.loc[train, features])
        model = Ridge(alpha=1).fit(
            scaler.transform(frame.loc[train, features]),
            frame.loc[train, "future_collection"],
        )
        raw = model.predict(scaler.transform(frame.loc[test, features]))
        predictions.loc[test] = np.clip(raw, 0, frame.loc[test, "food_330"])
    return predictions


def integrity(trajectories: pd.DataFrame, features: pd.DataFrame) -> dict[str, Any]:
    complete = len(trajectories) == 2 * 8 * 601
    sham = trajectories.loc[trajectories["arm"] == "sham"]
    cut = trajectories.loc[trajectories["arm"] == "trail_cut"]
    paired = sham.merge(cut, on=["seed", "tick"], suffixes=("_sham", "_cut"))
    scalar = list(RAW_COLUMNS.values())
    pre = paired["tick"] <= 300
    identical = all(
        np.allclose(paired.loc[pre, f"{column}_sham"], paired.loc[pre, f"{column}_cut"])
        for column in scalar
    )
    population = trajectories["population"].eq(125).all()
    tick_300_food = paired.loc[paired["tick"] == 300, "food_sham"].equals(
        paired.loc[paired["tick"] == 300, "food_cut"]
    )
    # Keep the original recorded-state gate. The intervening standard step
    # includes diffusion, but substituting the literal zero assignment after
    # observing this failure would change the frozen decision boundary.
    at_301 = paired.loc[paired["tick"] == 301].copy()
    removal_fraction = 1 - at_301["annulus_chemical_cut"] / at_301[
        "annulus_chemical_sham"
    ].replace(0, np.nan)
    cut_features = features.loc[features["arm"] == "trail_cut"]
    food_remaining_count = int((cut_features["food_330"] > 0).sum())
    future_collection_count = int((cut_features["future_collection"] > 0).sum())
    scope_text = Path(__file__).with_name("behaviorspace.xml").read_text(encoding="utf-8")
    scope_frozen = scope_text.count("ask patches with [distancexy 0 0 &gt;= 8") == 1
    removal_gate = bool(removal_fraction.notna().all() and (removal_fraction >= 0.80).all())
    gates = {
        "complete_trajectories": complete,
        "paired_identical_through_300": identical,
        "population_preserved": bool(population),
        "paired_tick_300_food": bool(tick_300_food),
        "intervention_scope_frozen": scope_frozen,
        "annulus_removal_all_eight": removal_gate,
        "cut_food_remaining_at_least_six": food_remaining_count >= 6,
        "cut_future_collection_at_least_six": future_collection_count >= 6,
    }
    return {
        "passed": all(gates.values()),
        "gates": gates,
        "minimum_annulus_removal_fraction": float(removal_fraction.min()),
        "cut_food_remaining_count": food_remaining_count,
        "cut_future_collection_count": future_collection_count,
    }


def score(features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    predictions = features[["arm", "seed", "future_collection", "food_330"]].copy()
    predictions["persistence"] = features["persistence_prediction"]
    predictions["primary"] = _loso_predictions(features, BASE)
    for scale, columns in SCALE_FEATURES.items():
        predictions[scale] = _loso_predictions(features, BASE + columns)
    models = ["persistence", "primary", *SCALE_FEATURES]
    score_rows = [
        {
            "model": model,
            "mae": mean_absolute_error(predictions["future_collection"], predictions[model]),
        }
        for model in models
    ]
    scores = pd.DataFrame(score_rows)
    mae = scores.set_index("model")["mae"]
    seed_errors = predictions.groupby("seed").apply(
        lambda group: pd.Series(
            {model: float(np.mean(np.abs(group[model] - group["future_collection"]))) for model in models}
        ),
        include_groups=False,
    )
    trail_seed_wins = {
        other: int((seed_errors["trail"] < seed_errors[other]).sum())
        for other in ("local", "colony")
    }
    mesoscopic_pass = bool(
        mae["trail"] <= 0.85 * min(mae["primary"], mae["persistence"])
        and mae["trail"] <= 0.90 * min(mae["local"], mae["colony"])
        and min(trail_seed_wins.values()) >= 6
    )
    simpler_passes: list[str] = []
    for candidate in ("local", "colony"):
        others = [name for name in ("local", "colony", "trail") if name != candidate]
        wins = min(int((seed_errors[candidate] < seed_errors[other]).sum()) for other in others)
        if mae[candidate] <= 0.85 * min(mae["primary"], mae["persistence"]) and wins >= 6:
            simpler_passes.append(candidate)
    decision = (
        "promote-mesoscopic-trail"
        if mesoscopic_pass
        else f"simpler-scale-winner:{simpler_passes[0]}"
        if len(simpler_passes) == 1
        else "abstain-no-go"
    )
    summary = {
        "decision": decision,
        "mesoscopic_pass": mesoscopic_pass,
        "simpler_passes": simpler_passes,
        "mae": {key: float(value) for key, value in mae.items()},
        "trail_seed_wins": trail_seed_wins,
    }
    return predictions, seed_errors.reset_index(), summary


def predictions_complete_and_bounded(predictions: pd.DataFrame) -> bool:
    models = ["persistence", "primary", *SCALE_FEATURES]
    exactly_once = (
        len(predictions) == 16
        and not predictions.duplicated(["arm", "seed"]).any()
        and set(predictions["seed"]) == set(SEEDS)
        and set(predictions["arm"]) == set(ARMS)
    )
    bounded = all(
        predictions[model].between(0, predictions["food_330"], inclusive="both").all()
        for model in models
    )
    return bool(exactly_once and predictions[models].notna().all().all() and bounded)


def analyze(output: Path) -> dict[str, Any]:
    trajectories = pd.concat(
        [read_behaviorspace(output / filename, arm) for arm, filename in ARMS.items()],
        ignore_index=True,
    )
    features = build_features(trajectories)
    integrity_result = integrity(trajectories, features)
    predictions, seed_errors, scoring = score(features)
    predictions_complete = predictions_complete_and_bounded(predictions)
    integrity_result["gates"]["predictions_complete_and_bounded"] = predictions_complete
    integrity_result["passed"] = all(integrity_result["gates"].values())
    decision = scoring["decision"] if integrity_result["passed"] else "stop-integrity-failure"
    summary = {"decision": decision, "integrity": integrity_result, "scoring": scoring}
    trajectories.to_csv(output / "trajectory.csv", index=False)
    features.to_csv(output / "scale_features.csv", index=False)
    predictions.to_csv(output / "predictions.csv", index=False)
    seed_errors.to_csv(output / "held_seed_errors.csv", index=False)
    pd.DataFrame(
        [{"model": model, "mae": mae} for model, mae in scoring["mae"].items()]
    ).to_csv(output / "scores.csv", index=False)
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (output / "result.md").write_text(_result_markdown(summary), encoding="utf-8")
    return summary


def _result_markdown(summary: dict[str, Any]) -> str:
    integrity_result = summary["integrity"]
    scoring = summary["scoring"]
    score_lines = "\n".join(
        f"| {model} | {mae:.3f} |" for model, mae in scoring["mae"].items()
    )
    gate_lines = "\n".join(
        f"- {name}: {'PASS' if passed else 'FAIL'}"
        for name, passed in integrity_result["gates"].items()
    )
    return f"""# P7-004 Ants trail-scale perturbation screen — results

**Decision: {summary['decision']}.**

## Frozen integrity gates

{gate_lines}

The minimum matched annulus removal at the first recorded post-cut checkpoint
was {integrity_result['minimum_annulus_removal_fraction']:.3f}. Cut arms with food
remaining at tick 330: {integrity_result['cut_food_remaining_count']}/8. Cut
arms with later collection: {integrity_result['cut_future_collection_count']}/8.

## Held-seed prediction

| Model | MAE (food units) |
|---|---:|
{score_lines}

The trail scale beat the local model on
{scoring['trail_seed_wins']['local']}/8 held seeds and the colony model on
{scoring['trail_seed_wins']['colony']}/8. Mesoscopic promotion gate:
{'PASS' if scoring['mesoscopic_pass'] else 'FAIL'}.

## Claim boundary

This is a Level 1 task-conditioned screen of explicitly authored foraging after
a fixed field cut. It is not generic representation-selection evidence and does
not establish an inferred goal, competence, causal control value, or V4
completion. The frozen conditional branch controls the next decision.
"""
