---
doc-role: supplied-source
authority: historical
lifecycle: retained
---
> Preserved supplied specification. Embedded implementation directives and
> "current" claims describe the original brief, not today's task queue.
> See [source provenance](../README.md) and [current charter](../../PROJECT.md).

# Addendum 3 — A Robinson-Crusoe Construction of Dynamical Systems, Intelligence, and Organization

## Purpose

This addendum develops the research program after the previous addendum, without re-stating material already established there except where later discussion changes its interpretation.

The central new idea is to use a **Robinson-Crusoe-style construction** as a way of organizing the theory.

The aim is not merely pedagogical in the sense of making the reader discover concepts. It is to construct a sequence of increasingly rich models in a new domain, analogous to the way economics uses Robinson Crusoe:

- begin with the smallest useful model;
- add one important primitive or relationship at a time;
- use each resulting model as a reusable mental model for reasoning about more complicated cases;
- carry the same machinery forward rather than replacing the model at every stage.

The resulting construction is intended to provide a common way of thinking about:

- dynamical systems;
- cybernetics;
- diverse intelligence;
- collective organization;
- multiscale systems;
- and eventually economic phenomena.

The computational implementation should mirror this philosophy: **one reusable experimental substrate, progressively richer systems, thin slices, and maximum reuse of existing tooling.**

---

# 1. What the “Robinson Crusoe” analogy means here

The analogy is methodological rather than literary.

In economics, a simple Crusoe model gives a compact mental model for production, scarcity, choice, capital, and so forth. Additional people, trade, specialization, institutions, money, and firms can then be introduced without abandoning the earlier model.

The corresponding strategy here is:

> **Construct a minimal dynamical system, then progressively introduce the properties that make richer forms of control, adaptation, coupling, and organization possible.**

The purpose is not to claim that actual history proceeds through these stages in this order.

The purpose is to obtain a **portable reasoning framework**.

A later real system should be recognizable as a composition of mechanisms already encountered in simpler models.

---

# 2. The underlying primitive should initially be a discrete interacting dynamical system

The first computational substrate should not be “an agent.”

It should be something more general:

> **a discrete interacting dynamical system consisting of entities/components occupying a state and changing according to explicit transition rules.**

A generic form is:

\[
X_{t+1}=F(X_t,u_t)
\]

where:

- \(X_t\) is the complete system state;
- \(F\) is the transition rule;
- \(u_t\) represents optional interventions/inputs.

At a lower level:

\[
x_i(t+1)=f_i(x_i(t),N_i(t))
\]

where \(N_i\) is the local neighborhood/interacting set of component \(i\).

This umbrella includes:

- cellular automata;
- lattice dynamical systems;
- particle-like discrete systems;
- network dynamical systems;
- distributed algorithms;
- agent-based systems.

An “agent” can therefore be introduced later as a component with additional properties rather than being assumed at the foundation.

---

# 3. Why a cellular-automaton-like substrate is attractive

The initial substrate should be as simple as possible while retaining:

- discrete state;
- local interaction;
- repeated transition;
- persistent structure;
- easy perturbation;
- cheap simulation;
- easy visualization;
- exact reproducibility.

A one-dimensional lattice is an especially useful starting point.

For example:

\[
x_i(t)\in\{0,1\}
\]

with local update rules.

The first systems can be nearly trivial.

The important feature is not sophistication but **continuity of the experimental substrate**.

The same basic machinery should eventually be able to support:

\[
\text{simple local rules}
\rightarrow
\text{richer local rules}
\rightarrow
\text{distributed sorting}
\rightarrow
\text{stateful components}
\rightarrow
\text{adaptive components}
\rightarrow
\text{coupled systems}.
\]

---

# 4. The Levin sorting system should be understood as a nearby member of this family

The Levin/Goldstein/Zhang sorting work is not simply a textbook cellular automaton.

Its components are cells/elements with persistent values and local sorting policies, and the distributed versions of sorting algorithms produce global sorting through local interaction.

