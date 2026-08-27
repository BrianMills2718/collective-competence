# goal-discovery

Does a tiny deterministic system show goal-like organisation, and how would we
tell? The programme answers one narrow question at a time:

> Given observable trajectories, which *pre-specified* candidate
> representations reveal stable tendencies, and which of those survive held-out
> perturbation tests strongly enough to support a claim beyond passive
> convergence?

Not a simulation platform, not an agent framework, no learned models, no
representation search, no universal goal-directedness score. Systems,
representations and interventions are all written by hand.

## State

| | | |
|---|---|---|
| 001 | cell-view sorting (Zhang/Goldstein/Levin replication) | **complete** — discovery, validation, confirmation |
| 002 | ball-in-bowl passive convergence | not started |
| 003 | thermostat-like negative feedback | not started |
| 004 | redundant compensatory controller | not started |
| 005 | deterministic adaptation across episodes | not started |

Experiment 001 is finished. Three things came out of it.

The replication is faithful: the paper's reported inversion — cell-view bubble
has the *lowest* final error under moveable frozen cells and the *highest* under
immovable ones — reproduces at every frozen-cell count, matching the published
means to within about 0.1 under immovable freezing.

The observable state is not sufficient to predict whether the goal is reached.
Freezing three cells mid-run changes no values at all, so every representation
reads identically the instant it fires, yet it costs the insertion algotype 97
percentage points of goal attainment. Scrambling a fifth of the array — maximally
visible to those same measures — costs it nothing. An attractor account predicts
the opposite.

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
