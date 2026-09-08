"""One substrate for the discovery phase: a generalized discrete interacting system.

Laboratory spec §28 specifies *"a discrete interacting dynamical system with
local state and explicit transition rules,"* of which *"a standard cellular
automaton is a particularly constrained case"*, and §29 starts it at 1-D. The
owner reached the same specification independently: *"basically like cellular
automata but probably more generalized"*. This module is that, and nothing more.

The substrate has two explicit payload modes rather than pretending every site
contains the same kind of thing.

**The goal is never inside the system.** No site, entity or rule holds a target.
A measurement is a function FROM a lattice, defined in `observe.py`, and the
lattice cannot read it. This is what makes goal *discovery* possible at all: an
analyst who can only watch has nothing privileged to find.

**One currency prices rule evaluation.** Every rule evaluation costs one
operation. A coordinator that scans without acting pays for those reads too.

**The schedule is a dial, not a decision.** Which site acts next is supplied by
the experiment. Synchronous update makes this a classic cellular automaton;
random site selection makes it the decentralized sorting rule; a sweep makes it
a coordinator.

**Conserving mode is entity mode.** When `conserving=True`, every non-empty site
contains a stable entity identity present in `entities`. Identities may move but
may not be created, duplicated or destroyed. Per-entity memory and the `dead`,
`frozen` and `unreliable` fault semantics belong to this mode. Sorting needs it.

**Non-conserving mode is local-state mode.** When `conserving=False`, site
payloads are rewritable local state values, not entity identities. `entities` is
therefore empty and values may be created, duplicated or destroyed by a rule.
Elementary cellular automata and scalar regulation use this mode. This is not a
claim that every dynamical system fits one container; it is the smallest shared
contract the current specimens actually use.

What is deliberately absent, because no queued experiment needs it yet and the
last contract was generalized backwards from failures rather than forwards from
goals: two dimensions, non-local coupling, entity creation and destruction in
entity mode, and any shared scalar. Add capability only when a concrete,
otherwise-unexpressible experiment requires it.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entity:
    """A mobile occupant record used only by conserving/entity-mode lattices.

    `ident` is the stable identity that rules and faults key on; it survives
    movement. `memory` holds persistent internal variables when a specimen needs
    them.
    """

    ident: int
    memory: dict[str, Any] = field(default_factory=dict)


@dataclass
class Faults:
    """Per-entity defects for local entity-mode interactions.

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


# A rule sees the site payloads in its window and one integer supplied as the
# initiator argument. In entity mode the payloads and initiator are stable entity
# identities, and a local rule must return a permutation of the window. In
# local-state mode the payloads are ordinary state values and may be rewritten.
# Synchronous state-mode rules receive the centre value in the initiator slot;
# they should treat it only as part of the generic Rule signature.
Window = tuple[int | None, ...]
Rule = Callable[[Window, int], Window]


class RuleViolation(RuntimeError):
    """A rule or lattice state violates the declared substrate mode."""


