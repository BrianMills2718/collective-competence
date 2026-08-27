"""Representation correctness against hand-computed toy arrays."""

from __future__ import annotations

import pytest

from src.experiments.sorting.observe import Observation
from src.experiments.sorting.representations import (
    boundary_length,
    inversions,
    largest_cluster_fraction,
    sortedness_value,
    unlike_neighbor_fraction,
)


def obs(values: list[int]) -> Observation:
    return {
        "values": values,
        "frozen": ["none"] * len(values),
        "algotypes": ["bubble"] * len(values),
        "tick": 0,
        "steps": 0,
    }


@pytest.mark.parametrize(
    "values,expected",
    [([0, 1, 2, 3], 0), ([2, 1, 3], 1), ([3, 2, 1], 2), ([1, 0, 3, 2], 2)],
)
def test_boundary_length_counts_adjacent_descents(values, expected):
    assert boundary_length(obs(values)) == expected


def test_unlike_neighbor_fraction_normalises_by_pairs():
    assert unlike_neighbor_fraction(obs([3, 2, 1])) == pytest.approx(2 / 2)
    assert unlike_neighbor_fraction(obs([1, 0, 3, 2])) == pytest.approx(2 / 3)


@pytest.mark.parametrize(
    "values,expected",
    [([0, 1, 2, 3], 1.0), ([3, 2, 1], 1 / 3), ([0, 1, 5, 2, 3], 3 / 5), ([9], 1.0)],
)
def test_largest_cluster_fraction_is_the_longest_ascending_run(values, expected):
    assert largest_cluster_fraction(obs(values)) == pytest.approx(expected)


def test_sortedness_counts_cells_at_their_final_index():
    assert sortedness_value(obs([0, 1, 2])) == 1.0
    assert sortedness_value(obs([0, 2, 1])) == pytest.approx(1 / 3)
    assert sortedness_value(obs([2, 1, 0])) == pytest.approx(1 / 3)  # the middle one


def test_inversions_counts_all_out_of_order_pairs_not_only_adjacent():
    assert inversions(obs([3, 2, 1])) == 3  # boundary_length would say 2
    assert inversions(obs([0, 1, 2])) == 0


def test_a_sorted_array_is_the_zero_of_every_distance_measure():
    o = obs(list(range(12)))
    assert boundary_length(o) == 0
    assert unlike_neighbor_fraction(o) == 0
    assert inversions(o) == 0
    assert largest_cluster_fraction(o) == 1.0
    assert sortedness_value(o) == 1.0


def test_empty_and_singleton_do_not_raise():
    for values in ([], [4]):
        for fn in (boundary_length, unlike_neighbor_fraction, largest_cluster_fraction,
                   sortedness_value, inversions):
            fn(obs(values))
