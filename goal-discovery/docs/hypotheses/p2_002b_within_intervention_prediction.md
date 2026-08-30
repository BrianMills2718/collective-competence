# P2-002b — within-intervention capability prediction

**Frozen after the P2-002 no-go and before generating any P2-002b trajectory.**
P2-002 is the pilot that selected the regimes; P2-002b uses disjoint seeds.

## Question

> Within ambiguous intervention classes, does the same nine-input
> capability-aware macro description predict goal attainment at least 20%
> better than both the intervention-only and value-only alternatives?

This is narrower than P2-002. It does not retroactively rescore or pass the
broad factorial.

## Discovery design

Run the Cartesian product of:

- size: 12;
- new initial-condition seeds: 201–212;
- activation schedule: index and shuffled;
- branch time: `n / 3` (tick 4);
- damage classes selected by the prior error audit:
  - two moveable freezes;
  - three moveable freezes;
  - one immovable freeze.

This is 72 branches. The generator, observation boundary, horizon, feature
families, logistic attainment estimator, ridge time estimator, seed grouping,
and metrics are unchanged from P2-002.

## Eligibility gate

Before model promotion is considered:

- none of the branches may already be sorted when damaged; and
- all six schedule × damage strata must contain both success and failure.

If this fails, report the regime instability and stop. Do not remove a failed
stratum after seeing its outcomes.

## Promotion gate

Use the unchanged P2-002 requirements. The capability-aware family must:

- reduce leave-one-seed-out attainment log loss by at least 20% versus
  intervention-only and value-only;
- stay within 10% of the observable-micro baseline with no more than one
  quarter as many inputs;
- have Brier loss below 0.25;
- remain better than both nulls after removing the direct
  resolvable-inversion feature.

Attainment and conditional time-to-goal remain separately reported. No
threshold or feature changes are permitted after generation.

## Conditional size holdout

Only after discovery eligibility and promotion pass, repeat the identical
schedule × damage design at size 24, branch tick 8, on seeds 501–512. Fit once
on the size-12 discovery rows. Require the frozen 20% advantage overall and
within both schedules, plus the compression, calibration, and ablation gates.

A pass reaches Level 2 predictive evidence. It unlocks a mechanism-ablation
sprint, not a claim of agency or causal emergence.
