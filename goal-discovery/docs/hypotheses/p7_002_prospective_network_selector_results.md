# P7-002 prospective network selector — results

**FAIL: the selected family improved untouched confirmation log loss by 8.4%,
below the frozen 10% promotion gate.**

## Integrity and task

All five arms were identical through the tick-20 observation boundary. The
mechanical eligibility rule selected discovery seeds 10001–10008 and confirmation
seeds 10014–10021; seed 10013 was already extinct at tick 20 and was excluded
without consulting its future outcome. Both splits contained extinction and
persistence. The installed NetLogo 7.0.4 model was unmodified.

Across each split's 40 arm-network cases, extinction fractions remained
non-degenerate. Discovery arm rates ranged from 12.5% to 62.5%; confirmation
rates ranged from 37.5% to 75%. This was a valid prediction task rather than a
failure of class balance or execution.

## Frozen discovery selection

| Family | Discovery log loss | Improvement over null | Decision |
|---|---:|---:|---|
| Identity-conditioned | 0.618 | 16.7% | selected |
| Temporal | 0.637 | 14.1% | not opened on confirmation |
| Network | 0.722 | 2.7% | not opened on confirmation |
| Relational | 0.742 | −0.1% | not opened on confirmation |
| Intervention-only null | 0.741 | — | comparison |

Identity-conditioned history was uniquely best by more than the frozen 0.005
tie margin and exceeded the 10% discovery threshold. Under the protocol, only
that family and its ablation were opened on confirmation.

## Untouched confirmation

| Model | Confirmation log loss | Improvement over null | Gate |
|---|---:|---:|---|
| Intervention-only null | 0.660 | — | comparison |
| Selected identity-conditioned | 0.604 | 8.4% | **fail; requires 10%** |
| Frozen identity ablation | 0.565 | 14.4% | diagnostic only |

The selected family's direction transferred, but not by the preregistered
margin. The ablation removed mean/max per-node duration features and performed
better than the full selected representation. That suggests excess descriptive
capacity or unstable duration summaries, but it cannot retroactively promote the
ablated model. Treating it as a pass would use confirmation outcomes for tuning.

## Decision and claim boundary

P7-002 does not promote the reusable selector and does not unlock a naturalistic
transfer or macro causal/control analysis. Do not add Virus seeds, relax the 10%
gate, or rerun confirmation with the ablated model.

The result purchases one bounded Level 1 methodology audit: determine whether
family comparison is being confounded by unequal descriptive/model capacity.
P7-003 uses all P7-002 outcomes as explicitly retrospective development evidence,
defines a capacity-matched four-summary-per-family contract, and either freezes
that contract for a different future prospective task or stops generic family
selection. It cannot generate a P7-002 claim.

The dynamic cockpit artifact exposes the real network trajectories, tick-20
intervention boundary, representation lenses, independent seed outcomes,
discovery scores, confirmation failure, and next decision from these artifacts.
