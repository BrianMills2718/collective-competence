---
doc-role: supplied-source
authority: historical
lifecycle: retained
---
> Preserved supplied specification. Embedded implementation directives and
> "current" claims describe the original brief, not today's task queue.
> See [source provenance](../README.md) and [current charter](../../PROJECT.md).

# Research Laboratory Specification
## Discrete Dynamical Systems -> Dynamical Structure -> Agency/Control -> Multiscale Analysis

### Purpose

Build a small, reusable research laboratory for testing ideas about dynamical structure, diverse intelligence, agency, control, and emergence. The project should optimize for **rapid implementation and feedback**, using mature existing software wherever possible.

The immediate objective is **not** to build an artificial economy, a general agent framework, Minecraft civilization, or a universal ontology. The immediate objective is to establish a reusable trajectory/perturbation/analysis loop on very simple deterministic systems and then increase complexity only when the previous experiment produces a reason to do so.

---

# 1. Core research idea

Start from a system that produces trajectories:

    X_0, X_1, ... , X_T

where X is the underlying state available to the experiment.

We can construct many observable representations:

    Y_t = f(X_t)

where f can be trivial or sophisticated: rates, counts, ratios, correlations, entropy, aggregate variables, graph statistics, temporal features, etc.

There should be two complementary directions:

**Bottom-up:** trajectories -> observables -> candidate representations -> recurring structure.

**Top-down:** candidate representation/coarse-graining -> prediction/intervention test -> retain/reject/refine.

We do not assume a unique "true" state space, goal space, or coarse-graining.

---

# 2. Black-box and white-box analysis

Because our first systems are synthetic, use both views.

### Black-box

Pretend the analyst only sees externally available observations and trajectories. Ask what dynamical structures, persistent tendencies, useful representations, and effective interventions can be discovered.

### White-box

Retain the exact specification: transition rules, topology, parameters, coupling, internal variables, controller/policy, and intervention schedule.

Compare black-box discoveries with white-box ground truth.

This creates a valuable methodological loop:

    observe blindly
        -> infer structure
        -> reveal mechanism
        -> test inference
        -> improve method

This is a major advantage of deterministic artificial systems.

---

# 3. Vocabulary

Use conservative mathematical language.

### Dynamical system
A state evolving according to a transition rule, e.g.

    X_(t+1) = F(X_t, u_t)

or continuous-time equivalent.

### Discrete dynamical system
A system with discrete time and/or discrete state variables.

### Entity / component / element
A constituent. Do not call every constituent an agent.

### Transition rule
The mechanism determining state transitions.

### Policy
A mapping from observations/internal state to actions.

### Controller
A mechanism specifically organized to influence another dynamical process toward a criterion. Do not force this term onto every local rule.

### Dynamical structure
Umbrella term for fixed points, periodic orbits, invariant sets/manifolds, attracting sets, metastable states, traveling structures, chaotic attractors, and persistent organizational patterns.

### Attractor
One important subclass of dynamical structure. Not every interesting persistent trajectory is an attractor.

---

# 4. Why prefer "dynamical structure" to "goal" initially

For early experiments, avoid unnecessary connotations from the word "goal".

Use terms such as:

- attractor;
- invariant structure;
- persistent pattern;
- preferred region;
- recurring tendency;
- stable dynamical structure.

Only later ask whether a persistent structure is usefully interpreted as a goal-directed tendency in the Levin sense.

Not every attractor is a point: fixed points, cycles, higher-dimensional sets, etc. are possible. A conservative distinction is between invariant/persistent structures and genuinely attracting structures.

---

# 5. Intelligence and cognition

Do not invent a new universal hierarchy of intelligence.

Use established dimensions from the diverse-intelligence literature as experimental variables where useful. Candidate dimensions include:

- sensing;
- persistence;
- memory;
- internal state;
- feedback;
- plasticity;
- learning;
- prediction;
- exploration;
- planning;
- generalization;
- communication;
- problem solving;
- self-modeling/metacognition;
- goal modification.

