"""Observation boundary for the Mesa bubble-sort spike."""

from __future__ import annotations

from typing import TypedDict

from .model import MesaBubbleModel


class Observation(TypedDict):
    values: list[int]
    frozen: list[str]
    cell_ids: list[int]
    tick: int
    steps: int


def observe(model: MesaBubbleModel) -> Observation:
    return {
        "values": [cell.value for cell in model.line],
        "frozen": [cell.freeze.value for cell in model.line],
        "cell_ids": [cell.cell_id for cell in model.line],
        "tick": model.tick,
        "steps": model.sorting_steps,
    }
