# Experiment 003 — negative feedback versus passive relaxation

**Pre-registered before the experiment is run.** This document contains no
results. Thresholds, interventions, and held-out cases below must not be changed
after inspecting their outcomes.

## What 003 is for

Experiments 001 and 002 established that convergence and recovery do not by
themselves distinguish active regulation from passive dynamics. Experiment 003
tests the next, deliberately narrow distinction:

> Does a bounded negative-feedback mechanism oppose measured error and preserve
> a target under disturbance better than matched passive relaxation?

This is a calibration of the regulation instrument. It is not a claim of
agency, intelligence, adaptation, compensation, or autonomous goal discovery.
The target is supplied to the model and the analysis.

## System

One scalar temperature is updated in discrete time. Both arms have the same
temperature, setpoint, ambient temperature, relaxation, disturbances, horizon,
and initial conditions:

```text
ambient_effect_t = alpha * (ambient - temperature_t)
temperature_(t+1) = temperature_t + ambient_effect_t + load_t + applied_control_t
```

The passive arm has no controller:

```text
applied_control_t = 0
```

The feedback arm senses temperature, calculates signed error, and applies
bounded proportional negative feedback:

```text
sensed_error_t = sensed_temperature_t - setpoint
commanded_control_t = clip(-gain * sensed_error_t, -control_limit, control_limit)
applied_control_t = commanded_control_t
```

The initial calibration parameters are frozen as:

| parameter | value |
|---|---:|
| setpoint | 20.0 |
| ambient | 20.0 |
| initial temperature | 20.0 |
| `alpha` | 0.05 |
| proportional gain | 0.25 |
| control limit | 2.0 |
| intervention tick | 20 |
| final tick | 160 |
| recovery tolerance | 0.25 |
| recovery dwell | 10 ticks |
| late-error window | ticks 140–159 |

These values make the passive arm a genuine matched recovery control: after a
one-time displacement it returns toward the setpoint because ambient equals the
setpoint. Under a persistent load it settles away from the setpoint. The active
arm differs only by its feedback path.

The model is deterministic. A seed is still recorded in the common trajectory
metadata for interface consistency, but varying it must not change an outcome.

## Interventions

Each intervention starts at tick 20. Paired arms receive the same intervention.

1. **State displacement.** Add a signed offset to true temperature once.
2. **Persistent load.** Add a signed thermal load on every subsequent tick.
3. **Sensor block.** In the feedback arm, force the reported temperature to the
   setpoint from the intervention tick onward. The controller therefore sees
   zero error even when true temperature differs.
4. **Actuator disable.** Continue to calculate and record the command, but force
   applied control to zero from the intervention tick onward.

Sensor block and actuator disable are mechanism interventions. They will be
combined separately with the same state displacements and persistent loads used
for the intact feedback arm. They must not alter passive-arm dynamics.

## Nulls and contrasts

- **Matched passive relaxation** is the primary null. It shows how quickly the
  shared physical dynamics recover without conditional control.
- **Sensor-blocked feedback** preserves the controller and actuator code but
  removes informative error input.
- **Actuator-disabled feedback** preserves sensing and the controller command
  but removes its causal influence on temperature.
- **Zero disturbance** checks that neither arm manufactures an apparent
  recovery episode and that the intact controller applies no control at the
  setpoint.

The passive arm, not an all-frozen or random system, is the load-bearing null:
it is matched on the ordinary tendency that could otherwise explain recovery.

## Observation boundary

The exported observation at every tick contains:

- true temperature;
- sensed temperature;
- setpoint and ambient temperature;
- ambient effect and persistent load;
- commanded and applied control;
- arm and intervention labels;
- sensor and actuator availability;
- tick and run metadata.

The analysis may derive errors, recovery, and control-direction agreement only
from this declared record. It must not import simulator objects or call model
transition functions.

The gain, control limit, update order, and failure rules are authoritative
white-box mechanism metadata. They may be used to verify implementation but
not silently substituted for observed trajectories. Because the setpoint is
declared, this experiment tests regulation around a known target; it does not
test whether a target can be inferred blind.

## Metrics

- **Absolute true error:** `abs(temperature - setpoint)`.
- **Recovery time:** ticks after a one-time displacement until absolute true
  error first enters the recovery tolerance and remains there for the full
  10-tick dwell. A run not satisfying this by tick 160 is unrecovered.
- **Late absolute error:** mean absolute true error over ticks 140–159.
- **Late-error ratio:** intact-feedback late absolute error divided by its
  paired passive value under the same persistent load.
- **Control-direction agreement:** among ticks where applied control is nonzero,
  the fraction satisfying
  `sign(applied_control) = -sign(sensed_error)`.
