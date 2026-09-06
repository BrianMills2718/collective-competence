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


def test_empty_and_singleton_return_their_pinned_degenerate_values():
    """The degenerate cases have conventions, and the conventions are the claim.

    This was written as `..._do_not_raise`: it called each function and discarded
    the result, so it passed for any return value at all, including one that
    silently changed. What matters about the empty and singleton cases is not
    that they survive but *what they decide* -- an empty observation has no
    cluster and no order, so both fractions are 0.0, while a single element is
    trivially one whole cluster and trivially sorted. Those two rows differ, and
    a change to either would have gone unnoticed.
    """
    expected = {
        (): {
            boundary_length: 0.0,
            unlike_neighbor_fraction: 0.0,
            largest_cluster_fraction: 0.0,
            sortedness_value: 0.0,
            inversions: 0.0,
        },
        (4,): {
            boundary_length: 0.0,
            unlike_neighbor_fraction: 0.0,
            largest_cluster_fraction: 1.0,
            sortedness_value: 1.0,
            inversions: 0.0,
        },
    }
    for values, wanted in expected.items():
        for fn, value in wanted.items():
            assert fn(obs(list(values))) == value, (
                f"{fn.__name__} on {list(values)!r}"
            )


def test_sorted_prefix_fraction_measures_only_the_run_from_position_zero():
    from src.experiments.sorting.representations import sorted_prefix_fraction

    assert sorted_prefix_fraction(obs([0, 1, 2, 3])) == 1.0
    assert sorted_prefix_fraction(obs([0, 1, 9, 2, 3])) == pytest.approx(3 / 5)
    assert sorted_prefix_fraction(obs([5, 0, 1, 2, 3])) == pytest.approx(1 / 5)
    # A long run in the middle is worth nothing to an insertion cell, which is
    # exactly why this is not largest_cluster_fraction.
    assert largest_cluster_fraction(obs([5, 0, 1, 2, 3])) == pytest.approx(4 / 5)
    assert sorted_prefix_fraction(obs([])) == 0.0
