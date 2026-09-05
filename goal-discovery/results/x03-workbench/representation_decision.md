# X03 existing-data representation screen

## Decision

PROMOTE `Capability state` into the next generator sprint. Its directional discovery score is 0.37 above boundary-only.

## What was tested

- Input: 30 already-generated X02 trajectories across 3 seeds.
- Snapshot: common tick-zero observation; six block-swap runs are excluded
  because their stored trajectories begin after intervention.
- Test: leave-one-seed-out 3-nearest-neighbor prediction of goal attainment and final boundary.
- Promotion threshold: at least 0.05 discovery-score lift over boundary-only.

## Guardrail

This is a rapid, directional screen on a small reused dataset. Condition and
capability are partly confounded: all freeze runs fail in X02. The result can
choose the next measurement to test, but it cannot establish a scientific
claim. Confirmation requires a new crossed experiment where capability state
and outcome vary independently.
