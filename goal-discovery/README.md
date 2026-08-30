# goal-discovery

Does a tiny deterministic system show goal-like organisation, and how would we
tell? The programme answers one narrow question at a time:

> Given observable trajectories, which candidate representations reveal stable
> tendencies, which survive held-out perturbation tests, and can a reusable
> black-box method propose useful representations rather than receiving all of
> them by hand?

Not a simulation platform, not an agent framework, and not a universal
goal-directedness score. Results through P4 use hand-specified representations;
the next phase tests a bounded off-the-shelf representation-discovery pipeline
before adding another generator.

The [current research plan](docs/plans/current_research_plan.md) is the one
authoritative roadmap. Older plans are retained as decision history.

## State

| | | |
|---|---|---|
| 001 | cell-view sorting (Zhang/Goldstein/Levin replication) | **complete** — discovery, validation, confirmation |
| 002 | ball-in-bowl passive convergence | **complete** — control on the 001 instrument |
| X01 | Mesa compatibility and visualization spike | **complete** — mixed decision; optional exploratory backend |
| X02 | NetLogo visual calibration | **complete** — adopted for the next visual prototype |
| X03 | linked trajectory workbench | **complete** — Panel/HoloViews gate passed; capability promoted |
| 003 | thermostat-like negative feedback | **complete** — regulation calibration passed R1–R5 |
| 003B | blind defended-target inference | **complete** — hidden target recovered; B1–B6 passed |
| 004 | redundant compensatory controller | **complete** — C1–C6 passed on 28 cases |
| 005 | deterministic adaptation across episodes | **complete** — A1–A6 passed on duplicate 24-case batches |
| V1 | calibrated evidentiary ladder | **complete** — requirement audit passed |
| P2-001 | predictive goal-model comparison | **complete** — v1 failed cleanly; v2 passed P1–P6 |
| P2-002 | distributed macro prediction | **complete / no-go** — two frozen predictor gates failed |
| P2-003 | immovable-barrier reachability | **complete** — exact on 7,440 exhaustive branches |
| P2-004 | moveable-cell order reachability | **complete** — exact on 90,720 new-size branches |
| P2-005 | opportunity-adjusted performance | **complete / no-go** — sorting line mechanically complete |
| P3-001 | standard NetLogo Flocking spike | **complete / adopted** — unmodified generator and visualizer |
| P3-002 | Flocking representation discrimination | **complete / no-go** — neither frozen macro-state passed |
| P3-003 | standard NetLogo Fireflies spike | **complete / no-go** — baseline synchrony too weak |
| P3-004 | standard NetLogo Slime spike | **complete / adopted** — strong aggregation recovery |
| P3-005 | Slime interaction discrimination | **complete / promoted** — sensing-dependent recovery |
| P3-006 | bidirectional target discrimination | **complete / no-go** — attractor, not defended band |
| P4-001 | standard NetLogo Heatbugs spike | **complete / adopted** — deep-freeze recovery |
| P4-002 | blind heterogeneous target inference | **complete / promoted** — 2.0° median target error |
| P5-000 | existing-data representation-discovery benchmark | **complete / no-go** — thermostat signal found; sorting lost to endpoint null; generic pipeline not promoted |
| P5-001 | standard Slime Mold Network threshold test | **complete / no-go** — extraction worked; mechanism direction reversed; network predictor failed |
| P5-002 | stability–plasticity confirmation | **complete / no-go** — directional trend too small and seed-sensitive; standard model line closed |
| P6-000 | phenomenon-first benchmark qualification | **complete / selected** — Morpheus M4377 neuromast regeneration clears the fixed scorecard |
| P6-001 | neuromast causal calibration | **complete / no-go** — strong local-feedback effect; one active seed failed and runaway control breached runtime design |
| P6-002 | archive-first benchmark contract | **complete / no selection** — V-Cornea and M9147 lack compact run-level ensemble/control evidence |
| P6-003 | compact evidence-package acquisition | **next** — metadata-first search for one qualifying archived run table |

Before Experiment 003, run the time-boxed
[Mesa compatibility spike](docs/plans/x01_mesa_spike.md). It asks whether an
off-the-shelf agent-based modeling framework can supply identity, space,
activation, data collection, and live visualization without weakening exact
replay or changing Experiment 001's behavior. It is an evaluation, not a
commitment to migrate the validated experiments.

