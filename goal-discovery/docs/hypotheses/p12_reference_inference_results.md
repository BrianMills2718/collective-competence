---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# P12 — a settling point is not a feedback reference

[Wiki](../../../roadmap/README.md) · [Frozen protocol](p12_reference_inference.md) ·
[Frozen candidates](../../results/p12-reference-inference/candidates.json) ·
[Measured challenges](../../results/p12-reference-inference/evaluation.json)

## Decision and strategic meaning

Retain observation-only causal reference inference as a **bounded calibration**.
Do not require adaptive probe selection when a fixed intervention suffices.
The next bottleneck is reducing researcher-supplied candidate families, not
making the selector win a constructed benchmark.

P11 supplied aligned ambient/reference and a 50:50 split. P12 removes both:
two learned affine drift fields, intact and actuator-disabled, identify the
passive equilibrium, relative gains, and the zero of the feedback contribution.
That zero is a candidate reference under the supplied model, not automatically
a goal, an attained state, or an unexpected-to-analyst discovery.

## Actual results

Six identification runs preceded six untouched challenge runs in the unchanged
NetLogo thermostat. All candidate equations and forecasts were committed before
challenge observations. Three deterministic fixtures are the independent units;
individual ticks are not independent trials and there are no confidence intervals.

| Fixture | Observed attractor | Passive equilibrium | Inferred reference | Small-load RMS error | Large-load RMS error |
|---|---:|---:|---:|---:|---:|
| a, feedback |21.25|16|23|2.05e-14|6.23230|
| b, feedback |24|26|18|6.98e-15|4.87844|
| c, passive |21.25|21.25|unidentifiable|4.49e-14|3.88e-13|

The configured references, unlocked for scoring, agreed within1e-6 in a/b.
The near-zero gain in c yielded no reference; its attractor was not relabeled a
goal. Small-load forecasts were adequate for all three. At load+4, controller
saturation made the frozen affine forecast inadequate for a/b; the passive
control remained adequately predicted. The supplied RMS tolerance was0.05.

Actual final temperatures were22.5/26/22.5 under small load and approximately
40.9954/49.3333/33.75 under large load. Thus inferring a reference neither proves
the system reaches it nor defends it against the specified demand. Prediction
failure diagnoses the candidate model's scope, not absence of a feedback mechanism.

Every recorded integrity check passed: matched prefixes, expected counts,
finite observations, source/candidate hashes, and unchanged staged model inputs.
Each challenge retained121 observations, including the25-row matched prefix and
96 post-probe responses. Raw CSV/XML/log/staging receipts are versioned beside
the JSON evidence. No source model, thresholds, or candidate was retuned.

## What was supplied and what remains unknown

- Supplied: scalar observation, additive affine/proportional family, knowledge
  of the actuator-disabled operation and load, timing, excitation, diagnostic
  fixtures, and forecast tolerance. Calibration truth is public to the analyst;
  only learner inputs are restricted to temperatures and known intervention.
- Learned: drift coefficients, mechanism split, passive/observed equilibria,
  identifiable reference, and conditional future predictions.
- Not demonstrated: proposing a previously unspecified kind of relation,
  unexpected competencies, general transfer, universal goal attribution, or
  adaptive experiment-selection advantage.
- Large-load failures were anticipated falsification controls. They do not
  independently discover saturation, justify a post-hoc clipped fit, or invalidate
  the local reference estimate within its stated assumptions.

## Audit and provenance

Protocol frozen at `5532d25`; scientific implementation `fd1eff6`; candidates
and forecasts `c5289bf`; first challenge results `82ae21b`. Use these revisions
for reproduction; never overwrite original evidence. Source/candidate hashes
and Git ancestry record ordering. Windows CSV clocks and WSL/Git clocks are
distinct clock domains, not independent common-clock chronology proof.

The preceding P11 audit recomputed all eight published comparisons and found
no measurement correction. This slice repairs two implementation boundaries:
missing engine CSV now raises a retained failed-probe error, and integrity-failed
nonempty probes no longer show a supported online/final headline. The repaired
adapter is exercised by all12 P12 real runs. P11 artifacts remain unchanged;
its original reproduction belongs at its recorded scientific revision.

Independent review refitted from raw CSVs using a separate covariance/slope
calculation, reproduced all six errors and verified all12 staging receipts.
Focused model/view/audit tests passed, including passive/flat-data abstention,
privileged-field rejection, matched prefixes, future-cutoff isolation, invalid
evidence, playback reset/pause/end, and missing engine output. Browser inspection
exercised Playing, challenge/system changes and resets, the large-load rejected
forecast and passive-control adequate forecast. Final integrated suite/runtime
receipts belong in the change review rather than another audit document.

## Inspect and reproduce

In the existing laboratory, **Settling vs reference · P12** shows learned
quantities, actual identification traces, and a challenge replay. Purple dashed
is the precommitted forecast; blue actual data and online RMS error stop at the
selected cutoff. Orange dotted marks the inferred reference when identifiable.
Final outcomes and all-six comparison are explicitly retrospective. Playback
replays saved observations, not new simulations.

From `goal-discovery`, with the recorded scientific revision checked out and
`P11_NETLOGO_STAGING` set to an existing Windows-local temporary directory:

```bash
python -m src.experiments.reference_inference.run identify --directory results/p12-reproduction
# Commit the new candidates.json before this separate outcome phase.
python -m src.experiments.reference_inference.run evaluate --directory results/p12-reproduction
```

The current plan owns subsequent authorization. The next meaningful advance
is a less-prescribed relation proposed and challenged on another existing
substrate, with passive alternatives retained—not more thermostat examples.
