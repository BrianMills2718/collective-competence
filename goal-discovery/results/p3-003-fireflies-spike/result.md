# P3-003 off-the-shelf Fireflies spike — results

**STOP — the standard Fireflies model missed the frozen adoption gate.**

Mean pre-branch phase order: **0.249**. Mean matched shock gap: **0.076**. Mean late gap: **0.104**.

| Seed | Pre order | Shock gap | Late gap | Gap closed |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.336 | 0.177 | 0.112 | 36.7% |
| 2 | 0.317 | 0.095 | 0.065 | 32.0% |
| 3 | 0.095 | 0.008 | 0.203 | -2553.1% |
| 4 | 0.249 | 0.027 | 0.037 | -39.1% |

## Frozen criteria

- pass — `installed_gui_model_present`
- pass — `four_complete_paired_trajectories`
- pass — `prebranch_trajectories_identical`
- fail — `baseline_synchronized_in_three_seeds`
- fail — `shock_detected_in_three_seeds`
- fail — `half_gap_closed_in_three_seeds`
- pass — `population_preserved`

## Interpretation boundary

This is an adoption test for an unmodified distributed synchrony generator. A separate interaction-disabled contrast is required before active regulation or goal-language is justified.