These are capabilities/dimensions, not necessarily a strict ladder. A system may have one without another.

For the initial laboratory, add them incrementally rather than implementing an elaborate agent architecture.

---

# 6. Levin connection

The relevant Levin program is not simply "everything is intelligent." The useful experimental stance is that goal-directed competence can be investigated across very different substrates and problem spaces, and that different systems may admit different effective control/intervention strategies.

In particular, use Levin-inspired ideas such as:

- competence in arbitrary problem spaces;
- diverse forms of goal-directedness;
- perturbation and recovery;
- alternative means to similar ends;
- scaling of cognition/agency;
- cognitive glue;
- the axis of persuadability/control.

Do not reimplement Levin's theory from scratch. Reuse his existing conceptual and quantitative work wherever possible.

---

# 7. Control / persuadability

A useful experimental question is:

> What type of intervention is most effective at changing the behavior of this system?

Possible intervention families:

- direct state/physical manipulation;
- parameter modification;
- rule/program modification;
- setpoint/control change;
- information input;
- training;
- communication/persuasion.

Measure effect size, reliability, cost, latency, and information requirements where meaningful.

This gives us a bridge between agency, system identification, and control without assuming that every system has a conventional controller.

---

# 8. Candidate goals should be discovered experimentally

A goal need not be specified by the experimenter.

For a candidate representation Y_t:

1. Observe trajectories.
2. Identify recurring convergence/persistence in Y.
3. Perturb the system.
4. Check whether the same structure reappears.
5. Block the usual route.
6. Check whether an alternative trajectory reaches the same region/structure.
7. Test across initial conditions and repeated runs.

Use cautious language such as:

> "The system exhibits a reproducible tendency toward/maintenance of G in representation Y."

Only then consider whether the behavior fits a stronger interpretation as goal-directed competence.

---

# 9. State, representation, metric, and coarse-graining

Do not treat these as independent pieces of ontology.

Start from measured variables and construct representations.

A rate is simply another observable:

    rate_t = (x_t - x_(t-1)) / dt

A candidate state representation might be:

    Y_t = (production, energy, connectivity, ...)

A metric defines some notion of distance/similarity/progress within a representation, but not every representation requires an ordinary continuous metric.

The key question is:

> Which combinations/transforms of observables expose stable, useful structure?

---

# 10. Coarse-graining and Hoel

Let:

    Y_t = f(X_t)

be a candidate coarse-graining.

A useful coarse-graining is not "the true macrostate." It is one that is useful for a stated purpose, such as:

- prediction;
- compression;
- causal analysis;
- intervention/control;
- interpretation.

Use Hoel-style causal-emergence methods as an analysis layer rather than making Hoel's framework the simulator architecture.

Potential later tools:

- PyMergence;
- einet;
- PyPhi for selected integration/causal questions.

---

# 11. Trajectory space

Trajectory space is combinatorially large. If there are k actions for T steps, there can already be roughly k^T action sequences.

Therefore do not enumerate trajectory space except in toy cases.

Instead use:

- sampled trajectories;
- empirical trajectory distributions;
- recurrence analysis;
- clustering/embeddings;
- transition graphs;
- entropy/information measures;
- reachability approximations.

The key object is often the **distribution over trajectories**, not an explicit list of every possible trajectory.

---

# 12. Why trajectory space matters

Two systems can have similar reachable outcomes while differing strongly in how they reach them.

We should distinguish:

- attainable states;
- attainable trajectories;
- successful trajectories;
- trajectory flexibility;
- efficiency;
- robustness.

Potentially interesting contrast:

    rigid system: few successful trajectories
    flexible system: many successful trajectories

This connects directly to Levin-style competence and alternative means of reaching an outcome.

---

# 13. Robustness and adaptation

