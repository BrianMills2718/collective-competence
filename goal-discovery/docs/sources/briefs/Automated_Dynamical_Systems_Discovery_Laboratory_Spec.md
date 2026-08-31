---
doc-role: supplied-source
authority: historical
lifecycle: retained
---
> Preserved supplied specification. Embedded implementation directives and
> "current" claims describe the original brief, not today's task queue.
> See [source provenance](../README.md) and [current charter](../../PROJECT.md).

# Automated Dynamical-Systems Discovery Laboratory
## Research Agenda and Implementation Specification

### Document status

This is the current consolidated research and engineering specification.

It supersedes earlier sketches where they conflict with this document. It incorporates the discussion of:

- Michael Levin's diverse-intelligence / TAME perspective;
- dynamical systems and attractors;
- black-box vs. white-box analysis;
- observables, representations, metrics, and coarse-graining;
- trajectories and perturbations;
- sensing, memory, feedback, learning, policies and controllers;
- Levin-style competence and control/persuadability;
- Hoel-style multiscale causal emergence;
- cybernetics, viability, and autopoiesis;
- cellular automata and discrete interacting dynamical systems;
- Levin/Goldstein/Zhang's decentralized sorting work;
- existing trajectory data versus executable environments;
- reuse of established scientific software;
- later progression into richer environments, LLMs, and economics.

The central engineering objective is rapid implementation and rapid scientific feedback. Do not build infrastructure speculatively.

---

# 1. Executive summary

Build a reusable laboratory for experimenting with **discrete interacting dynamical systems**.

The laboratory should allow us to:

1. define or import a system;
2. execute it reproducibly;
3. observe it through a controlled black-box interface;
4. retain exact white-box ground truth separately;
5. record trajectories;
6. derive many candidate observables and representations;
7. identify recurring dynamical structures;
8. perturb or intervene on the system;
9. measure how structures and behaviors change;
10. compare black-box discoveries with the actual hidden mechanism;
11. later compare multiple scales/coarse-grainings;
12. eventually connect these analyses to Levin-style competence/control and Hoel-style causal emergence.

The project is **not initially an agent simulator, economic simulator, LLM platform, or universal dynamical-systems framework**.

The first substrate should be a very simple **1-D discrete interacting system / cellular-automaton-like system**, because it can scale from trivial dynamics to richer local rules without changing the basic infrastructure.

The key idea is:

> **Build the experimental apparatus once, then progressively increase the complexity of the systems placed inside it.**

---

# 2. What we are ultimately trying to learn

The broad scientific question is:

> **How do useful dynamical structures, control relationships, and forms of competence arise and change as simple systems become internally richer, coupled, and organized across scales?**

A second, more ambitious question is:

> **Under what conditions does a higher-level description of a coupled system become sufficiently predictive, controllable, or causally informative that it is useful to treat the higher-level organization as a distinct system?**

Eventually we want to know whether analogous mechanisms appear in:

- simple deterministic systems;
- adaptive computational systems;
- physical/resource environments;
- collective agents;
- organizations;
- economic systems.

We should not assume in advance that the answer is yes.

---

# 3. The project is driven by valuable answers, not interesting behavior

An experiment is worth doing when its outcome could provide one or more of:

### Measurement

A reliable operational way to detect something currently vague.

### Mechanism

A reproducible mechanism that produces a phenomenon.

### Threshold

A transition point or regime boundary.

### Scaling relationship

A relationship that persists as system size, coupling, environment, or cognition changes.

### Theory discrimination

An experiment in which competing explanations make different predictions.

### Cross-scale result

Evidence that a particular macro representation has a distinct predictive, causal, or control role.

Merely observing:

- cooperation;
- specialization;
- money;
- hierarchy;
- surprising behavior;
- synchronized behavior;

is not automatically a scientific result.

---

# 4. Core methodological stance

Start with trajectories rather than ontology.

We should not begin by assuming:

- the correct system boundary;
- the correct state space;
- the correct coarse-graining;
- the correct goal;
- the existence of a higher-level agent;
- a universal intelligence metric.

Instead:

    observations
       ↓
    candidate observables
       ↓
    candidate representations
       ↓
    dynamical structures
       ↓
    perturbation/intervention
       ↓
    test persistence, prediction and control
       ↓
    compare scales and representations

The same process can also run top-down:

    candidate representation
       ↓
    prediction / intervention test
       ↓
    retain, reject, or modify

Both directions are legitimate.

---

# 5. The central data object is the trajectory

A trajectory is:

    τ = (X_0, X_1, ..., X_T)

or, from the black-box view:

    τ_O = (O_0, O_1, ..., O_T)

The laboratory should treat trajectories as the common currency across environments.