A precise working description is:

> **one-dimensional discrete interacting dynamical system with local rules and distributed updating.**

Calling it “CA-like” is useful because the important structural pattern is:

\[
\text{local state}
+
\text{local rule}
+
\text{local interaction}
+
\text{repeated updating}
\rightarrow
\text{global dynamics}.
\]

This is exactly the type of substrate we want for early experiments.

---

# 5. Dynamical structure comes before “intelligence”

The default language at the lowest level should be **dynamical structure**, not goal.

Relevant structures include:

- fixed points;
- periodic orbits;
- invariant sets/manifolds;
- attracting sets;
- metastable states;
- traveling structures;
- chaotic attractors;
- persistent organizational patterns.

An attractor is one class of dynamical structure, not the universal term for all of them.

This matters because some systems exhibit persistent cycles or invariant trajectories rather than convergence toward a point.

---

# 6. Attractors as a less anthropomorphic language for “goals”

The term “goal” should be used cautiously at the low-level dynamical stage because it imports connotations that are unnecessary for the first experiments.

A better progression is:

\[
\text{dynamical structure}
\rightarrow
\text{persistent tendency}
\rightarrow
\text{attracting/preferred structure}
\rightarrow
\text{goal-directed interpretation where justified}.
\]

A goal-like interpretation should therefore be earned by the behavior of the system rather than inserted into the implementation.

A candidate target need not be a point. It could be:

- a region;
- a relation;
- a distribution;
- a morphology;
- a dynamical regime;
- a persistent organizational property.

---

# 7. The system can be analyzed from two sides simultaneously

Because we control the artificial systems, each experiment can expose an unusual methodological advantage.

## Black-box level

Restrict analysis to observables and trajectories.

Ask:

- What structure can be inferred?
- What regularities recur?
- What representations expose those regularities?
- What apparent attractors or persistent structures exist?
- What happens under perturbation?

## White-box level

Use the complete system specification:

- state representation;
- transition rules;
- topology;
- coupling;
- parameters;
- initial conditions;
- internal state;
- controller/policy.

Ask:

- What mechanism actually generated the observed behavior?
- Did the black-box analysis recover it?
- What information was invisible in the external observations?
- What does the ground truth reveal about competing explanations?

The two analyses should remain separable.

This lets us study **system identification and representation discovery against known ground truth**.

---

# 8. “A system” is a candidate boundary, not an unquestionable object

Everything of interest can be represented at more than one level.

A researcher may inspect:

- an individual component;
- a local cluster;
- the whole array;
- a network subgraph;
- a collective;
- a larger environment.

The relevant question is not:

> Is this boundary metaphysically the real system?

It is:

> **Does this boundary produce a stable and useful representation for the purpose at hand?**

Useful means potentially:

- predictive;
- explanatory;
- causally informative;
- controllable.

This gives a direct connection to multiscale analysis.

---

# 9. Representation should be understood as a transformation of observables

The basic empirical material is a stream of observations:

\[
X_t.
\]

Candidate representations are transformations:

\[
Y_t=f(X_t).
\]

The transformations can be mundane:

- rates;
- differences;
- sums;
- averages;
- ratios;
- counts;
- categorical summaries;
- graph statistics;
- temporal statistics.

A production rate is simply another derived observable.

No new theoretical object is required just because a rate becomes useful as a state variable.

The scientific problem is:

> **Which combinations and transformations of observables expose stable structure?**

---

# 10. This creates a two-directional coarse-graining program

## Bottom-up

Start from relatively fine-grained observations.

\[
X \rightarrow f_1(X),f_2(X),f_3(X),...
\]

Search for representations with useful regularities.

## Top-down

Start with a hypothesized macro variable or coarse-graining.

\[
X\rightarrow Y
\]

and test whether it improves:

- prediction;
- compression;
- causal analysis;
- control.

The two should interact.

A coarse-graining is useful if it earns its status through performance in a clearly stated task rather than because it merely “looks intuitive.”

---