Robustness should be treated as performance across perturbations, not as a mystical additional property.

Given performance M and perturbation p:

    M_p = M(trajectory under p)

Possible summaries:

- success probability;
- average performance;
- failure probability;
- recovery probability;
- worst-case performance;
- variance.

Separate this from adaptation/reorganization:

    perturbation -> loss -> behavioral change -> recovery

is different from simply remaining unaffected.

---

# 14. Viability and autopoiesis

Do not equate:

    intelligence = viability = self-preservation = autopoiesis

They are distinct empirical properties.

A system may exhibit strong directed behavior while destroying its own organization.

Track separately:

- persistence of the system boundary;
- functional viability;
- adaptation;
- goal-directed tendency;
- environmental control.

Autopoiesis becomes relevant when processes constituting a system participate recursively in maintaining/reconstituting the organization defining the system. Do not infer autopoiesis simply from the presence of an attractor or tendency.

---

# 15. Classical dynamical-systems baseline

Before inventing intelligence-specific analysis, use standard tools:

- trajectories;
- phase/state portraits;
- fixed points/equilibria;
- local stability;
- Jacobians/eigenvalues when applicable;
- recurrence;
- bifurcations when useful.

The baseline question is simply:

> What dynamical structure does this system have?

Only afterward ask whether a richer Levin-style interpretation adds explanatory/predictive/control value.

---

# 16. Cellular automata as the initial substrate

The preferred starting class is a **discrete interacting dynamical system**, not necessarily an ABM and not necessarily a canonical cellular automaton.

A standard CA is a special case:

    cell lattice
    + local neighborhood
    + local update rule

The broader substrate should permit:

- arbitrary numbers of entities;
- entity-local state;
- local interaction;
- explicit transition rules;
- synchronous/asynchronous update;
- different coupling topologies.

This lets the same infrastructure move from simple CA rules toward richer distributed systems.

---

# 17. Levin's sorting system

Treat the distributed sorting work as a particularly valuable calibration case.

It is best described conservatively as a **one-dimensional discrete interacting/local-rule dynamical system** rather than simply calling it a standard cellular automaton.

It has CA-like features—local elements, local rules, repeated updates producing global organization—but differs from a canonical CA in important implementation details such as element identity/values, movement/swapping, and the execution/locking scheme.

Its value to this project is precisely that:

- the microscopic specification is understandable;
- the dynamics are discrete;
- the system is cheap to run;
- perturbations are easy;
- interesting collective competence has already been reported.

Use it first as a calibration target, not as evidence that our own analysis works merely because it reproduces the authors' conclusions.

---

# 18. One reusable experimental engine

Do NOT build a separate codebase for every experiment.

Instead build thin shared infrastructure and plug systems into it.

Conceptually:

    system.reset()
    system.observe()
    system.step(...)
    system.snapshot()
    system.restore()
    system.intervene(...)

Not every backend must implement every method.

The reusable scientific object should be the **trajectory plus metadata**.

---

# 19. Existing traces and executable worlds

Support two modes.

### Observational mode

Input existing trajectories/logs and search for candidate structures.

### Experimental mode

Run an executable system so that we can manipulate initial conditions and interventions.

The desired loop is:

    existing trace
        -> candidate structure
        -> recreate executable system
        -> perturb/intervene
        -> test hypothesis

This makes the project useful for existing CA experiments, published computational systems, game logs, and eventually rich environments, without requiring that everything originate inside our own simulator.

---

# 20. Existing software: reuse-first policy

Do not reinvent mature scientific infrastructure.

### Discrete/CA layer

Consider CellPyLib or comparable established CA libraries for standard cellular automata. Write a tiny adapter when necessary rather than a new CA engine.

### Scientific Python

Use:

- NumPy
- SciPy
- Matplotlib
- pandas or Polars
- scikit-learn where appropriate

### System identification

