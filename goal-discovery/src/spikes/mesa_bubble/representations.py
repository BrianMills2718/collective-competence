"""Minimal candidate representation reused by the Mesa compatibility spike."""

from __future__ import annotations

from itertools import pairwise

from .observe import Observation


def boundary_length(observation: Observation) -> float:
    """Number of adjacent descending pairs (the paper's Monotonicity Error)."""
    values = observation["values"]
    return float(sum(left > right for left, right in pairwise(values)))
