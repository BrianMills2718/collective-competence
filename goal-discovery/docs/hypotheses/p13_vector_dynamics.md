---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
---
# P13 — blind vector dynamics and causal challenge

[Wiki](../../../roadmap/README.md) · [Current plan](../plans/current_research_plan.md)

## Decision and claim boundary

Can a small observation-only proposal procedure infer a stable vector relation
on the existing passive bowl without receiving its target, equations, energy,
goal tolerance, or intervention outcomes? Can prospective challenges prevent
that inferred attractor from being mislabeled a general competency?

This is a reduction-in-prescribed-interpretation calibration on a second
substrate. The system, linear candidate grammar, coordinate identity, position
and velocity observations, challenge family, thresholds and expected controls
are supplied. A successful result is not unexpected science, agency, or an
open-ended discovery demonstration.

Reuse `BowlWorld` unchanged. Do not add a simulator, generic representation
framework, adaptive selector, or post-outcome model family. Observation records
contain exactly `tick`, opaque `run_id`, and eight ordered coordinates with
opaque ID, position x, and velocity v. Learner functions reject extra fields.
Configuration, stiffness, damping, epsilon, frozen state, RNG, intervention
label, authored target, `at_goal`, and `quiescent` never cross the learner boundary.

## Frozen proposal procedure

Discovery uses seeds6100–6107, n=8, spread10, ticks0–40 inclusive. Fit on
one-step transitions; leave one whole seed out at a time for model selection.
The supplied candidate families, from simplest to most expressive, are:

1. `persistence`: next full state equals current state;
2. `position_ar`: shared affine x-next from x; velocity persists;
3. `shared_local_linear`: one shared affine 2x2 transition maps each
   coordinate's own (x,v) to its next (x,v);
4. `full_vector_linear`: affine 16x16 transition can couple every coordinate.

Use NumPy least squares only. Scores are RMS error over every held-out scalar
state value; seeds are independent units. A family is discovery-adequate when
every leave-one-seed-out RMS <=1e-8. Select the first adequate family whose mean
RMS is within1e-10 of the best adequate mean. If none qualifies, abstain and do
not run outcome challenges as evidence for a candidate.

Refit the selected family on all discovery observations. Derive its affine
fixed point by solving `(I-A)z=c` and its spectral radius. Propose a stable
fixed-state relation only if the solve is full-rank, all quantities finite,
spectral radius<1, training RMS<=1e-8 and max absolute fixed-point component
<=20. For a local model, expose the shared2-vector fixed point; for a full model,
expose all16 components and cross-coordinate coefficient mass. These broad
validity bounds are numerical guards, not evidence of a goal.

Also freeze forecasts, selected-family bytes/hash and all candidate quantities
before outcomes. Commit and push the candidate before evaluating. Preserve
discovery observations as JSONL and refuse overwrite.

## Prospective challenges

Evaluation uses untouched seeds6200–6207 and four matched descendants per seed,
all from the exact tick40 snapshot and continuing through tick400:

| condition | operation at tick40 | learner input after operation |
|---|---|---|
| none | no change | observed state |
| displace | add ±6 to two seeded coordinates | resulting observed state only |
| kick | add ±2 to two seeded velocities | resulting observed state only |
| freeze | freeze one deterministically seeded coordinate away from the candidate | unchanged observed state only |

For exact replay, the intervention seed is `evaluation_seed * 10 + condition_index`
for the ordered conditions `none`, `displace`, `kick`, `freeze`. State challenges
sample without replacement from all eight coordinate IDs and then sample each
sign. The freeze challenge samples from coordinates whose post-prefix Euclidean
distance from the learned local fixed point is greater than 0.5; missing eligible
coordinates are an integrity failure. This minimum makes "away" operational
before outcomes and ensures the mechanism challenge is not a near-equilibrium
no-op. Selection remains evaluator-only metadata.

Each forecast begins from the post-operation observed state. The learner does
not receive condition or frozen status. Preserve exact snapshot lineage,
intervention seed/target IDs for evaluator provenance, and all observations as
JSONL. Outcome scoring unlocks condition metadata only after forecast creation.

Frozen checks:

- `none`, `displace`, `kick`: whole-state forecast RMS across ticks41–400
  <=1e-8; all coordinates are within0.01 Euclidean distance of the learned
  local fixed point throughout ticks369–400.
- `freeze`: whole-state forecast RMS>0.1, the frozen coordinate remains >0.01
  from the candidate throughout the final32 ticks, and every unaffected
  coordinate is within0.01. Forecast RMS restricted to unaffected coordinates
  remains <=1e-8.
- Every seed must satisfy its condition check; integrity failure remains in the
  denominator. Report counts by runs, not coordinate-ticks.
- The learned local law must agree with the hidden configured dynamics only as
  an evaluator diagnostic: coefficient max error<=1e-8 and fixed point within
  1e-8 of (0,0). This unlock does not select or retune the candidate.

If an expected scientific check fails with valid integrity, retain the negative
result and change direction. If integrity, leakage, rank, or candidate freeze
fails, repair before interpretation. Do not weaken thresholds, add nonlinear
terms, increase seeds, or reinterpret freeze failure as active defense.

## Inspectable result and next decision

Extend the existing desktop laboratory with one P13 view that connects:
observations -> family comparison -> learned equation/fixed point -> frozen
forecast -> cutoff-limited actual trajectory -> condition-specific conclusion.
Show coordinate/phase state at the selected tick and separate online evidence
from retrospective summaries. The default replay is seed6200; it is fixed here,
not selected for appearance.

If successful, retain a bounded cross-substrate proposal/falsification seam.
The next question becomes whether the same declared proposal grammar finds a
nontrivial relational candidate on a system with interactions, without exposing
authored mechanism fields. If it merely rediscovers the bowl's passive origin,
say so: method calibration advanced, scientific novelty did not.
