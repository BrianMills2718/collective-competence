# P7-004 Ants trail-scale perturbation screen — results

**Decision: abstain-no-go.**

## Frozen integrity gates

- complete_trajectories: PASS
- paired_identical_through_300: PASS
- population_preserved: PASS
- paired_tick_300_food: PASS
- intervention_scope_frozen: PASS
- annulus_removal_all_eight: PASS
- cut_food_remaining_at_least_six: PASS
- cut_future_collection_at_least_six: PASS
- predictions_complete_and_bounded: PASS

Instantaneous annulus removal was
1.000 by the frozen
assignment. The minimum matched gap after one subsequent standard step was
0.246. Cut arms with food
remaining at tick 330: 8/8. Cut
arms with later collection: 8/8.

## Held-seed prediction

| Model | MAE (food units) |
|---|---:|
| persistence | 91.532 |
| primary | 17.569 |
| local | 21.291 |
| colony | 19.226 |
| trail | 27.032 |

The trail scale beat the local model on
3/8 held seeds and the colony model on
3/8. Mesoscopic promotion gate:
FAIL.

## Claim boundary

This is a Level 1 task-conditioned screen of explicitly authored foraging after
a fixed field cut. It is not generic representation-selection evidence and does
not establish an inferred goal, competence, causal control value, or V4
completion. The frozen conditional branch controls the next decision.
