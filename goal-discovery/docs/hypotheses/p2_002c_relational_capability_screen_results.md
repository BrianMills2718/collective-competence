# P2-002c relational capability screen — results

## Decision

**No-go. Stop the current predictive representation-repair loop.**

The nine-input relational capability family improved log loss to 0.538 from
0.570 for the prior capability family. It beat value-only by 23.8%, but beat
intervention-only by only 12.4%, below the frozen 20% gate. No new-seed
validation is justified.

| Representation | Inputs | Log loss | Brier loss | Balanced accuracy |
|---|---:|---:|---:|---:|
| Relational capability | 9 | **0.538** | **0.185** | 0.719 |
| History-aware macro | 12 | 0.570 | 0.195 | **0.735** |
| Capability-aware macro | 9 | 0.570 | 0.194 | 0.707 |
| Intervention-only null | 6 | 0.614 | 0.209 | 0.663 |
| Value-only macro | 4 | 0.706 | 0.256 | 0.529 |
| Observable-micro baseline | 36 | 1.224 | 0.338 | 0.581 |

The aggregate predictive candidate is retired. Post-screen inspection produced
a different, mechanism-level clue: among all 24 stored one-immovable-cell
branches, goal attainment was 5/5 when no inversion path crossed the immovable
cell and 0/19 when at least one did. That observation is post hoc and cannot be
a result from this screen. It motivates a separately frozen exhaustive
falsification test of action reachability.

Evidence is in `results/p2-002c-relational-screen/`.
