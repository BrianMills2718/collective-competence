---
doc-role: working-laboratory-guide
authority: derived
lifecycle: active
sources:
  - substrate-design.md
  - ../roadmap/apparatus.md
  - ../goal-discovery/README.md
  - ../goal-discovery/src/lattice/core.py
  - ../goal-discovery/src/lattice/specimens/regulation.py
---
# Dynamical Laboratory

[Wiki home](index.md) · [Current work](current.md) · [Concepts](concepts.md) · [Substrate bench](bench.html)

The Dynamical Laboratory is the shared experimental apparatus for both research arms. It exists to make small dynamical systems easy to construct or import, run, observe under controlled access, perturb, compare, and inspect.

It is **apparatus, not the scientific result**.

## Current substrate

The active shared substrate lives under [`goal-discovery/src/lattice/`](../goal-discovery/src/lattice/). It is a generalized one-dimensional discrete interacting system with:

- sites containing mobile entities or local state;
- local transition rules;
- experiment-supplied schedules;
- synchronous or local update patterns where supported;
- per-entity faults/heterogeneity;
- snapshot and restore, including random state;
- a common operation currency for relevant comparisons;
- an observation contract that can deliberately hide channels from an analyst.

The same substrate reproduces the founding self-sorting implementation trajectory-by-trajectory across the gated comparison suite, expresses elementary cellular automata as a constrained case, and now carries a minimal passive-relaxation / negative-feedback regulation calibration without adding substrate features.

## Why one shared substrate

The point is not to claim universality. It is to prevent every small experiment from becoming a new simulator while still allowing meaningfully different systems to share experimental controls.

A substrate feature should be added because a concrete experiment cannot otherwise be expressed, not because it might be useful someday.

## Running and exploring

For an interactive view, open [`wiki/bench.html`](bench.html). It can configure and run the browser-port of the gated lattice engine, inject faults, snapshot state, and branch counterfactual arms from the same state.

For fixed visual examples, [`wiki/lattice.html`](lattice.html) shows sorting, cellular automata, and perturbation runs.

For exact command-line operation and package layout, use [`goal-discovery/README.md`](../goal-discovery/README.md) and the applicable subtree instructions.

## Designing a new specimen

Prefer the smallest system that can answer the scientific question.

A useful specimen description normally states:

1. **System and boundary** — what is being treated as the system?
2. **Local state and capabilities** — what can each component sense/do?
3. **Mechanism** — what rules, feedback, memory, coupling, or organization produce transitions?
4. **External goal criterion** — what counts as success for the experiment, whether or not anything inside the system represents it?
5. **Challenge** — what initial conditions, perturbations, defects, or environmental changes test the behavior?
6. **Comparators** — what simpler rival mechanism or null could explain the same observation?
7. **Measurements** — what quantities directly answer the question?

Do not add every possible measurement. Record enough to interpret the result and its failure modes.

## Counterfactual comparisons

When comparing an intervention with a control, restore the same underlying state — including random-generator state where relevant — before branching. Similar-looking initial conditions are not sufficient for clean attribution when stochastic trajectories matter.

## Black-box and white-box use

Analyst access is independent of specimen origin.

A system built in this repository may be analyzed blind-first by withholding mechanism and authored intent. Conversely, a system imported from elsewhere may be inspected white-box if the research question is mechanistic.

For a strong Goal Discovery demonstration, a simple information barrier is preferable to elaborate governance: construct the specimen in one context, give the analyst only the allowed observation/intervention interface, collect its inference, then reveal the hidden implementation for audit.

## What not to do

- Do not build a new substrate for every new specimen.
- Do not force every system into a resource-allocation framing or any other previous specimen's vocabulary.
- Do not place the goal inside the substrate just because the experimenter needs a success criterion.
- Do not add UI or infrastructure unless it enables an actual experiment or makes an existing instrument materially usable.
- Do not treat a passing implementation test as evidence for the scientific interpretation.

## Detailed references

Use [substrate design](substrate-design.md) for the design history and unresolved implementation questions, [`roadmap/apparatus.md`](../roadmap/apparatus.md) for the detailed implementation map, and the [reference index](reference/README.md) when investigating why a particular apparatus decision exists.
