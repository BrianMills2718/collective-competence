# Experiment 05 — local spatial pattern formation and repair

This is the first post-calibration **new Collective Competence specimen**. A ring of cells must satisfy a spatial constraint: adjacent cells must have different colours. There is no single target configuration; for a 24-cell ring with three colours there are **16,777,218** valid global patterns. The global success criterion is measured externally.

Each cell can inspect only its two immediate neighbours. When selected, a conflict-aware cell changes colour only if it matches at least one neighbour, choosing a colour used by neither neighbour. A random-local control selects the same kind of site and recolouring action but does not use neighbour information. One site selection/rule evaluation is one operation.

The rule contains no global target pattern and no map of desired cell states. It implements only the local constraint that adjacent colours differ.

## Formation

From random initial colours, 200 seeds were run for each size with a 10,000-operation budget.

| cells | conflict-aware success | mean ops | random-local success | mean ops among successes |
|---:|---:|---:|---:|---:|
| 12 | 200/200 | 12.2 | 200/200 | 265.5 |
| 24 | 200/200 | 31.2 | 56/200 | 4,845.8 |
| 48 | 200/200 | 78.9 | 0/200 | — |

Local conflict sensing therefore changes the problem from increasingly rare random search into rapid self-stabilization over the tested sizes.

## Repair without returning to the same microstate

After a valid 24-cell pattern formed, a contiguous lesion was forced by overwriting a block with its left neighbour's colour. This guarantees a real violation. Every lesion repaired in all 200 seeds for every tested width.

| lesion width | repairs | exact original restored | different valid endpoint | mean repair ops | mean Hamming distance from original |
|---:|---:|---:|---:|---:|---:|
| 1 | 200/200 | 75 | 125 | 14.5 | 1.26 |
| 2 | 200/200 | 36 | 164 | 17.8 | 1.93 |
| 4 | 200/200 | 13 | 187 | 23.0 | 3.23 |
| 8 | 200/200 | **0** | **200** | 31.8 | 5.87 |
| 12 | 200/200 | **0** | **200** | 36.0 | 8.50 |

The important result is not exact regeneration. For larger lesions the original microstate is never recovered, yet the global criterion is always recovered. Competence here is naturally relative to an **equivalence class of acceptable patterns**, not one privileged target state.

## Permanent-defect boundary

A single cell was forced into conflict and then frozen so it could never change. Its neighbours could reorganize around it: **200/200** trials returned to a valid pattern.

Two adjacent frozen cells were then locked to the same colour. That shared edge can never become valid, and **0/200** trials repaired. This is a structural impossibility boundary, not merely poorer performance.

## What this establishes

This gives a small, inspectable example of distributed pattern formation and repair with no centralized representation of a complete target. It also demonstrates why a goal criterion need not identify one unique state: many global configurations satisfy the same locally enforced condition.

The result is still deliberately narrow. This is a hand-authored self-stabilizing rule on a one-dimensional ring, not biological regeneration, agency, or a general theory of morphogenesis. The exact coloring problem is simple enough to reason about analytically; its role is to expose a different kind of competency and a clean set of failure boundaries.

## Next question

Now that the constructive phenomenon exists, the useful discovery question is whether a blind analyst can infer a **family-level criterion** such as the adjacency relation from formation and damage/repair behavior without being given an exact target pattern. That test should use this specimen as-is; do not build a new Goal Discovery framework around it.

## Reproduce

```bash
python3 experiments/05-pattern-repair/run.py
python3 -m pytest -q experiments/05-pattern-repair/test_model.py
```

Evidence: [`results/characterization.json`](results/characterization.json).
