# P4-002 blind heterogeneous Heatbugs target inference — results

**PROMOTE — blind per-agent target inference passed every frozen gate.**

Median target error: **2.00°**. Held-out direction accuracy: **71.5%** versus **55.5%** for the midpoint null.

| Seed | Inferred accuracy | Midpoint-null accuracy |
| ---: | ---: | ---: |
| 5 | 72.0% | 54.7% |
| 6 | 70.7% | 53.3% |
| 7 | 73.3% | 60.0% |
| 8 | 72.0% | 56.0% |
| 9 | 69.3% | 52.0% |
| 10 | 69.3% | 56.0% |
| 11 | 73.3% | 54.7% |
| 12 | 72.0% | 57.3% |

## Frozen criteria

- pass — `all_probe_agent_pairs_complete`
- pass — `paired_hidden_targets_agree`
- pass — `paired_initial_positions_agree`
- pass — `population_preserved`
- pass — `interpretable_response_rate_at_least_95pct`
- pass — `median_absolute_target_error_at_most_5`
- pass — `held_out_accuracy_at_least_70pct`
- pass — `seven_seeds_at_least_65pct`
- pass — `beats_midpoint_null_by_15_points`

## Interpretation boundary

Inference used identity, controlled probe temperature, and observed movement only. Truth was joined after estimates were fixed for scoring. The targets remain explicitly authored micro targets, not an emergent collective goal.

Scored agents: 200.
