# Phase 2 research pivot — from controller calibration to distributed discovery

> **Status: decision history.** Sections labelled “current next move” record
> the transition that was current at that point. The authoritative current
> allocation is [the current research plan](current_research_plan.md).

**Decision date:** after P2-001 v2. This supersedes the provisional plan to run
another nonlinear thermostat-family experiment next.

## Decision

End the engineered-controller track. Keep 003–005 and P2-001 as calibration
fixtures, but do not spend the next research cycle making them richer.

The compensation system reroutes because we wrote a rerouter. The adaptation
system improves because we wrote a gain update. P2-001 v2 predicts exactly
because its goal model matches the linear generator. These results validate the
instrument and its null comparisons; they are not discoveries of emergent
collective organization.

The strongest research clues so far came from cases that contradicted our
language or measurements:

1. observable state did not predict post-freeze behavior in sorting;
2. redundancy separated distributed sorting from the passive bowl;
3. selection could reach but not re-reach its target after spending its search
   capability;
4. blind inference found the coupled system's defended equilibrium rather than
   the controller's internal setpoint;
5. two proposed recovery measures failed when the matched-point definition
   changed.

These point toward empirical system boundaries, retained capability, and
macro-level predictive usefulness—not another hand-authored controller.

## P2-002 — distributed macro prediction

### Research question

> Can a compact, capability-aware description of a distributed sorting
> collective predict recovery after unfamiliar damage better than value-only,
> intervention-only, and microscopic baselines, across held-out system sizes
> and activation schedules?

There is no explicit setpoint, backup controller, or learning rule in this
experiment. The existing local sorting rules generate the behavior.

### Outcome

Predict two separately scored quantities after a branch intervention:

- whether the array reaches sorted order within a fixed remaining-step budget;
- remaining time to sorted order, conditional on success.

Do not collapse these into one competence score.

### Frozen candidate representation families

The discovery pass may compare only a small declared set:

1. **value-only macro:** existing disorder, cluster, prefix, sortedness, and
   inversion measures;
2. **intervention-only null:** damage kind, mode, count, timing, and size;
3. **capability-aware macro:** active fraction, immovable-barrier count and
   spacing, movable-frozen fraction, local active-neighbour availability, and
   algotype composition, all derived from declared observations;
4. **history-aware macro:** the above plus pre-branch rates and short-window
   variability;
5. **observable micro baseline:** the full observed cell values, freeze modes,
   and algotype labels using a size-normalized off-the-shelf model.

No simulator internals, hidden scheduler state, or future observations enter a
feature row. If a variable is not in `observe.py` or pre-branch history, it is
not available to black-box prediction.

### Rapid implementation sequence

This sequence follows `progress_allocation_protocol.md`. The default path ends
with a discovery decision after **90 minutes**. Later sprints are conditional,
not prepaid.

**Sprint 0 — reuse decision (complete).** Apply `reuse_survey_protocol.md`.
X03 selected Panel + HoloViews/hvPlot for analysis and retained NetLogo for
generator-side playback. No custom frontend.

**Sprint 1 — trajectory workbench, 45-minute cap (complete; gate passed).** Reuse existing 001 traces;
add no new simulator architecture. First selectable raster by minute 15; linked
branch and macro views by minute 35; smoke check and decision by minute 45.
Build only the eight-item acceptance gate in
`x03_visual_analytics_decision.md`. If the first artifact misses minute 15,
reduce scope or invoke the bounded fallback instead of extending the sprint.

**Sprint 2 — existing-data discovery, 45-minute cap (preflight complete).** Spend at most 15 minutes
on feature tables, 15 on off-the-shelf scikit-learn comparisons, 10 inspecting
linked failures, and 5 on the decision. Evaluate the five declared
representation families with grouped cross-validation. Do not build a model
framework or automatic representation search. Compare calibrated classification
loss for attainment and absolute error for time-to-goal. Report compression
separately from prediction.

The X02 preflight used the 30 trajectories that share a tick-zero observation
(three seeds; block-swap excluded because its export starts post-intervention).
An off-the-shelf scikit-learn leave-one-seed-out screen promoted capability
state over boundary-only: goal balanced accuracy was 1.00 versus 0.50. This is
pipeline and measurement evidence, not goal evidence. Every freeze run in X02
fails, so capability and outcome are confounded; the full five-family P2-002
comparison still requires the new crossed batch.

**Discovery stop — minute 90 (passed for measurement promotion only).** If no macro family beats
intervention-only and value-only nulls in discovery, stop and report that result
without generating confirmation data. The normal no-signal cost is therefore
90 minutes total.

