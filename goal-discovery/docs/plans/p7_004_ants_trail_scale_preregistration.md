---
doc-role: preregistration
authority: evidence
lifecycle: frozen
---
> Historical record. Its next-step language describes the decision at the time,
> not an active assignment. See the [current plan](current_research_plan.md)
> and [evidence index](plan_completion_ledger.md).


# P7-004 — Ants trail-scale perturbation screen

**Status:** frozen Level 1 preregistration. No P7-004 outcomes have been
generated or opened. This is the second science sprint in the OB-001 pilot.

**Subsequent disposition (not a protocol amendment):** executed once; stopped
on the original annulus-removal integrity gate. Scores are diagnostic only.
See the [result and correction history](../hypotheses/p7_004_ants_trail_scale_results.md).
The original pre-execution status and frozen contract above/below are retained.

## Decision and question

After P7-003, generic representation-family selection is closed. P7-004 asks a
task-conditioned V4 question instead:

> After a pheromone-trail cut, does a mesoscopic source-to-nest trail
> representation predict subsequent food collection better than equally small
> individual/local and whole-colony descriptions?

The decision is whether one organizational scale earns a fresh held-out
promotion test. The experiment is not a search for a generally best feature
family, and a winner is evidence only for this foraging task and perturbation.

## Why this is the cheapest justified next task

The bounded reuse check considered three installed options:

| Candidate | Reuse | Decision-changing value | Decision |
|---|---|---|---|
| NetLogo Flocking with stored P3-002 data | unmodified generator and complete local/global trajectories | outcomes are already open and the line's promotion gate is closed; another analysis could not supply fresh V4 evidence | no-go |
| NetLogo Virus on a Network with P7-002 data | complete trajectories and network adapter | confirmation is open and explicitly closed after P7-003; reuse would reopen the failed selector task | no-go |
| NetLogo Ants | installed unmodified model; patch-field export can reuse the Slime BehaviorSpace boundary, scikit-image threshold/skeleton operations, and NetworkX connectivity | fresh foraging task couples individual motion, a mesoscopic trail, and colony collection under a clean field perturbation | **select** |

No new simulator, graph library, visualization, or generic trajectory
framework is licensed. The standard NetLogo interface remains the visualizer.
If the existing adapters cannot be specialized inside the time cap, stop.

## Generator and task boundary

Use the installed, unmodified NetLogo 7.0.4 Models Library `Ants.nlogox` with
its standard rules, food placement, diffusion rate 50, evaporation rate 10,
and 125 ants. Record through tick 600 for eight new paired seeds.

The prediction task is continuous: predict food collected during ticks 331–600
(the reduction in total patch `food`) from allowed observations through tick
330. Food after tick 330 is sealed until the three representation tables and
predictions are fixed.

In the standard model, patch food is decremented when an ant picks it up, so
this is a collection outcome, not a nest-delivery counter. The target measures
recovery of colony foraging work after perturbation. It does not
imply that food collection is an inferred goal; the generator authors that
behavior explicitly.

## Intervention boundary

All arms share the same seed and trajectory through tick 300.

- **sham:** make no field change;
- **trail cut:** at tick 300, set `chemical` to zero on patches in the annulus
  `8 <= distancexy 0 0 < 13`.

The cut is deterministic, consumes no random draw, preserves ants, food,
positions, headings, carrying state, nest scent, and chemical outside the
annulus. It severs the pheromone field near the nest without adding a barrier;
ants may reconstruct the same or an alternative route under standard rules.
The intervention command may set patch `chemical` only. Any need to modify
model procedures is a stop.

## Observation boundary

Allowed through tick 330:

- turtle identity, position, heading, and carrying/not-carrying color state;
- patch position, `chemical`, `food`, `nest?`, and `food-source-number`;
- tick and arm.

Disallowed from feature construction:

- any tick after 330;
- future food collection or recovery labels;
- source code branches beyond the declared standard variables;
- tuned field thresholds, feature searches, embeddings, or learned graph
  representations.

The analysis may use generator-authored nest and food-source locations because
the task is intervention prediction, not blind goal discovery. Report that
choice as a claim boundary.

## Frozen competing scales

Every candidate adds exactly four summaries to the same two-input base null
(`arm`, total food remaining at tick 300). Each summary is computed from ticks
301–330 only. Standardize within each training fold.

### Individual/local scale

1. fraction of ants carrying food at tick 330;
2. mean chemical on the patch occupied by non-carrying ants at tick 330;
3. fraction of ants inside the cut annulus at tick 330;
4. slope of carrying fraction over ticks 301–330.

### Whole-colony aggregate scale

1. total chemical at tick 330;
2. mean patch chemical at tick 330;
3. total food-removal slope over ticks 301–330;
4. fraction of all ants within nest radius 5 at tick 330.

