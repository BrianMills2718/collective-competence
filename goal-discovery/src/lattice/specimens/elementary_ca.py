"""An elementary cellular automaton, on the same substrate as sorting.

This file exists to make one claim checkable. Laboratory spec §28 says the
substrate should be *"a discrete interacting dynamical system with local state
and explicit transition rules"* of which *"a standard cellular automaton is a
particularly constrained case."* Here that constrained case is instantiated on
the same `Lattice`, operation currency and observation contract as sorting, but
under the substrate's other payload semantics:

    sorting          conserving=True   -> mobile entity identities
    elementary CA    conserving=False  -> rewritable local site state

The CA therefore has no entity records: repeated 0/1 values are cell state, not
identities. `tests/test_lattice_expresses_both.py` checks Rule 90 against the
Sierpinski triangle, whose rows are binomial coefficients mod 2 -- ground truth
computed independently of this code.
"""

from __future__ import annotations

import random

from ..core import Lattice, Window, build, step_synchronous


def wolfram(number: int):
    """Wolfram's numbering: bit k of `number` is the output for neighbourhood k.

    The neighbourhood (left, centre, right) reads as a 3-bit integer, so
    `number` names all eight outputs at once. Rule 110 is Turing-complete;
    Rule 90 draws the Sierpinski triangle; Rule 30 is the standard chaotic one.
    """
    if not 0 <= number <= 255:
        raise ValueError("an elementary rule is numbered 0-255")

    def rule(before: Window, initiator: int) -> Window:
        left, centre, right = before
        index = (left or 0) * 4 + (centre or 0) * 2 + (right or 0)
        out = (number >> index) & 1
        return (left, out, right)

    return rule


def make(number: int, size: int = 65, seed: int | None = None,
         single_seed_cell: bool = True) -> tuple[Lattice, object]:
    """A ring of `size` binary local-state cells under elementary rule `number`.

    A ring, because a line has no complete neighbourhood at its ends and a
    boundary convention is a modelling choice this does not need to make.
    """
    if single_seed_cell:
        cells = [0] * size
        cells[size // 2] = 1
    else:
        rng = random.Random(seed if seed is not None else 0)
        cells = [rng.randrange(2) for _ in range(size)]
    lat = build(cells, radius=1, ring=True, conserving=False, centred=True)
    return lat, wolfram(number)


def evolve(lat: Lattice, rule, steps: int) -> list[tuple[int, ...]]:
    """Run synchronously and return every configuration, the first included."""
    rows = [tuple(lat.occupants)]
    for _ in range(steps):
        step_synchronous(lat, rule)
        rows.append(tuple(lat.occupants))
    return rows
