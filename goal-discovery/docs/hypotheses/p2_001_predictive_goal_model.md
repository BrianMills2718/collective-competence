# Phase 2 / Experiment 001 — predictive goal-model comparison

**Pre-registered after the V1 audit and before new P2-001 data are generated.**

## Question

Does a compact persistent-target model inferred through the blind trajectory
boundary predict unseen feedback trajectories better than a passive-attractor
model and a global memoryless reactive model?

## Blind record

The model comparison receives exactly: opaque system id, run id, tick,
intervention kind, signed magnitude, and temperature. Setpoint, ambient,
sensor, error, commands, gain, and transition terms remain hidden. A trusted
projection uses setpoint only to assign an opaque equality label; numeric values
are discarded before fitting.

## Models

Per-system targets are inferred on the fixed `.25` grid from late return
trajectories. Training fits one-step temperature change by least squares:

```text
goal:      delta = k * (inferred_target - temperature) + b * load
attractor: delta = a * (inferred_target - temperature) + b * load
reactive:  delta = c * temperature + d + b * load
```

The goal model is fitted on feedback systems. The attractor model is fitted on
matched passive systems. The reactive model is fitted on feedback systems but
has only one global intercept and no persistent per-system target. Held-out
predictions are recursive from the observed tick-20 state through tick 160.

## Frozen cases

Training systems have hidden targets `14, 18, 23, 27`, with return displacements
`-6, +5` and sustained loads `-.22, +.14`, in both passive and feedback arms
(32 runs).

Held-out systems have new hidden targets `16.5, 21.5, 25.5`. Each gets target
discovery displacements `-7, +4` (6 runs), then unseen feedback loads `-.29,
+.17, +.33` (9 prediction runs). Total: 47 deterministic runs.

## Frozen decisions

- **P1 target inference:** every held-out inferred target is within `.25` of
  its unlocked target.
- **P2 absolute prediction:** recursive goal-model MAE is at most `.02` on every
  held-out trajectory from ticks 21–160.
- **P3 attractor contrast:** goal MAE is at most 25% of passive-attractor MAE on
  every held-out trajectory.
- **P4 reactive contrast:** goal MAE is at most 25% of global reactive MAE on
  every held-out trajectory.
- **P5 mechanism recovery:** after unlock, fitted goal `k` lies in `[.25,.35]`
  and load coefficient `b` in `[.95,1.05]`.
- **P6 no leakage:** every persisted analysis row contains exactly the six
  declared blind fields.

Passing supports the narrow claim that a persistent per-system target is a
useful predictive representation for this family. It does not establish agency
or unrestricted goal discovery.
