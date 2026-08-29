# P2-003 — immovable-barrier reachability invariant

**Frozen after P2-002c and before generating P2-003 cases.**

## Candidate mechanism

In a line updated only by adjacent swaps, an immovable cell prevents every
value on one side from crossing to the other and cannot itself change position.
Define a branch as **barrier-feasible** exactly when no inverted value pair has
an interval containing an immovable cell.

Prediction:

> A bubble-rule sorting branch with immovable frozen cells can reach sorted
> order if and only if it is barrier-feasible.

This is an observable reachability statement. It uses values, positions, and
freeze modes only; it does not use future trajectories or simulator internals.

## Exhaustive test

Enumerate:

- every permutation of five distinct values;
- every nonempty subset of the five positions;
- index and shuffled activation schedules;
- immovable and moveable freeze modes;
- one deterministic transition seed per permutation × mask × schedule.

Run each case for `30 * n` ticks or until quiescent. This creates 7,440
immovable cases and 7,440 matched moveable controls.

## Frozen decisions

The immovable invariant passes only if:

- prediction accuracy is 100% overall;
- it has zero false-feasible and zero false-infeasible cases;
- accuracy is 100% under each activation schedule;
- no case is already inconsistent with its stored terminal state because of a
  time-limit exit.

The moveable arm is a specificity control. At least one matched branch whose
selected positions intersect an inversion path must recover under moveable
freezing while its immovable sibling fails. Otherwise the result would describe
damage count or selected positions rather than the barrier mechanism.

## Interpretation

A pass would establish a compact action-reachability invariant for this system,
not agency. It would explain one boundary of collective recovery and justify
testing whether analogous reachability constraints predict capability in other
local-interaction systems. A failure returns the programme to empirical
mechanism discovery without changing the rule after inspection.