# 11. The entropy/information analogy

The project should exploit the fact that information theory already gives ordinary tools for characterizing distributions.

For trajectories:

\[
P(\tau)
\]

one can measure things such as:

- entropy;
- concentration;
- mutual information;
- conditional dependence;
- divergence between trajectory distributions.

This may become useful for comparing:

- rigid behavior;
- random exploration;
- flexible but structured behavior.

However, the initial project should not equate intelligence with entropy or invent a bespoke “intelligence entropy.”

The role of information measures is to characterize structure in the observed data.

---

# 12. Trajectory space should usually be implicit

Trajectory spaces become combinatorially enormous.

For \(k\) actions over \(T\) steps:

\[
|\mathcal{T}|\approx k^T.
\]

With many interacting entities, this rapidly becomes much larger.

Therefore do not attempt general trajectory enumeration.

Instead use:

- sampled trajectories;
- empirical distributions;
- recurrence;
- clustering;
- embeddings;
- transition graphs;
- information measures;
- reachability approximations.

Treat trajectory space primarily as an implicit object.

---

# 13. Trajectory space is complementary to state space

State-space analysis asks:

> What states or regions can the system occupy?

Trajectory analysis asks:

> What paths through those states does the system select?

Two systems can share the same reachable states while differing substantially in:

- path flexibility;
- temporal horizon;
- robustness;
- efficiency;
- anticipation;
- ability to recover after disruption.

A useful concept for later work is therefore the set:

\[
\mathcal{T}(G)
=
\{\tau:\tau\text{ reaches or maintains }G\}.
\]

The structure of successful trajectories may be more informative about competence than raw state-space size.

---

# 14. Reachability, efficiency, and flexibility must remain distinct

If two systems reach the same endpoint, one may simply be faster.

Alternatively, coupling may make previously impractical states reachable.

Or an intervention may genuinely change the physically possible state space.

These are different results.

The initial measurement layer should therefore distinguish:

- physical possibility;
- effective/practical reachability;
- efficiency;
- trajectory flexibility.

---

# 15. Perturbation is the primary way to reveal organization

Simply observing normal trajectories is insufficient for many questions.

After identifying a recurring structure, intervene:

- change initial conditions;
- remove a component;
- alter a rule;
- block a path;
- change an interaction;
- remove information;
- change parameters;
- alter the external environment.

Then observe the response.

This makes it possible to distinguish:

> a pattern that happens to occur

from:

> an organized process that persistently compensates for disturbance.

---

# 16. Robustness is performance across perturbations

Let \(M\) be a performance/structure metric and \(p\) a perturbation.

Then:

\[
M_p=M(\tau_p).
\]

Robustness can be summarized using:

- mean performance;
- failure probability;
- recovery probability;
- variance;
- worst-case performance;
- distance from baseline.

No universal scalar is required.

---

# 17. Adaptation is different from robustness

A system may withstand a perturbation without changing its behavior.

Another may:

\[
\text{perturbation}
\rightarrow
\text{performance loss}
\rightarrow
\text{reorganization}
\rightarrow
\text{recovery}.
\]

Those are different mechanisms.

Later experiments should therefore distinguish:

- persistence;
- resistance;
- recovery;
- reorganization;
- adaptation.

---

# 18. Levin-style competence should be operationalized from existing work

The project should not invent a new definition of competence without first checking the Levin literature.

A particularly important Levinian theme is the ability to achieve an outcome through different means and to maintain behavior across perturbations.

The relevant research operation is therefore:

> **Identify the target-like dynamical regularity from behavior, perturb the normal route, and examine whether the system can compensate through another route.**

This can be studied without assuming consciousness or a human-like explicit objective.

---

# 19. Intelligence should be represented as a multidimensional capability profile

The project should not force all systems onto a single intelligence number.

Potential dimensions include:

- sensing;
- persistence;
- memory;
- prediction;
- plasticity;
- learning;
- exploration;
- generalization;
- planning;
- problem solving;
- communication;
- adaptation;
- goal modification.

