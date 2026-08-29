# P2-003 immovable-barrier reachability — results

## Decision

**Pass.** The frozen barrier-feasibility rule classified every one of the
7,440 exhaustive size-5 immovable cases correctly.

| Schedule | Cases | Accuracy | False feasible | False infeasible | Time-limit exits |
| --- | ---: | ---: | ---: | ---: | ---: |
| index | 3,720 | 100% | 0 | 0 | 0 |
| shuffled | 3,720 | 100% | 0 | 0 | 0 |

The matched moveable arm contained 2,622 cases in which the selected positions
crossed an inversion path, the immovable branch failed, and the moveable branch
recovered. The result therefore distinguishes an immovable action barrier from
damage count or position alone.

## What was learned

For this adjacent-swap system, an immovable cell creates a literal reachability
boundary. A branch can sort exactly when no initially inverted value pair would
need to cross an immovable position. This turns a vague notion of "retained
capability" into a compact observable invariant with no fitted parameters.

This result also explains why the preceding representation screens struggled:
they tried to estimate recovery probability while omitting the exact constraint
that makes many outcomes mechanically impossible.

## Boundary

This is exhaustive for distinct values at size 5 and both tested activation
schedules. The invariant also has a direct adjacent-swap argument, but this run
is evidence about this implementation rather than a general proof about every
distributed system. It establishes a recovery boundary, not agency or goal
possession.

Artifacts are in `results/p2-003-barrier-reachability/`.