This allows us to ingest:

- our own simulations;
- published experimental traces;
- game logs;
- cellular-automaton runs;
- later Minecraft/Dwarf Fortress traces;
- eventually other empirical data.

Simulation is therefore a **source of trajectories and a way to enable intervention**, not the entire research project.

---

# 6. Black-box and white-box analysis

Every synthetic system provides an unusually valuable separation.

## White-box

The system implementation contains:

- complete authoritative state;
- transition mechanics;
- internal variables;
- topology;
- update schedule;
- parameters;
- hidden random-generator state;
- any controller/policy;
- any hidden memory;
- exact intervention state.

## Black-box

The analyst receives only the configured observation:

    O_t = h(S_t)

plus whatever actions/interventions are intentionally exposed.

The analyst must not receive:

- hidden rules;
- hidden parameters;
- hidden state;
- hidden scheduler state;
- labels saying what mechanism/goal was intended.

## White-box evaluation

After black-box analysis, compare the discovered structure to implementation truth.

Ask:

- Did we recover genuine dependencies?
- Did we mistake passive convergence for active regulation?
- Did we falsely infer memory?
- Did we falsely infer adaptation?
- Did we miss an actual dependency?
- Did the discovered representation identify a useful macro structure?
- Does the implementation explain the observed phenomenon?

Crucially:

> **Implementation truth is ground truth about how the system was generated, not proof that the implementation variables constitute the scientifically best representation of the behavior.**

---

# 7. Add a third layer: analyst hypotheses

The laboratory should explicitly distinguish:

### World

What actually happens.

### Observation

What an analyst is allowed to see.

### Hypothesis

What an analyst proposes might be useful.

A hypothesis can specify:

- candidate observable;
- candidate representation;
- candidate attractor;
- candidate coarse-graining;
- candidate intervention;
- candidate control relation.

This distinction prevents accidentally encoding the desired conclusion into the observation or analysis layer.

---

# 8. Formal system model

Use a flexible model such as:

    S_{t+1} = F(S_t, I_t, E_t)

where:

- S_t = authoritative state;
- F = system transition rule;
- I_t = experimenter intervention;
- E_t = external input/condition.

For systems with an endogenous action-selection mechanism, additionally:

    O_t = h(S_t)

    M_t = g(M_{t-1}, O_t, A_{t-1}, I_t)

    A_t = π(O_t, M_t)

    S_{t+1} = F(S_t, A_t, I_t, E_t)

Do not require explicit actions, policies, memory, or controllers in the initial substrate.

This allows the experimental ladder to introduce those capabilities one by one.

---

# 9. History is not memory

The full observed history:

    H_t = (O_0, A_0, I_0, ..., O_t)

is not the same thing as an agent's internal memory.

Memory should be modeled separately:

    M_t = g(M_{t-1}, O_t, A_t, I_t)

This distinction becomes important when we later ask whether behavior depends on history, and whether the system itself retains and uses historical information.

---

# 10. Vocabulary: use "dynamical structure" as the broad term

Do not force everything into "attractor."

A dynamical structure may include:

- fixed points;
- periodic orbits;
- invariant sets;
- invariant manifolds;
- attracting sets;
- metastable states;
- traveling structures;
- switching regimes;
- recurring spatial patterns;
- chaotic attractors;
- other persistent organization.

An attractor is one important class.

For example:

- a frictionless harmonic oscillator can have invariant periodic orbits;
- a damped oscillator can converge toward a fixed-point attractor.

This distinction matters because not every persistent structure is attracting.

---

# 11. Attractors are representation-dependent objects in practice

An attractor is formally defined in a state/dynamical space, but the representation used by the analyst determines what structure is visible.

The same underlying trajectory may be represented using:

- raw component states;
- total energy;
- center of mass;
- correlation;
- cluster count;
- production rate;
- network connectivity.

Therefore the practical question is not:

> "What is the one true state space?"

but:

> **Which representations make the relevant dynamical structure visible and useful?**

---

# 12. Observables are the primitive analytical material

Suppose we observe:

    X_t = (x_1(t), ..., x_n(t))

We can construct:

    Y_t = f(X_t)

Examples:

- rates;
- ratios;
- differences;
- sums;
- counts;
- averages;
- variances;
- correlations;
- graph statistics;
- entropy;
- path length;
- resource levels.

Do not create a new conceptual category when an ordinary measurement will do.

A rate is simply another observable.

The analytical challenge is selecting/comparing observables and their combinations.

---

# 13. Representation and metric are related but distinct

A representation specifies what variables/objects constitute the coordinates or state description.

A metric specifies how similarity/difference is measured within that representation.

A representation may not even admit a useful conventional metric.

Examples:

- Euclidean distance;
- graph distance;
- edit distance;
- number of violated constraints;
- categorical equality;
- divergence between distributions.

Do not assume every problem space needs a smooth geometric metric.

---

# 14. Coarse-graining

A coarse-graining is a mapping such as:

    Z_t = f(X_t)

It may:

- aggregate entities;
- remove distinctions;
- average variables;
- identify clusters;
- summarize networks;
- aggregate over time;
- encode patterns;
- transform trajectories.

A coarse-graining should be judged by what it helps us do:

- predict;
- compress;
- explain;
- intervene;
- control;
- identify causal structure.

Do not assume that the lower-dimensional or simpler representation is automatically better.

---

# 15. State space, trajectory space, and action space

Treat these as analytical constructs rather than separate foundational ontologies.

### State space

Possible represented states.

### Action space

Possible actions or interventions.

### Trajectory space

Possible sequences through the represented state/action dynamics.

Trajectory space can become combinatorially enormous.

If there are k possible actions over T steps:

    |A^T| ≈ k^T

Therefore do not generally enumerate trajectories.

Use:

- sampling;
- empirical trajectory distributions;
- transition graphs;
- recurrence statistics;
- clustering;
- embeddings;
- entropy/information measures;
- reachability approximations.

---

# 16. The Levin problem-space insight

Do not assume intelligence must be measured in a human-defined physical space.

A problem space can instead be constructed from whatever variables are relevant:

- morphology;
- viability;
- production;
- network structure;
- information;
- resource balance;
- error;
- organization;
- spatial configuration.

The system does not need to represent that space in human terms.

The experimental question is:

> Which space/representation makes stable competence or organization visible?

---

# 17. Goal language should not dominate the first-stage analysis

For low-level experiments, use:

- dynamical structure;
- preferred region;
- invariant structure;
- persistent tendency;
- attractor;
- stable regime.

"Goal" should mainly enter when connecting results to Levin's conceptual framework or when a behavioral interpretation has been independently justified.

The candidate goal-like property should be inferred from behavior rather than simply assigned.

A system may tend toward:

- a point;
- a region;
- a relation;
- a distribution;
- a morphology;
- a dynamical regime;
- a self-maintaining organization.

---

# 18. Candidate goal-directedness

A candidate goal-like tendency is more credible if the system:

1. repeatedly approaches or maintains the same region/property;
2. does so across initial conditions;
3. compensates when the ordinary path is disrupted;
4. can sometimes reach the target through alternative trajectories;
5. retains the tendency under perturbation.

This is not a definition of intelligence. It is an experimental procedure for identifying candidate goal-directed structure.

---

# 19. Levin-style competence

Use existing Levin formulations rather than creating a new definition.

Particularly relevant are:

- achieving ends through different means;
- persistence;
- plasticity;
- memory;
- learning;
- exploration;
- generalization;
- prediction;
- planning;
- problem solving;
- control.

The project's role is to make these testable in artificial systems and compare them across substrates and scales.

---

# 20. Intelligence dimensions are experimental variables, not necessarily levels

Potential capabilities to manipulate independently:

    sensing
    memory
    feedback
    internal state
    prediction
    learning
    exploration
    generalization
    planning
    communication
    policy adaptation
    self-modeling

A system can have one without another.

Do not build a universal intelligence hierarchy unless the literature or experiments justify it.

---

# 21. Controllers and transition rules

Keep these concepts distinct.

### Transition rule

Defines how the system changes:

    X_{t+1} = F(X_t)

### Policy

Maps observations/internal state to actions:

    A_t = π(O_t, M_t)

### Controller

A mechanism organized to influence a dynamical process toward a specified criterion.

A complicated discrete dynamical system may exhibit behavior that is well described by a coarse-grained controller even though its microscopic rules contain no explicit controller object.

This is a particularly interesting possible research target:

> **Can an emergent controller-like description become more useful than the microscopic transition description for prediction or control?**

---

# 22. Control and persuadability

Use the Levin-inspired idea that different systems can have different optimal intervention channels.

Possible intervention classes:

    direct state modification
    parameter modification
    rule/program modification
    setpoint modification
    information input
    training
    communication/persuasion

Measure:

- effect;
- reliability;
- cost;
- information required;
- latency.

The project can compare:

> control OF a system

with:

> control BY a system.

---

# 23. Prediction and control are distinct

A representation can be highly predictive but provide little intervention leverage.

Therefore assess separately:

    predictive usefulness
    control usefulness

This may eventually connect Levin's persuadability ideas with Hoel-style multiscale analysis.

---

# 24. Perturbation is the main causal tool

Support interventions such as:

- initial-condition changes;
- state changes;
- component removal;
- rule changes;
- parameter changes;
- interaction blocking;
- information removal;
- environment changes;
- feedback interruption.

