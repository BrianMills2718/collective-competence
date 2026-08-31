---
doc-role: experiment-evidence
authority: evidence
lifecycle: completed
---
# Executable composition: bounded exploratory result

2026-08-31 · [Current priorities](../plans/current_research_plan.md) ·
[Viewing and reproduction](../../README.md#optional-composition-exploration)

## Decision

**Defer production adoption of a categorical runtime. Retain the optional
prototype and explicit interfaces.** This is a negative value-gate result for
the tested small pipelines, not a rejection of category theory or open games.

The laboratory's goal remains open-ended discovery of unexpected goals and
competencies across diverse systems. This experiment tested representation and
execution fidelity, **not discovery**. No unexpected goal was discovered.

Both implementations express every tested experiment and reject incompatible
connections. DisCoPy additionally provides algebraic diagram objects, composition,
and an executable interpretation of those objects. That is real functionality,
but it did not unlock a presently needed experiment or demonstrate lower
maintenance cost than a small validated Python pipeline. Runtime was not the
main objection; the value gate was not met.

## Research and off-the-shelf comparison

An [open game](https://arxiv.org/abs/1603.04641) includes strategies, play,
coplay, and context-dependent best-response structure. It does not require
every component to have a numeric utility, but choice/preference structure is
supplied. Inferring an unknown competency from observations is a separate
problem. [Open games with agency](https://arxiv.org/abs/2105.06763) and
[Cyber Kittens](https://arxiv.org/abs/2101.10483) refine agency/dynamical
realizations; they are not ready-made empirical goal detectors.

| Candidate | Capability and fit | Disposition |
|---|---|---|
| Ordinary typed Python | Existing kernels, explicit ports and runtime checks; no new runtime | Fair baseline and default direction |
| [DisCoPy](https://github.com/discopy/discopy), BSD-3-Clause, pinned 1.2.2 | Typed string diagrams interpreted into Python functions | Implemented as optional extra; not full open-game semantics |
| [AlgebraicDynamics.jl](https://github.com/AlgebraicJulia/AlgebraicDynamics.jl), MIT | Compositional open dynamical systems, Julia/Catlab ecosystem | Relevant future candidate; a language/runtime migration is not justified here |
| [open-game-engine](https://github.com/CyberCat-Institute/open-game-engine), AGPL-3.0 | Haskell implementation for games and supplied strategic structure | Not integrated; unnecessary setup and wrong immediate scientific question |

DisCoPy's [monoidal functor](https://docs.discopy.org/en/main/_api/discopy.monoidal.Functor.html)
maps the displayed diagram to the functions actually executed. We did not
implement strategy profiles, coplay or best responses, and do not call the
prototype categorical game theory.

## What was built and compared

One optional tab in the existing Panel cockpit, not a second production UI:
configuration → three replay branches → supplied-probe traces → executed wiring
and finite checks → measured cost and decision.

Each tick composes **context/intervention → unchanged native transition →
readout**, returning an immutable full-state/RNG snapshot for the next tick.
The outer loop supplies temporal feedback; there is no instantaneous feedback.

Three execution paths use the same kernels: a direct reference loop, an ordinary
validated Python pipeline, and the DisCoPy functor. Equality compares complete
samples/snapshots, including RNG and identities, not visually similar curves.
The native reference shares intervention/readout helpers: it tests wrapper
equivalence, not independently the correctness of all scientific definitions.

Sorting uses existing bubble, insertion and selection cells. Passive bowl
dynamics provide a low-cost transfer example and a control against confusing
convergence with agency. The same stage/pipeline/functor machinery, runner,
comparison logic and UI are reused; system-specific initialization, interventions
and probes remain explicit branches. This is not a universal substrate.

| Change | Sorting | Passive bowl |
|---|---|---|
| State | Exchange two cell blocks; retain identities, values and abilities | Displace every coordinate by +5; retain velocity |
| Environment | Replace scheduler | Remove damping |
| Mechanism | Immobilize the middle-position cell | Freeze coordinate zero |
| Null from tick zero | Random-swap cell rules with the same initial values | All coordinates frozen |

## Evidence and reproducibility

The machine-readable [batch record](../../results/composition/summary.json)
owns exact seeds, configurations, timings, source hashes and revision. It is
generated evidence, not a second planning authority. `demo.json` is regenerable.

- 144 configurations: four system/rule families × two sizes (8, 12) × six seeds
  (0, 1, 2, 3, 101, 102) × three interventions; 80 ticks, event before tick 15.
- 34,992 state triplets: three arms × 81 snapshots × 144 configurations.
  All three engines agreed exactly; no unexplained mismatches.
- Every baseline/intervention prefix matched through the pre-event snapshot.
  All interventions changed the next snapshot. A changed snapshot can reflect
  parameters alone; this does not establish changed behavior or competency.
- Left/right identity, regrouping, disjoint parallel composition, interchange,
  unchanged input, and invalid-wiring rejection passed finite checks for both systems.
- A deliberately type-correct no-op transition passes both connection checkers
  but fails the native behavior comparison. Type safety is not scientific validity.
- Focused composition/cockpit/sorting/bowl checks: **67 passed, 1 skipped**.
  The skip concerns absent regenerable historical Heatbugs data. Panel emitted
  future-deprecation warnings; no warning was counted as an experimental failure.

The runner aborts if implementation hashes change during a batch. Provenance
includes both kernels, sorting interventions, shared snapshot hashing, optional
implementation files and dependency lock. These fixed seeds are calibration
checks, not independent confirmatory evidence for discovered goals.

Timing uses five warm, alternating-order runs per engine, 12 components and
80 ticks, plus 20 construction measurements. See the batch record for absolute
milliseconds and ratios. Snapshot adapters cost substantially more than the
extra diagram dispatch in these small runs. These timings are local samples,
not a scalability result or a comparison of separately optimized frameworks.

Final batch source: clean revision `463da1948c199ce4d3b2d7cdc5ffdf59c633f0e4`;
source hashes remained unchanged during execution.

| System | Native ms | Python pipeline ms | DisCoPy ms | DisCoPy / Python |
|---|---:|---:|---:|---:|
| Sorting | 14.91 | 32.40 | 36.01 | 1.11× |
| Passive bowl | 13.86 | 32.69 | 36.27 | 1.11× |

Median construction was about 0.23–0.25 ms for the diagram/interpreter versus
0.00074–0.00081 ms for the Python pipeline. Absolute setup cost is small here;
the ratio alone would be a misleading adoption argument.

Implementation cost is also real: the core is 363 lines, including controls,
snapshots, adapters and tests-of-laws; the ordinary `Pipeline` is 15 lines and
the categorical constructor 28. Most code is shared experimental/visual support,
not a categorical advantage. Counts are cost context, not a productivity target.

## Visual audit and interpretation limits

The desktop browser rendered real numerical values and three branches. Changing
the system and environmental intervention reran the experiment; scrubbing the
timeline changed values and work counters. The rendered-system-switch test found
a Panel/Bokeh stylesheet synchronization error; toggling the containing layout
fixed it, with a rendered-template regression check added.

Pointer/button activation could not be verified reliably through this session's
browser automation. Automatic settings reruns and timeline scrubbing were
verified; Python tests also exercise Run and replay callbacks. Do not interpret
this as a verified mouse-driven Play/pause acceptance test. The diagram is
expanded by default so inspection does not depend on that control.

- Sorting scheduler changes also alter consumption of its shared random stream.
  They do not isolate ordering while holding later random draws constant.
- Null arms differ in mechanisms from the start; only baseline/changed arms have
  a matched pre-intervention past.
- Inversions and distance from zero are **hand-supplied probes**, not inferred goals.
  Whole-run plots are not online predictions at the selected replay time.
- Bowl position crossings are not settling. RMS **stored velocity** is also
  shown; frozen coordinates retain velocity state without moving.
- Whole-world steps, not interacting cell-level games, were composed. Parallel
  law checks use disjoint state, not interacting agents or shared randomness.
- Environments are prescribed by the experiment, not reciprocal evolving systems.
- The older cockpit tabs remain a historical published snapshot. The dirty main
  P8/P9 implementation was neither imported nor overwritten in this lane.

## Consequence for the next sprint

Keep immutable snapshots, explicit environment/state/mechanism distinctions,
declared observations and linked comparisons. Do not migrate the production
substrate to DisCoPy, Julia or open-game-engine based on this pilot.

After separately reconciling the implementation base, prioritize **a candidate
proposal procedure and one discriminating intervention**, including an ordinary
dynamical explanation and a passive control. Revisit categorical tooling only
when that work produces a concrete composition problem (for example reciprocal
environment ports, coupled subsystems or justified coarse-graining) and a testable
advantage beyond the validated Python baseline.

Project-local lesson: make the baseline fair and the first visual interaction
real before growing machinery. One evidence note and updates to current owners
were sufficient; no company-policy rollout or new documentation engine occurred.
