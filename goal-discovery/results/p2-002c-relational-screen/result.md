# P2-002c relational capability screen — results

## Decision

**STOP the current observation-repair direction.**

| Representation | Inputs | Log loss | Brier loss | Balanced accuracy |
| --- | ---: | ---: | ---: | ---: |
| Relational capability | 9 | 0.538 | 0.185 | 0.719 |
| History-aware macro | 12 | 0.570 | 0.195 | 0.735 |
| Capability-aware macro | 9 | 0.570 | 0.194 | 0.707 |
| Capability ablation | 8 | 0.608 | 0.206 | 0.693 |
| Intervention-only null | 6 | 0.614 | 0.209 | 0.663 |
| Value-only macro | 4 | 0.706 | 0.256 | 0.529 |
| Observable-micro baseline | 36 | 1.224 | 0.338 | 0.581 |

Frozen criteria:

- pass — `20pct_better_than_value`
- fail — `20pct_better_than_intervention`
- pass — `brier_below_0_25`
- pass — `no_more_than_nine_inputs`

This is an existing-data observation-design screen. A pass cannot change the P2-002b no-go; it can only justify a new-seed validation.
