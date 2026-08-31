---
doc-role: experiment-protocol
authority: experiment
lifecycle: active
---
# P14 protocol: can a learned relation survive rival explanations?

[Wiki](../../../roadmap/README.md) · [Current plan](../plans/current_research_plan.md) ·
[Prior flocking result](p3_002_flocking_representation_discrimination_results.md)

## Question and claim boundary

Can a rule-blind model of the relation between two persistent cell cohorts in
the unmodified NetLogo Flocking system predict untouched trajectories and
survive interventions that give passive dynamics, invariance, measurement
artifact, and competency different explanations?

This is a calibration of the laboratory's proposal/falsification seam. The
model is known to contain local flocking rules. Cohort membership, heading
vectors, candidate families, perturbations, thresholds, and the word
"relation" are supplied. A positive result cannot establish an unexpected
goal, agency, or a general discovery method.

## Reuse decision

Use the installed NetLogo 7.0.4 Sample Models/Biology/Flocking model without
modification and extend the existing BehaviorSpace adapter. Sorting would
repeat P10's known endpoint rule; the network and slime routes are closed under
their tested designs. Flocking is the cheapest existing system with live
part-part interaction, persistent identities, deterministic matched branches,
and an already verified generator path.

## Boundary and allowed observations

- Substrate: 100 moving NetLogo turtles in the standard toroidal Flocking world.
- Focal system: the complete flock; the environment is the toroidal spatial
  field and standard model parameters.
- Persistent cohorts: `A = who mod 4 = 0`; `B = all remaining turtles`. This
  arbitrary partition is supplied before data and carries no biological claim.
- Allowed observations at each tick: cohort mean heading vectors, whole-flock
  mean heading vector, current-neighbor heading disagreement, neighbor count,
  population, and vision. No rule names, target headings, source procedures, or
  post-intervention outcomes enter proposal.

## Frozen proposal grammar

Discovery uses 12 baseline seeds (`31001..31012`), ticks 50..149. Runs 1..6
fit candidates; runs 7..12 are untouched proposal holdout. Each candidate
predicts the next four-vector `(A_dx, A_dy, B_dx, B_dy)`:

1. `invariant`: the next vector equals the current vector.
2. `independent_affine`: each cohort's next vector uses only its own current
   vector plus an intercept.
3. `relational_affine`: each cohort's next vector may use both cohorts' current
   vectors plus an intercept.

Least squares is fixed; no regularization, family retuning, seed removal, or
post-outcome repair is allowed. Error is per-run root mean squared vector error.
The relational candidate is proposal-adequate only if it beats both rivals on
at least five of six holdout runs and its median improvement over the better
rival is at least 5%. Otherwise stop before intervention execution and record
`proposal_failed`; do not alter the grammar.

## Frozen rival explanations and predictions

| Explanation | Prediction that can win |
|---|---|
| Passive interacting dynamics | The frozen relational affine law predicts the fixed-cohort response after damage within its held-out baseline error envelope; recovery needs no competency interpretation. |
| Invariant | Whole-flock rotation preserves both relational readouts immediately while absolute heading changes; no return to the former absolute heading is required. |
| Measurement artifact | Current-neighbor disagreement appears to recover but the fixed identity-cohort heading gap does not, or the proposal fails untouched holdout. |
| Competency candidate | The relation transfers, both readouts recover after cohort damage only with interaction, and the frozen passive forecast is inadequate. This keeps competency live; it does not confirm it. |

The explanations are not exhaustive metaphysical categories. They are the
four operational rivals this experiment can distinguish.

## Frozen evaluation

Only after an adequate candidate is serialized and committed, run 10 new seeds
(`32001..32010`) to tick 350. Four arms are identical through tick 150:

- `sham`: no intervention;
- `cohort_rotate`: rotate cohort A by 180 degrees;
- `cohort_rotate_vision_off`: same rotation, then set vision to zero;
- `whole_rotate`: rotate every turtle by 90 degrees.

Readouts use an immediate window 151..160 and late window 320..350. Cohort gap
is the angular distance between the mean A and B vectors. Dynamic disagreement
uses the model's current-neighbor reporter. Absolute heading is the whole-flock
mean-vector direction.

## Integrity, decisions, and stopping

All gates count seeds; correlated ticks or turtles are not independent units.

- every arm contains ticks 0..350 for all 10 seeds;
- all arms are numerically identical through tick 150 within seed;
- population remains 100 and all required vectors/readouts are finite;
- cohort rotation increases both immediate cohort gap and dynamic disagreement
  over sham by at least 20 degrees in at least 8/10 seeds;
- whole rotation changes absolute heading by at least 75 degrees while changing
  immediate cohort gap by at most 5 degrees in at least 8/10 seeds.

If integrity fails, the experiment is invalid, not negative. With integrity:

- `artifact_supported` if late dynamic disagreement is within 5 degrees of
  sham in at least 8/10 active seeds but late cohort gap is not;
- `interaction_required` if active late cohort gap is at least 20 degrees lower
  than vision-off in at least 8/10 seeds;
- `relation_restored` if both active late gaps are within 5 degrees of sham in
  at least 8/10 seeds;
- `absolute_heading_not_defended` if the whole-rotation late heading remains at
  least 60 degrees from the prebranch heading in at least 8/10 seeds;
- `passive_forecast_adequate` if the frozen model's recursive four-vector RMSE
  through ticks 151..200 is no more than twice its median holdout one-step
  four-vector RMSE in at least 8/10 active seeds. This extrapolation may be too
  strict; its failure alone is never competency evidence.

`competency_survives` requires proposal adequacy, all integrity gates,
`interaction_required`, `relation_restored`, `absolute_heading_not_defended`,
failure of passive forecast adequacy, and no artifact support. Report this only
as a surviving candidate because the simple passive family is not an exhaustive
passive-mechanism class.

Stop after the committed result and one smallest visual readout. Do not tune
Flocking, add seeds, repair the candidate, or build generic UI/framework code.
