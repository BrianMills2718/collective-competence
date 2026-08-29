# Phase 2 / Experiment 001 v1 — result

## Decision

**FAIL: P1 and P2 failed; P3–P6 passed.** The failure is retained as evidence.

The blind estimates for held-out configured setpoints `16.5, 21.5, 25.5` were
`17.0, 21.25, 24.5`. This was not target leakage or optimizer failure. Ambient
remained 20 while the setpoint varied, so the no-load closed-loop equilibrium
was:

```text
(.05 * ambient + .25 * setpoint) / .30
```

Those equilibria are `17.083, 21.25, 24.583`, matching the blind estimates.
Trajectories therefore identified what the whole coupled system actually
returned to, while P1 incorrectly required the controller's internal setpoint.
The resulting target mismatch made recursive goal MAE `.008–.098`, failing the
frozen `.02` limit in six of nine cases.

The goal representation still beat both nulls and recovered coefficients
`k=.2911`, `b=.9566`, but v1 does not pass. No threshold or case was changed.
A separately preregistered v2 aligns ambient to each setpoint and uses entirely
new targets, displacements, and loads.
