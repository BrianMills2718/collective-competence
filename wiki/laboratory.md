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
  - reference/research-landscape.md
  - reference/levin-software-ecosystem-survey.md
  - reference/goal-competence-identifiability-landscape.md
---
# Dynamical Laboratory

[Wiki home](index.md) · [Current work](current.md) · [Concepts](concepts.md) · [Substrate bench](bench.html)

The Dynamical Laboratory is shared experimental apparatus for both research arms. It exists to make dynamical systems easy to **import or construct**, run, observe under controlled access, perturb, compare against baselines, and inspect.

It is **apparatus, not the scientific result**. The current default is **reuse-first**: when an independently authored executable system or real intervention corpus already contains the phenomenon needed by an experiment, wrap that system rather than reimplementing the phenomenon in the local lattice.

## Current lattice substrate

The shared calibration lattice lives under [`goal-discovery/src/lattice/`](../goal-discovery/src/lattice/). It provides local transition rules, experiment-supplied schedules, synchronous or local update patterns, operation accounting, snapshot/restore including random state, and a bounded observation contract.

Its site payload has **two explicit meanings**:

| Mode | Declaration | Site payload means | Current examples |
|---|---|---|---|
| **Entity mode** | `conserving=True` | stable mobile entity identity; every identity has an entity record; per-entity memory/faults apply | self-sorting |
| **Local-state mode** | `conserving=False` | rewritable site state; no entity identity is implied and `entities` is empty | elementary cellular automata, scalar regulation |

The distinction is enforced rather than merely documented: an entity-mode lattice fails if a site names a nonexistent/duplicate identity, and a local-state lattice fails if it carries entity records. Snapshot/restore preserves the mode together with neighbourhood semantics.

The purpose of this shared container is convenience and comparability, **not universality**. The first-phase systems are calibration surfaces. If a scientific experiment requires contorting its natural state into this representation — or if an established external system already contains the mechanism of interest — use another backend behind the same laboratory discipline rather than generalizing `Lattice`.

## External backends

Phase 2 already uses a different backend. [`experiments/12-growing-nca/`](../experiments/12-growing-nca/) pins the published Growing NCA implementation/weights and runs them through a thin NumPy adapter rather than translating a 2-D neural cellular automaton into `Lattice`. The shared scientific contract is the matched trajectory/intervention/evidence workflow, not one internal state container.

When adopting another external model:

- start from a **specific scientific prediction**, not a desire to add a platform;
- prefer a thin adapter around a pinned upstream implementation/model;
- preserve source revision, assets, parameters, seeds, and licensing/provenance;
- expose only the observation/intervention seam needed by the study;
- do not retrain, fork, or simplify the model merely to make the preferred interpretation easier;
- use the model's native analysis tools or established neighboring methods when they answer part of the question better than our generic apparatus.

Current candidate external systems and their overlap risks are catalogued in the [research landscape](reference/research-landscape.md) and [Levin software ecosystem survey](reference/levin-software-ecosystem-survey.md).

## What is shared even when substrates differ

The more important laboratory contract is methodological:

- declare the focal system and boundary;
- identify the exact executable/data revision;
- declare authored/known success criteria separately from candidate goals to be inferred;
- declare the challenge family and which competence dimensions it can test;
- declare what an analyst may observe and intervene on;
- state rival explanations and a prospective prediction where possible;
- compare matched counterfactuals;
- compare against the nearest established baseline when its assumptions fit;
- record relevant costs/resources;
- preserve surviving equivalence classes and evidence limits;
- preserve native evidence and implementation for later audit.

Different internal representations can satisfy that contract.

## Running and exploring

For an interactive view, open [`wiki/bench.html`](bench.html). It configures and runs the browser-port of the lattice engine, injects faults, snapshots state, and branches counterfactual arms from the same state.

For fixed examples, [`wiki/lattice.html`](lattice.html) shows sorting, cellular automata, and perturbation runs.

