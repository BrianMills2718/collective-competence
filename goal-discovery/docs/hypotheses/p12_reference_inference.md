---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
---
# P12 — observed attractor versus inferred feedback reference

[Wiki](../../../wiki/index.md) · [Current plan](../plans/current_research_plan.md)

## Question and decision

Can an observation-only learner distinguish an observed attractor from a
candidate feedback reference when ambient and reference differ and the mechanism
split is not supplied? Can it recognize failure of its supplied affine family?
This reduces assumptions in P11; it is not unexpected-to-analyst discovery,
an adaptive-selection benchmark, or evidence of agency.

Use the existing unmodified NetLogo thermostat and P11 Windows-local adapter.
The focal system is the scalar plant plus controller; load is external context.
No new simulator, feature tournament, or agent framework. A fixed causal probe
is appropriate: selecting a more elaborate policy is not the current bottleneck.

## Observation boundary and supplied assumptions

The learner receives ordered finite `{tick, temperature}` rows only. The
actuator-disabled probe is known to add a constant load u=0.4 at tick24. It
receives that intervention specification, but not arm, target, ambient, gain,
relaxation, control limit, configuration identity, or truth labels. Calibration
configuration is public in this protocol, withheld from learner function inputs;
this is not blindness of the human analyst.

The supplied family is an additive affine plant plus proportional feedback.
Fit intact `deltaT=B-k*T` from ticks0..24. Fit the disabled branch
`deltaT=Bp-alpha*T+u` from transitions24->25 through47->48. Infer g=k-alpha,
observed attractor B/k, passive equilibrium Bp/alpha, and candidate reference
r=(B-Bp)/g. The relation and intervention semantics are supplied; coefficients,
split, equilibria, and reference are inferred. A reference is not necessarily
the state actually maintained, much less a goal demonstrated under challenges.

Use NumPy least squares. Rank must be2, each fit RMS residual <=1e-8,
temperature span >=0.1, and 0<alpha<=k<1 within numerical tolerance1e-8.
If abs(g)<=1e-8, reference is unidentifiable; never divide by near-zero gain.
Other invalid fits return model-inadequate. Predict intact futures with the
learned total drift only, without fitting or supplying a saturation model.

## Fixed fixtures and timing

| Fixture | Arm | Initial | Ambient | Reference | alpha | g | cap |
|---|---|---:|---:|---:|---:|---:|---:|
| a | feedback |22|16|23|.08|.24|2|
| b | feedback |22|26|18|.15|.05|.5|
| c | passive |22|21.25|23|.32|0|2|

Two identification runs per fixture: intact prefix through24 and matched
prefix followed by disable-actuator+load.4 through48. Fit no early stopping.
Require exact shared prefix. These trajectories are observation inputs, not
held-out tests. Predict then commit candidates and all forecasts before outcomes.

Two intact challenges per fixture, each with the identical tick0..24 prefix:
load+.4 (within expected affine regime), load+4 (saturation challenge), persistent
from before step24->25 through tick120 (96 responses). Forecast starting from
the observed tick24 temperature; first forecast is tick25. No fit sees these
challenge responses. Preserve all full actual traces, forecast arrays, hashes,
and invalid runs. No cherry-picked replay: fixture a appears first by default.

## Frozen evaluation

- Forecast adequate iff RMS response error <=.05 over all96 post-probe rows.
  Otherwise reject this affine model for that challenge; do not refit or relabel
  poor prediction as competency. This tolerance is supplied, not a probability.
- Expected: inferred r agrees with withheld configured r within1e-6 for a/b,
  and differs from the observed attractor by >=1; c abstains on reference.
- Expected: all three small-load forecasts adequate; large-load forecasts for
  a/b rejected, c adequate. These six deterministic diagnostics have no sampling
  confidence intervals and do not prove generalization across systems.
- Compare reference, observed attractor, passive equilibrium, and actual final
  temperature directly. No threshold for claiming target attainment is introduced.
- Required integrity: frozen scientific source, frozen candidate bytes,
  byte-identical staging, exact matched prefixes, expected tick count/finite data.
  Invalid runs stay in denominator; failed integrity never produces supported
  inference. Recompute full-horizon decisions from raw CSVs at audit.

Complete the slice with an inspectable candidate -> challenge -> prediction
error -> qualified conclusion. A failed scientific expectation is a result;
software/integrity failure must be fixed or explicitly prevent interpretation.
Show saved-evidence playback with cutoff-limited error and separately labeled
final verdicts. Record known limitations instead of broadening the study.

## Next action contingent on evidence

If reference inference works, it earns a bounded causal-proposal method, not
an unexpected goal claim. If challenge failure is caught, preserve the failure
as the reopening condition for a later revised candidate family. Do not silently
fit a clipped controller after observing held-out outcomes. Prioritize proposing
and falsifying less-prescribed relations on an existing second substrate over
another thermostat parameter batch. The current plan chooses subsequent work.
