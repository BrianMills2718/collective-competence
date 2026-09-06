# Experiment 004 — redundant-route compensation results

[Result package](../../results/004-compensation/) — the raw output behind 28 preregistered runs.
Committed 2026-09-06; until then this record's pass table was the only
surviving trace of the run, because `results/*` is ignored by default and
the package was never added to the allowlist. See [F22](../../../wiki/failure-log.md).

## Decision

**PASS: C1–C6 all passed on all 28 preregistered runs.**

| Check | Result | Evidence |
|---|---|---|
| C1 intact regulation | pass | late-error ratio `0.14305` for every load |
| C2 either-route recovery | pass | A-disabled and B-disabled ratio `0.14305` |
| C3 distinct-route equivalence | pass | paired temperature trajectories equal within `1e-9` |
| C4 takeover | pass | failed route applied zero; survivor supplied 100% |
| C5 reallocation matters | pass | fixed/rerouted late-error ratio `1.75` |
| C6 route necessity | pass | dual-disabled/passive ratio `1.00` |

Loads were `-0.43, -0.27, +0.16, +0.36`. The surviving route reproduced the
intact controller's performance regardless of which route was removed. Merely
retaining half the actuator capacity was not enough: the fixed-allocation null
was 75% worse than active reallocation. Removing both routes exactly reproduced
the passive late error.

This supports the narrow claim of engineered compensation through two distinct
causal routes. The rerouting policy was supplied, so this is not adaptation.

## Reproduction

```bash
NETLOGO_CONSOLE=/path/to/netlogo-headless.sh \
  bash src/experiments/compensation/run_004.sh
```

NetLogo `7.0.4` was used. Frozen artifact SHA-256 values:

- model: `a7314ca5f363e88ebfd0b8b138df7813b1bab8f280bbd8e269e014b2e0132b2d`
- logic: `6b2f56386329e1fa7b56cd6c7f6dd2202a45af7629d0a620463eadfce1662a7b`
- setup: `2a26cbe84abf40c6a12c808d644337c0228d7b596c1bbae71f2a46a99c1e869d`
- analyzer: `cffb7ebf4299490f7e18debe07c298bf653497a399c5f2197037642765209059`