The spike reached exact behavioral parity and produced a live viewer, but Mesa
was not smaller or faster than the focused reference backend. The resulting
[mixed decision](docs/plans/x01_mesa_decision.md) keeps Mesa available for
agent-based exploration without making it the default laboratory architecture.

The subsequent [NetLogo calibration](docs/plans/x02_netlogo_calibration.md)
used the standard NetLogo world, controls, plots, deterministic runs, and
BehaviorSpace rather than a custom viewer. Its
[adoption decision](docs/plans/x02_netlogo_decision.md) selects NetLogo for the
Experiment 003 visual prototype while retaining Python for independent analysis
and evidence.

Experiment 003 then used that split directly: NetLogo supplied the standard
interactive model and BehaviorSpace batch runner, while Python independently
read the exported tables. All five pre-registered regulation checks passed on
34 held-out cases. See the
[confirmation results](docs/hypotheses/003_thermostat_results.md); this calibrates
negative feedback, not agency or autonomous goal discovery.

Experiment 003B then removed the declared target and every controller field from
the analysis boundary. Trajectories alone recovered `20.00`; new sustained
loads separated active defence from the matched passive attractor, and sensor or
actuator removal erased the advantage. The
[blind-inference results](docs/hypotheses/003b_blind_target_inference_results.md)
are the first target-discovery result in the repository, within a deliberately
small supplied candidate family.

Experiment 004 then separated compensation from spare capacity. Either of two
actuator routes could be destroyed and the survivor reproduced intact
performance; fixed allocation was 1.75 times worse, and removing both routes
reproduced the passive system. Experiment 005 separated retained adaptation
from repeated execution: final adaptive error fell to 19–25% of the common
first-episode/frozen baseline, while resetting memory erased the improvement.
The requirement-by-requirement [V1 audit](docs/audits/v1.md) passed. Phase 2 now
tests whether a compact persistent-goal model predicts held-out interventions
better than passive-attractor and memoryless-reactive alternatives.

The first Phase 2 preregistration exposed a real boundary mistake: when ambient
and internal setpoint differed, trajectories converged to their coupled
equilibrium rather than the internal setpoint. That [v1 failure](docs/hypotheses/p2_001_predictive_goal_model_results.md)
is retained. A new aligned, fully held-out v2 then inferred all three hidden
targets exactly and predicted nine unseen intervention trajectories to numerical
precision while both frozen null models failed. See the
[v2 results](docs/hypotheses/p2_001_predictive_goal_model_v2_results.md).

That closes the engineered-controller track. The
[Phase 2 research pivot](docs/plans/p2_research_pivot.md) moves the next test
back to decentralized sorting: can a compact capability-aware macro description
predict recovery after unfamiliar damage across new sizes and schedules, while
remaining competitive with the full observable microscopic state? This is the
first next-step question whose positive answer would materially support the
long-term collective-organization agenda.

P2-002 uses a two-layer visual instrument. NetLogo remains the animation and
trajectory generator; the external Panel/HoloViews workbench supplies linked
space-time, phase, branch, parameter, and model-diagnostic views. The
[X03 decision](docs/plans/x03_visual_analytics_decision.md) records the current
tool survey and fallback order. Every later capability follows the bounded
[reuse survey protocol](docs/plans/reuse_survey_protocol.md) before custom code
is considered.

The P2-002 predictor screens did not earn promotion: neither the original
capability representation nor a targeted relational repair cleared the frozen
margin over intervention-only prediction. That no-go exposed a better question.
P2-003 and P2-004 now give exact, observable recovery boundaries for the two
damage modes: immovable cells preserve spatial partitions, while moveable
passive cells preserve their relative order. The next sprint will condition
performance on reachability instead of treating impossible and unrealized
targets as the same negative label.

P2-005 then found no large opportunity-adjusted performance residual, closing
the sorting line as mechanically complete. A bounded reuse survey moved to the
installed NetLogo Models Library rather than building another generator.
Flocking and Fireflies were stopped by frozen gates. Slime passed: after
deterministic dispersal, cells with chemical sensing restored an average 24.10
nearby neighbors, while the matched sensing-disabled population remained at
1.74 even though its chemical field regenerated. P3-005 therefore promotes
**interaction-dependent aggregation recovery**—the strongest unscripted
collective candidate so far, but not yet evidence of an internal target. The
next sprint therefore tested a regulated band versus a simple attractor.

