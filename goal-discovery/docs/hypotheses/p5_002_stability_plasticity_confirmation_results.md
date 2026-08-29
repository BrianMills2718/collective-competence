# P5-002 — stability–plasticity confirmation results

**Decision: no-go. Close the standard Slime Mold Network line.**

P5-002 used the unchanged P5-001 model and field-to-network map, new seeds
801–806, boosts 0/40/80, and fixed near/far relocations. All 54 design cells
completed, and every field produced a nonempty skeleton with two food
components.

## Frozen gates

| Gate | Required | Result | Verdict |
|---|---:|---:|---|
| extraction integrity | ≥ 80% | 100% | pass |
| median sham gain, boost 0→80 | ≥ 0.30 | 0.090 | fail |
| seeds with sham gain ≥ 0.20 | ≥ 5 / 6 | 2 / 6 | fail |
| near median difference-in-differences | ≤ −0.30 | −0.190 | fail |
| near seeds at ≤ −0.20 | ≥ 5 / 6 | 3 / 6 | fail |
| far median difference-in-differences | ≤ −0.30 | −0.132 | fail |
| far seeds at ≤ −0.20 | ≥ 5 / 6 | 2 / 6 | fail |
| near retention drop, boost 0→80 | ≥ 0.25 | 0.045 | fail |
| far retention drop, boost 0→80 | ≥ 0.25 | 0.145 | fail |

Median retention was directionally nonincreasing for both geometries, but the
magnitude and paired-seed consistency were far below the frozen confirmation
requirements.

## Fresh-seed surface

| Boost | Sham organization | Near relocation | Far relocation |
|---:|---:|---:|---:|
| 0 | 0.786 | 0.612 | 0.508 |
| 40 | 0.852 | 0.622 | **0.579** |
| 80 | **0.885** | **0.639** | 0.526 |

The major P5-001 sham increase did not reproduce because the new boost-zero
baseline was already high. Per-seed high-signal difference-in-differences also
varied widely: near ranged from +0.223 to −0.594 and far from +0.095 to −0.710.
The candidate tradeoff is therefore seed-sensitive rather than a robust
model-level effect under this design.

## Decision and research implication

- Withdraw the stability–plasticity claim; do not average P5-001 and P5-002 into
  a post-hoc positive result.
- Retain the field/skeleton visualization as working infrastructure, but do not
  spend another sprint tuning this model, its layouts, or its network score.
- Keep causal/control analysis locked because no compact representation has
  earned held-out predictive value.
- The current bottleneck is no longer visualization or implementation. It is
  selection of a phenomenon with robust intervention/recovery structure and
  enough independent variation to support discovery.

The next step is a short phenomenon-first qualification survey of mature,
off-the-shelf benchmark models. It must select one model against explicit
evidence criteria or stop; it is not another broad generator screen.

## Reproduce and view

```bash
uv sync --extra network-analysis
uv run python -m src.spikes.netlogo_slime_network.run_p5_002
uv run pytest -q tests/test_slime_network.py
```

Regenerated artifacts live under `results/p5-002-stability-plasticity/`.