Use **PySINDy** when useful for learning governing dynamics from trajectories. Its current project includes discrete-system identification in addition to continuous nonlinear-system discovery.

### Dynamical systems

**PyDSTool** exists and is relevant, but its current project describes itself as a beta release and is not the preferred new dependency.

A Julia alternative, **DynamicalSystems.jl**, is strong, but do not make Julia mandatory unless a real experiment requires a capability that Python cannot reasonably supply.

### Causal emergence

Use PyMergence/einet where their input assumptions match the experiment.

### Computational topology

Use **GUDHI** when state/trajectory topology becomes relevant; do not make it an early dependency.

### ABM/multi-agent

Use PettingZoo, OpenSpiel, Mesa, Agents.jl, NetLogo, etc. only when the current experiment actually benefits from those abstractions.

### Rich worlds

Use Crafter, MiniHack, Minecraft/MineDojo, Dwarf Fortress/DFHack, etc. only when simpler substrates have justified the additional complexity.

---

# 21. Why Python-first

For this project, avoid adding Julia merely because Julia has an excellent dynamical-systems ecosystem.

The preferred first path is:

    Python
    + NumPy/SciPy
    + CA library or thin discrete-rule layer
    + PySINDy when needed
    + PyMergence when applicable
    + GUDHI when applicable

PyDSTool can be used if a specific capability is needed, but should not be the default foundation.

---

# 22. Thin-slice implementation ladder

Do not implement the whole architecture upfront.

## Slice 0

One trivial deterministic 1-D discrete system.

- Run it.
- Record trajectory.
- Plot trajectory.

## Slice 1

Two coupled elements.

Compare uncoupled vs coupled trajectories.

## Slice 2

N elements on a 1-D lattice.

Add local neighborhoods and rules.

## Slice 3

Add state perturbations and rule perturbations.

## Slice 4

Add a handful of candidate observables and representations.

Examples:

- number of active cells;
- center of mass when meaningful;
- run lengths;
- entropy;
- correlations;
- simple rates.

## Slice 5

Basic dynamical-structure analysis:

- periodicity;
- recurrence;
- fixed/periodic configurations;
- attractor/basin analysis where mathematically appropriate.

## Slice 6

Implement/adapt Levin-style distributed sorting.

## Slice 7

Generic perturbation/recovery analysis.

## Slice 8

Compare candidate coarse-grainings.

## Slice 9

Try PySINDy/system identification where appropriate.

## Slice 10

Try PyMergence once there is a suitable discrete/stochastic transition representation.

## Slice 11

Try GUDHI only if topology appears relevant.

## Slice 12+

Add sensing, internal state, memory, feedback, learning, richer coupling.

Then move to richer environments only when justified.

---

# 23. Candidate research questions for early experiments

Do not start with "is this intelligent?"

Start with:

- Which observables reveal recurring structure?
- Which representations make that structure easiest to detect?
- Which structures persist after perturbation?
- Can the system reach a recurring structure through multiple trajectories?
- Does coupling create new persistent structure?
- Does a macro representation become more predictive than the microscopic representation?
- Does a macro representation become more useful for intervention?
- Can black-box analysis recover structure that white-box analysis confirms?

These questions are deliberately substrate-neutral.

---

# 24. Potential higher-level-system tests

For a candidate collective boundary, compare:

### Component intervention
Change one component.

### Structural intervention
Change the relationship among components.

### Information intervention
Block or alter information flow.

### Feedback intervention
Interrupt a suspected feedback path.

### Member replacement
Replace a component while preserving as much surrounding structure as possible.

Then test whether the collective-level regularity persists.

A grouping should not be called a higher-level agent merely because it was useful to draw a box around it.

---

# 25. Scale and representation are experimental variables

A system can be analyzed at multiple resolutions:

    element level
    local cluster level
    global level

or with multiple observable sets.

Ask at each level:

- what can be predicted?
- what can be controlled?
- what regularities persist?
- how much information is lost?
- does a new dynamical structure appear?