- **Control effort:** sum of absolute applied control after intervention,
  reported descriptively and not used for the primary pass decision.
- **Overshoot:** the maximum signed crossing beyond the setpoint after a state
  displacement, also reported descriptively.

Ratios with a zero passive denominator are undefined and cannot count as a
pass. The persistent-load suite uses nonzero loads, for which the passive
denominator is expected to be nonzero.

## Pre-registered predictions and decisions

### R1 — faster recovery after displacement

For every held-out nonzero displacement, intact feedback must recover in fewer
ticks than matched passive relaxation. Both arms must recover by the horizon;
otherwise the calibration or horizon is inadequate and R1 does not pass.

### R2 — persistent-load rejection

For every held-out nonzero persistent load, intact feedback's late absolute
error must be no more than **25%** of the paired passive late absolute error.

### R3 — sensing is necessary for the advantage

Under every held-out disturbance, sensor blocking must remove the intact
feedback advantage. Its trajectory should match passive relaxation under the
declared sensor-block rule; operationally:

- under displacement, it must not recover faster than passive; and
- under persistent load, its late absolute error must be at least 90% of the
  paired passive error and must fail the R2 25% threshold.

### R4 — actuation is necessary for the advantage

Under every held-out disturbance, actuator disablement must remove the intact
feedback advantage. Its true-temperature trajectory must equal the paired
passive trajectory within numerical tolerance, even though commanded control
may remain nonzero. It must therefore satisfy the same operational decisions
as R3.

### R5 — control opposes sensed error

Across all intact-feedback held-out runs, applied control must oppose sensed
error on at least **95%** of ticks with nonzero applied control. The expected
value for this deterministic proportional controller is 100%; the 95% threshold
allows only recording or floating-point boundary effects, not systematic
same-direction action.

The regulation calibration passes only if R1–R5 all pass. Passing supports the
narrow statement that the instrument distinguishes active bounded negative
feedback from matched passive relaxation in this scalar system. It does not
support stronger claims.

## Held-out BehaviorSpace plan

Use one visible pilot solely to verify that controls, plots, intervention
markers, and trajectory export work: displacement `+6.0` and persistent load
`+0.3`, each run once in the intact and passive arms. Do not use pilot outcomes
to change the frozen dynamics, thresholds, metrics, or held-out cases above.

After the instrument is frozen, BehaviorSpace runs the following held-out
disturbances:

- state displacements: `-8.0`, `-4.0`, `+4.0`, `+8.0`;
- persistent loads: `-0.4`, `-0.2`, `+0.2`, `+0.4`;
- arms for each disturbance: passive, intact feedback, sensor-blocked feedback,
  and actuator-disabled feedback;
- zero-disturbance passive and intact-feedback controls.

This is 34 deterministic runs: 8 disturbances × 4 arms, plus 2 zero-disturbance
controls. BehaviorSpace exports every run's parameters and tick-level metrics.
Python reads the export, independently recomputes all decision metrics, and
writes the pass/fail table. No case may be removed as an outlier.

## What failures mean

- **R1 or R2 fails:** the selected controller does not establish the proposed
  advantage over passive relaxation under the frozen conditions. Report that
  result before changing parameters; any retuned controller is a new study.
- **R3 fails:** either blocked sensing still conveys useful error information or
  the arm is not a clean sensing null.
- **R4 fails:** disabled actuation still influences the plant or the update and
  export semantics are wrong.
- **R5 fails:** the implemented controller is not reliably negative feedback as
  defined, regardless of whether it happens to recover.
- **Passive fails to recover after displacement:** the primary null is
  misconfigured, so the R1 comparison is void.
- **Same configuration produces different trajectories:** reproducibility has
  failed and no scientific decision is reported.

Implementation failures are repaired without inspecting additional scientific
cases. Scientific threshold failures are reported, not repaired in place.

## Known limitations

- The target is given explicitly rather than discovered from trajectories.
- The controller is a single fixed proportional rule with no memory, learning,
  planning, or adaptation.
- The plant is linear, scalar, deterministic, and fully observed.
- Ambient equals the setpoint, which deliberately gives the passive null a
  natural recovery route after displacement.
- Sensor block reports the setpoint; other sensor failures such as delay, noise,
  drift, or a held last value are outside this experiment.
- The 25% load-rejection threshold calibrates this instrument and is not a
  universal definition of regulation.
- Success would show conditional error correction and mechanism dependence,
  not compensation, autonomy, intelligence, or agency.

## Reproduction record

The results must record the NetLogo version, model checksum or commit, complete
BehaviorSpace definition, parameters, update order, trajectory export, Python
analysis version, and decision table. A results document is written only after
the held-out batch completes.
