"""Sorting, expressed on the substrate. This file is the substrate's gate.

`experiments/01-self-sorting/selfsort.py` is the founding experiment and the
previous shared contract could not express it -- its own docstring said sorting
was deliberately not ported, because sorting has no resource and no shared
signal. That is the failure this substrate exists to fix, so the claim "the
substrate expresses the founding experiment" is not made in prose here. It is
checked by `tests/test_lattice_reproduces_selfsort.py`, which runs both
implementations over the same seeds and requires identical trajectories.

Nothing in this file is a goal. `RULE_ASCEND` is a local preference over an
adjacent pair; that it produces a sorted line is a fact about the measurement,
not about any entity.
"""

from __future__ import annotations

import random
from collections.abc import Iterator

from ..core import Faults, Lattice, Window, build

# Local preferences, keyed by the acting entity. Each decides only whether the
# pair it is looking at should exchange.
RULE_ASCEND = lambda left, right: left > right      # noqa: E731
RULE_DESCEND = lambda left, right: left < right     # noqa: E731
RULE_ALWAYS = lambda left, right: True              # noqa: E731


def pairwise(preferences: dict[int, object]):
    """Lift per-entity pair preferences into a substrate rule.

    The substrate's rule signature is window-in, window-out; sorting's rule is a
    predicate over an ordered pair. This is the whole adaptation, and it is four
    lines, which is the point: if expressing sorting needed more than this the
    substrate would be the wrong shape.
    """

    def rule(before: Window, initiator: int) -> Window:
        left, right = before
        if left is None or right is None:
            return before
        return (right, left) if preferences[initiator](left, right) else before

    return rule


def make(n: int, seed: int, faults: Faults | None = None,
         n_type_b: int = 0, all_always: bool = False) -> tuple[Lattice, object]:
    """A shuffled line of n entities, and the rule they act under.

    The draw order -- shuffle, then the type-B sample only when there is one --
    is fixed here because it is part of every recorded trial. Changing it
    changes results that are already published.
    """
    rng = random.Random(seed)
    values = list(range(n))
    rng.shuffle(values)
    type_b = set(rng.sample(range(n), n_type_b)) if n_type_b else set()
    if all_always:
        preferences = {v: RULE_ALWAYS for v in range(n)}
    else:
        preferences = {v: (RULE_DESCEND if v in type_b else RULE_ASCEND)
                       for v in range(n)}
    lat = build(values, faults=faults, rng=rng)
    return lat, pairwise(preferences)


# --- Controllers. The varied dimension, and why it is not in the core. ---
#
# A controller drives the lattice. It is a generator so an experiment can stop
# it, perturb between steps, or run it against a budget without the controller
# knowing. Each one differs ONLY in which site acts next and whether it looks
# before acting -- and looking costs, which is what makes the difference
# between them measurable rather than stylistic.


def decentralized(lat: Lattice, rule, budget: int) -> Iterator[None]:
    """No coordinator. A uniformly chosen adjacent pair acts, and one of its two
    occupants initiates. Never halts and never declares victory."""
    while lat.ops < budget:
        lat.apply(lat.rng.randrange(lat.size - 1), rule)
        yield


def watchdog(lat: Lattice, rule, budget: int) -> Iterator[None]:
    """A coordinator sweeping left to right forever, reading before it acts.

    The read is charged and the act that follows is not, because they are the
    same operation seen twice. A watchdog therefore pays for every scan whether
    or not it finds anything, which is the cost of never concluding it is done.
    """
    while lat.ops < budget:
        for i in range(lat.size - 1):
            if lat.ops >= budget:
                return
            before = lat.read(i)
            left, right = before
            if left is not None and right is not None and left > right:
                lat.apply(i, rule, charge=False)
            yield


def closed(lat: Lattice, rule, budget: int) -> Iterator[None]:
    """The same coordinator, but it stops once a full pass finds nothing.

    Robust to action faults, and blind afterwards: a disturbance arriving after
    it halts is one it is not present for. That is a property of the controller,
    not a gap in the measurement.
    """
    while lat.ops < budget:
        found = False
        for i in range(lat.size - 1):
            if lat.ops >= budget:
                return
            before = lat.read(i)
            left, right = before
            if left is not None and right is not None and left > right:
                found = True
                lat.apply(i, rule, charge=False)
            yield
        if not found:
            return


CONTROLLERS = {
    "decentralized": decentralized,
    "watchdog": watchdog,
    "closed": closed,
}
