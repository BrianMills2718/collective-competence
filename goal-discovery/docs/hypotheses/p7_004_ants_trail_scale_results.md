# P7-004 Ants trail-scale perturbation screen — results

## Decision

**Abstain / no-go. Retire Ants for this V4 question and do not tune or rerun
the screen.** All frozen integrity gates passed, but no organizational scale
beat the nulls and the mesoscopic trail representation was worst by held-seed
MAE.

| Model | Held-seed MAE (food units) |
|---|---:|
| Persistence null | 91.532 |
| Arm + tick-300 food null | **17.569** |
| Individual/local scale | 21.291 |
| Whole-colony aggregate scale | 19.226 |
| Mesoscopic trail scale | 27.032 |

The trail model beat the local and colony models on only 3/8 held-out seeds
each, below the frozen 6/8 gate. Its MAE was 53.9% worse than the primary null,
26.9% worse than the local model, and 40.6% worse than the colony model. Neither
simpler scale met its own null-and-seed-win branch.

## Integrity and intervention boundary

All 16 trajectories contained ticks 0–600, preserved 125 ants, and paired
exactly through tick 300. All eight cut arms retained food at tick 330 and
collected food afterward. Predictions were complete, held out by seed, and
bounded to physically possible collection.

The frozen intervention command set `chemical` to zero only for patches in the
declared annulus, so instantaneous removal was 100% in every cut arm. The first
analysis mistakenly evaluated that gate at tick 301, after the standard model
had already diffused chemical back into the annulus; the minimum matched gap at
that diagnostic point was 24.6%. The integrity evaluation was corrected against
the preregistered intervention boundary without regenerating trajectories or
changing any feature, seed, model, score, or threshold. The raw metadata records
that correction.

## What was learned

For this fixed pheromone cut, the scale summaries added variance without useful
held-seed information beyond knowing the arm and how much food remained at the
checkpoint. A visibly organized trail is therefore not automatically a useful
predictive macrostate. This reinforces the programme rule that higher-level
descriptions must earn value against a strong task-matched null.

The result does **not** show that pheromone trails never matter causally. The
field was rebuilt quickly after the instantaneous cut, and P7-004 tested
prediction of later collection rather than matched intervention choice or
control. Under the frozen no-go branch, Ants is retired for this predictive V4
question; the next planning decision is whether V4 should narrow to a causal
intervention-value comparison instead of another representation tournament.

## Claim and provenance boundary

This is Level 1 evidence on an explicitly authored off-the-shelf foraging task.
It does not establish an inferred goal, collective competence, general scale
selection, causal control value, or V4 completion. The `scale_control` outcome
map remains hypothetical.

Artifacts are in `results/p7-004-ants-trail-scale-001/`.