**Sprint 3 — promotion, 20-minute cap (complete).** The crossed prototype is
frozen in `docs/hypotheses/p2_002_distributed_macro_prediction.md`.  It fixes the
feature families, off-the-shelf estimators, thresholds, seeds, schedules,
dimensionless timings, and the conditional size-24 batch.  It deliberately
does not add a model framework or dashboard feature.

**Sprint 3 discovery result — no-go.** The frozen size-12 batch ran 144 branches
and broke the original confound, but capability-aware log loss improved only
18.9% over intervention-only, short of the frozen 20% gate. The threshold was
not repaired and the size-24 batch was not generated. Full results are in
`docs/hypotheses/p2_002_distributed_macro_prediction_results.md`.

**P2-002b design (frozen).** The reflection is recorded in
`docs/audits/2026-08-29_p2_002_reflection.md`; the full new-seed design is in
`docs/hypotheses/p2_002b_within_intervention_prediction.md`. It keeps the
generator, five representations, estimators, metrics, and 20% gate unchanged,
but restricts discovery to the three previously ambiguous damage classes at
tick `n / 3`. All six schedule × damage strata must contain both outcomes.

**P2-002b result — no-go.** All six targeted strata contained both outcomes,
but capability-aware prediction improved only 7.2% over intervention-only and
19.3% over value-only. Both missed the unchanged 20% gate. The current
capability feature set is retired and size 24 remains locked. See
`docs/hypotheses/p2_002b_within_intervention_prediction_results.md`.

**P2-002c result — no-go.** Relational capability improved log loss to 0.538 but
beat intervention-only by only 12.4%, below the frozen 20% gate. The current
predictive representation-repair loop is stopped. See
`docs/hypotheses/p2_002c_relational_capability_screen_results.md`.

**P2-003 result — pass.** The barrier-feasibility rule classified all 7,440
size-5 immovable cases correctly under both schedules, with no time-limit exits.
There were 2,622 matched cases that recovered when the same frozen cells were
moveable, establishing that the signal is barrier-specific. See
`docs/hypotheses/p2_003_barrier_reachability_results.md`.

**P2-004 result — pass.** The passive-order rule classified all 90,720 new
size-6 moveable-damage cases correctly under both schedules, with zero
time-limit exits. The result supplies the complementary reachability boundary:
moveable passive cells can be carried but cannot cross each other. See
`docs/hypotheses/p2_004_moveable_order_reachability_results.md`.

**Current next move:** stop scaling the enumeration and separate opportunity
from performance. In a bounded P2-005 prototype, use an off-the-shelf graph
reachability routine on tiny state spaces to label target-reachable branches
across bubble, insertion, and selection rules, then measure whether the actual
rule realizes available routes robustly across schedules. Promote only if an
opportunity-adjusted difference survives held-out cases. The allocation audit
is in `docs/audits/2026-08-29_reachability_reflection.md`.

**P2-005 result — no-go and sorting-line stop.** All integrity gates passed,
but every reachable bubble and insertion case succeeded robustly and selection's
largest residual gap was only 8 points, below the frozen 20-point gate. No
size-5 confirmation data were generated. Sorting is mechanically complete for
the present agenda. See
`docs/hypotheses/p2_005_opportunity_adjusted_performance_results.md`.

**Phase 3 move:** the bounded reuse survey selects the installed, standard
NetLogo Flocking model for a 45-minute adoption spike. It adds leaderless
movement and dynamic neighborhoods without adding a new simulator or frontend.
Fireflies is the fallback and Slime the later field-mediated candidate. See
`docs/plans/p3_generator_reuse_survey.md` and
`docs/hypotheses/p3_001_flocking_spike.md`.

**P3-001 result — adopt.** The unmodified standard Flocking model produced
complete paired trajectories; the heading displacement created a 22.66-degree
matched local shock and the late local gap closed in every seed. Global
polarization did not recover on the same timescale, so no generic recovery claim
is made. See `docs/hypotheses/p3_001_flocking_spike_results.md`.

**Current next move:** P3-002 discriminates local alignment, polarization
strength, and prior absolute heading using new seeds, a vision-off null, and a
whole-flock rotation. The design and thresholds are frozen in
`docs/hypotheses/p3_002_flocking_representation_discrimination.md`.

**P3-002 result — no-go.** Local disagreement recovered and interaction beat
the vision-off null, but polarization passed in only four of eight seeds and
prior absolute heading returned in none. Neither frozen representation earned
confirmation. See
`docs/hypotheses/p3_002_flocking_representation_discrimination_results.md`.

