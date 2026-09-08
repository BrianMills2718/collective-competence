---
doc-role: working-laboratory-guide
authority: derived
lifecycle: active
sources:
  - substrate-design.md
  - ../roadmap/apparatus.md
  - ../goal-discovery/README.md
  - ../goal-discovery/src/lattice/core.py
  - ../experiments/12-growing-nca/README.md
---
# Dynamical Laboratory

[Wiki home](index.md) · [Current work](current.md) · [Concepts](concepts.md) · [Substrate bench](bench.html)

The Dynamical Laboratory is shared experimental apparatus for both research arms. It exists to make small dynamical systems easy to construct or import, run, observe under controlled access, perturb, compare, and inspect.

It is **apparatus, not the scientific result**.

## Current lattice substrate

The active shared lattice lives under [`goal-discovery/src/lattice/`](../goal-discovery/src/lattice/). It provides local transition rules, experiment-supplied schedules, synchronous or local update patterns, operation accounting, snapshot/restore including random state, and a bounded observation contract.

Its site payload has **two explicit meanings**:

| Mode | Declaration | Site payload means | Current examples |
|---|---|---|---|
| **Entity mode** | `conserving=True` | stable mobile entity identity; every identity has an entity record; per-entity memory/faults apply | self-sorting |
| **Local-state mode** | `conserving=False` | rewritable site state; no entity identity is implied and `entities` is empty | elementary cellular automata, scalar regulation |

The distinction is enforced rather than merely documented: an entity-mode lattice fails if a site names a nonexistent/duplicate identity, and a local-state lattice fails if it carries entity records. Snapshot/restore preserves the mode together with neighbourhood semantics.

The purpose of this shared container is convenience and comparability, **not universality**. If a simple scientific experiment repeatedly requires contorting its natural state into this representation, that is evidence to use another substrate behind the same laboratory discipline rather than to keep generalizing `Lattice`.

## External backends

Phase 2 already uses a different backend. [`experiments/12-growing-nca/`](../experiments/12-growing-nca/) pins the published Growing NCA implementation/weights and runs them through a thin NumPy adapter rather than translating a 2-D neural cellular automaton into `Lattice`. The shared scientific contract is the matched trajectory/intervention/evidence workflow, not one internal state container.

When adopting another external model, prefer a **thin adapter around a pinned upstream implementation**. Preserve provenance, expose the minimum observation/intervention seam needed by the experiment, and avoid forking/retraining merely to make the system easier to interpret.

## What is shared even when substrates differ

The more important laboratory contract is methodological:

- declare the focal system and boundary;
- run a reproducible dynamical system;
- declare what an analyst may observe;
- intervene or perturb in a controlled way;
- compare matched counterfactuals where meaningful;
- record relevant costs/resources;
- preserve native evidence and implementation for later audit.

Different internal representations can satisfy that contract.

## Running and exploring

For an interactive view, open [`wiki/bench.html`](bench.html). It configures and runs the browser-port of the lattice engine, injects faults, snapshots state, and branches counterfactual arms from the same state.

For fixed examples, [`wiki/lattice.html`](lattice.html) shows sorting, cellular automata, and perturbation runs.

For exact command-line operation and package layout, use [`goal-discovery/README.md`](../goal-discovery/README.md) and the applicable subtree instructions.

## Designing a new specimen

Prefer the smallest system that can answer the scientific question. A useful specimen description normally states:

1. **System and boundary** — what is being treated as the system?
2. **Local state and capabilities** — what can each component sense/do?
3. **Mechanism** — what rules, feedback, memory, coupling, or organization produce transitions?
4. **External goal criterion** — what counts as success for the experiment, whether or not anything inside the system represents it?
5. **Challenge** — what initial conditions, perturbations, defects, or environmental changes test the behavior?
6. **Comparators** — what simpler rival mechanism or null could explain the same observation?
7. **Measurements** — what quantities directly answer the question?

Do not add every possible measurement. Record enough to interpret the result and its failure modes.

## Counterfactual comparisons

When comparing an intervention with a control, restore the same underlying state — including random-generator state and declared system semantics where relevant — before branching. Similar-looking initial conditions are not sufficient for clean attribution when stochastic trajectories matter.

## Black-box and white-box use

Analyst access is independent of specimen origin. A system built in this repository may be analyzed blind-first by withholding mechanism and authored intent. Conversely, an imported system may be inspected white-box if the research question is mechanistic.

For a strong Goal Discovery demonstration, prefer a simple information barrier: construct the specimen in one context, give the analyst only the permitted observations/interventions, collect its inference, then reveal implementation for audit.

## What not to do

- Do not build a new substrate for every new specimen.
- Do not force every specimen into the existing lattice when its natural state does not fit.
- Do not force every system into a resource-allocation framing or another previous specimen's vocabulary.
- Do not place the goal inside the substrate just because the experimenter needs a success criterion.
- Do not add UI or infrastructure unless it enables an actual experiment or materially improves an existing instrument.
- Do not treat a passing implementation test as evidence for the scientific interpretation.

## Detailed references

Use [substrate design](substrate-design.md) for design history, [`roadmap/apparatus.md`](../roadmap/apparatus.md) for the detailed implementation map, and the [reference index](reference/README.md) when investigating why a particular apparatus decision exists.