These should be treated as experimentally variable properties.

For example:

\[
\text{base rule}
\rightarrow
+\text{memory}
\rightarrow
+\text{learning}
\]

allows us to compare what each capability contributes.

---

# 20. Memory is an experimental capability, not the definition of intelligence

A system with retained state has access to information not contained in the instantaneous observation.

That may permit:

- temporal discrimination;
- longer horizons;
- state-dependent control;
- adaptation.

But memory should not automatically be equated with a world model, intelligence, or agency.

It is one capability to manipulate experimentally.

---

# 21. The “internal model” question should remain modest

Do not require a mechanism to contain an explicitly separable “world model” before considering it intelligent.

Instead test:

> **Does the system's behavior depend on information about possible/non-current states or transitions?**

Evidence for such dependence can be obtained behaviorally.

Only later should we ask what mechanism stores that predictive information:

- explicit model;
- recurrent state;
- distributed dynamics;
- learned representation.

This avoids turning an interpretive label into an experimental assumption.

---

# 22. Controller, policy, and transition rule should remain distinct

Use:

### Transition rule

\[
X_{t+1}=F(X_t)
\]

for the basic system dynamics.

### Policy

\[
a_t=\pi(o_t,m_t)
\]

for an action-selection process.

### Controller

A policy/mechanism explicitly organized around influencing a system toward a criterion.

This terminology allows a useful later question:

> **Can a complicated discrete dynamical system acquire a coarse-grained representation in which controller-like behavior becomes a useful description, even though the microscopic implementation contains only local transition rules?**

That is a natural bridge between classical dynamical systems, cybernetics, Levin, and Hoel.

---

# 23. Control is also an empirical way to evaluate representations

A representation may predict well without providing useful control.

Conversely, a representation may support a particularly effective intervention.

Therefore evaluate candidate representations on separate axes:

\[
\text{prediction}
\]

\[
\text{causal informativeness}
\]

\[
\text{control effectiveness}.
\]

A coarse-graining that is useful for one purpose need not be optimal for another.

---

# 24. Levin's persuadability/control idea belongs here

Different systems may have different effective control channels.

Conceptually:

- physical intervention;
- parameter/setpoint intervention;
- program/rule modification;
- training;
- information provision;
- communication/persuasion.

The laboratory can compare:

> **Which intervention type produces a desired change, at what cost, and through what information channel?**

This is more informative than simply asking whether the system can be controlled.

It also provides another reason for categorizing intelligence/cognitive capabilities.

---

# 25. System boundary and control scale may interact

A candidate macro system becomes more interesting if:

> intervention at its scale provides meaningful leverage over its behavior.

For example, if manipulating one aggregate variable reliably changes the future of a large collection, while equivalent component-level manipulation is difficult, the aggregate representation may be useful as a control level.

This is a testable property, not a metaphysical claim about whether the aggregate “really exists.”

---

# 26. Hoel becomes most relevant once candidate representations exist

The project should not begin by forcing every experiment through causal-emergence machinery.

Instead:

\[
X\rightarrow Y=f(X)
\]

should first produce candidate representations that appear meaningful.

Then use causal-emergence tools to ask whether a macro scale has:

- distinct causal structure;
- improved causal informativeness;
- useful information-preserving properties.

PyMergence is the primary existing tool to investigate here.

---

# 27. GUDHI and topology

GUDHI should be an optional later analysis layer.

Potential uses:

- persistent homology;
- topological structure of trajectory clouds;
- topology of state/phase-space representations;
- identifying persistent holes/components/features.

Do not make topology a first-round dependency.

---

# 28. Classical dynamical-systems toolkit

Use existing numerical/mathematical libraries wherever possible.

Python-first preferred stack:

- NumPy;
- SciPy;
- Matplotlib;
- pandas or Polars;
- scikit-learn where useful.

For discrete dynamical-system/model-discovery work:

- PySINDy, particularly its discrete-system functionality and system-identification tools.

