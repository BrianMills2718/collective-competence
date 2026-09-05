---
doc-role: preregistration
authority: evidence
lifecycle: frozen
---
> **Classified 2026-09-05.** This file carried no frontmatter at all, so it
> declared neither a role nor a lifecycle and read as an ordinary historical
> plan. It is a **frozen preregistration**, which the repository's own rule
> places on the preserve list alongside result measurements, original briefs
> and historic audits. Body unchanged.

# P7-005 — network-informed intervention-value audit

**Status:** executed once / complete-negative. This frozen Level 1 retrospective
causal contract is retained unchanged; see
`docs/hypotheses/p7_005_network_intervention_value_results.md`. No new Virus
outcomes may be generated.

## Question and V4 decision

> On the already-generated Virus on a Network cases, does an observable
> network-scale action—immunizing the highest-degree nodes—reduce subsequent
> infection burden relative to scale-free random immunization at the same
> budget?

This asks whether a higher-level description changes intervention value. It is
not another representation-prediction contest and cannot reopen the failed
P7-002/P7-003 selector claim.

## Why this is the cheapest justified sprint-3 test

The five P7-002 arms already contain matched baseline, random, and degree-based
immunization at 10% and 20% budgets on an unmodified off-the-shelf NetLogo
model. Their network seeds, pre-intervention states, node degree, interventions,
and post-intervention trajectories are stored. Reusing them requires only one
specialized causal summary and creates no new simulator, adapter, feature
family, visualization, or trajectory.

P7-004 Ants is retired for predictive scale selection. Designing new Ants
policies would require choosing a stronger cut after observing rapid field
reconstruction. A fresh generator would cost more before testing the narrower
question that the existing Virus arms already instantiate.

## Evidence and claim boundary

Use only `results/p7-002-network-level2/` and the mechanically eligible P7-002
seeds:

- discovery: 10001–10008;
- confirmation: 10014–10021.

The policies and trajectories were prospectively fixed for P7-002, but this
causal outcome and promotion gate are being defined after the extinction
outcomes were opened. P7-005 is therefore retrospective Level 1 evidence. A
pass can mark causal intervention value as measured on this task; it cannot
establish prospective transfer, rescue the selector, or license a general
control claim.

## Frozen causal contrast and competing scale

At tick 20 compare, within the same network seed and budget:

- **scale-free null:** immunize `n-of` nodes at random;
- **network-scale action:** immunize `max-n-of` nodes by observable link degree.

Budgets remain exactly 15/150 nodes (10%) and 30/150 nodes (20%). The baseline
arm is a no-action descriptive reference, not the primary null. No feature
model is fitted: the representation earns value only if the action it selects
causes a better downstream result than the same-budget scale-free action.

## Observation, intervention, and outcome boundaries

- Observations and network ranking use only the shared trajectory through tick
  20 and observable degree.
- The intervention is the already-frozen call to the standard model's
  `become-resistant` procedure at tick 20.
- The primary outcome is cumulative infected-node-ticks over ticks 21–100,
  padding early extinction with zeros through tick 100.
- The paired causal effect is `random burden - degree burden`; positive values
  favor network-scale targeting.
- Secondary, non-gating outcomes are endpoint infected count and extinction by
  tick 100.

No post-tick-20 state may enter action selection. Do not change seed eligibility,
budgets, horizon, model parameters, or outcome after opening this contrast.

## Frozen integrity gates

All must pass:

1. exactly 16 eligible seeds and four intervention rows per seed exist;
2. random and degree arms within each seed/budget are identical through the
   tick-20 observation;
3. each trajectory is complete through tick 100 or reaches zero infected and
   is padded only with zeros;
4. every arm preserves 150 nodes;
5. the resistant-count jump is exactly 15 or 30 nodes, except nodes already
   resistant at tick 20, which must be identically accounted for by the public
   procedure;
6. both budgets contain all 16 matched seed pairs;
7. no new NetLogo output is created and stored source/setup hashes still match
   the P7-002 metadata.

An integrity failure stops the sprint without repairing data or generating new
seeds.

## Frozen decision gate

Network-scale intervention value passes only if degree targeting:

- reduces pooled mean infected-node-ticks by at least 15% versus matched random
  targeting;
- has lower burden in at least 11/16 seeds at the 10% budget and at least 11/16
  seeds at the 20% budget; and
- has a positive mean paired effect separately in the original discovery and
  confirmation seed pools at both budgets.

Ties count as non-wins. Report every paired seed effect and both secondary
outcomes. Do not substitute a significance test or tune a threshold after the
contrast opens.

## Time cap, stop, and retirement branches

Cap the sprint at **45 minutes**, with a complete paired causal table by minute
15 and the decision artifact by minute 35.

- **Pass:** mark V4 causal intervention value `measured-retrospective` for this
  task, keep general/prospective control claims locked, and decide separately
  whether a fresh prospective confirmation is worth funding.
- **Fail:** evidence-close the current internal V4 route. P7-003, P7-004, and
  P7-005 then jointly show that neither generic selection, a task-conditioned
  predictive scale, nor this network-informed action earned promotion. Do not
  add Virus seeds, tune immunization, or switch outcomes.
- **Integrity stop:** retain V4 as unresolved and retire this evidence source.

In every branch, stop Virus analysis after this one contrast. Do not add a UI or
generalize OB-001 into company planning in this sprint.

## Outcome-backcasting trace

```text
Mature outcome supported: intervention and control value of higher-level scales
Target version: V4 — perturbation and scale
Question made answerable: does a network-scale observation improve a matched
  intervention decision beyond a scale-free action?
Placeholder replaced: hypothetical causal intervention-value comparison
Evidence and provenance produced: fixed paired burden table, integrity ledger,
  budget/split effects, decision artifact, source hashes
Acceptance test: all integrity gates plus the frozen effect/seed-win/split gate
Stop/removal rule: one contrast only; fail closes the current internal V4 route
Possible artifact or plan revision: measured-retrospective on pass,
  evidence-closed-no-go on fail, unresolved on integrity stop
```
