---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-005 — the statistic measures differentiation, and C2-001 was missing a control

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_005_idiosyncratic_fraction.md) ·
[Completion condition](../PROJECT.md) · [C2-001](c2_001_derived_phase_results.md) ·
[Result package](../../results/q1-005-idiosyncratic/)

## Decision

**The reinterpretation is wrong, exactly as predicted. Clause 2 fails and the
instrument is not qualified.**

| arm | idiosyncratic fraction | persistence | need satisfaction |
|---|---|---|---|
| `derived_phase` (differentiated + coordinated) | 0.934 | 0.921 | 0.438 |
| `constant_phase` (uniform) | 0.000 | 0.698 | 0.000 |
| `random_attempt` (differentiated, **not** coordinated) | **0.948** | 0.877 | 0.375 |

- **G1 (necessity): passes.** Coordinated 0.934 ≥ 0.30, uniform 0.000 ≤ 0.10.
- **G2 (sufficiency): fails**, margin **−0.014** against a required +0.20. The
  random population scores *higher* than the coordinated one.

The idiosyncratic fraction measures **differentiation**, not coordination. An
instrument using it would report structure in a population acting independently
at random, which is precisely what
[the completion condition's clause 2](../PROJECT.md) forbids.

The frozen prediction was that G1 would pass and G2 would fail, recorded before
implementation specifically so a pass could not be presented as expected. It
held. The convenient post-hoc reading of the two prior results is discarded.

## The more important finding: C2-001 was missing this control

`random_attempt` reaches **0.375** need satisfaction against `derived_phase`'s
**0.438**.

[C2-001](c2_001_derived_phase_results.md) headlined derived phase against
`level_only`, which scores **0.000**, and concluded that environmental
heterogeneity substitutes for designer labelling. It never included a random
control. Against random independent action — matched here on duty cycle, so the
arms differ only in whether acting is structured — the advantage is 0.063
absolute, about 17% relative, not the total effect the level-only comparison
implied.

**This is the same defect as [C1-001](c1_001_shared_scarcity_signal_results.md)'s
frozen control**, which compared an adaptive signal against a badly chosen
constant rather than the best one, and which that record caught only after the
fact. It is now the second time in this session that an effect was measured
against a control weaker than the obvious rival, and both times the correction
came from a later experiment rather than the original design.

What survives of C2-001: deriving a phase from a subunit's own need does beat
random independent attempts, and the distinct-phase mechanism it established is
unaffected. What does not: the size of the effect, and any reading in which
environmental heterogeneity is doing most of the work. Most of the benefit over
`level_only` is available from desynchronization alone, which randomness
supplies for free.

**C2's status must narrow accordingly**, and does.

## What this leaves standing

- `constant_phase` at exactly 0.000 confirms the statistic responds to
  differentiation as designed. The measurement is sound; the interpretation was
  wrong.
- Persistence, the Q1-004 statistic, also fails to separate here: 0.921
  coordinated against 0.877 random. Both statistics tested so far measure
  properties of *differentiated activity* rather than of coordination.
- The rival source is now named. Any future coordination statistic must be shown
  to separate coordinated action from **matched independent randomness**, not
  merely from uniformity. That control should be standing, not per-experiment.

## Effect on the completion condition

Clause 2 fails on both statistics tested. The instrument is **not qualified**,
and the reason is now specific rather than vague: the detector can see that
entities are doing different things, and cannot see whether those differences are
*related*. Detecting relation — not variety — is the open problem.

## Limits

One substrate, one duty cycle, one random policy. A different random policy, or a
harder allocation problem where randomness collapses, might separate the arms;
the duty-cycle matching was fixed in the protocol precisely so that could not be
tuned after the fact.

## Provenance

Protocol frozen with numeric thresholds before implementation — the defect
[Q1-004](q1_004_second_family_qualification_results.md) recorded against itself.
Estimator imported unchanged. The random arm's probability was fixed by matched
duty cycle, not tuned. Thresholds were not restated after any number was seen.
