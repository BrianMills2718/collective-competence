"""Candidate representations for experiment 001. FROZEN SET, version below.

These are declared before confirmatory testing and are not to be extended,
retuned, or reweighted on the strength of a confirmation result. Adding one
means a new version string and a new discovery pass.

Naming note. The brief names three day-one measures -- unlike-neighbour
fraction, boundary length, largest-cluster fraction -- in the vocabulary of a
2-D grid of cell types. Zhang/Goldstein/Levin is a 1-D array of distinct
numbers, so each is implemented as its direct 1-D analogue and the mapping is
recorded here rather than left for a reader to guess:

    unlike-neighbour fraction  ->  adjacent pairs out of ascending order,
                                   as a fraction of all adjacent pairs
    boundary length            ->  the same quantity unnormalised, which is
                                   also the paper's Monotonicity Error
    largest-cluster fraction   ->  longest run already in ascending order,
                                   as a fraction of the array

`sortedness_value` is the paper's own headline measure and is included so
results can be read against it directly.
"""

from __future__ import annotations

from collections.abc import Callable

from src.experiments.sorting.observe import Observation

REPRESENTATION_SET_VERSION = "sorting-reps-v2"


def boundary_length(obs: Observation) -> float:
    """Paper's Monotonicity Error: number of adjacent pairs out of order.

    Instantaneous. Units: count, 0..n-1. Tests whether disorder is localised at
    a shrinking number of seams.
    """
    v = obs["values"]
    return float(sum(1 for i in range(len(v) - 1) if v[i] > v[i + 1]))


def unlike_neighbor_fraction(obs: Observation) -> float:
    """Boundary length normalised by array size. Instantaneous, 0..1.

    Comparable across array sizes, which the raw count is not.
    """
    n = len(obs["values"])
    return boundary_length(obs) / (n - 1) if n > 1 else 0.0


def largest_cluster_fraction(obs: Observation) -> float:
    """Longest ascending run, as a fraction of the array. Instantaneous, 0..1.

    Distinguishes 'nearly sorted with one displaced element' from 'globally
    mixed', which boundary length alone cannot.
    """
    v = obs["values"]
    if not v:
        return 0.0
    best = run = 1
    for i in range(1, len(v)):
        run = run + 1 if v[i] >= v[i - 1] else 1
        best = max(best, run)
    return best / len(v)


def sorted_prefix_fraction(obs: Observation) -> float:
    """Longest ascending run *starting at position 0*, divided by N. 0..1.

    Added for the confirmation phase and declared in
    docs/hypotheses/001_sorting_confirmation.md before use. Validation found
    `boundary_length` insufficient for the insertion algotype, whose cells move
    only when everything to their left is already sorted: prefix length governs
    its rate and no measure in v1 could see it.

    Distinct from `largest_cluster_fraction`, which finds the longest run
    anywhere. A run in the middle is worth nothing to an insertion cell.
    """
    v = obs["values"]
    if not v:
        return 0.0
    run = 1
    for i in range(1, len(v)):
        if v[i] < v[i - 1]:
            break
        run += 1
    return run / len(v)


def sortedness_value(obs: Observation) -> float:
    """Paper's Sortedness Value: fraction of cells sitting at the index they
    would occupy in the fully sorted array. Instantaneous, 0..1."""
    v = obs["values"]
    if not v:
        return 0.0
    target = sorted(v)
    return sum(1 for a, b in zip(v, target) if a == b) / len(v)


def inversions(obs: Observation) -> float:
    """Total pairs out of order, not only adjacent ones. Instantaneous,
    0..n(n-1)/2. A global distance where boundary length is a local one."""
    v = obs["values"]
    return float(sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > v[j]))


REPRESENTATIONS: dict[str, Callable[[Observation], float]] = {
    "boundary_length": boundary_length,
    "unlike_neighbor_fraction": unlike_neighbor_fraction,
    "largest_cluster_fraction": largest_cluster_fraction,
    "sorted_prefix_fraction": sorted_prefix_fraction,
    "sortedness_value": sortedness_value,
    "inversions": inversions,
}

# name -> (family, units, history window)
REPRESENTATION_METADATA = {
    "boundary_length": ("instantaneous", "count", 0),
    "unlike_neighbor_fraction": ("instantaneous", "fraction", 0),
    "largest_cluster_fraction": ("instantaneous", "fraction", 0),
    "sorted_prefix_fraction": ("instantaneous", "fraction", 0),
    "sortedness_value": ("instantaneous", "fraction", 0),
    "inversions": ("instantaneous", "count", 0),
}


def evaluate(obs: Observation) -> dict[str, float]:
    return {name: fn(obs) for name, fn in REPRESENTATIONS.items()}