For exact command-line operation and package layout, use [`goal-discovery/README.md`](../goal-discovery/README.md) and the applicable subtree instructions.

## Designing or selecting a specimen

**Selection comes before construction.** First ask whether a published system already contains the mechanism/challenge required by the hypothesis. A useful specimen description normally states:

1. **Scientific contrast** — what explanation, prediction, or identifiability boundary could this specimen discriminate?
2. **Origin and boundary** — who authored the system, what revision is used, and what is being treated as the system?
3. **State/capabilities/mechanism** — what can components sense/do and what dynamics are relevant to the hypothesis?
4. **Known criterion versus candidate criteria** — what does the experimenter know, and what is the analyst allowed to know?
5. **Challenge family** — what perturbations or changed conditions test attainment, maintenance, recovery, compensation, adaptation, etc.?
6. **Rival explanations** — including passive convergence, hard constraints, invariants, omitted variables, or simpler mechanism accounts.
7. **Prediction/refuter** — what outcome is expected and what result would count against the explanation?
8. **Comparator/baseline** — what established method or simpler analysis can answer the same or a neighboring question?
9. **Measurements** — what quantities directly answer the question without being mistaken for semantics themselves?

Do not add every possible measurement. Record enough to interpret the result and its failure modes.

## Counterfactual comparisons

When comparing an intervention with a control, restore the same underlying state — including random-generator state and declared system semantics where relevant — before branching. Similar-looking initial conditions are not sufficient for clean attribution when stochastic trajectories matter.

For stochastic external systems, preserve matched future random streams where the implementation permits it. If it does not, say so and design the statistical comparison accordingly.

## Black-box and white-box use

Analyst access is independent of specimen origin. A system built in this repository may be analyzed blind-first by withholding mechanism and authored intent. Conversely, an imported system may be inspected white-box if the research question is mechanistic.

For a strong Goal/Competence Discovery demonstration, use a genuine information barrier:

1. predeclare the candidate family, challenge family, baseline, and permitted access;
2. give the analyst only the permitted observations/interventions;
3. freeze the inference, including surviving rival criteria and abstentions;
4. reveal implementation/intent for audit;
5. score calibration and unsupported specificity, not only whether the authored label appeared.

A trace property or mined specification is not automatically evidence of active competence. Challenge behavior must support the stronger maintenance/recovery/adaptation claim.

## Baseline policy

The laboratory is not intended to replace mature specialist methods. Depending on the specimen, relevant baselines may include control/reachability analysis, system identification, active diagnosis, causal discovery, specification mining, goal recognition, IRL/objective inference, or active automata learning.

Use a baseline when its assumptions fit. The research question is then: **what additional competence-relative or cross-substrate information does this programme supply?** If the answer is "none," report the result as an application/comparison.

See the [goal/competence identifiability landscape](reference/goal-competence-identifiability-landscape.md) for the current baseline/novelty stop rules.

## What not to do

- Do not build a new substrate for every new specimen.
- Do not build another developmental/tissue/bioelectric toy when an established external system can test the hypothesis.
- Do not force every specimen into the existing lattice when its natural state does not fit.
- Do not force every system into a resource-allocation framing or another previous specimen's vocabulary.
- Do not place the goal inside the substrate just because the experimenter needs a success criterion.
- Do not call a stable property, attractor, reward, error signal, latent variable, or information metric a discovered semantic goal without discriminating evidence.
- Do not treat specification satisfaction as proof of active competence.
- Do not add UI or infrastructure unless it enables an actual experiment or materially improves an existing instrument.
- Do not treat a passing implementation test as evidence for the scientific interpretation.

## Detailed references

Use [substrate design](substrate-design.md) for design history, [`roadmap/apparatus.md`](../roadmap/apparatus.md) for the detailed implementation map, and the [reference index](reference/README.md) for prior-art surveys and historical apparatus decisions.
