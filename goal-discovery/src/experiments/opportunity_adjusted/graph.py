"""Translate local sorting actions into an off-the-shelf NetworkX state graph."""

from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, cast

import networkx as nx

from src.experiments.sorting.model import Algotype, Cell, Freeze, SortingWorld

CellState = tuple[int, int, str, str, int]
WorldState = tuple[CellState, ...]
GOAL_NODE = ("__sorted_goal__",)


class _FixedLook:
    """Small RNG substitute that exposes one frozen bubble-side observation."""

    def __init__(self, *, right: bool) -> None:
        self._value = 0.0 if right else 1.0

    def random(self) -> float:
        return self._value


@dataclass(frozen=True)
class Opportunity:
    reachable: bool
    shortest_activations: int | None
    graph_nodes: int
    graph_edges: int


def encode(world: SortingWorld) -> WorldState:
    return tuple(
        (
            cell.cell_id,
            cell.value,
            cell.algotype,
            cell.freeze.value,
            cell.ideal_position,
        )
        for cell in world.cells
    )


def decode(state: WorldState) -> SortingWorld:
    cells = [
        Cell(
            cell_id=cell_id,
            value=value,
            algotype=cast(Algotype, algotype),
            freeze=Freeze(freeze),
            ideal_position=ideal_position,
        )
        for cell_id, value, algotype, freeze, ideal_position in state
    ]
    world = SortingWorld(cells=cells, order="index", seed=0)
    world.rng = random.Random(0)
    return world


def values(state: WorldState) -> tuple[int, ...]:
    return tuple(cell[1] for cell in state)


def _activate(state: WorldState, position: int, *, look_right: bool | None) -> WorldState:
    world = decode(state)
    cell = world.cells[position]
    if cell.algotype == "bubble":
        if look_right is None:
            raise ValueError("bubble activation requires an explicit observation side")
        world.rng = cast(Any, _FixedLook(right=look_right))
    world._RULES[cell.algotype](world, position)
    return encode(world)


def successors(state: WorldState) -> Iterator[WorldState]:
    """Yield distinct state-changing outcomes of one allowed cell activation."""

    candidates: set[WorldState] = set()
    for position, cell_state in enumerate(state):
        if Freeze(cell_state[3]) is not Freeze.NONE:
            continue
        algotype = cell_state[2]
        looks: tuple[bool | None, ...] = (False, True) if algotype == "bubble" else (None,)
        for look_right in looks:
            candidate = _activate(state, position, look_right=look_right)
            if candidate != state:
                candidates.add(candidate)
    yield from sorted(candidates)


def build_graph(initial: SortingWorld) -> nx.DiGraph:
    """Build the complete finite graph reachable by asynchronous local activations."""

    start = encode(initial)
    graph = nx.DiGraph()
    graph.add_nodes_from((start, GOAL_NODE))
    frontier = [start]
    expanded: set[WorldState] = set()
    while frontier:
        state = frontier.pop()
        if state in expanded:
            continue
        expanded.add(state)
        if values(state) == tuple(sorted(values(state))):
            graph.add_edge(state, GOAL_NODE)
        for successor in successors(state):
            graph.add_edge(state, successor)
            if successor not in expanded:
                frontier.append(successor)
    return graph


def opportunity(initial: SortingWorld) -> Opportunity:
    """Use NetworkX reachability and path length on the generated state graph."""

    start = encode(initial)
    graph = build_graph(initial)
    reachable = nx.has_path(graph, start, GOAL_NODE)
    shortest = nx.shortest_path_length(graph, start, GOAL_NODE) - 1 if reachable else None
    return Opportunity(
        reachable=reachable,
        shortest_activations=shortest,
        graph_nodes=graph.number_of_nodes() - 1,
        graph_edges=graph.number_of_edges(),
    )
