# P7-004 Ants trail-scale perturbation screen — results

## Decision

**Stop — integrity failure. Retire this P7-004 run and do not tune or rerun it
under the frozen screen.** The original executable integrity check found that
the annulus cut removed only 24.6% of matched chemical at the first recorded
post-cut checkpoint, below the frozen 80% gate. The prediction scores below are
retained as diagnostics, but they cannot support the preregistered scale
decision.

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

## Integrity failure and intervention boundary

All 16 trajectories contained ticks 0–600, preserved 125 ants, and paired
exactly through tick 300. All eight cut arms retained food at tick 330 and
collected food afterward. Predictions were complete, held out by seed, and
bounded to physically possible collection. Those gates passed; the annulus
removal gate did not.

The intervention command structurally sets `chemical` to zero only for patches
in the declared annulus. However, the frozen prose did not define an
instantaneous measurement artifact, and the original executable analysis bound
the 80% gate to tick 301, the first recorded post-cut state. That check produced
a minimum matched removal of 24.6%. Reinterpreting the gate as the literal
assignment after observing this failure would change the decision boundary
post-outcome, so the original executable interpretation remains controlling.
No trajectory, feature, seed, model, score, or threshold was changed.

## What was learned

Conditioned on this integrity-failed run, the scale summaries added variance
without useful held-seed information beyond knowing the arm and how much food
remained at the checkpoint. This diagnostic is consistent with a visibly
organized trail not being automatically useful as a predictive macrostate, but
the frozen screen cannot elevate that observation to its planned Level 1 claim.

The result does **not** establish that pheromone trails lack predictive or
causal value. The field was rebuilt quickly after the instantaneous cut, and P7-004 tested
prediction of later collection rather than matched intervention choice or
control. Under the frozen integrity-failure branch, this run is retired; any
future Ants experiment would require a new preregistration rather than a
reinterpretation or rerun of P7-004.

## Claim and provenance boundary

This is an integrity-failed Level 1 attempt on an explicitly authored
off-the-shelf foraging task. Its score table is diagnostic only. It does not
establish an inferred goal, collective competence, general scale selection,
predictive scale value, causal control value, or V4 completion. The
`scale_control` outcome map remains hypothetical.

Artifacts are in `results/p7-004-ants-trail-scale-001/`.
