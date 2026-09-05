# P7-005 network-informed intervention value — results

**Decision: evidence-closed-no-go.**

## Integrity

- exactly_16_seeds_and_four_intervention_rows: PASS
- matched_through_tick_20: PASS
- complete_or_extinct_trajectories: PASS
- node_count_150: PASS
- fixed_15_and_30_node_public_actions: PASS
- both_budgets_have_16_pairs: PASS
- stored_source_and_setup_hashes_match: PASS

## Frozen causal gate

- Random mean burden: 205.906
- Degree mean burden: 173.562
- Pooled reduction: 15.7%
- Degree wins at 10%: 10/16
- Degree wins at 20%: 9/16
- Gate: FAIL

| Split and budget | Mean random-minus-degree burden |
|---|---:|
| discovery_10 | 173.250 |
| discovery_20 | -19.875 |
| confirmation_10 | -39.750 |
| confirmation_20 | 15.750 |

This is retrospective Level 1 evidence on already-open P7-002 trajectories. It
cannot rescue the representation selector or establish prospective/general
control value.
