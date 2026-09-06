# Experiment 005 — deterministic adaptation results

[Result package](../../results/005-adaptation/) — the raw output behind the 24-case matrix, run twice.
Committed 2026-09-06; until then this record's pass table was the only
surviving trace of the run, because `results/*` is ignored by default and
the package was never added to the allowlist. See [F22](../../../wiki/failure-log.md).

## Decision

**PASS: A1–A6 all passed on the 24-case matrix, run twice.**

| Check | Result | Evidence |
|---|---|---|
| A1 within-run improvement | pass | episode-5/episode-1 error `0.1913–0.2515` |
| A2 frozen-policy contrast | pass | adaptive/frozen final error `0.1913–0.2515` |
| A3 memory null | pass | reset-between and frozen errors equal within `1e-9` |
| A4 policy change | pass | all adaptive gain paths rose from `.05` |
| A5 common baseline | pass | all episode-1 errors matched within `1e-9` |
| A6 reproducibility | pass | normalized scientific rows identical across fresh batches |

The result held for both load signs and actuator effectiveness from `.42` to
`1.08`. By episode 5 the retained-history controller had 19–25% of its initial
and frozen-policy error. Resetting gain between episodes eliminated the entire
advantage, while the common first episode showed that the arms did not begin
with unequal policies.

This supports deterministic, history-dependent parameter adaptation across the
declared plant family. It does not support open-ended learning or goal discovery.

## Reproduction

```bash
NETLOGO_CONSOLE=/path/to/netlogo-headless.sh \
  bash src/experiments/adaptation/run_005.sh
```

NetLogo `7.0.4` was used. Frozen artifact SHA-256 values:

- model: `a20e11e54808ee20c73415a49a8bb285d4fe647ca44ca4f14f33d0e8a7255e22`
- logic: `ea77be37f918fb2a09e5975856a0d376467fd7452ecee49dd06430562c99007d`
- setup: `fd348df685cebf439353f7a3dfe98706f149e6975cac50878af17b4dde11a663`
- analyzer: `03f15614009ec40e4f61e6a3b7f8e2dd62d89a228cc34e0c745d513541632643`
