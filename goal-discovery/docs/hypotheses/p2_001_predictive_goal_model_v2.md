# Phase 2 / Experiment 001 v2 — aligned predictive goal model

**Pre-registered after reporting the v1 failure and before generating v2 data.**

## Why v2 exists

V1 confounded an internal controller setpoint with the equilibrium of a plant
whose ambient remained 20. V2 changes one declared design fact: setup sets
ambient equal to each hidden setpoint. The configured target is therefore also
the no-load closed-loop and passive equilibrium. All scientific cases are new.

The blind six-field boundary, three model equations, recursive prediction,
least-squares fitting, candidate grid, thresholds P1–P6, and interpretation
limits are unchanged from v1.

## New frozen cases

Training systems use targets `12.5, 17.5, 22.5, 28.5`, return displacements
`-5.5, +6.5`, and loads `-.24, +.13`, in passive and feedback arms (32 runs).

Held-out systems use targets `15.25, 19.75, 24.25`, target-discovery
displacements `-8, +3.5`, and unseen feedback loads `-.31, +.18, +.35`
(15 runs). Total remains 47 deterministic runs.

## Frozen decisions

- **P1:** each held-out target estimate is within `.25` after unlock.
- **P2:** goal recursive MAE is at most `.02` for every held-out trajectory.
- **P3:** goal MAE is at most 25% of passive-attractor MAE for every case.
- **P4:** goal MAE is at most 25% of global-reactive MAE for every case.
- **P5:** unlocked goal `k` is `[.25,.35]` and load `b` is `[.95,1.05]`.
- **P6:** persisted rows contain exactly the six declared blind fields.

V2 passes only if P1–P6 pass without removing any case.
