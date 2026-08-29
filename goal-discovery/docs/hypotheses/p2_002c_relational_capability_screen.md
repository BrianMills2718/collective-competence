# P2-002c — relational capability existing-data screen

**Frozen before computing the new representation on stored P2-002b branches.**
This is an exploratory observation-design screen, not new evidence.

## Question

Does an observable relational description of frozen values and barriers explain
the within-intervention outcomes that the current count/local capability state
misses?

## Input

Reuse only the 72 stored P2-002b branch observations. Generate no trajectories.
Parse `values_json` and `freeze_modes_json`; do not access simulator objects,
future states, or outcomes while deriving features.

## Frozen nine-input candidate

Retain the four value-geometry features and replace the five current capability
features with:

1. mean normalized displacement of frozen values from their target positions;
2. maximum normalized displacement of a frozen value;
3. largest contiguous frozen block as a fraction of size;
4. active/frozen interface edges as a fraction of all edges;
5. fraction of all inversions whose required path crosses an immovable cell.

The candidate therefore remains exactly one quarter the 36-input micro
baseline. The five relationships are selected from the known local-swap
mechanics, not from a feature search.

## Screen

Use the unchanged leave-one-seed-out logistic estimator and metrics. Promote
only to a separately frozen new-seed validation if relational capability:

- reduces log loss by at least 20% versus intervention-only and value-only;
- has Brier loss below 0.25;
- and uses no more than nine inputs.

Because the same P2-002b outcomes motivated this repair, a screen pass is only a
Level 1 signal. Failure retires the current observation-repair direction and
redirects the programme to a different system/representation question.