That P3-006 falsification failed as intended: neither dispersed nor compressed
Slime populations returned to one candidate band, so the phenomenon is now
classified as interaction-dependent attractor reconstruction. The next
off-the-shelf bridge, Heatbugs, passed its recovery calibration and then a blind
per-agent inference test. Four observable movement probes recovered 200 hidden
targets with 2.0° median error and predicted held-out directions at 71.5%, 16
points above an identity-free null. Because those micro targets are explicitly
authored in the standard generator, Heatbugs now stops. The next bounded move
was an existing-data representation-discovery benchmark. The installed Slime
Mold Network was retained as the conditional first new generator, but it had to buy a
mechanism, regime threshold, or cross-scale prediction rather than another
adoption result.

P5-000 then stopped the generic black-box route cleanly. Off-the-shelf temporal
features detected the engineered thermostat's early feedback response but made
sorting recovery prediction worse than the frozen endpoint null. The apparent
72-case sorting set contained only 12 distinct pre-damage histories, so the
missing information is relational and post-intervention rather than another
scalar transform. The [P5-000 results](docs/hypotheses/p5_000_representation_discovery_benchmark_results.md)
activate one tightly bounded Slime Mold Network experiment aimed at spatial and
network structure; they do not license a larger learned model.

P5-001 converted every continuous fluid field into a usable off-the-shelf
skeleton graph, producing the first genuinely spatial systems-analysis view in
the programme. Its promotion claim still failed: early topology worsened
held-out prediction, and stronger signaling reduced rather than improved
relative relocation retention. At the same time, unchanged-route organization
rose from 0.324 to 0.885 while relocated organization peaked at an intermediate
boost. The [P5-001 results](docs/hypotheses/p5_001_slime_mold_network_threshold_results.md)
therefore fund exactly one fresh-seed stability–plasticity confirmation, not a
larger model or graph-analysis programme.

P5-002 then rejected that candidate tradeoff on fresh seeds and a second
relocation distance. The spatial visual instrument remained reliable, but the
effect size and paired-seed consistency did not. The
[P5-002 results](docs/hypotheses/p5_002_stability_plasticity_confirmation_results.md)
close the standard Slime Mold Network line and keep causal/control machinery
locked. The next move is a short phenomenon-first qualification of no more than
three mature off-the-shelf benchmarks, not another open-ended generator screen.

P6-000 found the first benchmark that clears that harder bar: the published
Morpheus [zebrafish neuromast model](docs/plans/p6_000_phenomenon_qualification.md)
starts from experimental severe-ablation images and uses stochastic local
neighbor feedback to recover organ size, cell-type proportions, and radial
architecture. Its mechanism can be disabled in place, its CLI ran a real
1,000-step diagnostic in 3.49 seconds on WSL, and Morpheus already supplies the
GUI and spatial plotting surface. P6-001 therefore buys one causal calibration,
not a custom generator, viewer, or broad platform migration.

P6-001 then found a large model-internal causal effect but rejected M4377 as the
programme benchmark. Three fresh seeds rebuilt 58–65-cell radially ordered
organs; one lost the sustentacular population and stalled at eight cells.
Proliferation-off controls remained at five, while removing the local stopping
rule drove every seed to at least five times the target before model day 2.67
and made the fixed endpoint computationally pathological. The
[P6-001 results](docs/hypotheses/p6_001_neuromast_causal_calibration_results.md)
close that line. The next selection must prove ensemble recovery rate and a
bounded or event-based causal control from compact published artifacts before
we install another simulator or generate trajectories.

P6-002 applied that corrected gate before installation. V-Cornea has three
injury severities, rich spatial recovery measures, live visualization, and
headless scripts, but its compact public surface does not expose the per-run
recovery denominator or a matched mechanism-off recovery comparison. Morpheus
M9147 is compact and spatial, but its released reproduction fixes one seed and
one lesion geometry and omits the reduced mechanism models. The
[archive-first decision](docs/plans/p6_002_archive_first_benchmark_contract.md)
therefore selects neither. P6-003 searches for a compact run-level evidence
package, not another simulator.