Every perturbation should be logged as an explicit object.

---

# 25. Robustness and adaptation

Do not collapse these.

### Robustness

Performance remains acceptable after disturbance.

### Adaptation

Performance falls and the system changes behavior so that function is restored or improved.

Measure perturbation-response distributions rather than assuming one universal robustness score.

Possible summaries:

- recovery probability;
- recovery time;
- mean post-perturbation performance;
- worst-case performance;
- performance variance.

---

# 26. System stability provides a classical baseline

Use ordinary dynamical-systems concepts before introducing intelligence interpretations:

- equilibrium;
- stability;
- asymptotic stability;
- instability;
- recurrence;
- basin structure;
- periodicity;
- qualitative regime changes.

A system moving toward a stable fixed point is not automatically intelligent.

An important scientific question is when observed behavior goes beyond ordinary passive dynamical convergence and exhibits the kinds of flexible compensation/competence discussed by Levin.

---

# 27. Natural timescales

Many systems have multiple characteristic timescales.

Potential measured ratios include:

- adaptation time / environmental-change time;
- coordination time / system evolution time;
- communication delay / decision time;
- recovery time / disturbance interval.

Do not invent such ratios without evidence. Look for natural scale ratios when the data suggest them.

This is a useful bridge to classical dynamical modeling and eventually to economic feedback analysis.

---

# 28. Cellular automata and the initial substrate

The preferred first substrate is:

> **a discrete interacting dynamical system with local state and explicit transition rules.**

A standard cellular automaton is a particularly constrained case.

A general entity-based discrete system may contain:

- discrete positions;
- heterogeneous entity states;
- local neighborhoods;
- explicit coupling;
- different update schedules;
- persistent internal variables.

The initial substrate should remain simple enough to simulate thousands or millions of times.

---

# 29. Why start with a 1-D discrete system

A 1-D local-rule system provides:

- tiny state;
- cheap execution;
- exact observability;
- deterministic reproducibility;
- arbitrary perturbation;
- easy visualization;
- scalable population size;
- simple rule changes;
- natural coupling.

The important progression is:

    one element
        ↓
    two interacting elements
        ↓
    N interacting elements
        ↓
    richer local rules
        ↓
    persistent state
        ↓
    sensing
        ↓
    feedback
        ↓
    learning

The same infrastructure can support the progression.

---

# 30. Levin's decentralized sorting as a calibration system

The decentralized sorting work is an especially useful reference system because:

- the microscopic rules are understandable;
- local interaction is explicit;
- the global objective is clear;
- perturbation is possible;
- surprising system-level behavior occurs;
- the system is close in spirit to local-rule/discrete dynamical systems.

Do not require the project to replicate the paper's exact implementation before it can move forward.

Instead use it as a calibration point:

> Can generic trajectory/representation/perturbation analysis rediscover the relevant dynamical structures/competencies from trajectories without being told the paper's interpretation?

The system should be described precisely rather than casually labeled a standard cellular automaton.

A useful description is:

> **one-dimensional distributed local-rule discrete dynamical system.**

---

# 31. Existing traces and executable worlds

Both modes should be first-class.

## Trace mode

    existing log
      ↓
    trajectory analysis
      ↓
    candidate representations
      ↓
    candidate structure

## Executable mode

    executable system
      ↓
    trajectory
      ↓
    candidate structure
      ↓
    perturbation/intervention
      ↓
    new trajectory
      ↓
    causal test

This means we can use existing data for discovery before paying the engineering cost of recreating a system.

Executable systems become necessary when controlled interventions matter.

---

# 32. Generated systems

Eventually support constrained families of systems.

Do not begin with arbitrary program generation.

Start with parameterized families:

- size;
- state alphabet;
- neighborhood radius;
- local rule;
- coupling graph;
- update schedule;
- initial conditions.

Then sample within those families.

The purpose is not to create random complexity.

It is to explore whether observed regularities persist across a controlled family of systems.

---

# 33. Randomized system families

When generation is introduced, use:

> **randomization within a known constrained family**

rather than unconstrained random programs.

The experimental question becomes:

- Which dynamical regimes are common?
- Which features predict persistent structure?
- Which perturbation responses are robust?
- Which representations generalize?

This is more useful than simply producing surprising examples.

---

# 34. Null models

Every important claim should have plausible controls.

Examples:

    no coupling
    shuffled trajectories
    altered update schedule
    randomized rule within same family
    removed feedback
    disabled memory
    disabled communication

Use the simplest null model appropriate to the claim.

The question is:

> **How much of the observed phenomenon requires the feature we are claiming causes it?**

---

# 35. Representation discovery should initially be modest