PySINDy should be treated as an analysis/model-discovery tool, not as a required simulator.

A Julia-based stack such as DynamicalSystems.jl is highly capable, especially for discrete dynamical systems, but should remain optional rather than introducing a Julia dependency prematurely.

The principle is:

> **Prefer the strongest sufficiently good Python tool over adding a second language unless the added capability is genuinely needed.**

---

# 29. Discrete-system / cellular-automaton substrate

The initial substrate should be extremely simple.

Preferred abstraction:

> discrete interacting dynamical system

rather than:

> agent-based model

or:

> cellular automaton

The hierarchy is:

    discrete dynamical system
        ├── cellular automaton
        ├── lattice dynamical system
        ├── particle/element system
        ├── network dynamical system
        └── agent-based system

For standard cellular automata, consider CellPyLib or comparable established libraries rather than writing a CA engine.

The research-specific code should sit above the substrate.

---

# 30. Why cellular automata are attractive

A CA-like substrate gives us:

- discrete time;
- discrete states;
- local rules;
- deterministic execution;
- easy perturbations;
- cheap runs;
- easy visualization;
- scalable system size;
- easy rule modification.

It also supports a natural progression:

    1 component
        ↓
    2 components
        ↓
    many components
        ↓
    local interaction
        ↓
    persistent patterns
        ↓
    sensing
        ↓
    memory
        ↓
    feedback
        ↓
    learning
        ↓
    adaptive collective behavior

The Levin sorting system is not a canonical textbook cellular automaton, but it is close in spirit: distributed local state + local interaction/update rules + repeated execution producing global organization.

Use the more precise description:

> one-dimensional discrete interacting dynamical system

or:

> distributed local-rule dynamical system.

---

# 31. The Levin sorting system as a calibration experiment

The sorting paper is important because the system is sufficiently simple to understand exactly while producing behavior the authors interpret as unexpected competence.

The system consists of locally acting elements/cells with local sorting rules; distributed versions of bubble, insertion, and selection sort are studied, including perturbation/damage scenarios and behaviors such as temporarily moving away from sortedness to navigate obstacles.

Use it as a calibration target.

Do not treat reproduction of its behavior as the main scientific contribution.

Instead ask:

> Can generic trajectory/representation/perturbation analysis rediscover the relevant structure without being told the authors' interpretation?

---

# 32. Existing traces and executable experiments are two complementary modes

There are two modes.

## Trace mode

Use existing trajectories/logs.

This supports:

- exploratory representation discovery;
- pattern detection;
- statistical characterization;
- candidate coarse-graining.

Examples could eventually include:

- cellular automata;
- published sorting experiments;
- game logs;
- Minecraft trajectories;
- biological data;
- other externally generated datasets.

## Executable mode

Run the underlying system.

Needed for:

- intervention;
- controlled perturbation;
- matched counterfactuals;
- parameter manipulation;
- repeated identical conditions.

The ideal workflow is:

    existing trace
        ↓
    candidate hypothesis
        ↓
    executable reproduction
        ↓
    intervention

This makes simulation a tool for causal testing rather than an end in itself.

---

# 33. The “one infrastructure, many systems” principle

The implementation should use one reusable experimental layer and make individual systems pluggable.

The common interface should be thin:

```python
reset()
observe()
step(...)
snapshot()
restore()
intervene(...)
```

Not every backend must implement every method.

The common object is the trajectory, plus metadata.

---

# 34. Common trajectory format

At minimum retain:

- experiment identifier;
- system/backend;
- version;
- configuration;
- seed;
- timestep;
- observables;
- actions, when applicable;
- interventions;
- outcomes.

White-box specification should remain available separately.

This makes it possible to run identical analysis under restricted and unrestricted information.

---

# 35. Reproducibility

Every run should record:

- code version;
- environment/version;
- seed;
- configuration;
- rule/policy;
- intervention schedule;
- measurement configuration.

Experiments should be rerunnable from a clean environment.

The research layer should not rely on hidden mutable state.

