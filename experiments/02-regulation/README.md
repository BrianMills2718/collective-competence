# Experiment 02 — passive relaxation vs negative-feedback regulation

This is a qualitatively different control specimen placed on the shared lattice
after the simple sorting example. It is first a **calibration/port**, not a new
claim about regulation itself: the repository's earlier scalar thermostat
already established this contrast in NetLogo. Porting it also forced the shared
lattice to state honestly when site payloads are mobile entity identities versus
rewritable local state; no new dynamical capability was added.

## System

One integer-valued temperature occupies a one-site, non-conserving centred
lattice in **local-state mode**: the site payload is temperature, not an entity
identity, and the lattice carries no entity records. The one-site form is
deliberate: this experiment distinguishes passive convergence from feedback
regulation; it does not claim collective competence.

Both arms experience passive relaxation toward ambient temperature 100. The
feedback arm additionally senses error from an authored setpoint of 100 and
applies proportional corrective control. The passive arm has no controller.

The goal criterion used for measurement is external: temperature within 3 units
of 100. For this calibration the controller's authored setpoint is known; a later
Goal Discovery analysis should withhold it from the analyst.

## Interventions

Two intervention families expose the mechanism:

- **State displacement:** add -40, -20, +20, or +40 to a settled state and measure
  first return to the tolerance band.
- **Persistent load:** add -4, -2, +2, or +4 every step and measure mean absolute
  setpoint error over the final 20 steps of a 100-step run.

Two feedback ablations are controls: block sensing by pinning the sensed value to
the setpoint, or disable actuation. Either should remove the feedback advantage.
All arms start from the same substrate snapshot.

## Result

| displacement | passive recovery | feedback recovery |
|---:|---:|---:|
| -40 | 11 | **2** |
| -20 | 8 | **2** |
| +20 | 8 | **2** |
| +40 | 11 | **2** |

Feedback therefore restores the criterion faster for every tested displacement.

| persistent load | passive late error | feedback late error |
|---:|---:|---:|
| -4 | 16.0 | **6.0** |
| -2 | 8.0 | **3.5** |
| +2 | 8.0 | **3.5** |
| +4 | 16.0 | **6.0** |

For every load, **sensor blocked = passive** and **actuator disabled = passive**
exactly. The advantage therefore depends on the feedback path rather than merely
on a different transition rate hidden elsewhere in the specimen.

This reproduces the qualitative result of the earlier thermostat calibration on
the shared lattice: ordinary convergence to a desirable state and active
regulation can look similar until displacement/load challenges reveal the
feedback mechanism.

This **white-box characterization alone** does not establish goal discovery,
adaptation, agency, or collective competence. The setpoint and controller were
authored; the separate blind check below asks what survives when those semantics
are withheld.

## Blind Goal Discovery check

The calibration was then packaged for the **existing P15 proposal grammar** as an
opaque `branched_scalar_series` case. The proposal process received one anonymous
continuous field, four known intervention inputs (`-4, -2, +2, +4`), a baseline
branch and an anonymous `disable_channel_000` branch. It did **not** receive the
authored setpoint, semantic field name, passive/feedback labels, or implementation.
No new analyzer was written for this experiment.

The unchanged P15 proposer returned `candidate: branched_affine_drift`, passed its
fixed qualification gate on all four independent units, and improved predictive
loss by **90.7%** over persistence. More importantly, it inferred a candidate
reference independently in every unit: **99.16, 98.81, 99.45, 98.55** (mean
**98.99**) against the withheld authored setpoint of 100. It retained
`goal_or_competence_promoted: false`: this is evidence for a reference-like
dynamical structure, not certification of one unique true goal.

A separate zero-context Codex session was then given only the opaque package,
outside the repository. It independently described the intact branch as
**regulation-like**, identified a descriptive symmetry/reference near **100**,
and explicitly refused to infer a unique objective, sensor/comparator/actuator
mechanism, or internal goal representation. It retained passive damping,
input-dependent targets/feedforward, hidden dynamics/quantization, and limited
initial-condition coverage as rival explanations or limits.

So this is a bounded positive result for Goal Discovery: **the existing analytic
machinery and a fresh reader can recover a useful reference/regulation
interpretation from behavior and intervention without the authored semantic
answer**. It does not establish uniqueness, agency, adaptation, or a general
solution to goal discovery.

Evidence:
- [`results/blind_p15_summary.json`](results/blind_p15_summary.json)
- [`results/blind_case.json.gz`](results/blind_case.json.gz)
- [`results/blind_reader.md`](results/blind_reader.md)

Reproduce the deterministic P15 portion with:

```bash
python3 experiments/02-regulation/blind.py
```

## Reproduce

```bash
python3 experiments/02-regulation/run.py
```

The committed result is [`results/characterization.json`](results/characterization.json).
Implementation: [`goal-discovery/src/lattice/specimens/regulation.py`](../../goal-discovery/src/lattice/specimens/regulation.py).
