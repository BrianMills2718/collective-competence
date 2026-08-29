# Phase 2 / Experiment 001 v2 — results

## Decision

**PASS: P1–P6 all passed on all 47 preregistered runs.**

The v1 failure remains reported separately. V2 changed the confounded plant
setup, used entirely new cases, and retained every original decision threshold.

| Check | Result | Evidence |
|---|---|---|
| P1 target inference | pass | `15.25`, `19.75`, `24.25`, all exact |
| P2 absolute prediction | pass | goal MAE `2.1e-15–1.0e-14` |
| P3 attractor contrast | pass | attractor MAE `2.52–4.90` |
| P4 reactive contrast | pass | reactive MAE `.239–1.094` |
| P5 mechanism recovery | pass | target correction `.3000`, load `1.0000` |
| P6 no leakage | pass | persisted rows contain exactly six blind fields |

The compact persistent-target model was fitted on four training systems, then
recursively predicted nine trajectories from three new hidden-target systems
under new sustained loads. It recovered the actual deterministic transition to
floating-point precision. The passive-attractor null under-corrected error; the
single global reactive null could not express different persistent target
locations.

This supports a persistent per-system goal coordinate as a useful predictive
representation for this aligned linear family. The result does not establish
that goal language will outperform equally expressive alternatives in nonlinear,
noisy, or partially observed systems.

## Reproduction

```bash
NETLOGO_CONSOLE=/path/to/netlogo-headless.sh \
  bash src/experiments/predictive_goal/run_p2_001_v2.sh
```

NetLogo `7.0.4` was used. SHA-256 values:

- model: `9376166947a4b41f3bbb8349b48978df9a55ac18d735a7578c13c52eb09aa590`
- model logic: `c77daa66e0dcd222d5d31da35cc5a62f1704d1cf21386793692416b42f4aa0f6`
- v2 setup: `05c3071e43cfffdf7dafd50f5c7f1e774c44577915f75f8cf21a58d6c880047c`
- analyzer: `0591708c42d5279e42a516b2e4b81eb77aef8c23b2803bac2fcd5015c14e74c4`
