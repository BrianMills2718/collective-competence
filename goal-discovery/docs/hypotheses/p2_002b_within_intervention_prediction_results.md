# P2-002b within-intervention prediction — results

## Decision

**No-go. The current capability feature set is retired; size 24 was not run.**

All six schedule × damage strata passed the outcome-variation eligibility gate,
so this is a valid negative test of the intended within-condition question.
Capability-aware log loss was 0.570, versus 0.614 for intervention-only and
0.706 for value-only. Those are improvements of 7.2% and 19.3%, both below the
unchanged 20% gate.

## What ran

- 72 size-12 branches on new seeds 201–212;
- index and shuffled activation;
- damage at tick 4;
- two/three moveable freezes and one immovable freeze;
- no pre-sorted branches;
- every one of the six exact strata contained success and failure.

| Schedule | Damage | Successes | Goal rate |
|---|---|---:|---:|
| index | immovable × 1 | 2 / 12 | 16.7% |
| index | moveable × 2 | 9 / 12 | 75.0% |
| index | moveable × 3 | 7 / 12 | 58.3% |
| shuffled | immovable × 1 | 3 / 12 | 25.0% |
| shuffled | moveable × 2 | 11 / 12 | 91.7% |
| shuffled | moveable × 3 | 5 / 12 | 41.7% |

## Representation results

| Representation | Inputs | Log loss | Brier loss | Balanced accuracy | Time MAE / cell |
|---|---:|---:|---:|---:|---:|
| History-aware macro | 12 | **0.570** | 0.195 | **0.735** | 0.258 |
| Capability-aware macro | 9 | 0.570 | **0.194** | 0.707 | **0.219** |
| Capability ablation | 8 | 0.608 | 0.206 | 0.693 | **0.219** |
| Intervention-only null | 6 | 0.614 | 0.209 | 0.663 | 0.228 |
| Value-only macro | 4 | 0.706 | 0.256 | 0.529 | 0.240 |
| Observable-micro baseline | 36 | 1.224 | 0.338 | 0.581 | 0.321 |

Short history did not materially improve log loss over the capability family.
The size-normalized linear micro baseline was poor. The result therefore does
not justify a bigger generic model; it points to a missing relational
observation.

## Reflection

The current capability features mostly count active/frozen cells and test local
adjacent resolvability. They do not represent which value is frozen where, how
far frozen cells are from their target positions, or whether an immovable
barrier traps long-range inversions. Those are visible, mechanics-based
relationships—not simulator internals.

Before generating more trajectories, one final existing-data screen will test a
small relational capability representation. A failure retires this observation
repair. A pass can only freeze a new-seed validation; it cannot promote P2-002b
or unlock size 24 on the reused data.

## Evidence

Machine-readable runs, trajectories, predictions, scores, eligibility,
decisions, and the evidence figure are in
`results/p2-002b-within-intervention/`.
