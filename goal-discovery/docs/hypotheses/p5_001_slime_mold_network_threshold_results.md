# P5-001 — Slime Mold Network threshold results

**Decision: no-go for the promoted representation claim.**

The protocol was frozen in commit `0baeaee` before data generation. NetLogo ran
the installed source model unchanged. All 30 checkpoint and 60 late design cells
completed; the three independent arms ran concurrently, and analysis was rerun
without repeating simulation after raising Python's CSV field-size limit for the
legitimate 201 × 201 patch exports.

## Integrity and extraction

- Source model SHA-256:
  `93b05eeb698936369e66dd81fba1aaa23ccf21978a5af4b7d081e6dc81ae3e1b`.
- Seeds 701–706, boosts 0/20/40/60/80, and all arm/tick cells were complete.
- Global Otsu thresholding, small-object removal, skeletonization, and the
  eight-neighbor graph produced a nonempty skeleton and two food components in
  **100% of 90 fields**. No segmentation parameter was tuned.

The field-to-network visualization therefore worked as an instrument. The
scientific and predictive promotion gates did not.

## Frozen gate results

| Gate | Required | Result | Verdict |
|---|---:|---:|---|
| positive-boost relocation advantage | ≥ 0.15 | best was **−0.292** at boost 20 | fail |
| seeds clearing paired advantage | ≥ 5 / 6 | 1 / 6 | fail |
| adjacent median jump | ≥ 0.10 | 0.292 between 0 and 20 | pass, opposite direction |
| network MAE versus intervention null | ≤ 90% | 0.132 versus **0.095** | fail |
| network MAE versus density null | ≤ 90% | 0.132 versus **0.105** | fail |
| network MAE versus shuffled 5% | below 0.099 | 0.132 | fail |

Median relocation retention ratios were 1.000, 0.708, 0.690, 0.588, and 0.511
as signal boost increased. The method did not discover a transferable early
network predictor; adding checkpoint topology made held-out error 39% worse
than the intervention-only null.

## What the visual audit revealed

The failure is directional rather than featureless:

| Boost | Sham organization | Relocated organization | Retention ratio |
|---:|---:|---:|---:|
| 0 | 0.324 | 0.524 | 1.000 (clipped) |
| 20 | 0.783 | 0.563 | 0.708 |
| 40 | 0.860 | **0.589** | 0.690 |
| 60 | 0.876 | 0.514 | 0.588 |
| 80 | **0.885** | 0.453 | 0.511 |

All late skeletons connected their current food components. Stronger signaling
mainly strengthened and shortened the unchanged food route; after relocation,
organization peaked at an intermediate boost and then fell. This suggests a
stability–plasticity tradeoff: the same mechanism that consolidates an
established route may make rapid reconfiguration harder. That interpretation
was not the frozen P5-001 claim and is not confirmed here.

## Decision and next allocation

- Do not promote the early network predictor, tune the failed graph features,
  or unlock causal/control analysis.
- Retain the Otsu/skeleton/graph adapter as a validated measurement and visual
  instrument, not as a predictive representation discovery result.
- Spend one reduced P5-002 sprint on fresh seeds and two relocation geometries
  to confirm or reject the newly observed stability–plasticity direction.
- Stop the standard-model line if that fresh confirmation fails. If it passes,
  the next experiment must isolate memory/path dependence rather than add more
  feature machinery.

## Reproduce and view

```bash
uv sync --extra network-analysis
uv run python -m src.spikes.netlogo_slime_network.run
uv run pytest -q tests/test_slime_network.py
```

The ignored evidence directory contains `network_metrics.csv`, `retention.csv`,
`summary.json`, `metadata.json`, and `decision.png` under
`results/p5-001-slime-mold-network-001/`.
