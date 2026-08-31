"""Parse observable P7-002 NetLogo trajectories for analysis and visualization."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

INFECTED = "count turtles with [infected?]"
RESISTANT = "count turtles with [resistant?]"
NODE_STATE = (
    "map [t -> (list ([who] of t) (precision ([xcor] of t) 3) "
    "(precision ([ycor] of t) 3) ([infected?] of t) ([resistant?] of t) "
    "([count link-neighbors] of t))] sort turtles"
)
NEIGHBORS = "map [t -> [sort [who] of link-neighbors] of t] sort turtles"
NODE_PATTERN = re.compile(
    r"\[(-?\d+) (-?[\d.]+) (-?[\d.]+) (true|false) (true|false) (\d+)\]"
)
NEIGHBOR_PATTERN = re.compile(r"\[([0-9 ]*)\]")


def _column(frame: pd.DataFrame, name: str) -> pd.Series:
    selected = frame.loc[:, name]
    return selected.iloc[:, -1] if isinstance(selected, pd.DataFrame) else selected


def read_behaviorspace(path: Path, arm: str) -> pd.DataFrame:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise ValueError(f"{path} has no BehaviorSpace table header") from error
    headers = rows[header_index]
    data = [row for row in rows[header_index + 1 :] if row and any(value.strip() for value in row)]
    if not data or any(len(row) != len(headers) for row in data):
        raise ValueError(f"{path} has no rectangular BehaviorSpace data")
    raw = pd.DataFrame(data, columns=headers)
    required = {"[run number]", "ticks", INFECTED, RESISTANT, NODE_STATE, NEIGHBORS}
    if missing := required - set(raw):
        raise ValueError(f"{path} lacks required P7-002 metrics: {sorted(missing)}")
    return pd.DataFrame(
        {
            "arm": arm,
            "seed_index": _column(raw, "[run number]").astype(int),
            "tick": _column(raw, "ticks").astype(float).round().astype(int),
            "infected": _column(raw, INFECTED).astype(int),
            "resistant": _column(raw, RESISTANT).astype(int),
            "node_state": _column(raw, NODE_STATE),
            "neighbors": _column(raw, NEIGHBORS),
        }
    ).sort_values(["seed_index", "tick"])


def parse_nodes(raw: str) -> pd.DataFrame:
    records = NODE_PATTERN.findall(raw)
    if not records:
        raise ValueError("Node-state reporter did not contain parseable nodes")
    return pd.DataFrame(
        [
            {
                "who": int(who),
                "x": float(x),
                "y": float(y),
                "infected": infected == "true",
                "resistant": resistant == "true",
                "degree": int(degree),
            }
            for who, x, y, infected, resistant, degree in records
        ]
    )


def parse_edges(raw: str) -> list[tuple[int, int]]:
    inner = raw[1:-1]
    neighbor_lists = [
        [int(value) for value in group.split()] if group.strip() else []
        for group in NEIGHBOR_PATTERN.findall(inner)
    ]
    edges = {
        tuple(sorted((who, neighbor)))
        for who, neighbors in enumerate(neighbor_lists)
        for neighbor in neighbors
        if who != neighbor
    }
    return sorted(edges)


@dataclass(frozen=True)
class NetworkDataset:
    trajectories: pd.DataFrame
    snapshots: dict[tuple[str, int, int], pd.DataFrame]
    edges: dict[tuple[str, int], list[tuple[int, int]]]

    @property
    def arms(self) -> list[str]:
        return list(dict.fromkeys(self.trajectories["arm"]))

    @property
    def runs(self) -> list[int]:
        return sorted(self.trajectories["seed_index"].unique())

    @property
    def max_tick(self) -> int:
        return int(self.trajectories["tick"].max())

    def snapshot(self, arm: str, run: int, tick: int) -> pd.DataFrame:
        key = (arm, run, tick)
        if key not in self.snapshots:
            raise KeyError(f"No exact snapshot for {arm=} {run=} {tick=}")
        return self.snapshots[key]

    def available_ticks(self, arm: str, run: int) -> list[int]:
        return sorted(
            tick
            for candidate_arm, candidate_run, tick in self.snapshots
            if candidate_arm == arm and candidate_run == run
        )


def load_dataset(
    directory: Path,
    arm_files: dict[str, str],
    *,
    run_indices: list[int] | None = None,
    snapshot_stride: int = 1,
) -> NetworkDataset:
    frames: list[pd.DataFrame] = []
    snapshots: dict[tuple[str, int, int], pd.DataFrame] = {}
    edges: dict[tuple[str, int], list[tuple[int, int]]] = {}
    for arm, filename in arm_files.items():
        frame = read_behaviorspace(directory / filename, arm)
        if run_indices is not None:
            frame = frame[frame["seed_index"].isin(run_indices)]
        frames.append(frame.drop(columns=["node_state", "neighbors"]))
        snapshot_frame = frame[
            frame["tick"].mod(snapshot_stride).eq(0) | frame["tick"].isin([19, 20, 21])
        ]
        snapshot_frame = pd.concat(
            [snapshot_frame, frame.groupby("seed_index", as_index=False).tail(1)]
        ).drop_duplicates(["seed_index", "tick"])
        for row in snapshot_frame.itertuples(index=False):
            snapshots[(arm, row.seed_index, row.tick)] = parse_nodes(row.node_state)
        for seed_index, group in frame.groupby("seed_index"):
            edges[(arm, int(seed_index))] = parse_edges(str(group.iloc[0]["neighbors"]))
    return NetworkDataset(
        trajectories=pd.concat(frames, ignore_index=True), snapshots=snapshots, edges=edges
    )


def validate_matched_preintervention(dataset: NetworkDataset, checkpoint: int = 20) -> None:
    baseline = dataset.arms[0]
    for run in dataset.runs:
        base = dataset.trajectories.loc[
            (dataset.trajectories["arm"] == baseline)
            & (dataset.trajectories["seed_index"] == run)
            & (dataset.trajectories["tick"] <= checkpoint),
            ["tick", "infected", "resistant"],
        ].reset_index(drop=True)
        for arm in dataset.arms[1:]:
            candidate = dataset.trajectories.loc[
                (dataset.trajectories["arm"] == arm)
                & (dataset.trajectories["seed_index"] == run)
                & (dataset.trajectories["tick"] <= checkpoint),
                ["tick", "infected", "resistant"],
            ].reset_index(drop=True)
            if not candidate.equals(base):
                raise ValueError(f"{arm} run {run} is not matched to baseline through tick 20")
            if dataset.edges[(arm, run)] != dataset.edges[(baseline, run)]:
                raise ValueError(f"{arm} run {run} changes network topology before intervention")
            common_ticks = set(dataset.available_ticks(baseline, run)).intersection(
                dataset.available_ticks(arm, run)
            )
            for tick in sorted(value for value in common_ticks if value <= checkpoint):
                base_nodes = dataset.snapshot(baseline, run, tick).sort_values("who").reset_index(drop=True)
                candidate_nodes = (
                    dataset.snapshot(arm, run, tick).sort_values("who").reset_index(drop=True)
                )
                if not candidate_nodes.equals(base_nodes):
                    raise ValueError(
                        f"{arm} run {run} changes node state before intervention at tick {tick}"
                    )
