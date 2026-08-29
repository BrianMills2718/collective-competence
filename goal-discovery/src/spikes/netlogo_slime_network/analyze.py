"""Convert P5-001 patch fields to skeleton graphs and score frozen gates."""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler

ARMS = {
    "checkpoint": "p5-001-checkpoint.csv",
    "sham": "p5-001-sham.csv",
    "relocate": "p5-001-relocate.csv",
}
BOOSTS = (0, 20, 40, 60, 80)
SEEDS = tuple(range(701, 707))
FIELD_METRIC = "[(list pxcor pycor cp-fluid wall? food)] of patches"
FIELD_PATTERN = re.compile(r"\[\s*(-?\d+)\s+(-?\d+)\s+([^\s\]]+)\s+(true|false)\s+([^\s\]]+)\s*\]")
SCALAR_COLUMNS = {
    "count cytoplasm": "cytoplasm_count",
    "count cytoplasm with [carrying-signal > 0]": "signal_carriers",
    "sum [cp-fluid] of patches": "total_fluid",
}
NETWORK_COLUMNS = [
    "skeleton_length",
    "endpoints",
    "branch_points",
    "attachment_distance",
    "connected",
    "path_length",
    "organization_score",
]


@dataclass(frozen=True)
class Field:
    cp: np.ndarray
    wall: np.ndarray
    food: np.ndarray


@dataclass(frozen=True)
class NetworkSurface:
    metrics: dict[str, float | bool]
    active: np.ndarray
    skeleton: np.ndarray


def read_behaviorspace(
    path: Path,
    arm: str,
    *,
    boosts: tuple[int, ...] = BOOSTS,
    seeds: tuple[int, ...] = SEEDS,
    expected_tick: int | None = None,
) -> pd.DataFrame:
    csv.field_size_limit(sys.maxsize)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise ValueError(f"{path} has no BehaviorSpace header") from error
    headers = rows[header_index]
    data = [row for row in rows[header_index + 1 :] if row and any(value.strip() for value in row)]
    expected_rows = len(boosts) * len(seeds)
    if len(data) != expected_rows or any(len(row) != len(headers) for row in data):
        raise ValueError(f"{path} does not contain {expected_rows} rectangular final rows")
    frame = pd.DataFrame(data, columns=headers)
    required = {"[run number]", "food-signal-boost", "ticks", FIELD_METRIC, *SCALAR_COLUMNS}
    if missing := required - set(frame):
        raise ValueError(f"{path} lacks fields: {sorted(missing)}")
    frame["run_number"] = frame["[run number]"].astype(int)
    frame["boost"] = frame["food-signal-boost"].astype(float).round().astype(int)
    frame["tick"] = frame["ticks"].astype(float).round().astype(int)
    frame["seed"] = min(seeds) + ((frame["run_number"] - 1) % len(seeds))
    frame["arm"] = arm
    for source, target in SCALAR_COLUMNS.items():
        frame[target] = frame[source].astype(float)
    expected_tick = expected_tick or (300 if arm == "checkpoint" else 600)
    if set(frame["boost"]) != set(boosts) or set(frame["seed"]) != set(seeds):
        raise ValueError(f"{path} does not match frozen boosts/seeds")
    if not frame["tick"].eq(expected_tick).all():
        raise ValueError(f"{path} stopped at an unexpected tick")
    if frame.groupby(["boost", "seed"]).size().ne(1).any():
        raise ValueError(f"{path} has duplicate or missing design cells")
    return frame[
        [
            "arm",
            "run_number",
            "boost",
            "seed",
            "tick",
            *SCALAR_COLUMNS.values(),
            FIELD_METRIC,
        ]
    ]


def parse_field(raw: str) -> Field:
    matches = FIELD_PATTERN.findall(raw)
    if len(matches) != 201 * 201:
        raise ValueError(f"expected 40,401 patch tuples, found {len(matches):,}")
    cp = np.zeros((201, 201), dtype=float)
    wall = np.zeros((201, 201), dtype=bool)
    food = np.zeros((201, 201), dtype=bool)
    for x_text, y_text, cp_text, wall_text, food_text in matches:
        x = int(x_text)
        y = int(y_text)
        row, column = 100 - y, x + 100
        cp[row, column] = float(cp_text)
        wall[row, column] = wall_text == "true"
        food[row, column] = float(food_text) > 0
    return Field(cp=cp, wall=wall, food=food)


