# P2-004 moveable-cell order reachability — results

**PASS — the passive-order rule exactly classified the exhaustive size-6 cases.**

The new-size experiment evaluated 90,720 moveable-damage branches.

| Schedule | Cases | Accuracy | Time-limit exits |
| --- | ---: | ---: | ---: |
| index | 45,360 | 100.0% | 0 |
| shuffled | 45,360 | 100.0% | 0 |

False feasible: **0**. False infeasible: **0**. Mode-specific successful controls: **24,180**.

## Frozen criteria

- pass — `accuracy_is_100_percent`
- pass — `zero_false_feasible`
- pass — `zero_false_infeasible`
- pass — `every_schedule_is_100_percent`
- pass — `zero_time_limit_exits`
- pass — `both_outcomes_present`
- pass — `mode_specific_success_exists`

## Interpretation boundary

This establishes an exact size-6 reachability invariant for this implementation of cell-view bubble sorting under moveable damage. It identifies preserved relative order among passive cells; it does not establish agency or goal possession.