First manually define a handful of sensible observables.

Then compare them.

Only later build automated search over transformations.

Potential future pipeline:

    raw trajectories
        ↓
    candidate observables
        ↓
    candidate combinations
        ↓
    prediction test
        ↓
    perturbation test
        ↓
    causal/control test
        ↓
    ranked representations

Avoid building this search engine before the basic laboratory works.

---

# 36. System identification

Treat system identification as an inverse problem:

Forward:

    known F → trajectories

Inverse:

    trajectories → estimated F

Possible tool:

- PySINDy / discrete system identification.

Use it later to ask:

> How much of the hidden transition structure can be recovered from black-box trajectories?

Compare the recovered model with the actual white-box rule.

Do not make system identification a prerequisite for the first experiments.

---

# 37. Hoel-style causal emergence

After candidate representations exist, introduce multiscale causal analysis.

Potential questions:

- Does a coarse-grained representation retain more useful causal information?
- Does a macro level become more predictive?
- Does a macro level become more controllable?
- Does causal emergence correlate with collective competence?
- Can these quantities diverge?

Potential tool:

- PyMergence.

Do not build a causal-emergence implementation ourselves initially.

---

# 38. Topological analysis

Use GUDHI later when the data suggest topological structure is relevant.

Potential applications:

- trajectory-cloud topology;
- persistent homology;
- state-space topology;
- recurring structures.

This is an analysis adapter, not core infrastructure.

---

# 39. Classical dynamical-systems analysis

Initial Python stack should be:

- NumPy;
- SciPy;
- Matplotlib;
- pandas or Polars;
- scikit-learn where useful.

Potential specialized tools:

- CellPyLib for conventional CA;
- PySINDy for system identification;
- PyMergence for causal-emergence analysis;
- GUDHI for computational topology.

A Julia library such as DynamicalSystems.jl is an excellent reference/optional future tool, but **Julia should not be a mandatory dependency** unless later experiments reveal a capability that Python cannot reasonably replace.

PyDSTool exists but should not be adopted by default as the core dependency given its older ecosystem.

---

# 40. Reuse-before-build rule

Before implementing a scientific capability:

1. search for an existing mature library;
2. inspect papers with usable reference implementations;
3. determine whether an existing tool can be adapted;
4. only build a replacement if necessary.

Prefer:

> mature external component + thin adapter

over:

> internally rebuilt version.

The custom code should concentrate on experimental glue and research-specific measurements.

---

# 41. Proposed software architecture

Keep the custom architecture minimal:

    dynamical_lab/
        core/
            experiment.py
            trajectory.py
            intervention.py
            observation.py

        systems/
            discrete_system.py
            ca.py
            sorting.py

        analysis/
            observables.py
            representations.py
            trajectories.py
            structures.py
            perturbations.py
            control.py

        adapters/
            cellpylib.py
            pysindy.py
            pymergence.py
            gudhi.py

        experiments/
            001/
            002/
            003/

Do not build a second universal simulator.

---

# 42. Minimal system interface

Conceptually:

    reset()
    observe(...)
    step(...)
    snapshot()
    restore(...)

Where possible also:

    intervene(...)

Not every system needs every capability.

The trajectory layer should remain independent of the backend.

---

# 43. Configuration format

Systems should be declaratively configurable.

Example:

```yaml
system:
  family: local_rule_1d
  size: 32

state:
  alphabet: [0, 1]

topology:
  kind: line
  boundary: fixed

rule:
  kind: neighbor_table
  radius: 1

schedule:
  kind: synchronous

initialization:
  kind: seeded_random
  seed: 42

observation:
  expose:
    - local_state
  hidden:
    - rule
    - schedule
```

Keep the schema intentionally small.

Do not turn it into a general-purpose programming language.

---

# 44. Observation configuration

The observation function must be explicit:

    O_t = h(S_t)

This allows systematic experiments in observability.

For the same system, compare:

- full-state observation;
- local observation;
- aggregate observation;
- noisy observation;
- partial observation.

This later becomes relevant to memory, prediction, control, and distributed knowledge.

---

# 45. Update schedules are experimental variables

Support at least eventually:

- synchronous;
- deterministic sequential;
- seeded random sequential;
- block/partial parallel.

The same microscopic rule can produce different macro behavior under different schedules.

This makes schedule itself a potential experimental variable rather than hidden simulator behavior.

---

# 46. Intervention schema

An intervention should explicitly record:

- target;
- type;
- magnitude;
- timing;
- duration;
- cost;
- pre-intervention state;
- post-intervention state;
- result.

Interventions can include:

    change state
    remove component
    alter rule
    alter parameter
    remove information
    block interaction
    change schedule
    alter environment

