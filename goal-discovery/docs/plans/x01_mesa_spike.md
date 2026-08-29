# Infrastructure spike X01 — Mesa compatibility and visualization

## Decision to make

Can Mesa replace enough hand-written simulation and visualization plumbing to
speed up later experiments while preserving this programme's reproducibility
and evidentiary boundaries?

This is a time-boxed compatibility test, not a new scientific experiment and
not authorization to migrate the validated Experiment 001 implementation.

## Why now

The systems need identifiable components, private state, local interaction,
movement, configurable activation, interventions, data collection, and a way to
watch trajectories. Mesa provides standard abstractions for most of these and a
Solara-based interactive visualizer. Experiment 001 is now a useful calibration
case because its expected trajectories and conclusions are already recorded.

## Smallest useful prototype

Implement one case only:

- the Experiment 001 bubble algotype;
- one 40-cell one-dimensional array;
- shuffled activation with an explicit seed;
- the existing block-swap intervention;
- moveable and immovable freezing for one cell;
- the existing observable and `boundary_length` representation;
- a live view with play, pause, step, reset, tick, and intervention marker.

Do not port insertion, selection, validation, confirmation, or Experiment 002
during the spike.

## Comparisons against the reference backend

For fixed configurations and seeds, compare:

1. initial observable state;
2. activation order at each tick;
3. observable trajectory and terminal state;
4. swap, step, and tick counts;
5. intervention semantics;
6. exact restore-and-continue behavior;
7. derived representation values;
8. runtime for a small repeated batch.

Byte-identical observable histories are preferred. If Mesa's internal ordering
makes that unreasonable, any statistical comparison must be declared before it
is run and must not replace the existing reference implementation.

## Required capabilities

Mesa is viable only if the prototype demonstrates all of the following:

- deterministic replay from configuration and seed;
- exact snapshot and restoration, including random-number state;
- explicit rather than implicit activation order;
- faithful distinction between moveable-frozen and immovable-frozen cells;
- clean separation of authoritative state, observation, and representation;
- raw trajectory export compatible with the current evidence format;
- live visualization without making the visualizer part of the evidence path;
- no Mesa objects leaking into representation analysis.

## Adoption decision

Adopt Mesa for Experiment 003 and later prototypes only if:

- all required capabilities pass;
- the bubble calibration agrees with the reference backend;
- the implementation is materially smaller or clearer;
- interactive visualization works with little experiment-specific UI code;
- batch execution remains practical;
- Mesa does not force a general agent-framework architecture into `common/`.

Keep the current backend and add only a result viewer if any critical criterion
fails. A mixed decision is allowed: Mesa may be used for rapid exploratory
models while the present implementation remains the replication reference.

## Rapid-iteration execution

Work in this order, stopping as soon as a critical gate fails:

1. Reproduce one seeded bubble baseline and export its observable trajectory.
2. Match activation order, counts, terminal state, and `boundary_length` against
   the reference backend.
3. Prove deterministic replay and exact snapshot-restore continuation.
4. Add the block-swap intervention and both freezing semantics, then rerun the
   focused parity checks.
5. Add the smallest Solara view that supports play, pause, step, reset, tick,
   frozen-cell display, and the intervention marker.
6. Measure repeated-batch runtime and compare implementation size and clarity.
7. Write the adopt, mixed, or decline decision before beginning Experiment 003.

Stop the spike immediately if deterministic replay, exact restoration,
intervention fidelity, or evidence-format compatibility cannot be achieved
without changing the validated reference model. Stop at the time box if the
remaining issues are non-critical and record them rather than broadening scope.

The adoption gate passes only when every required capability passes, parity is
demonstrated, batch use remains practical, and visualization requires little
experiment-specific UI code. Otherwise choose mixed only for a clearly bounded
exploratory role, or decline Mesa and retain the current backend.

The review packet consists of the isolated prototype, focused parity/replay
tests, the live view, measured runtime and code-size notes, and the one-page
decision record. These are decision artifacts, not grounds for migrating
completed experiments.

## Time box and deliverables

Stop after one focused implementation session or when a critical incompatibility
is established. Produce only:

- a disposable or isolated Mesa bubble prototype;
- focused parity and replay tests;
- one live visualization;
- a short decision note: adopt, mixed, or decline;
- measured reasons for the decision.

Do not begin Experiment 003 until the decision note is written. Do not migrate
completed experiments as part of this spike.
