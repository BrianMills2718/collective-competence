---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# P13 — blind vector dynamics calibrates proposal and falsification

[Wiki](../../../roadmap/README.md) · [Frozen protocol](p13_vector_dynamics.md) ·
[Candidate and observations](../../results/p13-vector-dynamics/) ·
[Current plan](../plans/current_research_plan.md)

## Decision

Retain the observation-only **candidate -> frozen forecast -> prospective
challenge** seam. It transferred from the scalar thermostat calibration to the
existing eight-coordinate bowl without exposing the bowl's target, equations,
energy, tolerance, intervention label, or frozen mechanism state.

Do not promote the learned origin to an unexpected goal or the passive return to
a competency. Position, velocity, coordinate identity, the linear family grammar,
and the intervention menu were supplied. The selected law describes passive
dynamics; persistent mechanism loss defeats whole-system restoration.

## Actual evidence

Eight discovery runs (seeds6100–6107, ticks0–40) were the independent
selection units. Leave-one-run-out one-step RMS selected the first adequate
family under the frozen simplicity rule:

| Supplied family | Mean held-out RMS | Worst-run RMS | Adequate on every run? |
|---|---:|---:|---|
| Persistence |0.658284|0.779580|no|
| Position-only affine, velocity persists |0.612114|0.724445|no|
| Shared local affine2x2 |1.31e-15|2.27e-15|yes|
| Full affine16x16 |0.799916|1.04066|no|

The expressive full-vector family did not generalize across initial-condition
runs; the compact shared law did. Refit on all discovery data, it learned

`x(next) = 0.862 x + 0.920 v + 5.55e-17`

`v(next) = -0.138 x + 0.920 v - 2.78e-17`

with training RMS1.50e-15, spectral radius0.959166, and fixed point within
1.53e-16 of(0,0). The candidate and raw discovery observations were committed
before any evaluation future was produced.

Eight untouched evaluation seeds6200–6207 each produced four matched branches
from its exact tick40 snapshot. All32 forecasts through tick400 were frozen and
committed before outcomes. Every integrity check and preregistered condition
check passed:

| Challenge | Passing independent runs | Whole-forecast RMS range | Meaning |
|---|---:|---:|---|
| None |8/8|1.32e-15–1.88e-15|held-out control follows learned passive law|
| Displace two positions±6 |8/8|3.77e-15–5.31e-15|state damage remains predicted and settles|
| Kick two velocities±2 |8/8|3.86e-15–4.37e-15|second state damage remains predicted and settles|
| Freeze one away coordinate |8/8|0.213–0.426|whole-system prediction fails as preregistered|

Under freeze, unaffected-coordinate RMS remained1.09e-15–1.82e-15 and every
unaffected coordinate settled near the learned fixed point. The frozen
coordinate remained away. Thus the failure is localized persistent mechanism
loss, not general model collapse. Evaluator-only comparison after forecast
freeze found coefficient max error8.88e-16 and fixed-point max error1.53e-16.

## Alternatives and claim boundary

- **Passive attraction:** supported as the sufficient account of state return.
- **Invariant or constraint:** the origin is a stable fixed relation under the
  inferred law, but its importance was not independently proposed; the supplied
  state grammar made it readily expressible.
- **Artifact/overfit:** simple baselines and the full-vector model failed held-run
  prediction; the local law passed untouched state challenges. This narrows the
  artifact explanation but does not make the interpretation open-ended.
- **Competency or defended goal:** not supported. State recovery follows passive
  dynamics, and removing one coordinate's ability to update strands it rather
  than eliciting compensation by the rest of the system.

This experiment reduces prescribed interpretation relative to P12 because the
reference or target value was not supplied to the learner. It does not remove
the larger prescription: an analyst supplied x/v observations, stable coordinate
identity, a linear proposal grammar, and challenge types. The bowl coordinates
also do not interact. No universal substrate, general vector-discovery method,
agency test, unexpected goal, or cross-system reliability follows.

## What changed and what stops here

P13 earns one reusable seam across P10/P12/P13: strict observation records,
independent-run proposal selection, immutable candidate/forecast lineage,
matched interventions, abstention/integrity behavior, and cutoff-safe replay.
That is method calibration, not a generic simulator abstraction.

Stop extending this bowl line. More seeds, nonlinear families, UI polish, or a
post-hoc model for freezing would optimize a known passive result. Production
categorical execution, generic dashboards, completion enforcement, and browser
button debugging are not scientific prerequisites. Reopen only for a concrete
defect in the retained instrument.

The next high-value decision is whether a similarly explicit but less local
proposal grammar can generate and distinguish a relational candidate in an
existing **interacting** system. Before execution it must name passive/invariant,
artifact, and competency alternatives and an intervention on which they disagree.
If the candidate merely restates a supplied observable, the grammar remains
bowl-specific, no discriminating intervention exists, or infrastructure expands
before a frozen prediction, stop and redesign rather than scale.

## Provenance and inspection

Protocol first frozen at `11a479c` and operationalized before outcomes at
`8878d72`; learner/runner frozen at `b92c780`; candidate and raw discovery data
at `ac78433`; compact prospective forecasts at `a0450ff`; outcomes at `17259bb`.
Candidate SHA-256 is
`e60172472ab2c789f4c02e2759f137d447647c0e9293d5bf37420bf797a21b4f`;
forecast-bundle SHA-256 is
`c2d2831ecbd625035b104d74e7d2399ff99935098e418722295d765456e0ceac`;
raw evaluation SHA-256 is
`41d80c5d01de420483c0a3015a19395c68cbcf8d559537384db260cf782fe000`.

The first cockpit tab, **Blind vector dynamics · P13**, replays saved evidence.
Purple is the full frozen forecast; blue actual observations stop at the selected
tick. Choose state damage, then freeze, to see accurate return versus localized
mechanism failure. Candidate-family scores, equations, coordinate state, final
results, hashes, and non-claim are connected in the same view.

Run the three stages separately from `goal-discovery`; commit after each of the
first two stages because the runner rejects uncommitted candidate/probe lineage:

```bash
uv run python -m src.experiments.vector_dynamics.run discover
uv run python -m src.experiments.vector_dynamics.run plan
uv run python -m src.experiments.vector_dynamics.run evaluate
```

The current plan owns the next authorization. P13 completes this bounded
checkpoint; it does not authorize an autonomous campaign on further systems.