This becomes the basis for later causal/control analysis.

---

# 47. Experimental repeatability

Every run must record:

- system family/version;
- configuration;
- seed;
- observation configuration;
- intervention configuration;
- agent/controller version if applicable;
- code version;
- analysis version.

A result should be regenerable from stored configuration plus versioned code.

---

# 48. Independent experiment definitions, shared infrastructure

The correct interpretation of "rebuild experiments" is:

> **Do not make every experiment a dependency on the accumulated history of the project.**

But:

> **Do build shared experimental infrastructure once.**

Each experiment should be independently understandable and rerunnable while using the same laboratory interfaces.

---

# 49. Thin-slice implementation sequence

## Slice 0 — One trivial discrete system

Create a 1-D discrete state system with one element and a deterministic periodic rule.

Demonstrate:

- execution;
- trajectory logging;
- reproducibility;
- basic visualization.

## Slice 1 — Two coupled elements

Add local coupling.

Compare:

- uncoupled;
- coupled.

## Slice 2 — N elements

Generalize to a 1-D array.

Add local neighborhoods.

## Slice 3 — Perturbation

Add state and rule perturbations.

Record branches from exact snapshots.

## Slice 4 — Candidate observables

Add a small number of derived observables.

## Slice 5 — Dynamical structure analysis

Detect:

- periodicity;
- recurrence;
- fixed/periodic configurations;
- obvious persistent structures.

## Slice 6 — Levin sorting

Add the decentralized sorting system as a calibration system.

## Slice 7 — Black-box/white-box evaluation

Hide the rules from the analysis layer and compare discoveries against implementation truth.

## Slice 8 — Representation comparison

Compare alternative observables/coarse-grainings.

## Slice 9 — Perturbation/recovery

Measure persistence, recovery, and alternative trajectories.

## Slice 10 — System identification

Test PySINDy or equivalent against known systems.

## Slice 11 — Hoel analysis

Add PyMergence where the representation is suitable.

## Slice 12 — Topology

Add GUDHI only where justified.

## Slice 13 — Sensing/memory/feedback

Introduce these one at a time.

## Slice 14 — Adaptation/learning

Again, one capability at a time.

## Slice 15 — Richer environments

Only now consider Crafter, MiniHack, Minecraft, Dwarf Fortress, etc.

## Slice 16 — LLM agents

Only when there is an established measurement problem worth testing with richer cognition.

## Slice 17 — Economics

Only when earlier experiments establish a useful general phenomenon.

---

# 50. Intelligence/cognition progression

When ready to add richer systems, use approximately:

    local dynamics
        ↓
    sensing
        ↓
    persistent internal state
        ↓
    memory
        ↓
    feedback
        ↓
    prediction
        ↓
    adaptive policy
        ↓
    learning
        ↓
    collective coordination
        ↓
    LLM cognition

This is an experimental progression, not a claim that these are universal stages of intelligence.

---

# 51. What we should look for in trajectories

Possible features include:

### Persistence

A structure remains present.

### Convergence

The system approaches a recurring region.

### Recovery

The system returns after perturbation.

### Alternative pathways

Different trajectories reach similar outcomes.

### Flexible compensation

Blocking one route induces another.

### Temporal dependence

Behavior depends on historical state.

### Prediction-like behavior

Behavior depends on information about future consequences.

### Reorganization

The system changes its dynamical organization following perturbation.

### Collective structure

Coupling produces persistent macro-level organization.

No single feature should automatically be interpreted as intelligence.

---

# 52. System boundary as an empirical object

A proposed system boundary should be evaluated by whether it exposes:

- stable regularities;
- predictive power;
- control leverage;
- causal usefulness;
- persistent organization.

Possible progression:

    arbitrary grouping
        ↓
    descriptive boundary
        ↓
    predictively useful boundary
        ↓
    causally useful boundary
        ↓
    control-useful boundary
        ↓
    candidate higher-level system

Do not assume the final step is always reached.

---

# 53. Higher-level organization

If a collection of components exhibits persistent macro behavior, ask:

- Is the macrostate predictive?
- Is it robust?
- Does it survive member replacement?
- Does structural perturbation break it?
- Does macro-level intervention have leverage?
- Is the macro representation more compact/informative?
- Does it correspond to a different causal organization?

A group should not be called an agent merely because it was convenient to draw a box around it.

---

# 54. Component replacement

A particularly useful eventual intervention:

    collective A + B + C

Replace:

    B → B'

while preserving relevant structural conditions.

Ask:

- Does the collective function persist?
- Which properties are preserved?
- Which disappear?
- Is function tied to the component or to the organization?

This can reveal where system-level properties reside.

---

# 55. Viability and autopoiesis

Keep these separate from generic goal-directedness.