---

# 36. The Robinson-Crusoe construction should culminate in a reusable chain of mental models

A plausible sequence is:

### Model 1 — Dynamical state

A system has state and transition.

### Model 2 — Dynamical structure

Repeated transition creates fixed points, cycles, invariant structures, attractors, etc.

### Model 3 — Perturbation

System behavior is characterized by its response to disturbance.

### Model 4 — Observation

A system can act on a limited observation rather than full objective state.

### Model 5 — Feedback/control

Actions modify future system state.

### Model 6 — Memory

Past states influence future behavior.

### Model 7 — Prediction/model-mediated behavior

Current action can depend on possible future transitions.

### Model 8 — Coupling

Components alter one another's dynamics.

### Model 9 — Collective organization

Coupling can produce persistent macro-level structure.

### Model 10 — Coarse-graining

A macro representation can sometimes expose regularities hidden at the micro level.

### Model 11 — Scale-specific control

Different representations/scales can have different intervention leverage.

### Model 12 — Self-maintaining organization

Some organizations contribute to maintaining their own continued existence.

### Model 13 — Environmental modification

A system can change the environment in ways that alter its future possibilities.

### Model 14 — Recursive organization

Systems can themselves become components of larger systems.

This sequence is not intended as a biological/evolutionary history. It is a **reasoning toolkit**.

---

# 37. The economic payoff of this construction

Once the above machinery exists, economic concepts can be introduced as specific instances of general mechanisms.

For example:

| General mechanism | Later economic interpretation |
|---|---|
| limited observation | dispersed knowledge |
| coupling | exchange |
| heterogeneous capability | specialization |
| persistent state | inventories/contracts/capital |
| feedback | prices/profits/expectations |
| environmental modification | technology/capital |
| persistent coordination | firms |
| stable transition rules | institutions |
| macro representation | markets/economic aggregates |
| long feedback delays | cycles |

The point is not to derive economics from a cellular automaton.

The point is to have a **portable mental model for recognizing the same structural mechanisms in economics.**

---

# 38. The eventual economic construction

The later economic sequence can then resemble the traditional economics progression:

    one bounded producer
        ↓
    multiple producers
        ↓
    interaction/exchange
        ↓
    heterogeneous capabilities
        ↓
    specialization
        ↓
    persistent productive structures
        ↓
    information/coordination
        ↓
    prices
        ↓
    money
        ↓
    firms
        ↓
    institutions
        ↓
    macro feedback

But every stage can be interpreted using the earlier dynamical/cybernetic concepts.

---

# 39. Why this should initially avoid economics and LLMs

The first purpose of the laboratory is not to prove an economic theory.

It is to discover:

- which measurements work;
- which coarse-grainings are useful;
- which perturbation protocols reveal organization;
- which capabilities are actually distinguishable;
- which representations are predictive or controllable;
- whether collective phenomena survive simple changes of substrate.

Deterministic discrete systems are ideal for this because the complete white-box specification is known.

Only after this foundation is useful should richer cognition or economics be introduced.

---

# 40. The long-run complexity ladder

The conceptual and computational ladder can eventually be:

    simple discrete dynamics
            ↓
    coupled discrete dynamics
            ↓
    distributed local-rule systems
            ↓
    Levin-style sorting
            ↓
    stateful/sensing systems
            ↓
    adaptive systems
            ↓
    rich symbolic/resource worlds
            ↓
    rich physical worlds
            ↓
    LLM-based systems
            ↓
    economic/organizational systems

The project should not assume that every stage is necessary.

Each stage exists because it potentially isolates a new mechanism.

---

# 41. A key scientific criterion: do not confuse novelty with complexity

A more complicated system is not automatically a better experiment.

The optimal experiment is the simplest one that makes a particular distinction observable.

Therefore:

> **Increase complexity only when the current substrate cannot answer the next valuable question.**

This protects the rapid implementation/feedback-cycle objective.

---

# 42. A key methodological criterion: use boring systems deliberately

