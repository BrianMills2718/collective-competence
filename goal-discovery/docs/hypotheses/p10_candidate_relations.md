---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
---
# P10: learned endpoint relations versus restoration

[Wiki](../../../wiki/index.md) · [Current plan](../plans/current_research_plan.md)

## Question and scope

Can an inspectable learner propose an endpoint relation without receiving the
sorting target, then distinguish restoration from a history-dependent regularity?
This is a bounded proposal-and-intervention calibration, not discovery of an
unexpected competency or a general attribution of goals.

The experimenter knows the specimen is bubble cell-view sorting. Duplicate
values deliberately make value order and identity history separable. The
learner does not receive that rule or a sorting metric. Candidate language,
feature family, learner, probes, and expected distinguishing contrast below are
supplied by the researcher; we do not claim analyst novelty.

## Frozen observations, learner, and splits

- Unchanged `SortingWorld`; focal system is the cells on a fixed line. The
  activation scheduler is external context, not a reciprocally evolving world.
- Allowed observations: tick and rows of position, carried value, opaque identity.
  No rule names, internal target, capability, action narrative, or authored metric.
  Identity is a lookup key; its numeric/lexical ordering is never a feature.
- Pair features: signed carried-value difference and signed **initial-position**
  difference. Both orientations of every distinct pair are training rows.
  Label: whether the first identity is left of the second at the fixed endpoint.
- Off-the-shelf scikit-learn decision tree: max_depth=3, min_samples_leaf=2,
  random_state=0, other classifier defaults. Export the entire learned tree,
  including thresholds, leaves, training revision, settings, and content hash.
- Discovery: seeds 100–111 inclusive, 12 cells, values 0–5 each repeated twice,
  initial permutation shuffled with the seed, shuffled activation, 96 ticks.
- Held-out evaluation: seeds 1000–1023 inclusive, 16 cells, values 0–7 each
  repeated twice, initial permutation shuffled with the seed, 128 ticks;
  index activation on even seeds, reverse-index activation on odd seeds.
- Fixed horizons only: do not stop using rule-aware quiescence.
- Freeze this protocol before discovery. Commit the executable implementation
  and learned candidate before opening held-out runs. No fitting during evaluation.
  No retuning or additional seeds after seeing failures in this sprint.

Observation relabeling must preserve predictions. Relabel only observation IDs;
changing simulator IDs would also change scheduler semantics.
The independent unit is a run/seed, not a pair or frame.

## Distinguishing interventions

At the fixed held-out endpoint select two pairs using **observations**, not
the learned rule: (a) the first and last positions, requiring unequal values;
(b) the first equal-valued pair in positional enumeration.
The same selected identities define the candidate relation throughout replay.
Expected relative orientation comes from the frozen learner using the original
initial frame, not from outcomes after intervention.

Each probe has three branches cloned from the identical full snapshot:

1. Baseline: no intervention, original activity.
2. Active: transpose the two complete cells; original activity resumes.
3. Disabled: the same transposition, then disable all cells with immovable freeze.

Record and verify snapshot identity/RNG, preserved cell attributes for active
transposition, conserved values/identities, unchanged counters and tick, and
disabled-only capability change. Shared RNG origin does not assert identical
subsequent random events under different mechanisms.

Run every branch for exactly 64 further ticks. The value multiset is conserved
by these operations; that is not evidence of its recovery after disruption.
The equal-valued swap changes identity history without changing value arrangement.
The unequal-valued swap changes both. These probes are supplied, not automatically
selected by the discovery procedure.

## Metrics, gates, and abstention

- Report all 24 per-run endpoint pair accuracies and initial-position-order
  baseline accuracies. Do not pool correlated pairs into confidence estimates.
- Endpoint gate: at least 20/24 runs have candidate accuracy >=0.95 and exceed
  the initial-order baseline on the same run.
- Probe eligibility requires unchanged observed cell ordering during the final
  eight pre-intervention frames, a candidate-correct relation before the swap,
  and the swap reversing that relation. Missing pairs or failed eligibility
  remain visible and count as nonpasses, not removed denominators.
- Restoration means the selected pair agrees with its predeclared candidate
  orientation in **every one of the final eight branch frames**.
- Contrast gate: unequal active restores in >=20/24 runs and unequal disabled
  restores in <=4/24; equal active restores in <=4/24.
- Any snapshot/projection/conservation failure invalidates the affected run.
  Report integrity separately from score; invalid results cannot promote a claim.
- A calibration pass requires endpoint and contrast gates, intact projection/
  intervention checks, and observation-ID relabel invariance.
- Otherwise abstain or qualify the result; do not change the gate.

The expected contrast is disclosed in advance: an endpoint predictor can combine
recoverable value order with non-restored initial tie order. Even a pass supports
only this bounded distinction, not active agency, general goal discovery, causal
uniqueness, or transfer across substrates. A learned relation equivalent to a
known sorting measure is procedural proposal progress, not a new scientific fact.
The disabled baseline rules out inert persistence, not every passive attractor.

## Artifact and resource bound

Keep measured discovery/evaluation JSON with candidate, every seed, branch
decisions, integrity checks, protocol/source/candidate hashes, revisions, UTC
timestamps, and one first-held-out-seed replay. Use the existing Panel apparatus:
learned rule -> selected pair -> matched trajectories -> per-seed evidence ->
claim limit. Full-run results remain labeled retrospective during replay.

One 60–90 minute learning sprint: target first authentic observation in 30 minutes.
Reuse the model, snapshots, scikit-learn, Panel, and plotting components.
No new engine, generic feature tournament, categorical migration, or new dashboard.
If the proposal fails, preserve that result and update the current plan; no
confirmation-grade campaign or automatic retry is authorized by this protocol.