Measure:

- persistence of the system boundary;
- survival;
- maintenance of organization;
- recovery;
- continued functional operation.

A system can show strong directional behavior while reducing its own viability.

Autopoiesis becomes relevant when the processes constituting a system recursively contribute to producing/maintaining the organization that defines it.

Do not equate:

    intelligence = self-preservation = autopoiesis.

---

# 56. A note on the "everything has intelligence/goals" perspective

The project can accommodate a very broad Levin-style view in which goal-directed competence is potentially found across many scales and substrates.

But universal attribution is not by itself informative.

The scientifically useful questions are:

- What tendency?
- In what problem space?
- At what scale?
- How stable?
- How reproducible?
- How perturbation-resistant?
- What control channel works?
- Does the tendency preserve the system itself?
- Does the representation improve prediction/control?

"Everything has some degree of goal-directedness" can therefore function as a **research-generating premise**, not as the output of every experiment.

---

# 57. Nonstationarity

Once systems can learn, adapt, construct tools, or alter their environment:

    F_t ≠ F_{t+1}

may hold.

The environment itself can become part of the adaptive process.

This is likely important later for:

- technology;
- capital;
- institutions;
- learning;
- economics.

Do not build for full nonstationarity initially.

---

# 58. Technology as transition-structure modification

An important eventual concept is that a system need not merely navigate a fixed state space.

It can modify its future transition structure.

Examples conceptually:

    tool
      ↓
    new action
      ↓
    new reachable trajectories
      ↓
    environment altered
      ↓
    further actions become possible

This is potentially a more precise version of "state-space warping":

> **a system changes the structure of its future controllability.**

This will become important for capital, infrastructure, organizations, and economics.

---

# 59. Economic application

Economics should be deferred until the foundational experiments provide useful measurement.

Later candidate questions:

### Specialization

Does distributing limited capability across coupled components expand collective effective capability?

### Dispersed knowledge

When does decentralized information outperform centralized coordination?

### Prices

When does a compressed signal improve decentralized control under dispersed information?

### Money

Under what conditions does a generalized coordination medium change effective action/reachability?

### Firms

When does persistent internal coordination outperform repeated external exchange?

### Institutions

When do recurring interactions become structures that alter future transitions?

### Cycles

How do expectations, delays, and feedback generate stability or instability?

---

# 60. Why not start with economics

A manually constructed example such as:

    A gathers wood
    B gathers ore
    wood + ore → shelter

already encodes most of the economic structure we are supposedly trying to discover.

Early experiments should therefore avoid semantic economic scaffolding.

Let the substrate generate the dynamics.

---

# 61. Why not start with LLMs

LLMs introduce substantial confounding:

- pretrained world knowledge;
- hidden priors;
- prompt effects;
- model-specific reasoning;
- language-mediated behavior;
- difficult-to-control memory;
- potentially opaque internal representations.

They are useful later because they provide a way to vary cognitive richness while holding the environment/measurement apparatus approximately constant.

They should not be the starting point.

---

# 62. Why games may eventually outperform "research-grade" environments

A mature game engine may provide:

- richer physics;
- more interactions;
- persistent state;
- more edge cases;
- better-tested world dynamics;
- enormous existing tooling.

Therefore environment selection should optimize:

> useful existing complexity / engineering required

rather than:

> academic appearance of the environment.

Potential later environments include:

- Crafter;
- MiniHack;
- Minecraft/MineDojo;
- Dwarf Fortress/DFHack.

Different environments can answer different questions.

---

# 63. Environment portfolio, not a single canonical world

The project should eventually maintain adapters rather than forcing all experiments into one world.

Possible categories:

    abstract coordination
        → OpenSpiel / PettingZoo

    ABM
        → NetLogo / Mesa / Agents.jl

    compact rich worlds
        → Crafter / MiniHack

    rich physical/resource worlds
        → Minecraft / Dwarf Fortress

    specialized economics
        → economic simulation tooling

The common object remains the trajectory plus experiment/intervention metadata.

---

# 64. The research matrix

The important experimental axes are largely independent.

### Environment

    simple
      →
    rich

### Cognitive capability

    reactive
      →
    adaptive / model-mediated
      →
    LLM

### Coupling

    independent
      →
    interacting
      →
    persistently coupled
      →
    organized collective

An experiment can vary one axis while holding others constant.

This is preferable to a single linear "intelligence ladder."

---

# 65. Suggested early experimental matrix

A minimal first set:

