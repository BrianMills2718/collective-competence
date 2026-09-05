# P2-002b within-intervention prediction — results

## Discovery decision

**STOP before the size-24 batch.**

The new-seed size-12 study contains 72 branches and has an overall goal rate of 51.4%.

### Outcome eligibility

| Schedule | Damage | Successes | Goal rate |
| --- | --- | ---: | ---: |
| index | immovable × 1 | 2 / 12 | 16.7% |
| index | moveable × 2 | 9 / 12 | 75.0% |
| index | moveable × 3 | 7 / 12 | 58.3% |
| shuffled | immovable × 1 | 3 / 12 | 25.0% |
| shuffled | moveable × 2 | 11 / 12 | 91.7% |
| shuffled | moveable × 3 | 5 / 12 | 41.7% |

### Representation comparison

| representation | n features | log loss | brier loss | balanced accuracy | time to goal mae per cell |
| --- | --- | --- | --- | --- | --- |
| History-aware macro | 12 | 0.570 | 0.195 | 0.735 | 0.258 |
| Capability-aware macro | 9 | 0.570 | 0.194 | 0.707 | 0.219 |
| Capability ablation | 8 | 0.608 | 0.206 | 0.693 | 0.219 |
| Intervention-only null | 6 | 0.614 | 0.209 | 0.663 | 0.228 |
| Value-only macro | 4 | 0.706 | 0.256 | 0.529 | 0.240 |
| Observable-micro baseline | 36 | 1.224 | 0.338 | 0.581 | 0.321 |

### Frozen criteria

- pass — `all_six_strata_present`
- pass — `all_six_strata_mixed`
- pass — `no_pre_sorted_branches`
- fail — `20pct_better_than_value`
- fail — `20pct_better_than_intervention`
- pass — `within_10pct_of_micro`
- pass — `quarter_micro_features`
- pass — `brier_below_0_25`
- pass — `ablation_beats_both_nulls`

## Interpretation boundary

This study tests whether observable retained capability adds predictive information inside nominally matched damage classes. It does not test agency, goal possession, or causal emergence.
