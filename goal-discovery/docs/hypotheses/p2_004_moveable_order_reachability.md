# P2-004 — moveable-cell order reachability invariant

**Frozen after P2-003 and before generating any size-6 cases.**

## Candidate mechanism

A moveable frozen cell cannot initiate a swap, but an active neighbour can swap
with it. Two frozen cells can therefore move through active cells but can never
cross one another: their relative order is invariant.

Prediction:

> A bubble-rule sorting branch with moveable frozen cells can reach sorted
> order if and only if the values carried by the frozen cells are already in
> ascending relative order.

Equivalently, there is no initially inverted pair whose two endpoints are both
moveable-frozen. The prediction uses only the branch observation and has no
fitted parameters.

## New-size exhaustive test

Enumerate:

- every permutation of six distinct values;
- every nonempty subset of the six positions;
- index and shuffled activation schedules;
- moveable freeze mode only;
- one deterministic transition seed per permutation × mask × schedule.

Run each case for `30 * n` ticks or until quiescent. This creates 90,720 new
branches. None were used to formulate the rule.

## Frozen decisions

The invariant passes only if:

- prediction accuracy is 100% overall;
- there are zero false-feasible and zero false-infeasible cases;
- accuracy is 100% under each activation schedule;
- there are no time-limit exits;
- both reachable and unreachable cases occur;
- at least one branch is infeasible under the P2-003 immovable-barrier rule but
  feasible and successful under this moveable-order rule.

No threshold or rule changes are allowed after inspecting size-6 outcomes.

## Interpretation

A pass would complete a compact, mode-specific reachability account for this
sorting system: immovable damage preserves spatial partitions, while moveable
damage preserves only the relative order of passive identities. These
invariants can then be used to separate opportunity from performance in later
goal-directedness tests. A failure stops this mechanism claim without another
feature-repair loop.