This is where Hoel-style multiscale analysis becomes relevant.

---

# 26. Natural scales and dimensionless quantities

Classical modeling suggests looking for characteristic timescales and dimensionless ratios rather than relying only on absolute measurements.

Examples to investigate later—not assumptions to hard-code:

    adaptation time / environmental change time
    coordination time / system evolution time
    communication delay / decision time

If a useful dimensionless regime emerges, test whether it generalizes across system sizes or substrates.

---

# 27. Randomly generated systems: later, not first

Eventually a system generator could vary:

- number of elements;
- number of states;
- neighborhood radius;
- rule density;
- coupling topology;
- update schedule;
- initial configuration.

Then run large numbers of systems and search for classes of behavior.

Do this only after the manually specified systems establish that the analysis pipeline is producing interpretable results.

Random generation should explore a well-defined family, not simply create arbitrary noise.

---

# 28. Reproducibility

Every experiment should record:

- code version;
- environment/backend version;
- seed;
- system configuration;
- rule/policy version;
- intervention schedule;
- measurement configuration.

Every major result should be regenerable from a clean environment.

---

# 29. Suggested repository structure

    dynamical-lab/
        README.md
        pyproject.toml

        core/
            experiment.py
            trajectory.py
            interventions.py

        systems/
            ca.py
            levin_sorting.py
            coupled_rules.py

        analysis/
            observables.py
            trajectory.py
            dynamics.py
            representations.py
            perturbations.py

        adapters/
            cellpylib.py
            pysindy.py
            pymergence.py
            gudhi.py

        experiments/
            001_baseline/
            002_coupling/
            003_sorting/

        results/

Do not allow the repository to evolve into a general-purpose agent framework without an experiment forcing that abstraction.

---

# 30. Economics and LLMs are later variables

Economics eventually provides a rich application domain for:

- dispersed knowledge;
- specialization;
- exchange;
- prices;
- money;
- firms;
- institutions;
- expectations;
- delayed feedback;
- cycles.

LLMs eventually provide a richer cognitive substrate.

Neither belongs in the first implementation.

The experimental ladder should allow us to ask what additional effects appear as we move from:

    deterministic local dynamics
        -> stateful systems
        -> adaptive systems
        -> richer environments
        -> LLM systems
        -> economic organization

---

# 31. Falsifiability and boring results

Do not design experiments to produce impressive behavior.

Accept results such as:

- coupling has no measurable effect;
- the macro representation adds no predictive value;
- apparent emergence disappears under perturbation;
- causal emergence and competence diverge;
- memory changes little;
- richer controllers add little;
- LLM agents offer no advantage in a given environment.

A negative result can eliminate a mechanism or constrain a theory.

---

# 32. Immediate coding task

Implement only the first thin slice:

1. A tiny 1-D discrete dynamical system.
2. Reproducible execution.
3. Trajectory logging.
4. One or two plots.
5. One simple perturbation.
6. One simple derived observable.

Then add a second coupled element.

Do not build the later architecture yet.

The purpose of the first slice is to validate the experimental loop, not to demonstrate intelligence.

---

# 33. Long-run scientific objective

The mature question is approximately:

> Given observable trajectories from a dynamical system, which representations/coarse-grainings expose stable structure, and how do those structures change under perturbation, intervention, coupling, and scale?

Then:

> Under what conditions do coupled systems exhibit higher-level dynamical organization, distinct effective capabilities, or Levin-style goal-directed competence?

Then:

> At what scales do causal and control descriptions become more useful?

Only then ask whether analogous mechanisms help explain features of biological collectives, organizations, markets, or economic systems.

---

# 34. Prime directive

**Build the minimum. Borrow everything else. Measure before theorizing. Perturb before declaring emergence. Compare representations rather than assuming one. Keep black-box and white-box views separate. Increase complexity only when a previous experiment earns it.**
