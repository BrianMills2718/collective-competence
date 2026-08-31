# P7-005 network-informed intervention-value audit — results

## Decision

**Evidence-closed no-go.** All seven integrity gates passed. Degree-informed
immunization reduced pooled mean infected-node burden by 15.7%, clearing the
frozen average-effect threshold, but failed both robustness requirements.

| Quantity | Frozen requirement | Observed | Gate |
|---|---:|---:|---|
| Pooled burden reduction | at least 15% | 15.7% | pass |
| Degree wins, 10% budget | at least 11/16 | 10/16 | fail |
| Degree wins, 20% budget | at least 11/16 | 9/16 | fail |
| Positive effect in both splits, both budgets | 4/4 cells | 2/4 | fail |

Random targeting averaged 205.906 infected-node-ticks versus 173.562 for degree
targeting. That pooled advantage was not stable:

| Split | Budget | Mean random-minus-degree burden |
|---|---:|---:|
| Discovery | 10% | +173.250 |
| Discovery | 20% | −19.875 |
| Confirmation | 10% | −39.750 |
| Confirmation | 20% | +15.750 |

The 10% budget showed a 23.2% pooled reduction, while the 20% budget was 1.7%
worse under degree targeting. Extinction rates were 25.0% random versus 43.8%
degree at 10%, and identical at 68.8% at 20%; these were frozen as secondary,
non-gating outcomes.

## Integrity and recovery note

Exactly 16 mechanically eligible seeds and 32 same-budget pairs were present.
All policies matched through tick 20, trajectories were complete or padded only
after extinction, node count remained 150, both budgets had every pair, the
stored source/setup hashes matched, and the XML retained the fixed 15- and
30-node public interventions. No NetLogo outcome was generated.

The first finalization attempt wrote the frozen paired tables and then failed to
serialize a NumPy boolean. Type normalization completed the decision artifact
from the same stored trajectories and contract. No source outcome, causal
contrast, threshold, or result changed, and the finalized output refuses a
second run.

## What was learned

Network degree can look useful in the pooled average while selecting an action
that is unreliable across independent networks, budgets, and splits. The sign
reversals are exactly why V4 required per-unit failures and intervention-value
robustness rather than one aggregate improvement.

Together, P7-003, P7-004, and P7-005 close the current internal V4 route:

- generic representation selection was unstable;
- task-conditioned predictive scales did not beat the simple null; and
- the network-informed action did not provide robust causal value.

Do not add Virus seeds, tune immunization, change the outcome, or return to Ants
prediction. A future V4 reopening requires a genuinely new causal task or a
qualified external evidence bundle, not another internal repair loop.

## Claim boundary

This is retrospective Level 1 causal evidence from policies and trajectories
originally frozen for P7-002. It does not rescue that selector, establish
prospective transfer, or justify general network-control or competence claims.
V4 is evidence-closed for the current internal route, not universally refuted.

Artifacts are in `results/p7-005-network-intervention-value/`.