**P3-003 result — no-go.** The standard Fireflies run completed cleanly, but
baseline phase order averaged only 0.249, the matched shock gap averaged 0.076,
and no seed closed half its gap. The threshold was not tuned after seeing the
result. See `docs/hypotheses/p3_003_fireflies_spike_results.md`.

**P3-004 result — adopt Slime.** The standard Slime model produced a large,
visible aggregation loss after deterministic dispersal and three of four seeds
closed more than half that gap. All frozen integrity and adoption gates passed.
See `docs/hypotheses/p3_004_slime_spike_results.md`.

**P3-005 result — promote the causal candidate.** After the same dispersal,
chemical-sensing cells recovered to 24.104 mean nearby neighbors while the
matched sensing-disabled cells remained at 1.743, despite regenerating the
chemical field. All eight frozen gates passed. This supports
interaction-dependent reconstruction, not yet an internal target or goal. See
`docs/hypotheses/p3_005_slime_interaction_discrimination_results.md`.

**Current next move:** stop generator screening and run one bounded
bidirectional falsification. Infer a candidate aggregation band from
pre-branch behavior, perturb below it by dispersal and above it by deterministic
compression, and ask whether both move back toward the same band. If no stable
band exists or correction is one-directional, classify P3-005 as a positive-
feedback attractor rather than target regulation. The allocation audit is in
`docs/audits/2026-08-29_p3_generator_reflection.md`.

**P3-006 result — no-go.** Neither perturbation direction returned to the
candidate band, and only two of four baselines passed the slope-stability gate.
P3-005 is classified as interaction-dependent attractor reconstruction, not
target regulation. See
`docs/hypotheses/p3_006_slime_bidirectional_target_results.md`.

**P4-001 result — adopt the Heatbugs bridge.** The standard model closed 98.1%
of the matched deep-freeze unhappiness gap and passed all eight integrity and
adoption criteria. See `docs/hypotheses/p4_001_heatbugs_spike_results.md`.

**P4-002 result — promote blind micro-target inference.** Movement under four
controlled thermal gradients recovered 200 hidden target temperatures with
2.0° median error. The inferred representation predicted held-out movement at
71.5% accuracy versus 55.5% for the identity-free midpoint null. All nine
frozen gates passed. Because the targets are authored explicitly in the
standard generator, stop Heatbugs here. See
`docs/hypotheses/p4_002_heatbugs_blind_target_inference_results.md`.

**Current next move:** run a bounded adoption spike on the installed standard
Slime Mold Network model. Require a visible, reproducible food-conditioned
network response and a signal-disabled null before attempting any endogenous
collective target representation. See
`docs/audits/2026-08-29_p4_target_inference_reflection.md`.

**Sprint 4 — smallest held-out batch, 45–60-minute cap; not yet unlocked.** Run
the frozen size-24 branches only after a new within-condition discovery study
passes. The broad P2-002 screen did not unlock this spend.

**Sprint 5 — synthesis, 20-minute cap; conditional.** Explain successes and
failures by algotype and intervention, regenerate one static evidence figure,
and decide whether Level 3 confirmation or multiscale causal/control analysis is
justified. A passing exploratory result does not automatically buy a full audit.

Expected elapsed time is **90 minutes for a no-go** and **roughly 2.5–3 hours for
a promoted held-out result**. Any extension requires a written replan identifying
the new information it can buy.

### Go/no-go gate

Advance toward multiscale causal/control analysis only if a compact macro family:

- improves held-out attainment loss by at least 20% over both value-only and
  intervention-only nulls;
- stays within 10% of the observable-micro baseline while using at most one
  quarter as many input features;
- preserves its advantage on every held-out size and both activation schedules;
- produces calibrated probabilities rather than only correct labels;
- survives at least one targeted feature-ablation test.

Failure is informative. If only the micro baseline generalizes, retain the
micro description. If no model generalizes, improve the observation or outcome
definition before invoking macro agency.

## What is deliberately deferred

- more thermostat/controller variants;
- automatic representation generation;
- PyMergence or custom causal-emergence calculations;
- LLM agents, rich games, and economics;
- polished visualization beyond what is needed to inspect evidence.

Visualization required to inspect, select, compare, and falsify evidence is not
deferred. Only cosmetic polish and custom frontend engineering are deferred.

Those become justified only after P2-002 establishes a real predictive signal
in an unscripted distributed system.
