# P5-000 — existing-data representation-discovery benchmark

**Frozen on 2026-08-29 before automated feature extraction or scoring.**

## Epistemic status

This is a retrospective method benchmark over already generated data. Earlier
outcomes and hand-designed analyses are known, so passing can promote a method
and generate a new perturbation hypothesis; it cannot supply fresh confirmation
of a scientific claim. The benchmark asks whether a single off-the-shelf
temporal-feature pipeline adds held-out predictive information across two very
different generators without using hidden mechanism fields or post-boundary
observations.

## Frozen pipeline

Both tasks use `tsfresh` with `EfficientFCParameters` to extract label-free
features from a long table with `run_id`, ordered `time`, `kind`, and `value`.
Model fitting is identical across tasks:

1. replace infinities with missing values and remove all-missing columns;
2. fit median imputation and zero-variance removal on each training fold;
3. fit `SelectKBest(f_classif, k=min(12, available features))` on that fold;
4. standardize selected columns on that fold; and
5. fit logistic regression with `C=1`, `liblinear`, `max_iter=2000`, and
   `random_state=0`.

All preprocessing that can use the outcome is inside grouped cross-validation.
The primary score is pooled held-out log loss; balanced accuracy is descriptive.
Probabilities are clipped to `[1e-6, 1 - 1e-6]` before scoring. No model or
threshold is tuned after looking at a task score.

## Task S — decentralized sorting recovery

Source tables are `results/p2-002-crossed/discovery_runs.csv` and
`discovery_trajectories.csv`.

- Include only the 72 branches with `branch_tick = 4`.
- The outcome is `reached_goal`.
- Hold out one of seeds 101–106 at a time.
- The observation boundary is the pre-branch trajectory through tick 4,
  inclusive. Only `boundary_norm` and `inversions_norm` are observable series.
- Allowed intervention metadata are activation schedule, freeze mode, and
  frozen-cell count. Seed, final state, reachability labels, microscopic values,
  frozen identities, and every post-branch row are forbidden.
- Null S0 uses only the allowed intervention metadata.
- Null S1 adds the final observed value of each whitelisted series at tick 4.
- Model S2 uses allowed intervention metadata plus extracted temporal features.

The inclusive tick-4 boundary is valid because the trajectory row is recorded
immediately before the frozen-cell intervention is applied. Tests must enforce
that event order rather than infer it from the phase label alone.

## Task T — thermostat mechanism-portability check

Source tables are the four load-arm BehaviorSpace exports under
`results/003-thermostat`: `load_feedback`, `load_passive`,
`load_sensor-blocked`, and `load_actuator-disabled`.

- Each signed load magnitude is one run, for 16 runs total.
- Define preserved regulation as late mean absolute temperature error over
  ticks 140–160 no more than 25% of the matched passive arm's error at the same
  signed load magnitude.
- Hold out one absolute load magnitude, 0.2 or 0.4, at a time.
- The observation boundary is ticks 20–35 inclusive, after load onset. Only
  `temperature` is observable as a temporal series.
- Allowed metadata are signed load magnitude only. Arm name, sensed temperature,
  controller variables, block/disable flags, and late observations are forbidden
  from predictors.
- Null T0 uses signed load magnitude only.
- Null T1 adds temperature at tick 20.
- Model T2 uses signed load magnitude plus extracted temporal features.

This small deterministic task checks adapter and mechanism portability; it is
not treated as an independent population estimate. Failure stops promotion.

## Frozen attacks

For each task, repeat S2/T2 for 99 fixed label permutations (`9000` through
`9098`) while preserving features, folds, and class count. The real-label log
loss must be below the fifth percentile of shuffled scores.

Define the top extracted feature as the one selected in the largest number of
training folds, breaking ties lexicographically. Re-run grouped validation with
that feature removed. The ablated model may degrade by no more than 20% in log
loss and must retain the task's required advantage over both nulls. Intervention
metadata are not eligible to be called the top extracted feature.

## Promotion gate

Promote the pipeline only if all of the following hold:

- both adapters pass their observation-boundary and group-integrity tests;
- S2 pooled held-out log loss is at most 90% of both S0 and S1 log loss;
- T2 pooled held-out log loss is lower than both T0 and T1 log loss;
- the real score clears the frozen shuffle test on both tasks;
- the frozen top-feature ablation remains within the stated robustness bound on
  both tasks; and
- the same extraction and estimator code runs unchanged for both tasks.

If the sorting task does not yield a valid first held-out comparison within the
sprint, stop. A no-go preserves the hand-designed representations and records
which observation or sample boundary failed; it does not authorize a larger
learned model, more generators, or dashboard work.

## Decision unlocked

A pass licenses exactly one new, separately frozen perturbation experiment
using the discovered feature family. A fail redirects the next sprint toward
the missing observation identified by the benchmark. Neither result licenses a
general claim that the features are causal, goal-specific, or scale-optimal.