@dataclass
class Lattice:
    """A 1-D line of sites under one of two declared payload semantics.

    In conserving/entity mode, `occupants[i]` is an entity identity or `None`
    and every present identity must exist in `entities`. In non-conserving
    local-state mode, `occupants[i]` is a rewritable state value and `entities`
    must be empty. Nothing here knows what the system is for.
    """

    occupants: list[int | None]
    entities: dict[int, Entity]
    faults: Faults
    rng: random.Random
    radius: int = 1
    ring: bool = False
    ops: int = 0
    # Conserving=True means entity mode: stable identities move but are not
    # created or destroyed. Conserving=False means local-state mode: rules may
    # rewrite site values. The flag therefore carries semantic, not merely
    # arithmetic, meaning and is part of every snapshot.
    conserving: bool = True
    # How a neighbourhood is taken. ANCHORED gives 2*radius sites starting at i
    # (the adjacent pair sorting exchanges). CENTRED gives 2*radius+1 sites
    # around i (the neighbourhood a CA or scalar state rule rewrites from).
    centred: bool = False

    @property
    def size(self) -> int:
        return len(self.occupants)

    def validate(self) -> None:
        """Fail loudly when site payloads do not match the declared mode."""
        if self.conserving:
            present = [value for value in self.occupants if value is not None]
            if len(present) != len(set(present)):
                raise RuleViolation(
                    "conserving/entity mode requires unique occupant identities"
                )
            missing = sorted(set(present) - set(self.entities))
            if missing:
                raise RuleViolation(
                    f"conserving/entity mode has occupant identities with no "
                    f"entity record: {missing}"
                )
        elif self.entities:
            raise RuleViolation(
                "non-conserving/local-state mode must not carry entity records; "
                "site payloads are state values, not identities"
            )

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
        """Every anchor with a complete neighbourhood."""
        if self.ring:
            return tuple(range(self.size))
        width = 2 * self.radius + (1 if self.centred else 0)
        if self.centred:
            return tuple(range(self.radius, self.size - self.radius))
        return tuple(range(self.size - width + 1))

    def read(self, i: int) -> Window:
        """Read a neighbourhood and charge one operation."""
        self.validate()
        self.ops += 1
        return tuple(self.occupants[k] for k in self.window_at(i))

    def apply(self, i: int, rule: Rule, initiator: int | None = None,
              charge: bool = True) -> bool:
        """Evaluate `rule` on one window and install the result.

        `apply` supplies the entity-mode fault semantics used by sorting. It is
        also usable with an empty-fault local-state lattice, but state-mode
        synchronous systems normally use `step_synchronous` instead.
        """
        self.validate()
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
                "permutation of it. This lattice is declared conserving/entity "
                "mode, so a rule may move identities but may not create, destroy "
                "or duplicate them. Set conserving=False for rewritable local "
                "state such as a cellular automaton."
            )
        if after == before:
            return False
        for k, occupant in zip(sites, after):
            self.occupants[k] = occupant
        self.validate()
        return True

    def _choose_initiator(self, before: Window) -> int | None:
        """Pick one present payload; in entity mode this is the acting identity."""
        present = [o for o in before if o is not None]
        if not present:
            return None
        if len(present) == 1:
            return present[0]
        if len(present) == 2:
            return present[0] if self.rng.random() < 0.5 else present[1]
        return present[self.rng.randrange(len(present))]


# A schedule yields the anchor site for the next interaction. It is handed the
# lattice so it can look, but looking costs like every other rule evaluation.
Schedule = Callable[[Lattice, int], Iterator[int]]


def build(values: Sequence[int], faults: Faults | None = None,
          rng: random.Random | None = None, radius: int = 1,
          ring: bool = False, conserving: bool = True,
          centred: bool = False) -> Lattice:
    """Build either an entity-mode or local-state-mode lattice.

    Conserving mode interprets each value as one unique entity identity and
    creates its record. Non-conserving mode interprets values as site state and
    deliberately creates no entity records.
    """
    if conserving and len(values) != len(set(values)):
        raise ValueError(
            "conserving/entity mode requires unique initial entity identities"
        )
    lat = Lattice(
        occupants=list(values),
        entities=(
            {v: Entity(ident=v) for v in values}
            if conserving else {}
        ),
        faults=(faults.copy() if faults else Faults()),
        rng=rng if rng is not None else random.Random(0),
        radius=radius,
        ring=ring,
        conserving=conserving,
        centred=centred,
    )
    lat.validate()
    return lat


def step_synchronous(lat: Lattice, rule: Rule) -> bool:
    """Update every site at once from the previous configuration (spec §45).

    Every rule evaluation sees the same configuration. This is the natural
    schedule for local-state systems such as cellular automata and the scalar
    regulation calibration. Each evaluation costs one operation.
    """
    lat.validate()
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
    lat.validate()
    return changed


# --- Snapshot and restore (spec §42; First Wave's branching discipline) ---
# Every intervention arm restores the same configuration, entity memory, faults,
# random-generator state, operation count, neighbourhood semantics and payload
# mode. A similar-looking state is not an exact counterfactual.


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
    conserving: bool
    centred: bool


def snapshot(lat: Lattice) -> Snapshot:
    lat.validate()
    return Snapshot(
        occupants=tuple(lat.occupants),
        memory=tuple((ident, tuple(sorted(e.memory.items())))
                     for ident, e in sorted(lat.entities.items())),
        faults=lat.faults.copy(),
        rng_state=lat.rng.getstate(),
        ops=lat.ops,
        radius=lat.radius,
        ring=lat.ring,
        conserving=lat.conserving,
        centred=lat.centred,
    )


def restore(snap: Snapshot) -> Lattice:
    """A lattice that will behave identically to the one snapshotted."""
    rng = random.Random()
    rng.setstate(snap.rng_state)
    lat = Lattice(
        occupants=list(snap.occupants),
        entities={ident: Entity(ident=ident, memory=dict(mem))
                  for ident, mem in snap.memory},
        faults=snap.faults.copy(),
        rng=rng,
        radius=snap.radius,
        ring=snap.ring,
        ops=snap.ops,
        conserving=snap.conserving,
        centred=snap.centred,
    )
    lat.validate()
    return lat
