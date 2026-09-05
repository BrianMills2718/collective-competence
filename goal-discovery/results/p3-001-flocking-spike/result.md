# P3-001 off-the-shelf Flocking spike — results

**ADOPT — the standard Flocking model passed the frozen trajectory gate.**

Mean matched shock gap: **22.66°**. Mean late gap: **-0.34°**. Mean closure: **101.5%**.

| Seed | Shock gap | Late gap | Gap closed |
| ---: | ---: | ---: | ---: |
| 1 | 24.30° | -0.62° | 102.6% |
| 2 | 21.89° | -2.68° | 112.2% |
| 3 | 22.30° | 1.14° | 94.9% |
| 4 | 22.16° | 0.82° | 96.3% |

## Frozen criteria

- pass — `installed_gui_model_present`
- pass — `four_complete_paired_trajectories`
- pass — `shock_detected_in_at_least_three_seeds`
- pass — `half_gap_closed_in_at_least_three_seeds`

## Interpretation boundary

This only tests whether an unmodified off-the-shelf generator produces a visible, measurable perturbation trajectory. Recovery here may be passive alignment. A separate frozen experiment must compare defended macro-state hypotheses and nulls.
