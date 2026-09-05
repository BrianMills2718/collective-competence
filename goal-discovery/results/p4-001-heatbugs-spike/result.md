# P4-001 off-the-shelf Heatbugs spike — results

**ADOPT — Heatbugs passed the frozen bridge-calibration gate.**

Mean pre-branch unhappiness: **4.208**. Mean matched shock gap: **12.388**. Mean late gap: **0.240**.

| Seed | Pre unhappiness | Shock gap | Late gap | Gap closed |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 4.622 | 12.177 | -0.248 | 102.0% |
| 2 | 4.407 | 12.649 | 0.748 | 94.1% |
| 3 | 4.242 | 12.040 | 0.324 | 97.3% |
| 4 | 3.561 | 12.684 | 0.138 | 98.9% |

## Frozen criteria

- pass — `installed_gui_model_present`
- pass — `four_complete_paired_trajectories`
- pass — `prebranch_trajectories_identical`
- pass — `population_preserved`
- pass — `paired_ideal_mean_preserved`
- pass — `baseline_settled_in_three_seeds`
- pass — `shock_detected_in_three_seeds`
- pass — `half_gap_closed_in_three_seeds`

## Interpretation boundary

Heatbugs contains explicit individual ideal temperatures. Passing only earns a later blind-inference experiment that hides those targets and the generator's unhappiness calculation.
