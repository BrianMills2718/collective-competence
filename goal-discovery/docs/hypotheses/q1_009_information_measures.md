---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
---
# Q1-009 — does a macro description of these specimens carry causal structure?

[Wiki](../../../wiki/index.md) · [Ontology: what this vocabulary makes decidable](../../../wiki/ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not) ·
[Current plan](../plans/current_research_plan.md) · [Q1-008](q1_008_null_coupling_control_results.md)

**Frozen 2026-09-05, after the calibration in `results/q1-009-information/calibration.json`
and before the specimen and measure tested below were looked at.** Thresholds are
derived from that calibration, which is the one thing Q1-006 and Q1-008 both
failed to do.

## Why this experiment and not the Q1-006 re-run

The founding
[laboratory spec §37](../sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md)
asks whether causal emergence correlates with collective competence, and predicts
that causal emergence and agency "increase together—or systematically diverge."
It was experiment 06 of the original ladder and was deferred on 2026-08-29 as
"premature without a generalizing macro signal" — circular, since the measure's
purpose is to test whether a macro description carries signal.

Q1-006's re-run resolves a gate on a statistic that
[Q1-004](q1_004_second_family_qualification_results.md) already records as "partly
measuring the wrong thing." This asks whether there is macro structure to detect
at all, which is prior to choosing a detector for it.

## What is already measured, and therefore not a finding here

The calibration is **exploratory** and is not evidence for anything below. It
established, on the contended-slot arms:

- emergence (EI macro minus EI micro) is **negative in all three arms** and its
  shuffle null is unstable across seed counts, so **emergence is measured and
  reported but not gated**;
- the stable discriminating quantity is **EI micro above its own shuffle null**,
  at +0.21 bits for `derived_phase` at both 1600 and 3200 seeds;
- `constant_phase` reads highest on emergence-above-null because it is
  degenerate — all units share one phase, so micro and macro coincide.

## Frozen declarations

**Specimen origin** constructed. **Analyst access** white-box. **Research
purpose** Goal and Competence Discovery (instrument characterisation).

**Held out until execution:** the `renewable_commons` specimen has not been
measured with either statistic, and **empowerment has not been computed on
anything**. Those are the prospective arms.

**Observation contract.** Act/no-act of the first 5 units. Micro state = their
joint pattern (32 states); macro state = how many of them act (6 states, group
sizes 1,5,10,10,5,1 — unequal by design, since equal groups make emergence
mathematically impossible).

**Sampling.** 1600 seeds per arm, horizon 120, giving ≥6000 transitions per
occupied micro row. **5 independent shuffle-null replicates per arm**, reported
as mean and spread; the calibration used one replicate and that is why its null
was noisy.

**Empowerment.** Channel capacity in bits from `do(unit u acts / does not act at
tick t)` to u's own remaining need 5 ticks later, bucketed into 3 levels,
estimated over 40 units×ticks per seed across 200 seeds, then averaged over
units. Interventional: the action is overwritten and the system run forward under
its ordinary rules.

## Predictions, committed before execution

1. **Commons ordering.** On `renewable_commons`, EI-micro-above-null is largest
   for `live`, and `frozen` and `none` are both lower. *Reasoning:* the adaptive
   signal is the only arm that coordinates, per C1-001.
2. **Empowerment ordering on the slot.** `derived_phase` > `random_attempt` >
   `constant_phase`. *Reasoning:* a private phase window gives a unit a reliable
   uncontested slot; a shared phase makes every attempt collide.
3. **Empowerment is higher on the commons than on the slot**, because a divisible
   stock lets a unit's own draw determine its own outcome, while congestion makes
   others dominate it.
4. **The two measures agree in ordering on the slot arms** — both rank
   `derived_phase` first. *This is the prediction most worth being wrong about:*
   the founding spec expects agreement or systematic divergence, and divergence
   is the more informative outcome.

## Frozen gates

| Gate | Requirement |
|---|---|
| **G1 — structure above null** | `live` on the commons exceeds its shuffle-null EI-micro by **≥ 0.10 bits**, half the +0.21 measured for the coordinated slot arm. |
| **G2 — discrimination** | On the commons, `live` minus `none` in EI-micro-above-null is **≥ 0.05 bits**. |
| **G3 — empowerment is not vacuous** | The empowerment spread across the three slot arms is **≥ 0.05 bits**; below that the measure does not distinguish these arms and no ordering is read from it. |

Emergence has **no gate**, by the calibration above. It is reported.

## Disposition table

| Outcome | Reading |
|---|---|
| G1 and G2 pass | A macro-relevant statistic separates coordinated from uncoordinated on a **second** specimen. The 2026-08-29 deferral was wrong and this line is worth continuing. |
| G1 passes, G2 fails | The statistic sees structure but not coordination. It is measuring the substrate, not the mechanism. Report and stop the line. |
| G1 fails | These specimens carry no macro-relevant causal structure detectable this way. The deferral's conclusion was right for the wrong reason. Record and stop; do not retune the coarse-graining to find some. |
| G3 fails | Report empowerment as inapplicable to this family. Do not read an ordering from a spread smaller than the gate. |
| Predictions 1–4 split | **Report the split; do not round it to either story.** Per C2-002, the disposition band that forbids rounding is what produced the useful result. |

## Stop conditions

Stop and report rather than adjust if: the coarse-graining is changed after any
EI number is seen; the observed-unit count is changed after any EI number is
seen; a gate is restated after a number is seen; the null replicate count is
reduced; or the seed count is lowered below 1600 for the gated arms.

Retuning allowance: **none.** The calibration was the tuning step and it is
committed.