### Mesoscopic trail scale — primary higher-level candidate

For each food source with food remaining, threshold the chemical field at the
fixed model response floor `chemical >= 0.05`, skeletonize it with
scikit-image, and use eight-neighbor NetworkX connectivity. Record:

1. fraction of remaining-food sources connected to the nest component;
2. maximum connected chemical-component area divided by world area;
3. total skeleton length divided by world area;
4. mean shortest connected skeleton path length from nest boundary to a
   remaining-food source, assigning the world diagonal when none connects.

The fixed 0.05 boundary comes from the standard ants' sensing rule. Do not run
alternative thresholds in this sprint.

## Nulls, scoring, and independence

- **Primary null:** ridge regression on arm and food remaining at tick 300.
- **Persistence null:** predict each branch's ticks 331–600 collection by
  extrapolating its ticks 271–300 collection rate, truncated to `[0, food
  remaining]`.
- **Scale models:** one ridge model per four-summary scale, each including the
  two primary-null inputs; fixed `alpha = 1`.

Use leave-one-seed-out folds so paired arms from a seed never cross the
training/test boundary. Primary score is held-seed mean absolute error (MAE) in
food units. Report per-seed paired errors and trail-model coefficient signs;
do not tune the estimator or choose a different loss after outcomes open.

## Integrity and smallest useful evidence

Eight seed-pairs are sufficient for this Level 1 screen only if all gates pass:

1. all 16 trajectories contain ticks 0–600 and paired arms are identical
   through tick 300;
2. each arm preserves 125 ants and the same tick-300 food state within seed;
3. trail cut changes only annulus chemical at intervention;
4. the cut removes at least 80% of annulus chemical in all eight cut arms;
5. at least six cut arms have nonzero food remaining at tick 330;
6. at least six cut arms collect nonzero food after tick 330;
7. every held-seed prediction is produced exactly once and remains within the
   physically possible collection range after truncation.

Failure of gates 5 or 6 means the checkpoint/task has insufficient outcome
variation. Stop; do not move the checkpoint or change parameters around the
observed result.

## Frozen decision gate

The mesoscopic trail scale earns a separately preregistered Level 2 test only
if all integrity gates pass and it:

- reduces held-seed MAE by at least 15% versus both the primary and persistence
  nulls;
- reduces held-seed MAE by at least 10% versus both other scale models; and
- beats each other scale model on at least six of eight held-out seeds.

If another scale meets both null improvements and beats the other models on at
least six seeds, record that task-specific scale as the calibration winner; it
may motivate a fresh test but does not establish higher-level value. Otherwise
the result is abstain/no-go.

## Time cap and stop rule

Cap the full sprint at **90 minutes**, with the first complete paired seed by
minute 25 and the frozen eight-seed decision by minute 75. Use the remaining 15
minutes only for the decision artifact and plan/state update.

Stop immediately on any of these conditions:

- the installed model cannot run unchanged through BehaviorSpace;
- patch/turtle export or trail summaries require new infrastructure rather
  than specialization of existing adapters;
- the field mask is unusable at the fixed sensing threshold in more than two
  cut arms;
- an integrity gate fails;
- the time cap is reached.

No-go does not authorize tuning the intervention, threshold, checkpoint,
features, model parameters, or seeds. Do not add a UI.

## Conditional branches

- **Mesoscopic pass:** freeze a small fresh-seed/parameter Level 2 confirmation
  before generating it; V4 remains planned until that prospective gate passes.
- **Individual/local or aggregate pass:** record that higher-level trail value
  was not shown; decide whether the winning scale supports a different
  task-conditioned claim before any follow-on.
- **Abstain or integrity failure:** retire Ants for this V4 question and review
  whether V4 should narrow to causal comparison rather than predictive scale.
- **Any post-hoc clue:** log it as a possible new sprint only; it cannot alter
  P7-004's decision.

## Outcome-backcasting trace

```text
Mature outcome supported: compare scales for prediction and intervention value
Target version: V4 — perturbation and scale
Question made answerable: does a mesoscopic organization add held-out value
  after a meaningful perturbation?
Placeholder replaced: hypothetical scale/control comparison
Evidence and provenance produced: paired trajectories, fixed scale tables,
  held-seed predictions, null comparison, integrity ledger, decision artifact
Acceptance test: integrity gates plus frozen MAE/seed-win promotion gate
Stop/removal rule: retire Ants for this question on no-go; do not fill the V4
  artifact with a nonpassing result
Possible artifact or plan revision: promote, narrow, or retire the trail-scale
  hypothesis; revise V4 if prediction alone proves uninformative
```

The result may move the `scale_control` outcome-map entry from hypothetical to
measured only after data are generated under this frozen contract. This
preregistration by itself changes no scientific provenance state.