def _pixel_to_xy(pixel: tuple[int, int]) -> tuple[int, int]:
    row, column = pixel
    return column - 100, 100 - row


def _nearest_node(nodes: np.ndarray, centroid: np.ndarray) -> tuple[tuple[int, int], float]:
    distances = np.linalg.norm(nodes - centroid, axis=1)
    index = int(np.argmin(distances))
    pixel = tuple(int(value) for value in nodes[index])
    return pixel, float(distances[index])


def field_to_network(field: Field) -> NetworkSurface:
    try:
        from skimage.filters import threshold_otsu
        from skimage.measure import label, regionprops
        from skimage.morphology import remove_small_objects, skeletonize
    except ImportError as error:
        raise RuntimeError("run `uv sync --extra network-analysis`") from error

    values = field.cp[~field.wall]
    if np.ptp(values) <= np.finfo(float).eps:
        active = np.zeros_like(field.wall)
    else:
        threshold = float(threshold_otsu(values))
        active = (field.cp > threshold) & ~field.wall
        active = remove_small_objects(active, max_size=8, connectivity=2)
    skeleton = skeletonize(active)
    pixels = np.argwhere(skeleton)
    food_labels = label(field.food, connectivity=1)
    foods = regionprops(food_labels)
    base: dict[str, float | bool] = {
        "active_area": float(active.sum()),
        "skeleton_length": float(len(pixels)),
        "endpoints": 0.0,
        "branch_points": 0.0,
        "attachment_distance": float("nan"),
        "connected": False,
        "path_length": float("nan"),
        "organization_score": 0.0,
        "food_components": float(len(foods)),
    }
    if len(pixels) == 0 or len(foods) != 2:
        return NetworkSurface(base, active, skeleton)

    graph = nx.Graph()
    pixel_set = {tuple(int(value) for value in pixel) for pixel in pixels}
    for pixel in pixel_set:
        graph.add_node(pixel)
        row, column = pixel
        for row_step in (-1, 0, 1):
            for column_step in (-1, 0, 1):
                if row_step == column_step == 0:
                    continue
                neighbor = (row + row_step, column + column_step)
                if neighbor in pixel_set:
                    graph.add_edge(pixel, neighbor, weight=math.hypot(row_step, column_step))
    degrees = dict(graph.degree())
    base["endpoints"] = float(sum(degree == 1 for degree in degrees.values()))
    base["branch_points"] = float(sum(degree >= 3 for degree in degrees.values()))
    centroids = [
        np.asarray(region.centroid) for region in sorted(foods, key=lambda item: item.centroid)
    ]
    attachments = [_nearest_node(pixels, centroid) for centroid in centroids]
    nodes = [item[0] for item in attachments]
    mean_attachment = float(np.mean([item[1] for item in attachments]))
    base["attachment_distance"] = mean_attachment
    connected = nx.has_path(graph, nodes[0], nodes[1])
    base["connected"] = connected
    if connected:
        path_length = float(nx.shortest_path_length(graph, nodes[0], nodes[1], weight="weight"))
        separation = float(np.linalg.norm(centroids[0] - centroids[1]))
        efficiency = separation / path_length if path_length > 0 else 0.0
        base["path_length"] = path_length
        base["organization_score"] = efficiency / (1 + mean_attachment / 10)
    return NetworkSurface(base, active, skeleton)


def extract_metrics(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[tuple[str, int, int], Field]]:
    records: list[dict[str, Any]] = []
    fields: dict[tuple[str, int, int], Field] = {}
    for _, row in frame.iterrows():
        field = parse_field(str(row[FIELD_METRIC]))
        surface = field_to_network(field)
        key = (str(row["arm"]), int(row["boost"]), int(row["seed"]))
        fields[key] = field
        records.append(
            {
                "arm": row["arm"],
                "boost": int(row["boost"]),
                "seed": int(row["seed"]),
                "tick": int(row["tick"]),
                "cytoplasm_count": float(row["cytoplasm_count"]),
                "signal_carriers": float(row["signal_carriers"]),
                "total_fluid": float(row["total_fluid"]),
                **surface.metrics,
            }
        )
    return pd.DataFrame(records), fields