Research time is allocated by the
[progress-allocation protocol](docs/plans/progress_allocation_protocol.md):
maintain one active learning sprint, produce an observable artifact in the
first quarter, require a discriminating result by 60% of the cap, and purchase
additional confidence only in a separate sprint after promotion. The
[company-planning reflection](docs/audits/2026-08-29_company_planning_reflection.md)
records why generator screening and dashboard work are now stopped.

Experiment 001 is finished. Three things came out of it.

The replication is faithful: the paper's reported inversion — cell-view bubble
has the *lowest* final error under moveable frozen cells and the *highest* under
immovable ones — reproduces at every frozen-cell count, matching the published
means to within about 0.1 under immovable freezing.

The observable state is not sufficient to predict whether the goal is reached.
Freezing three cells mid-run changes no values at all, so every representation
reads identically the instant it fires, yet it costs the insertion algotype 97
percentage points of goal attainment. Scrambling a fifth of the array — maximally
visible to those same measures — costs it nothing.

Experiment 002 then showed that a ball in a bowl does the same thing, so that
test detects a gap in the representation set rather than anything about agency.
**What actually separates the two systems is redundancy**: the array reaches its
goal with three of forty cells frozen and unable to act, because neighbours
carry them, while the bowl is stranded forever by one frozen coordinate of
eight, because nothing can act on anything else.

And two measures I invented to detect that failed and were withdrawn, which is
in [the confirmation results](docs/hypotheses/001_sorting_confirmation_results.md)
alongside the rest.

What 001 does **not** show is regulation, compensation, or adaptation. Those need
the contrastive systems 002–005.

## The evidentiary ladder

The programme exists to keep these apart, because every one of them can look
like the one above it in a single suggestive plot.

| | Means | Needs |
|---|---|---|
| Passive convergence | flows to an attractor | repeated approach from varied starts |
| Persistence | stays once there | long dwell, low escape |
| Regulation | negative feedback counters disturbance | error falls faster than an unperturbed baseline |
| Compensation | *different* routes restore the same macro condition | recovery despite targeted damage, by more than one route |
| Adaptation | earlier episodes improve later ones | frozen-policy control fails where this succeeds |
| Goal-model support | a compact goal description predicts interventions | beats attractor and reactive nulls on held-out interventions |

Default reading for anything this repository reports:
*a candidate goal-directed tendency* — a representation-defined region
trajectories repeatedly move toward, stay in, or return to under a
pre-registered class of perturbations. Nothing more.

## Layers

```
S_t  --h-->  O_t  -->  Z_t = f(H_t)
```

`S_t` authoritative simulator state · `O_t` what analysis may see ·
`Z_t` a candidate representation over history. A representation becomes a
*state representation* only by passing a declared sufficiency test. Analysis
code never imports simulator internals.

## Run it

```bash
cd goal-discovery
make dayone          # sync, test, baseline, branch — from a clean checkout
```

or piecemeal:

```bash
uv sync
uv run pytest -q
uv run python -m src.experiments.sorting.run baseline
uv run python -m src.experiments.sorting.run branch
uv run python -m src.experiments.sorting.run branch --algotype selection
```

To run the isolated Mesa spike and its live viewer:

```bash
uv sync --extra mesa-spike
uv run --extra mesa-spike pytest -q tests/test_mesa_spike.py
uv run --extra mesa-spike solara run src/spikes/mesa_bubble/viz.py
```

The preferred visual calibration is the standard NetLogo model at
`src/spikes/netlogo_bubble/netlogo-bubble.nlogox`. See its adjacent README for
interactive and headless instructions.

To open the linked trajectory workbench on the existing X02 runs:

```bash
uv sync --extra visual-workbench
uv run --extra visual-workbench panel serve src/workbench/app.py --show --port 5010
```

Choose or filter a run in the outcome table. The cell raster, macro signals,
phase path, capability view, and matched baseline all follow that selection.
The **Future mockup** tab previews the intended end-state research workflow;
panels marked MOCKED are deliberately not backed by new experiment machinery
yet, so they can be reviewed before implementation.
The **Save selected evidence PNG** button writes a static evidence sheet under
`results/x03-workbench/`. Regenerate the rapid representation screen with:

