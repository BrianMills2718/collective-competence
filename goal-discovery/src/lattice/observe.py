"""Measurements and analyst-visible channels over the shared lattice.

These are functions FROM a lattice. The lattice cannot call them and holds no
reference to them, which is the mechanical form of *"the target lives only in
the measurement"*.

`occupants` is deliberately the raw site-payload channel. In conserving/entity
mode those integers are stable entity identities. In non-conserving/local-state
mode they are rewritable site-state values. The observation contract exposes the
values, not their hidden mechanism or intended interpretation. Sorting-specific
measurements such as `inversions` are separate functions and should only be used
when the experiment declares that representation meaningful.
"""

from __future__ import annotations

from .core import Lattice


def occupant_values(lat: Lattice) -> list[int]:
    """Raw non-empty site payloads under the lattice's declared payload mode."""
    return [o for o in lat.occupants if o is not None]


def inversions(lat: Lattice) -> int:
    """Pairs out of ascending order. Zero exactly when sorted.

    This is a sorting representation, not a generic lattice property.
    """
    vals = occupant_values(lat)
    return sum(1 for i in range(len(vals)) for j in range(i + 1, len(vals))
               if vals[i] > vals[j])


def local_disorder(lat: Lattice) -> int:
    """Adjacent pairs out of order in the sorting representation."""
    vals = occupant_values(lat)
    return sum(1 for i in range(len(vals) - 1) if vals[i] > vals[i + 1])


def is_sorted(lat: Lattice) -> bool:
    return inversions(lat) == 0


# --- The observation contract (spec §6, §43, §44) ---
#
# Spec §6 is the load-bearing sentence: *"The analyst must not receive: hidden
# rules; hidden parameters; hidden state; hidden scheduler state; labels saying
# what mechanism/goal was intended."* Asking for a channel that was not exposed
# raises rather than returning nothing: an empty reading and a forbidden reading
# must never look alike.

CHANNELS = {
    "occupants": occupant_values,
    "inversions": inversions,
    "local_disorder": local_disorder,
    "ops": lambda lat: lat.ops,
    "size": lambda lat: lat.size,
}

# Anything here is white-box and may never be exposed through Observation.
NEVER_EXPOSED = frozenset({"rule", "schedule", "faults", "rng", "memory", "entities"})


class HiddenChannel(RuntimeError):
    """An analyst asked for something the contract does not expose."""


class Observation:
    """h(S_t): what an analyst is allowed to see of a lattice, and nothing more."""

    def __init__(self, expose: frozenset[str] | set[str] | tuple[str, ...]):
        expose = frozenset(expose)
        forbidden = expose & NEVER_EXPOSED
        if forbidden:
            raise HiddenChannel(
                f"{sorted(forbidden)} is white-box state and can never be exposed "
                "to an analyst. Spec §6: the analyst must not receive hidden "
                "rules, parameters, state or scheduler state."
            )
        unknown = expose - set(CHANNELS)
        if unknown:
            raise HiddenChannel(f"no such observation channel: {sorted(unknown)}")
        if not expose:
            raise HiddenChannel(
                "an observation contract that exposes nothing is not a black-box "
                "experiment, it is a broken one. Name the channels."
            )
        self.expose = expose

    def read(self, lat: Lattice) -> dict:
        return {name: CHANNELS[name](lat) for name in sorted(self.expose)}

    def __repr__(self) -> str:
        return f"Observation(expose={sorted(self.expose)})"


FULL_STATE = Observation({"occupants", "inversions", "local_disorder", "ops", "size"})
LOCAL_ONLY = Observation({"local_disorder", "ops", "size"})