def _ridge_score(frame: pd.DataFrame, features: list[str]) -> float:
    predictions = pd.Series(index=frame.index, dtype=float)
    for seed in SEEDS:
        train = frame["seed"] != seed
        test = ~train
        imputer = SimpleImputer(strategy="median").fit(frame.loc[train, features])
        train_values = imputer.transform(frame.loc[train, features])
        test_values = imputer.transform(frame.loc[test, features])
        scaler = StandardScaler().fit(train_values)
        model = Ridge(alpha=1).fit(
            scaler.transform(train_values), frame.loc[train, "organization_score"]
        )
        predictions.loc[test] = model.predict(scaler.transform(test_values))
    return float(mean_absolute_error(frame["organization_score"], predictions))


def _prediction_scores(metrics: pd.DataFrame) -> dict[str, Any]:
    checkpoint = metrics.loc[metrics["arm"] == "checkpoint"].copy()
    checkpoint = checkpoint.rename(
        columns={
            column: f"checkpoint_{column}"
            for column in ["total_fluid", "active_area", *NETWORK_COLUMNS]
        }
    )
    final = metrics.loc[metrics["arm"].isin(["sham", "relocate"])].copy()
    final["relocated"] = (final["arm"] == "relocate").astype(float)
    final = final.merge(checkpoint, on=["boost", "seed"], validate="many_to_one")
    null = ["boost", "relocated"]
    density = null + ["checkpoint_total_fluid", "checkpoint_active_area"]
    network = density + [f"checkpoint_{column}" for column in NETWORK_COLUMNS]
    scores = {
        "intervention_mae": _ridge_score(final, null),
        "density_mae": _ridge_score(final, density),
        "network_mae": _ridge_score(final, network),
    }

    rng_seeds = range(9100, 9199)
    shuffled_scores: list[float] = []
    checkpoint_network = [f"checkpoint_{column}" for column in NETWORK_COLUMNS]
    for rng_seed in rng_seeds:
        rng = np.random.default_rng(rng_seed)
        shuffled = final.copy()
        for boost in BOOSTS:
            rows = shuffled.loc[
                shuffled["boost"] == boost, ["seed", *checkpoint_network]
            ].drop_duplicates("seed")
            order = rng.permutation(len(rows))
            mapping = {
                int(seed): rows.iloc[source][checkpoint_network].to_numpy()
                for seed, source in zip(rows["seed"], order, strict=True)
            }
            for seed, values in mapping.items():
                mask = (shuffled["boost"] == boost) & (shuffled["seed"] == seed)
                shuffled.loc[mask, checkpoint_network] = values
        shuffled_scores.append(_ridge_score(shuffled, network))
    scores["shuffle_fifth_percentile_mae"] = float(np.percentile(shuffled_scores, 5))
    scores["shuffle_median_mae"] = float(np.median(shuffled_scores))
    scores["prediction_gate"] = bool(
        scores["network_mae"] <= 0.9 * min(scores["intervention_mae"], scores["density_mae"])
    )
    scores["shuffle_gate"] = bool(scores["network_mae"] < scores["shuffle_fifth_percentile_mae"])
    return {"scores": scores, "final": final, "shuffle_scores": shuffled_scores}


