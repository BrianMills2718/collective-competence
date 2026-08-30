# P2-002 crossed distributed macro prediction — prototype results

## Decision

**No-go at the frozen discovery gate. The size-24 batch was not generated.**

The capability-aware macro family was the best attainment predictor, but its
leave-one-seed-out log loss was 0.264 versus 0.326 for the intervention-only
null: an 18.9% reduction, short of the frozen 20% requirement. The threshold
was not changed after seeing the result.

## What ran

- 144 deterministic size-12 branches;
- six unseen initial-condition seeds;
- index and shuffled activation;
- tick-zero and tick-four damage;
- moveable and immovable freezing;
- one, two, and three frozen cells;
- 1,714 stored trajectory rows.

The batch broke the original confound. Overall goal attainment was 32.6%, and
three of the six freeze mode/count classes contained both successes and
failures.

## Representation results

| Representation | Inputs | Held-out log loss | Brier loss | Balanced accuracy | Conditional time MAE / cell |
|---|---:|---:|---:|---:|---:|
| Capability-aware macro | 9 | **0.264** | **0.083** | **0.895** | 0.234 |
| History-aware macro | 12 | 0.286 | 0.094 | 0.842 | 0.294 |
| Capability ablation | 8 | 0.301 | 0.097 | 0.837 | 0.234 |
| Intervention-only null | 6 | 0.326 | 0.105 | 0.842 | 0.308 |
| Value-only macro | 4 | 0.630 | 0.218 | 0.517 | **0.228** |
| Observable-micro baseline | 36 | 0.669 | 0.174 | 0.748 | 0.451 |

The capability family passed every frozen criterion except the 20% improvement
over intervention-only. It compressed the observable-micro description by
fourfold, was calibrated on this screen, and survived removal of the direct
resolvable-inversion feature. Value-only geometry was marginally best for
conditional time-to-goal, so attainment and recovery time remain distinct
prediction problems as planned.

## Error audit

The no-go is informative rather than a disappearance of the signal.

Capability adds the most information in genuinely ambiguous regimes:

- shuffled, tick 4, three moveable freezes: log-loss gain 0.517;
- index, tick 4, two moveable freezes: gain 0.300;
- index, tick 4, three moveable freezes: gain 0.278;
- either schedule, tick 4, one immovable freeze: gain about 0.23.

It loses to the intervention-only null in deterministic regimes such as one
moveable freeze (all succeed) and early immovable freezing (all fail). The
aggregate test therefore mixes the hard within-condition question with easy
condition-label prediction.

This does not retroactively pass P2-002. It identifies the next discriminating
experiment: freeze a new, outcome-balanced study centered on the boundary
regimes above and test within intervention strata on unseen seeds before paying
for a new size.

## Evidence

Machine-readable runs, trajectories, predictions, condition summaries, error
audit, decisions, and the static evidence figure are in
`results/p2-002-crossed/`.

## Interpretation boundary

The result supports retained capability as a promising measurement candidate.
It does not establish a higher-level agent, a goal, or causal emergence. The
current decision is to improve theory discrimination, not to add system
complexity or visualization machinery.