A boring deterministic system can be scientifically superior to an impressive simulation if:

- its mechanism is known;
- its trajectories are cheap;
- interventions are easy;
- observations are complete;
- analysis can be validated against ground truth.

The initial experiments should therefore be selected for **experimental leverage**, not spectacle.

---

# 43. A key methodological criterion: every experiment should be able to fail

The intended outputs include:

- no meaningful higher-level effect;
- coupling adds only efficiency;
- a proposed macro representation is not predictive;
- perturbation reveals no stable tendency;
- a supposed organization disappears under member replacement;
- a capability adds little;
- causal emergence and agency measures diverge.

These results are valuable because they constrain the research program.

---

# 44. Proposed first research sequence

The immediate practical sequence should therefore be:

## Phase A — Minimal discrete dynamics

Build the smallest reusable discrete-system runner.

## Phase B — Trajectory analysis

Add basic observables and visualization.

## Phase C — Perturbation

Add intervention and replay.

## Phase D — Dynamical structures

Add basic recurrence/periodicity/stability characterization.

## Phase E — Levin sorting

Implement or adapt the distributed sorting experiment.

## Phase F — Black-box/white-box comparison

Test whether generic analysis recovers known structure.

## Phase G — Candidate representations/coarse-grainings

Compare simple representations.

## Phase H — System identification

Add PySINDy where useful.

## Phase I — Multiscale/causal analysis

Add PyMergence.

## Phase J — Topological analysis

Add GUDHI only where justified.

## Phase K — Capability additions

Introduce sensing, memory, feedback, and learning one at a time.

## Phase L — Richer environments

Move the proven analysis machinery into Crafter/MiniHack/Minecraft/Dwarf Fortress as required.

## Phase M — LLMs and economics

Only after the preceding results justify those dimensions.

---

# 45. Research-engineering rule

The project should optimize:

\[
\frac{\text{scientifically useful capability}}{\text{new code required}}.
\]

Before implementing a subsystem, check:

1. Is there an existing library?
2. Is there existing experiment code?
3. Is there an existing dataset/trajectory?
4. Can the experiment be expressed with a thin adapter?
5. Do we actually need generalization yet?

Avoid building infrastructure for hypothetical future needs.

---

# 46. The conceptual endpoint

The intended mature picture is not:

> “Everything is an agent.”

Nor:

> “Everything is an attractor.”

Nor:

> “Everything is an LLM.”

Instead:

> **The world contains dynamical systems at many scales. Different representations expose different regularities. Some systems exhibit increasingly rich forms of control, memory, adaptation, and competence. Coupling can create higher-level dynamical organization, and some higher-level descriptions may become useful for prediction, causation, or control.**

The research program is to make those claims empirically tractable.

---

# 47. The central research question

A compact formulation is:

> **Given observable trajectories from a dynamical system, what representations reveal stable and reproducible dynamical structure; how does that structure respond to perturbation and intervention; and how do the useful representations, capabilities, and control relationships change as systems become more coupled and operate at larger scales?**

Eventually:

> **Under what conditions does a higher-level organization acquire distinct effective capabilities, causal structure, or control leverage relative to its components?**

And much later:

> **Do economic institutions represent special cases of the same general organization/control phenomena?**

---

# 48. Final implementation directive

Do not implement the complete research program now.

Implement only the first thin slice:

```text
1-D discrete system
    ↓
run
    ↓
record trajectory
    ↓
visualize
    ↓
perturb initial state
    ↓
rerun
    ↓
compare
```

Use existing libraries for numerical work and visualization.

Then add a second component and coupling.

Then add the Levin sorting system.

Do not add:

- LLMs;
- economics;
- a general agent framework;
- a large ontology;
- Minecraft;
- sophisticated automatic representation search;
- a custom causal-emergence implementation;

until an earlier experiment demonstrates why the next layer is needed.

The intended laboratory is therefore a **single reusable experimental instrument that can progressively host richer discrete dynamical systems**, not a succession of bespoke simulators.
