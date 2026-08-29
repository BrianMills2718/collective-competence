# P2-004 moveable-cell order reachability — results

## Decision

**Pass.** The frozen passive-order rule classified every one of the 90,720 new
size-6 moveable-damage branches correctly.

| Schedule | Cases | Accuracy | False feasible | False infeasible | Time-limit exits |
| --- | ---: | ---: | ---: | ---: | ---: |
| index | 45,360 | 100% | 0 | 0 | 0 |
| shuffled | 45,360 | 100% | 0 | 0 | 0 |

Both outcomes were present: 25,214 branches reached sorted order and 65,506 did
not. There were 24,180 successful branches that the P2-003 immovable-barrier
rule would classify infeasible, satisfying the frozen mode-specificity gate.

## What was learned

Moveable frozen cells retain mobility but not agency: active neighbours can
carry them, while two passive cells cannot cross one another. Their relative
value order is therefore the exact observable boundary on recovery for this
system.

Together P2-003 and P2-004 replace a weak fitted recovery predictor with two
zero-parameter mechanisms:

- immovable damage preserves spatial partitions;
- moveable damage preserves the relative order of passive identities.

This is directly useful to the goal-discovery programme because later studies
can now distinguish an unreachable target from failure to exploit an available
route. Treating both as ordinary negative outcomes had obscured the structure
in P2-002.

## Boundary and next decision

The result is exhaustive for distinct values at size 6 and both tested
schedules. It is still a property of this bubble-rule, adjacent-swap system,
not evidence of agency.

The next research sprint should not enlarge this enumeration. It should use an
off-the-shelf graph reachability routine on tiny systems to separate three
quantities across different algotypes: whether the target is reachable, whether
the actual rule realizes a reachable route, and how robustly it does so across
schedules. That is the smallest test of whether opportunity-adjusted competence
adds information beyond these exact mechanical constraints.

Artifacts are in `results/p2-004-moveable-order-reachability/`.
