# P6-001 — neuromast local-feedback causal calibration

**Frozen after P6-000 and before generating P6-001 trajectories.**

## Sprint card

**Goal movement:** establish whether a published multiscale regeneration model
supplies a clean causal recovery contrast through an observable macro boundary.

**Unknown being tested:** whether local homotypic-neighbor stopping feedback is
necessary for bounded recovery of organ size and composition after severe
ablation in the selected off-the-shelf model.

**Observable artifact:** one three-timepoint cell-layout strip and one decision
figure linking cell count, composition error, late growth, and radial order.

**Competing explanations:** successful recovery is caused by local stopping
feedback; it is merely passive tissue relaxation; or stochastic proliferation
alone is sufficient and the stopping rule is unnecessary.

**Time to first artifact:** 20 minutes.  
**Maximum sprint time:** 90 minutes.  
**End decision:** promote one held-out-layout prediction or close M4377.

## Claim under test

In the published M4377 Morpheus neuromast model, local cell-type-specific
neighbor thresholds cause a severely ablated tissue to recover a bounded,
approximately proportional organ-level macrostate. Removing the neighbor-
dependent stopping terms while retaining stochastic proliferation should
produce overgrowth; removing proliferation should leave the damaged tissue far
from the recovered macrostate.

This is a Level 1 calibration of a published authored mechanism. Passing does
not establish an autonomous goal, discover the mechanism, validate the model's
biology, or show that the laboratory can yet infer recovery on unseen tissue
layouts.

## Frozen source and execution boundary

Use the authors' Figure 4 example `E03.xml` from Zenodo record
[`13922477`](https://zenodo.org/records/13922477), contained in
`xml_examples.zip` with SHA-256
`03aae512a6d299593a45db46ae4946867993be3b8144528399cf81e9271417f1`.
The extracted XML SHA-256 is
`b289691efcb699bf141106ae47cc024a3be75aad6927b0bf9a6bcf5794d0ab26`.
It embeds the damaged E03 cell layout and runs to 210,000 Monte Carlo steps.

Use the official Morpheus 2.4.1 static Linux simulator from the
[2.4.1 release](https://morpheus.gitlab.io/download/2.4.1/), SHA-256
`06a9b44dca3195536907657348e5c6882711f9ce6e60f39af71fef2362e093c7`.
The adapter may download and cache these exact artifacts but must reject a hash
mismatch.

The generator and analysis remain separate. The generator variants may change
only:

- the random seed;
- logger cadence from every step to every 5,000 steps;
- logger fields to include `cell.center.x`, `cell.center.y`, and `cell.volume`;
- the two neighbor-stopping predicates for the declared feedback-disabled arm;
- the two division probabilities for the declared proliferation-disabled arm;
- removal of Gnuplot output for headless runs.

No adhesion, motility, cell-size, fate, division timing, initial-layout, or
other model parameter may change. The standard Morpheus GUI remains the live
visualizer; Matplotlib may render the one compact decision artifact from logged
observables.

## Frozen design

Use fresh seeds 801–804. For each seed, run three matched conditions:

1. `active`: published dynamics unchanged;
2. `feedback_disabled`: replace only
   `Mantle_Neighbours < umbral` and
   `Sustentacular_Neighbours < umbral` in division conditions with a constant
   true predicate, retaining stochastic proliferation and fate rules;
3. `proliferation_disabled`: set global division probabilities `pm = 0` and
   `ps = 0`, retaining the same cell mechanics and damaged layout.

There are 12 runs. Conditions and seeds may run concurrently with one Morpheus
thread per run. All conditions use the same 210,000-step horizon and log at
times 0, 5,000, ..., 210,000.

## Observation and frozen measures

Analysis may observe only logged time, cell identity, cell type, center,
volume, same-type neighbor counts, and population counts. It may not read the
condition's thresholds, probabilities, or division predicate when computing
outcomes.

Use the published E03 day-7 experimental macrostate from
`data_neuromast.csv` as a declared calibration target:

- hair cells: 14;
- sustentacular cells: 27;
- mantle cells: 11;
- total cells: 52.

For each logged time, define the composition vector in the order hair,
sustentacular, mantle. Define macro distance as:

```text
abs(total - 52) / 52
+ 0.5 * L1(observed composition proportions, [14, 27, 11] / 52)
```

Define late growth as the absolute total-count change from time 170,000 to
210,000 divided by final total count.

Define radial order from cell centers relative to the current organ centroid:

```text
0.5 * P(radius(hair) < radius(sustentacular))
+ 0.5 * P(radius(sustentacular) < radius(mantle))
```

Compute each probability over all cross-type cell pairs. A missing type makes
the score zero. This is an observable spatial-order instrument, not a biological
claim that those two inequalities exhaust neuromast architecture.

## Frozen calibration gate

Promote only if all conditions hold:

- all 12 runs complete, have the declared source hashes, contain all three cell
  types at time zero, and expose identical time-zero macrostate across matched
  conditions;
- active feedback has median final macro distance at least 30% lower than each
  control, and is lower than each control in at least three of four paired
  seeds;
- active feedback has median late growth no greater than 0.10;
- feedback-disabled final cell count is at least 25% above its paired active
  count in at least three of four seeds;
- proliferation-disabled final cell count is no more than one cell above its
  time-zero count in every seed; and
- active feedback has median final radial-order score at least 0.70.

The primary claim is the two-control causal separation in macro distance. The
late-growth, overgrowth, no-growth, and radial-order clauses prevent a low
distance at one endpoint from being mistaken for bounded organ reconstruction.

## Integrity attacks

- Verify source, simulator, protocol, and generated-variant hashes.
- Parse one logger file independently and confirm counts equal the number of
  unique observed cells of each type at every logged time.
- Confirm the two control variants differ from active only at the frozen XML
  locations plus instrumentation.
- Re-run one active seed and require identical terminal observables.
- Report, but do not repair, any Morpheus v4-to-v5 automatic-conversion warning.

## Decision and stop rule

Stop immediately if one matched three-condition seed cannot finish within 25
minutes or if the logged center/type boundary is invalid. Stop after the 12-run
gate; do not tune thresholds, target values, horizon, or radial metric.

A pass licenses one separately frozen test that trains a compact macro
predictor on E03 plus a small set of source layouts and predicts active recovery
on held-out experimental layouts against count-only and intervention-only
nulls. It does not yet unlock broad causal-emergence tooling. A failure closes
M4377 and records which hard requirement the runtime test failed to realize.