```bash
uv run --extra visual-workbench python -m src.workbench.analysis
```

Run the frozen P2-002 crossed prediction prototype with:

```bash
uv run python -m src.experiments.distributed_prediction.run
```

It generates the size-12 discovery batch, scores the five declared
representation families with held-out seeds, and creates the size-24 batch only
if the frozen promotion gate passes. The first completed run stopped before
size 24; see
`docs/hypotheses/p2_002_distributed_macro_prediction_results.md`.

Run the two exhaustive reachability tests with:

```bash
uv run python -m src.experiments.distributed_prediction.reachability
uv run python -m src.experiments.distributed_prediction.moveable_reachability
```

Their frozen designs and results are in
`docs/hypotheses/p2_003_barrier_reachability*.md` and
`docs/hypotheses/p2_004_moveable_order_reachability*.md`.

Run the adopted off-the-shelf Slime experiments with:

```bash
uv run python -m src.spikes.netlogo_slime.run
uv run python -m src.spikes.netlogo_slime.run_p3_005
```

The first command tests whether the unmodified visual generator has a usable
loss-and-recovery trajectory. The second compares matched recovery with
chemical sensing active and disabled. The installed `Slime.nlogox` remains the
interactive visualization; the adapter modifies no generator source.

Run the Heatbugs bridge calibration and blind target probes with:

```bash
uv run python -m src.spikes.netlogo_heatbugs.run
uv run python -m src.spikes.netlogo_heatbugs.run_p4_002
```

P4-002 keeps `ideal-temp`, `unhappiness`, and the generator decision
calculation outside inference. Hidden truth is joined only after estimates are
fixed for frozen scoring.

The first adopted experiment is
`src/experiments/thermostat/thermostat.nlogox`. Open it in NetLogo 7.0.4 to use
the controls and live plots; its adjacent README explains the display and the
embedded 34-case BehaviorSpace suite.

Each run writes a fresh directory under `results/` holding the raw trajectory,
the derived representation values, run metadata (git commit, seeds, rule and
representation versions, snapshot id) and the figures. Runs never overwrite each
other — `results/LATEST` names the most recent.

## Where to look

- [`docs/hypotheses/001_sorting_validation_results.md`](docs/hypotheses/001_sorting_validation_results.md)
  — **start here.** What validation found, including the two rules that failed
  and the one prediction that was wrong.
- [`docs/hypotheses/001_sorting.md`](docs/hypotheses/001_sorting.md) — the
  experiment: hypothesis, representations, interventions, phase split, nulls,
  limitations, reproduction command.
- [`001_sorting_validation.md`](docs/hypotheses/001_sorting_validation.md) and
  [`_v2`](docs/hypotheses/001_sorting_validation_v2.md) — the pre-registrations,
  both committed before their seeds were run. v1 failed on its own pilot; v2
  says why and what it cost.
- [`docs/sources/README.md`](docs/sources/README.md) — which rule came from the
  paper, which from its reference code, and the two deliberate deviations.
- `src/experiments/sorting/representations.py` — the frozen candidate set.

## House rules

- **Determinism is a blocker, not a nicety.** Same config and seed, byte-identical
  history. Activation order is declared, never implicit.
- **Restore, never approximate.** A counterfactual starts from the exact
  snapshot its sibling started from, RNG stream included.
- **Raw trajectories are the evidence.** Figures are regenerated from them.
- **Freeze before confirming.** Representations, thresholds and decision rules
  are fixed before the confirmation set is touched.
- **Keep `common/` small.** A helper that serves one experiment belongs in that
  experiment.
- **Survey before building.** Check installed tools, reference implementations,
  and maintained libraries against the active experiment before adding custom
  infrastructure.
- **Explore interactively, decide reproducibly.** Linked dashboards help find
  structure; frozen claims are regenerated from raw trajectories by versioned
  analysis code.
- **Match confidence to consequence.** Discovery gets cheap safeguards;
  confirmation-grade checking is conditional on a result earning promotion.
- **Replan at 2×.** When an artifact takes twice its estimate, reduce scope,
  change tools, or justify the new information the extension can buy.
