# P7-001: cross-system representation tournament

**Evidence level:** 1 — calibration of the selection process  
**Frozen before execution:** 2026-08-29  
**Time cap:** 90 minutes; no model tuning or new trajectories

## Decision being purchased

Can one explicit, task-conditioned rule select a useful representation family,
or abstain, across four contrasting experiments already completed by the
laboratory?

This tournament tests the laboratory's decision process. It does not provide
prospective generalization evidence because the underlying experiment results
are already known. Passing licenses a separately frozen held-out test; it does
not license a scientific claim about universal representation discovery.

## Inputs and integrity checks

The runner reads the existing compact result artifacts and refuses to score if
their expected task, group, or row structure is absent:

| Calibration task | Candidate | Primary null | Required structure |
|---|---|---|---|
| Thermostat preservation | automated temporal features | intervention-only log loss | one task row; 16 runs; 2 held-out load groups |
| Sorting recovery | relational capability | intervention-only log loss | representation table; 72 runs |
| Heatbugs target inference | identity-conditioned history | per-seed modal/null accuracy | eight held-out seeds, numbered 5–12 |
| Slime recovery | checkpoint network features | best of intervention and density MAE | P5-001 prediction summary |

No raw simulation is rerun. These compact outputs are regenerable and remain
ignored by Git; the versioned result document records their values and hashes.

## Frozen selection rules

The rules intentionally use calibration thresholds below later promotion gates:

1. **Temporal:** select if log loss improves on the primary null by at least 20%.
2. **Relational:** select if log loss improves on the primary null by at least 10%.
3. **Identity-conditioned:** select if mean held-out accuracy exceeds the mean
   null by at least 0.10.
4. **Network:** select if MAE improves on the strongest simple null by at least
   10%; otherwise abstain.

For losses, relative improvement is `(null - candidate) / null`. For accuracy,
the decision statistic is the absolute candidate-minus-null improvement. A value
exactly at the threshold selects the candidate.

The expected calibration actions are temporal/select, relational/select,
identity-conditioned/select, and network/abstain. These encode the known
direction of each calibration and are used only to test whether the common
selection process reproduces it.

## Gate and failure actions

- **4/4 correct:** pass; freeze one prospective Level 2 selector test before
  inspecting its held-out outcomes.
- **2–3/4 correct:** partial; repair only the failed rule or observation family
  in one bounded Level 1 sprint.
- **0–1/4 correct:** fail; stop the generic selector line and reconsider
  task-specific priors.

Regardless of outcome, do not tune these four experiments, change thresholds,
or add a fifth calibration after seeing the score.

## Required artifacts

- a row-level score table with source paths and selection decisions;
- a machine-readable summary including input SHA-256 hashes;
- one static select/abstain decision figure;
- a versioned result note stating what investment the outcome licenses.
