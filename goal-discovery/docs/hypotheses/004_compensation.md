# Experiment 004 — redundant-route compensation

**Pre-registered after 003B and before any 004 batch is generated.**

## Question

Can a controller preserve the same scalar target after either of two distinct
actuator routes is disabled by reallocating the complete command to the route
that remains?

This calibrates compensation. The target, route identities, faults, and
allocation rule are supplied; success is not evidence of autonomous agency.

## System and controls

The scalar plant from 003 is retained. At each tick:

```text
temperature' = temperature + .05 * (20 - temperature)
             + route_a_applied + route_b_applied + persistent_load
desired_total = clip(-.30 * (temperature - 20), -2, 2)
```

In the rerouting arm, `desired_total` is divided equally among currently
available routes. If one route fails, the survivor receives the full command.
In the fixed-allocation null, each route is assigned half the command even when
its sibling fails, so the unavailable half is lost. Passive commands zero.

At tick 20 a sustained load and the declared fault begin. The horizon is 160;
late error is mean `abs(temperature - 20)` over ticks 140–159.

## Held-out matrix

Loads are `-0.43, -0.27, +0.16, +0.36`, none used in 003 or 003B. Each runs in:

1. passive;
2. intact rerouting controller;
3. route A disabled, rerouting;
4. route B disabled, rerouting;
5. route A disabled, fixed allocation;
6. route B disabled, fixed allocation;
7. both routes disabled.

This is 28 deterministic runs. No case may be removed.

## Frozen decisions

- **C1 — intact regulation:** intact late error is at most 25% of passive for
  every load.
- **C2 — either-route recovery:** each single-route rerouting arm is at most
  25% of passive for every load.
- **C3 — distinct-route equivalence:** paired A-disabled and B-disabled
  temperature trajectories agree within `1e-9` at every recorded tick.
- **C4 — takeover:** after the fault, the disabled route applies exactly zero
  and the surviving route supplies at least 95% of total absolute applied
  control in each single-fault rerouting run.
- **C5 — reallocation matters:** each fixed-allocation single-fault late error
  is at least 1.5 times its matched rerouting error.
- **C6 — routes are causally necessary:** dual-disabled late error is at least
  90% of passive and fails the 25% regulation threshold for every load.

004 passes only if C1–C6 pass. Reproducibility failure voids the decision.

## Interpretation limit

Passing shows engineered flexible compensation by two distinct causal routes.
It does not show learning: the takeover rule is fixed before the run.
