# X01 decision — mixed use of Mesa

## Decision

**Mixed.** Keep the completed Experiment 001 implementation as the replication
reference. Keep Mesa as an optional backend for rapid exploration when a system
is naturally agent-based and its built-in activation and live controls remove
more work than they add. Do not make Mesa the default architecture and do not
migrate completed experiments.

## What passed

- Exact tick-for-tick bubble trajectories against the reference backend.
- Exact step, swap, activation-order, and terminal-state parity.
- Index, reverse-index, and shuffled activation across multiple seeds.
- Moveable and immovable freeze semantics.
- Seeded block-swap parity without consuming the transition RNG.
- JSON snapshot, restore, and identical future replay.
- Observation and `boundary_length` agreement.
- A live Solara viewer with play, pause, step, reset, parameters, freeze
  interventions, current state, boundary history, and intervention markers.
- Viewer server startup and an HTTP 200 response.

Eleven focused compatibility tests cover these gates.

## What did not earn full adoption

Mesa 3.4 and later require Python 3.12, while this project currently supports
Python 3.11. The spike therefore uses Mesa 3.3.x. Its visualization extra also
needed an explicit `networkx` dependency in this environment.

On 200 seeded, reverse-sorted 40-cell bubble runs capped at 4,000 ticks:

| backend | elapsed | mean per run | total ticks |
|---|---:|---:|---:|
| reference | 0.6075 s | 3.037 ms | 12,243 |
| Mesa | 1.4679 s | 7.340 ms | 12,243 |

Mesa was 2.42 times slower, though both remain fast enough for small
experiments. More importantly, the isolated Mesa bubble model is 331 lines
while the 359-line reference model implements bubble, insertion, selection,
and the random-swap null. The custom live viewer adds 239 lines. Mesa supplied
useful controls and agent management but did not materially reduce the code for
this exact-replication case.

These measurements are a local engineering comparison, not a scientific
result. They are sufficient to fail the spike's full-adoption gate.

## Operating rule

Use Mesa when the prototype needs several persistent agents, spatial movement,
configurable activation, and live interaction. Prefer a direct deterministic
model for small equations or controllers where Mesa's agent abstractions do not
remove complexity. In either case, preserve the same observation,
representation, intervention, trajectory, and metadata boundaries.

Mesa remains an optional `mesa-spike` dependency so the core laboratory does
not acquire the visualization stack by default.

## Next step

Begin Experiment 003 as the smallest thermostat-like negative-feedback test.
Choose its backend by fit, not by momentum from this spike. Its first prototype
must contrast active feedback against a passive system and visualize setpoint,
error, disturbance, and control action.
