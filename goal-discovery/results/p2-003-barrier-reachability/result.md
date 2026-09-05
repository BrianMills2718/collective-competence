# P2-003 immovable-barrier reachability — results

**PASS — the barrier rule exactly classified the exhaustive size-5 cases.**

The experiment evaluated 14,880 branches: 7,440 immovable cases and 7,440 matched moveable controls.

| Schedule | Immovable cases | Accuracy | Time-limit exits |
| --- | ---: | ---: | ---: |
| index | 3,720 | 100.0% | 0 |
| shuffled | 3,720 | 100.0% | 0 |

False feasible: **0**. False infeasible: **0**. Matched moveable specificity cases: **2,622**.

## Frozen criteria

- pass — `immovable_accuracy_is_100_percent`
- pass — `zero_false_feasible`
- pass — `zero_false_infeasible`
- pass — `every_schedule_is_100_percent`
- pass — `zero_immovable_time_limit_exits`
- pass — `moveable_specificity_case_exists`

## Interpretation boundary

This establishes an exact size-5 reachability invariant for this implementation of cell-view bubble sorting under immovable damage. It identifies a mechanistic boundary on collective recovery; it does not establish agency, goal possession, or emergence.
