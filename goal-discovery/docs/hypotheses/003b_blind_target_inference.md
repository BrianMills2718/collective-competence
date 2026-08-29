# Experiment 003B — blind defended-target inference

**Pre-registered before the 003B runs are generated.** Experiment 003 results
have already been seen, so none of its disturbance magnitudes are reused as
003B confirmation cases. Rules below are frozen before the new NetLogo batch.

## Purpose

Experiment 003 showed that known-target measurements distinguish negative
feedback from passive relaxation. 003B asks the first actual goal-discovery
question in this programme:

> With the setpoint hidden, can trajectory-only analysis infer the state the
> system returns toward, then distinguish active defence of that candidate from
> a matched passive attractor on new interventions?

This is still a calibration. It tests one scalar supplied candidate family, not
open-ended goal discovery, agency, compensation, or adaptation.

## Blind observation boundary

The inference code receives only:

- run identifier and tick;
- system label (`feedback`, `passive`, or a mechanism-null label);
- intervention family and signed magnitude;
- true temperature.

It must not receive setpoint, ambient temperature, sensed temperature, error,
controller command, applied control, passive term, gain, or control limit.
Raw BehaviorSpace output necessarily contains simulator parameters, so a
whitelist projection creates the blind analysis table before inference. The
target is unlocked only after all estimates and held-out decisions are fixed.

## Candidate family and discovery

Candidate targets are the fixed grid `10.00, 10.25, ..., 30.00`. For each of the
intact feedback and passive systems separately, score a candidate by mean
absolute distance from it over ticks 140–159 across six one-time-displacement
discovery runs. Choose the lowest-loss candidate; an exact tie is resolved by
the lower numeric candidate.

New discovery displacements are `-10, -6, -3, +2, +5, +9`, applied at tick 20.
They were not used in Experiment 003. The frozen plant, controller, and horizon
remain `20/20/20`, `alpha=.05`, gain `.25`, limit `2`, and tick 160.

Candidate stability is measured by repeating inference while leaving out each
feedback discovery run in turn.

## Held-out defence test

The target estimate is frozen before opening four new persistent-load cases:
`-0.37, -0.13, +0.19, +0.31`. Each is run in four arms:

- matched passive relaxation;
- intact feedback;
- feedback with its sensor pinned to the hidden setpoint;
- feedback with its actuator disabled.

For a run, late target error is mean `abs(temperature - inferred_target)` over
ticks 140–159. Intact feedback is paired with passive by load magnitude.
Mechanism-null arms are evaluated relative to the intact feedback estimate.

## Frozen decisions

- **B1 — recovery candidate:** after target unlock, the intact-feedback estimate
  must be within `0.25` of the true target.
- **B2 — stable inference:** leave-one-displacement-out feedback estimates must
  span no more than `0.25`.
- **B3 — defended rather than merely attractive:** on every held-out load,
  intact feedback late error must be no more than `25%` of matched passive late
  error, using their separately frozen discovery estimates.
- **B4 — sensing is necessary:** sensor-blocked late error must be at least
  `90%` of passive error and must fail the `25%` defence threshold for every
  load.
- **B5 — actuation is necessary:** actuator-disabled late error must be at least
  `90%` of passive error and must fail the `25%` threshold for every load.
- **B6 — no target leakage:** the persisted blind table contains exactly the
  declared fields and none of the hidden simulator/controller fields.

003B passes only if B1–B6 all pass. Passive may infer the same attractor; that is
not a failure. The distinguishing evidence is whether the inferred candidate is
preserved under held-out sustained loads and whether that advantage depends on
sensing and actuation.

## Batch size and reproducibility

The batch contains 28 deterministic runs: 12 discovery runs (six displacements
times two intact systems) and 16 held-out runs (four loads times four arms).
Python independently reads the exported tables, creates the blind projection,
infers candidates, and writes the decision report. Same model, setup file, and
NetLogo version must reproduce identical scientific columns.

## Interpretation limits

Passing would show that a hidden scalar target can be recovered from return
trajectories and identified as actively defended relative to a matched passive
null. The candidate grid, intervention labels, system boundary, scalar state,
and disturbance family are all supplied. The result therefore does not yet
support unrestricted target discovery or attribution of agency.
