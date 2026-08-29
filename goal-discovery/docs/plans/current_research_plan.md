# Current research plan

**Status:** authoritative roadmap. Historical plans explain how the programme
arrived here but do not define the current next move.

## Objective and present bottleneck

The long-run objective is to discover which observable representations and
scales make dynamical structure, prediction, control, and collective competence
most legible, then test whether any higher-level description earns distinct
predictive, causal, or control value.

The laboratory now has enough generators, perturbations, nulls, and
visualization. Its bottleneck is a reusable black-box method for proposing and
testing representations across systems. Post-002 evidence also needs to be
sealed in version control before more evidence accumulates.

## Allocation decision

Stop generator screening and dashboard development. The next complete learning
cycle uses existing data. Slime Mold Network is conditional follow-on work, not
the default next experiment.

### 0. Seal the current evidence state — complete

Decision unlocked: whether every later result can be reconstructed and its
protocol/source identity audited from a clean checkout.

- inventory the dirty and untracked post-002 work;
- preserve protocols, source, environment locks, and compact decision artifacts;
- record which large raw tables are regenerated rather than versioned;
- create one versioned research-state checkpoint after explicit repository-owner
  approval.

Stop after the checkpoint and clean-checkout instructions exist. Do not use this
task to refactor experiments or broaden validation.

Outcome: the checkpoint commit containing
[`2026-08-29_post_002_evidence_checkpoint.md`](../audits/2026-08-29_post_002_evidence_checkpoint.md)
preserves the post-002 programme state, records the ignored-artifact boundary,
and verifies the clean source/test surface. This does not retroactively timestamp
the earlier protocols; future held-out protocols must be committed before data.

### 1. Existing-data representation-discovery benchmark — complete / no-go

Goal movement: determine whether one thin, off-the-shelf black-box pipeline can
surface useful temporal representations across contrasting systems rather than
adding another hand-selected generator.

The frozen
[`P5-000 benchmark`](../hypotheses/p5_000_representation_discovery_benchmark.md)
uses the one existing task with enough independent groups for a meaningful
screen—sorting recovery across six held-out seeds—and a deliberately limited
thermostat mechanism-portability check across held-out load magnitudes. Flocking,
Slime, and Heatbugs have too few independent trajectories for this benchmark;
reusing their many time rows as independent examples would manufacture sample
size. Hidden mechanism fields and post-boundary observations remain excluded.

Rapid sequence:

| Time | Work | Required output |
|---:|---|---|
| 0–10 min | freeze tasks, observation whitelist, nulls, and gate | one sprint card |
| 10–25 min | map stored tables to one thin run/time/variable schema | first real normalized trace |
| 25–50 min | run a bounded off-the-shelf temporal feature extractor and first held-out score | ranked features plus null |
| 50–70 min | run the same pipeline on the remaining tasks | cross-task score table |
| 70–82 min | shuffle/leakage and feature-ablation attack | falsification result |
| 82–90 min | decide and save one evidence surface | promote, change, or stop |

Use `tsfresh` first because it supplies systematic temporal features without a
custom search engine. Use PySINDy only as a conditional low-dimensional system-
identification comparison; it does not replace representation discovery.

Promotion gate:

- the same pipeline runs on at least two contrasting systems;
- it beats the frozen intervention-only and endpoint-plus-intervention nulls on
  held-out groups in both tasks, including a 10% margin on the primary sorting
  task;
- its useful features survive the shuffle/leakage boundary and one ablation;
- the result is interpretable enough to propose a separately frozen
  perturbation prediction;
- the adapter remains thin and removable rather than becoming a framework.

Stop at minute 50 if there is no valid first held-out comparison. A no-go means
retain hand-designed representations and diagnose the missing observation; it
does not buy a larger learned model.

Outcome: the same generic pipeline detected the engineered thermostat response
but was worse than the simple endpoint null on sorting and failed the frozen
robustness gate. The 72 sorting branches contain only 12 distinct pre-damage
histories; their missing information is post-intervention relational structure,
not another transform of the same five scalar points. See the
[`P5-000 results`](../hypotheses/p5_000_representation_discovery_benchmark_results.md).
Do not tune or enlarge this pipeline.

### 2. Slime Mold Network threshold experiment — active, 90 minutes

This condition is now met: Step 1 identified a specific spatial/network
observation that the repeated scalar histories cannot test. Start with a model-
surface audit and a frozen protocol; do not generate evidence first.

The experiment must buy more than adoption. Use the installed, unmodified model
to test:

- food-conditioned network response against `food-signal-boost = 0`;
- a bounded signal-strength sweep for a reproducible regime threshold;
- reconfiguration after food relocation or route obstruction;
- whether a compact field/network representation predicts recovery on held-out
  seeds or layouts better than density and intervention-only nulls.

The standard NetLogo interface is the visualization. Produce only one static
decision figure. Stop if no stable metric or discriminating null appears by
minute 55.

### 3. Multiscale causal/control analysis — conditional

Unlock only when a compact macro representation predicts held-out intervention
responses and has a manageable transition representation. Then run a bounded
reuse spike for PyMergence/einet or a Koopman-style control comparison. Do not
implement causal-emergence mathematics locally.

## Explicit stop and defer list

- more Heatbugs probes or Slime aggregation-band repairs;
- another adoption-only NetLogo generator;
- more dashboard, mockup, or frontend work without a changed result;
- broad simulator or trajectory-framework refactors;
- causal-emergence tooling before a suitable macro transition model;
- richer environments, LLM agents, and economics.

## Portfolio view

Steps 0 and 1 are complete. Step 2 is active because P5-000 located a concrete
spatial/network observation gap; Step 3 remains conditional. This keeps the next
sprint tied to a falsified bottleneck rather than to generator novelty.
