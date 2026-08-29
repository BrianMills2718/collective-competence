# P5-000 — representation-discovery benchmark results

**Decision: no-go. Do not promote the generic `tsfresh` pipeline.**

This is a Level 1 retrospective method result, not fresh confirmation of a
scientific claim. The protocol was frozen in commit `4c4d630` before automated
feature extraction or scoring.

## Integrity

- One shared `tsfresh` extraction and grouped logistic-regression pipeline ran
  unchanged on both tasks.
- The sorting adapter exposed only ticks 0–4 before the intervention and held
  out each of six seeds.
- The thermostat adapter exposed only temperature at ticks 20–35 plus signed
  load and held out each absolute load magnitude.
- Tests enforce those observation boundaries and exclude mechanism, seed, and
  future-outcome fields.
- All 99 frozen within-group label permutations and the frozen top-feature
  ablation ran for both tasks.

## Frozen scores

Lower log loss is better. The shuffle column is the fifth percentile of the 99
shuffled-label losses; the real score had to be lower.

| Task | Runs / groups | Intervention null | Endpoint null | Automated | Shuffle 5% | Top feature removed | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| sorting recovery | 72 / 6 | 0.397 | **0.275** | 0.484 | 0.659 | 0.484 | fail score and ablation |
| thermostat preservation | 16 / 2 | 0.580 | 0.580 | **0.126** | 0.509 | 0.307 | fail robustness |

Sorting automated balanced accuracy was 0.726, below the endpoint null's
0.852. Thermostat automated balanced accuracy was 1.000 versus 0.500 for both
nulls, but removing its top feature increased log loss by 143%, beyond the
frozen 20% robustness limit. Both real-label scores beat their shuffled-label
boundaries, so the result is not a pure label-shuffle artifact.

## What was learned

The negative result is structural, not a request for a larger model. The 72
sorting branches contain only **12 distinct pre-intervention temporal
histories**—one for each seed/schedule pair. Each history is then repeated
across six damage conditions. Outcome variation within those repeats is caused
by the later damage configuration, so expanding five scalar pre-branch points
into 1,554 generic features cannot create the missing relational information.
Indeed, it made held-out log loss 76% worse than the simple endpoint null.

The thermostat check shows the limited case where the method is useful. Generic
early-response features recover a supplied negative-feedback mechanism across
held-out load magnitudes. The most consistently selected family was a chunked
linear-trend slope feature. But the result depends too strongly on that family
and comes from only two deterministic holdout groups, so it is a diagnostic,
not a promoted discovery method.

The benchmark therefore rejects the broad idea that generic scalar time-series
expansion is the current missing machinery. The missing observation is more
specific: spatial or network organization that can change after intervention
and can be evaluated across genuinely independent seeds/layouts.

## Decision and next move

- Keep `tsfresh` as an optional diagnostic; do not build a representation-search
  framework around it and do not tune this failed benchmark.
- Do not run PySINDy or causal-emergence tooling on these short repeated traces.
- Activate the already-conditional P5-001 Slime Mold Network sprint because the
  benchmark identified its exact prerequisite: a spatial/network observation
  unavailable in the stored scalar histories.
- P5-001 must use the unmodified off-the-shelf NetLogo generator and earn a
  mechanism contrast, regime threshold, and held-out cross-scale prediction.
  Another adoption or animation result is insufficient.

## Reproduce

```bash
uv sync --extra representation-discovery
uv run python -m src.experiments.representation_discovery.run
uv run pytest -q tests/test_representation_discovery.py
```

Compact outputs are regenerated under
`results/p5-000-representation-discovery/`: `scores.csv`,
`ranked_features.csv`, `summary.json`, extracted feature tables, and
`decision.png`.
