# P2-002 crossed distributed prediction — results

## Discovery decision

**STOP before the size-24 batch.**

The size-12 batch contains 144 branches and an overall goal rate of 32.6%. 3 of the six freeze mode/count classes contain both success and failure, so the original frozen-equals-failed confound is broken.

| representation | n features | log loss | brier loss | balanced accuracy | time to goal mae per cell |
| --- | --- | --- | --- | --- | --- |
| Capability-aware macro | 9 | 0.264 | 0.083 | 0.895 | 0.234 |
| History-aware macro | 12 | 0.286 | 0.094 | 0.842 | 0.294 |
| Capability ablation | 8 | 0.301 | 0.097 | 0.837 | 0.234 |
| Intervention-only null | 6 | 0.326 | 0.105 | 0.842 | 0.308 |
| Value-only macro | 4 | 0.630 | 0.218 | 0.517 | 0.228 |
| Observable-micro baseline | 36 | 0.669 | 0.174 | 0.748 | 0.451 |

Promotion criteria:

- pass — `20pct_better_than_value`
- fail — `20pct_better_than_intervention`
- pass — `within_10pct_of_micro`
- pass — `quarter_micro_features`
- pass — `brier_below_0_25`
- pass — `ablation_beats_both_nulls`

## Interpretation boundary

This test concerns predictive usefulness of an observable macro description. A pass would not establish agency, goal possession, or causal emergence. A failure is a decision to revise the observation/outcome before adding analysis machinery.