| Experiment | Environment | Dynamics | Coupling | Purpose |
|---|---|---|---|---|
| 0 | 1-D discrete | deterministic | none | establish trajectory machinery |
| 1 | 1-D discrete | deterministic | local | detect coupling effects |
| 2 | 1-D discrete | deterministic | local | perturbation/recovery |
| 3 | 1-D discrete | deterministic | local | representation comparison |
| 4 | Levin sorting | deterministic | distributed | calibration |
| 5 | simple adaptive rule system | stateful | local | memory/feedback |
| 6 | same | adaptive | local | learning |
| 7 | compact rich world | richer | local/multi-agent | environment stress test |

Only proceed when each stage produces useful feedback.

---

# 66. What would count as a successful first round

Not a discovery about consciousness.

Not an economy.

Not AGI.

Not an intelligence score.

A successful first round demonstrates:

1. a tiny discrete system can run reproducibly;
2. trajectories can be captured;
3. black-box observations can be separated from white-box mechanics;
4. interventions can branch from exact snapshots;
5. simple observables can produce useful representations;
6. known dynamical structures can be identified;
7. analysis can compare representations;
8. Levin-like calibration behavior can be examined without hard-coding its interpretation.

That is enough to justify the next slice.

---

# 67. Potentially strong future scientific results

Examples include:

> A particular representation reliably exposes a stable macro-dynamical structure across many microscopic systems.

> A specific coupling regime produces a reproducible increase in collective competence.

> There is a threshold in information/cognitive capacity beyond which a different organizational regime emerges.

> A macro representation becomes more causally informative and more controllable than the micro description.

> A Levin-style competence measure correlates with a particular property of the trajectory distribution.

> Causal emergence and agency increase together—or systematically diverge.

> Similar organizational transitions appear across radically different computational substrates.

Any such finding should be tested across independent systems and, ideally, independently reproduced.

---

# 68. Falsification / null outcomes

The project must allow conclusions such as:

- coupling has no meaningful effect;
- richer cognition adds little;
- macro descriptions are not causally superior;
- causal emergence does not correlate with competence;
- apparent intelligence is explained by passive dynamics;
- perturbation resilience is entirely due to redundancy;
- a candidate system boundary is unstable;
- a proposed representation fails to generalize.

These are valid scientific outcomes.

Do not add complexity merely to manufacture a positive result.

---

# 69. Final implementation rule

At every step:

> **What valuable answer could this experiment produce?**

Then:

> **What is the smallest existing system capable of answering it?**

Then:

> **What existing libraries already provide the required machinery?**

Then:

> **What is the minimum new code we need?**

Only after the experiment produces useful information should the next layer be added.

---

# 70. Immediate task for the coding agent

Implement **Slice 0 only**.

### Requirements

Create a minimal 1-D discrete dynamical-system substrate.

It should:

- contain one or more discrete elements;
- apply an explicit deterministic transition rule;
- execute for T steps;
- support a seed/configuration;
- record a trajectory;
- expose observations;
- preserve hidden white-box configuration separately;
- render a simple trajectory visualization;
- support exact snapshot/restore.

Then write one small experiment demonstrating:

    reset
    → run
    → snapshot
    → perturb initial state
    → restore
    → rerun

The implementation should be small enough that the entire system can be understood in one sitting.

Do not implement:

- automatic rule generation;
- LLMs;
- memory;
- learning;
- economics;
- agent frameworks;
- PyMergence;
- GUDHI;
- automatic representation discovery;
- generalized causal inference.

Those are later slices.

---

# 71. Definition of done for Slice 0

The agent should be able to show:

1. one deterministic system;
2. two runs with identical configuration produce identical trajectories;
3. a changed initial state produces a different trajectory;
4. a restored snapshot reproduces the same continuation exactly;
5. black-box observations do not contain hidden rule/configuration data;
6. white-box configuration remains available to the evaluator;
7. the trajectory can be exported in a simple machine-readable form;
8. a basic visualization is generated.

Only then proceed to Slice 1.

---

# 72. Guiding principle

The intended system is not:

> **a giant artificial civilization simulator.**

It is:

> **a reusable experimental instrument for taking dynamical systems, observing them at chosen resolutions, perturbing them, and discovering which representations and scales make their organization, competence, and control most legible.**

The project should grow by **thin slices**.

The desired progression is:

    simple discrete dynamics
       ↓
    coupling
       ↓
    perturbation
       ↓
    representation
       ↓
    dynamical structure
       ↓
    Levin-style competence
       ↓
    control
       ↓
    multiscale analysis
       ↓
    richer cognition
       ↓
    richer environments
       ↓
    collective organization
       ↓
    economics

Each stage is optional and conditional on the scientific value of the previous stage.

The core asset is not the simulator.

The core asset is the **ability to run and analyze controlled experiments quickly, compare black-box behavior against known mechanisms, and progressively determine which representations, scales, and intervention strategies genuinely reveal something about complex organization.**