def _mechanism_scores(metrics: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    final = metrics.loc[metrics["arm"].isin(["sham", "relocate"])].pivot(
        index=["boost", "seed"], columns="arm", values="organization_score"
    )
    final["retention_ratio"] = np.where(
        final["sham"] > 0,
        (final["relocate"] / final["sham"]).clip(0, 1),
        0.0,
    )
    retention = final.reset_index()
    medians = retention.groupby("boost")["retention_ratio"].median().reindex(BOOSTS)
    positive_advantage = medians.drop(index=0) - medians.loc[0]
    best_boost = int(positive_advantage.idxmax())
    paired = retention.pivot(index="seed", columns="boost", values="retention_ratio")
    seeds_clearing = int((paired[best_boost] - paired[0] >= 0.15).sum())
    jumps = medians.diff().abs().dropna()
    largest_jump = float(jumps.max())
    upper = int(jumps.idxmax())
    lower = BOOSTS[BOOSTS.index(upper) - 1]
    valid = (metrics["skeleton_length"] > 0) & (metrics["food_components"] == 2)
    integrity_rate = float(valid.mean())
    gate = bool(
        integrity_rate >= 0.8
        and positive_advantage.loc[best_boost] >= 0.15
        and seeds_clearing >= 5
        and largest_jump >= 0.10
    )
    return retention, {
        "extraction_integrity_rate": integrity_rate,
        "boost_zero_median_retention": float(medians.loc[0]),
        "best_positive_boost": best_boost,
        "best_median_advantage": float(positive_advantage.loc[best_boost]),
        "seeds_clearing_paired_advantage": seeds_clearing,
        "largest_adjacent_median_jump": largest_jump,
        "candidate_boundary": float((lower + upper) / 2),
        "mechanism_gate": gate,
        "median_retention_by_boost": {str(boost): float(value) for boost, value in medians.items()},
    }


def _decision_figure(
    metrics: pd.DataFrame,
    fields: dict[tuple[str, int, int], Field],
    retention: pd.DataFrame,
    summary: dict[str, Any],
    path: Path,
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axis = axes[0, 0]
    for seed, group in retention.groupby("seed"):
        axis.plot(group["boost"], group["retention_ratio"], color="#9aa0a6", alpha=0.45)
    medians = retention.groupby("boost")["retention_ratio"].median()
    axis.plot(medians.index, medians.values, marker="o", color="#3c78d8", linewidth=3)
    axis.set(
        title="Relocation retention by signal boost", xlabel="food-signal-boost", ylabel="ratio"
    )
    axis.set_ylim(0, 1.05)
    axis.grid(alpha=0.2)

    prediction = summary["prediction"]
    axis = axes[0, 1]
    values = [prediction["intervention_mae"], prediction["density_mae"], prediction["network_mae"]]
    axis.bar(
        ["intervention", "density", "network"], values, color=["#999999", "#666666", "#3c78d8"]
    )
    axis.axhline(prediction["shuffle_fifth_percentile_mae"], color="#cc0000", linestyle="--")
    axis.set(title="Held-out late-score prediction", ylabel="MAE (lower is better)")
    axis.grid(axis="y", alpha=0.2)

    best_boost = int(summary["mechanism"]["best_positive_boost"])
    for axis, arm in zip(axes[1], ["sham", "relocate"], strict=True):
        field = fields[(arm, best_boost, 701)]
        surface = field_to_network(field)
        axis.imshow(field.cp, cmap="gray", origin="upper")
        overlay = np.ma.masked_where(~surface.skeleton, surface.skeleton)
        axis.imshow(overlay, cmap="autumn", alpha=0.9, origin="upper")
        food = np.argwhere(field.food)
        axis.scatter(food[:, 1], food[:, 0], s=8, color="#00cc44")
        axis.set_title(f"{arm.title()} · boost {best_boost} · seed 701")
        axis.axis("off")
    fig.suptitle(f"P5-001 decision: {summary['decision']}", fontsize=16)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def analyze(output: Path, *, model_present: bool = True) -> dict[str, Any]:
    raw = pd.concat(
        [read_behaviorspace(output / filename, arm) for arm, filename in ARMS.items()],
        ignore_index=True,
    )
    metrics, fields = extract_metrics(raw)
    retention, mechanism = _mechanism_scores(metrics)
    prediction_result = _prediction_scores(metrics)
    prediction = prediction_result["scores"]
    passed = bool(
        model_present
        and mechanism["mechanism_gate"]
        and prediction["prediction_gate"]
        and prediction["shuffle_gate"]
    )
    summary: dict[str, Any] = {
        "experiment": "P5-001",
        "decision": "promote" if passed else "no-go",
        "promoted": passed,
        "model_present": model_present,
        "mechanism": mechanism,
        "prediction": prediction,
    }
    metrics.to_csv(output / "network_metrics.csv", index=False)
    retention.to_csv(output / "retention.csv", index=False)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _decision_figure(metrics, fields, retention, summary, output / "decision.png")
    return summary
