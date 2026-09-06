"""One substrate for the discovery phase: a generalized discrete interacting system.

Laboratory spec §28 specifies *"a discrete interacting dynamical system with
local state and explicit transition rules,"* of which *"a standard cellular
automaton is a particularly constrained case"*, and §29 starts it at 1-D. The
owner reached the same specification independently: *"basically like cellular
automata but probably more generalized"*. This module is that, and nothing more.

Five commitments, each of which the previous `src/substrate/` broke and each of
which the founding sorting experiment needs.

**The goal is never inside the system.** No site, entity or rule holds a target.
A measurement is a function FROM a lattice, defined in `observe.py`, and the
lattice cannot read it. This is what makes goal *discovery* possible at all: an
analyst who can only watch has nothing privileged to find.

**One currency prices everything.** Every rule evaluation costs one operation,
whoever asks for it. A coordinator that scans without acting still pays, which
is what makes "robustness is bought, not free" a measurement rather than an
opinion.

**The schedule is a dial, not a decision.** Which site acts next is supplied by
the experiment. Synchronous update makes this a classic cellular automaton;
random site selection makes it the decentralized sorting rule; a sweep makes it
a coordinator. The sharpest result in this repository is a scheduler result, so
the scheduler cannot be baked into the container.

**Faults are first-class and per-entity.** `dead`, `frozen`, `unreliable` and a
global `p_fail`, applied at the moment of action, not simulated by an experiment
on top.

**Entities are mobile and carry identity.** This is the one real generalization
beyond a cellular automaton, and sorting is why: a sorting agent's rule and its
defects travel with the value, not with the position it happens to occupy. A
classic CA is the special case where entities never move and a rule rewrites
only the centre of its window.

What is deliberately absent, because no queued experiment needs it yet and the
last contract was generalized backwards from failures rather than forwards from
goals: two dimensions, non-local coupling, entity creation and destruction, and
any shared scalar. Add capability when a concrete, otherwise-unexpressible
experiment requires it, and say which one.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entity:
    """A mobile occupant of a site.

    `ident` is the stable identity that rules and faults key on; it survives
    movement. `memory` is the spec's *"persistent internal variables"* and is
    empty until an experiment needs it -- an entity with memory is a different
    capability claim than an entity without, and the register tracks which.
    """

    ident: int
    memory: dict[str, Any] = field(default_factory=dict)


@dataclass
class Faults:
    """Per-entity defects, applied at the moment of action.

    `p_fail` is the population-wide action failure rate. `unreliable` overrides
    it per entity. `frozen` entities never act, but may still be acted upon.
    `dead` entities block any interaction touching them, including one they did
    not initiate.
    """

    p_fail: float = 0.0
    unreliable: dict[int, float] = field(default_factory=dict)
    frozen: set[int] = field(default_factory=set)
    dead: set[int] = field(default_factory=set)

    def copy(self) -> "Faults":
        return Faults(
            p_fail=self.p_fail,
            unreliable=dict(self.unreliable),
            frozen=set(self.frozen),
            dead=set(self.dead),
        )


# A rule sees the identities occupying its window and the identity acting, and
# returns the window's new arrangement -- a permutation of what it was given, or
# the same tuple to hold. Returning a permutation is what lets entities move;
# returning a tuple that differs only in the centre is a classic cellular
# automaton. A rule may not invent, duplicate or destroy an identity, and
# `apply` checks that rather than trusting it.
Window = tuple[int | None, ...]
Rule = Callable[[Window, int], Window]


class RuleViolation(RuntimeError):
    """A rule returned something that is not a rearrangement of its window."""


@dataclass
class Lattice:
    """A 1-D line of sites, each empty or holding one entity.

    `occupants[i]` is the identity at site i, or None. `entities` maps identity
    to its record. Nothing here knows what the system is for.
    """

    occupants: list[int | None]
    entities: dict[int, Entity]
    faults: Faults
    rng: random.Random
    radius: int = 1
    ring: bool = False
    ops: int = 0
    # Whether occupants are CONSERVED. Sorting conserves: its entities move but
    # are never created or destroyed, and its rule must return a permutation of
    # the window. A classic cellular automaton does not conserve: its rule
    # rewrites a site's state from its neighbourhood. Both are "explicit
    # transition rules on a local neighbourhood" (spec §28), so this is a
    # declared property of the system, not a law of the substrate. It was a law
    # in the first draft of this file, which silently made the constrained case
    # -- the cellular automaton -- inexpressible on a substrate whose whole
    # claim is that a cellular automaton is a constrained case of it.
    conserving: bool = True
    # How a neighbourhood is taken. Two conventions, because two kinds of rule
    # need different ones and pretending otherwise is where this file first went
    # wrong. ANCHORED gives 2*radius sites starting at i -- the adjacent pair a
    # sorting exchange acts on. CENTRED gives 2*radius+1 sites around i -- the
    # neighbourhood a cellular automaton rewrites its centre from. Anchored is
    # the natural window for a conserving rule and centred for a rewriting one,
    # but they are independent properties and the substrate does not couple
    # them.
    centred: bool = False

    @property
    def size(self) -> int:
        return len(self.occupants)

    def window_at(self, i: int) -> tuple[int, ...]:
        """The site indices in the neighbourhood at i.

        Centred: `2 * radius + 1` sites around i. Anchored: `2 * radius` sites
        starting at i -- with radius=1, the adjacent pair a sorting exchange
        acts on. On a ring the window wraps; on a line it must fit.
        """
        if self.centred:
            width = 2 * self.radius + 1
            start = i - self.radius
        else:
            width = 2 * self.radius
            start = i
        if self.ring:
            return tuple((start + k) % self.size for k in range(width))
        if start < 0 or start + width > self.size:
            raise IndexError(
                f"window at {i} does not fit a line of {self.size}; a line has "
                "no complete neighbourhood at its ends, so a schedule must not "
                "offer that site"
            )
        return tuple(start + k for k in range(width))

    def sites(self) -> tuple[int, ...]:
        """Every anchor with a complete neighbourhood. A schedule iterates this
        rather than range(size), so boundary handling lives in one place."""
        if self.ring:
            return tuple(range(self.size))
        width = 2 * self.radius + (1 if self.centred else 0)
        if self.centred:
            return tuple(range(self.radius, self.size - self.radius))
        return tuple(range(self.size - width + 1))

    def read(self, i: int) -> Window:
        """Read a neighbourhood. Costs one operation, because looking is the
        same primitive acting uses -- this is what makes a coordinator that only
        monitors pay for its monitoring."""
        self.ops += 1
        return tuple(self.occupants[k] for k in self.window_at(i))

    def apply(self, i: int, rule: Rule, initiator: int | None = None,
              charge: bool = True) -> bool:
        """Evaluate `rule` on the window at i and install the result.

        Costs one operation unless the caller already paid with `read`.
        Returns whether the lattice actually changed. Faults are checked here,
        in a fixed order, so every experiment inherits the same fault semantics:
        dead blocks first because a dead entity blocks interactions it did not
        initiate; then frozen; then the stochastic failure.
        """
        if charge:
            self.ops += 1
        sites = self.window_at(i)
        before = tuple(self.occupants[k] for k in sites)

        if any(o is not None and o in self.faults.dead for o in before):
            return False
        if initiator is None:
            initiator = self._choose_initiator(before)
        if initiator is None:
            return False
        if initiator in self.faults.frozen:
            return False
        q = max(self.faults.p_fail, self.faults.unreliable.get(initiator, 0.0))
        if q > 0.0 and self.rng.random() < q:
            return False

        after = rule(before, initiator)
        if len(after) != len(before):
            raise RuleViolation(
                f"rule returned {len(after)} sites for a window of {len(before)}"
            )
        if self.conserving and sorted(x for x in after if x is not None) != sorted(
                x for x in before if x is not None):
            raise RuleViolation(
                f"rule rearranged {before!r} into {after!r}, which is not a "
                "permutation of it. This lattice is declared conserving, so a "
                "rule may move occupants within its window but may not create, "
                "destroy or duplicate them. Set conserving=False for a system "
                "whose rule rewrites site state, such as a cellular automaton."
            )
        if after == before:
            return False
        for k, occupant in zip(sites, after):
            self.occupants[k] = occupant
        return True

    def _choose_initiator(self, before: Window) -> int | None:
        """Pick which occupant of the window acts, uniformly among two.

        Kept as its own method because its draw is part of the substrate's
        random stream and any change to it changes every recorded trial.
        """
        present = [o for o in before if o is not None]
        if not present:
            return None
        if len(present) == 1:
            return present[0]
        if len(present) == 2:
            return present[0] if self.rng.random() < 0.5 else present[1]
        return present[self.rng.randrange(len(present))]


# A schedule yields the anchor site for the next interaction, forever or until
# it decides to stop. It is handed the lattice so it can look -- but looking
# costs, like everything else, so a schedule that inspects before choosing is
# more expensive than one that does not, and that difference is measurable.
Schedule = Callable[[Lattice, int], Iterator[int]]


def build(values: Sequence[int], faults: Faults | None = None,
          rng: random.Random | None = None, radius: int = 1,
          ring: bool = False, conserving: bool = True,
          centred: bool = False) -> Lattice:
    """A lattice whose site i holds the entity identified by values[i]."""
    return Lattice(
        occupants=list(values),
        entities={v: Entity(ident=v) for v in set(values)},
        faults=(faults.copy() if faults else Faults()),
        rng=rng if rng is not None else random.Random(0),
        radius=radius,
        ring=ring,
        conserving=conserving,
        centred=centred,
    )


def step_synchronous(lat: Lattice, rule: Rule) -> bool:
    """Update every site at once from the previous configuration (spec §45).

    The classic cellular-automaton schedule, and the reason it needs its own
    function: every other schedule here reads and writes one window at a time,
    so a later site would see an earlier site's new value. Synchrony means every
    rule evaluation sees the SAME configuration. Each evaluation is charged, so
    a synchronous sweep of an n-site lattice costs n operations -- the same
    currency as everything else.
    """
    before = tuple(lat.occupants)
    updated: list[int | None] = list(before)
    for i in lat.sites():
        lat.ops += 1
        window = tuple(before[k] for k in lat.window_at(i))
        centre = window[len(window) // 2]
        out = rule(window, centre if centre is not None else 0)
        for k, occupant in zip(lat.window_at(i), out):
            if k == i or not lat.centred:
                updated[k] = occupant
    changed = updated != list(before)
    lat.occupants = updated
    return changed


# --- Snapshot and restore (spec §42; First Wave's branching discipline) ---
#
# First Wave is explicit about why this exists: *"Never approximate a
# counterfactual by starting from a 'similar-looking' state."* Every arm of an
# intervention comparison restores the SAME snapshot, so the arms differ only by
# the intervention. That requires the random generator's state too -- without it
# two arms diverge for reasons that have nothing to do with the intervention,
# and the comparison silently measures noise.


@dataclass(frozen=True)
class Snapshot:
    """Everything needed to reproduce subsequent behaviour exactly."""

    occupants: tuple[int | None, ...]
    memory: tuple[tuple[int, tuple[tuple[str, Any], ...]], ...]
    faults: Faults
    rng_state: Any
    ops: int
    radius: int
    ring: bool


def snapshot(lat: Lattice) -> Snapshot:
    return Snapshot(
        occupants=tuple(lat.occupants),
        memory=tuple((ident, tuple(sorted(e.memory.items())))
                     for ident, e in sorted(lat.entities.items())),
        faults=lat.faults.copy(),
        rng_state=lat.rng.getstate(),
        ops=lat.ops,
        radius=lat.radius,
        ring=lat.ring,
    )


def restore(snap: Snapshot) -> Lattice:
    """A lattice that will behave identically to the one snapshotted."""
    rng = random.Random()
    rng.setstate(snap.rng_state)
    return Lattice(
        occupants=list(snap.occupants),
        entities={ident: Entity(ident=ident, memory=dict(mem))
                  for ident, mem in snap.memory},
        faults=snap.faults.copy(),
        rng=rng,
        radius=snap.radius,
        ring=snap.ring,
        ops=snap.ops,
    )
