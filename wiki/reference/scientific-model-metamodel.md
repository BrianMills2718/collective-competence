---
doc-role: scientific-metamodel-design-reference
authority: exploratory
lifecycle: active
sources:
  - ../ontology.md
  - ../questions.md
  - ../../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md
---
# Scientific model metamodel direction

[Reference index](README.md) · [Research ontology](../ontology.md) · [Research questions](../questions.md)

## Direction

The project should investigate a **general metamodel for scientific and empirical models**, using Collective Competence as the first proving ground.

This is not an attempt to build a special ontology framework for competence, nor is the scope defined by Collective Competence. The working hypothesis is that the right primitives should abstract across scientific domains because they describe recurring structure in scientific models themselves: systems, quantities and variables, typed relations, equations and constraints, dynamics, observations, instruments, interventions, analyses, evidence, and the conditions under which claims are identifiable.

Collective Competence is useful because it already forces the metamodel to handle both directions of scientific reasoning:

- **white-box / generative:** declared mechanisms, state, coupling, and rules produce trajectories and candidate capabilities;
- **black-box / inferential:** a declared access contract exposes only selected observations and interventions, from which goal criteria, competence profiles, mechanisms, or equivalence classes may or may not be identifiable.

White-box and black-box should therefore be represented as **different access conditions on the same underlying scientific model**, not as separate ontologies.

This page is exploratory design work. It does not replace the canonical project ontology, change current experimental priorities, or commit the repository to SysML, KerML, RDF/OWL, or another serialization.

## The problem the metamodel should solve

A scientific theory is more than a vocabulary of named concepts and `is-a` relations. For a familiar example, classical mechanics may declare `Mass`, `Velocity`, and `KineticEnergy` as quantity kinds, but much of the theory is carried by additional structure:

```text
K = 1/2 m v^2
```

plus dimensional constraints, reference-frame assumptions, applicability conditions, definitions of state and dynamics, and empirical procedures by which `m`, `v`, or their consequences are observed or estimated.

The corresponding metamodel should make it possible to state, without introducing physics-specific primitives:

1. what entities, systems, properties, variables, quantities, processes, and relations a model contains;
2. how model elements specialize other elements (`is-a`) and how instances participate in typed relations or roles;
3. which functions, equations, predicates, constraints, and dynamical rules relate them;
4. the domain, assumptions, boundary conditions, units, dimensions, and applicability regime of those relations;
5. what is observable, measurable, controllable, hidden, assumed, or inferred under a declared access contract;
6. which instruments/observers and procedures produce observations or measurements;
7. how observations are transformed into representations, estimates, or derived quantities;
8. which interventions and experimental conditions distinguish candidate explanations;
9. how uncertainty, observational/interventional equivalence, and identifiability are represented; and
10. which claims are supported, contradicted, underdetermined, or not tested by which evidence.

The metamodel is the **grammar of scientific models**. Domain theories remain models expressed with that grammar. `KineticEnergy` and `Competence` should normally be theory-level concepts, not universal metamodel primitives.

## Layer separation

Keep at least these levels distinct:

```text
scientific metamodel
  Types, roles, relations, functions, quantities, processes,
  observations, interventions, analyses, claims, evidence, ...
        ↓ conforms to / specializes
scientific theory or domain model
  Mass, Velocity, KineticEnergy, GoalCriterion, Competence, ...
        ↓ instantiated/configured by
study / experimental model
  selected system, boundary, access contract, interventions,
  measurement and analysis procedures, candidate hypotheses, ...
        ↓ produces
empirical instances and evidence
  runs, observations, measurements, estimates, failures, results
```

A domain concept may specialize a metamodel concept through `is-a`, but the scientific content is not exhausted by the type hierarchy. Formal relations, processes, measurements, and inference matter equally.

## Candidate primitive families — v0

These are requirements to test against existing modeling standards, not yet a new schema.

| Family | Candidate primitives / capabilities | Why it is needed |
|---|---|---|
| Identity and typing | type, instance, specialization / `is-a`, identity | Reusable vocabulary and type structure |
| Structure | entity, system, part, environment, boundary, composition, connection | Declare what the modeled system is |
| Properties and variables | property, quantity, state variable, parameter, latent variable, observable variable | Represent theoretical and empirical state |
| Relations and roles | association, n-ary relation, participant role, cardinality | Express facts whose meaning depends on several typed participants |
| Mathematics | function, equation/relation, predicate, constraint, expression | Carry formal theory rather than only taxonomy |
| Applicability | domain, assumption, initial/boundary condition, regime, invariant | State when a relation or model is valid |
| Dynamics | state, process/behavior, transition, event, trajectory, time | Represent change and causal/dynamical models |
| Quantification | quantity kind, value, unit, dimension, uncertainty | Connect mathematical variables to measured quantities |
| Observation and measurement | measurand, observation, measurement, procedure, instrument/observer, result, calibration | Connect theory to empirical access |
| Intervention | controllable target, intervention, operation, treatment/perturbation, condition | Represent active experimentation |
| Experimental design | trial, condition family, comparator/control, sampling/coverage | Define the tested population of situations |
| Analysis and inference | transformation, representation, estimator, analysis, candidate model/hypothesis, prediction | Connect observations to inferred scientific claims |
| Access | access contract, known/hidden/observable/intervenable status, access phase | Put white-box and black-box analysis on one underlying model |
| Identifiability | equivalence class, distinguishing intervention, identifiable/partially identifiable/underdetermined | Represent what the evidence can actually discriminate |
| Epistemic status | claim, evidence, provenance, uncertainty, assessment/review status | Separate model content from warrant for believing it |
| Views | viewpoint, view/projection, notation | Produce multiple useful visualizations without treating a diagram as the model |

A primitive belongs here only if repeated concrete models need it and an established standard does not already supply it adequately.

## Relations: binary, n-ary, and processual

Simple binary facts should stay simple. `Robustness is-a CompetenceDimension` does not need an intermediate object.

Promote a relationship when its meaning depends on additional participants, typed roles, conditions, time, uncertainty, or provenance. For example, a scientific attribution may involve a system, boundary, property, scale, and context. An n-ary association should preserve those participant roles rather than flattening them into ambiguous binary edges.

Do **not** use an n-ary association merely because it can hold many fields when the modeled thing is actually an occurrence or procedure. A measurement, experiment, intervention, or competence assessment occurs, consumes inputs, may contain substeps, and produces results; it should be represented as a process/case/activity with role-typed parameters rather than as a timeless tuple.

This distinction is one reason KerML/SysML v2 is worth testing: KerML supports associations with multiple typed ends, while SysML v2 also provides first-class behavior, calculation, analysis, and verification constructs.

## White-box and black-box as access semantics

Let a scientific model contain a full modeled state and structure `M`. An analyst need not receive all of `M`.

An access contract should be able to declare, by phase:

```text
known(M)
observable(M)
intervenable(M)
hidden(M)
```

and the concrete observations made available by an observation mapping such as:

```text
o_t = H(x_t, access_contract)
```

The same underlying system can therefore support:

- a white-box causal analysis in which mechanism and internal state are inspectable;
- a black-box analysis in which only permitted observations and interventions are visible; or
- a blind-first / reveal-later design in which access changes after prospective inference has been frozen.

This generalizes the repository's existing `analyst_access_phases` contract rather than replacing it.

## Forward and inverse semantics

The metamodel should make both directions explicit.

A **forward/generative model** maps state, parameters, conditions, and interventions to predicted trajectories or observations:

```text
(model, state, parameters, inputs/interventions)
    -> dynamics
    -> predicted state / observations
```

An **inverse/inferential model** maps permitted observations and interventions to estimates, candidate models, parameters, goals, or equivalence classes:

```text
(observations, interventions, access contract)
    -> analysis / inference
    -> estimate, candidate set, equivalence class, or abstention
```

The inverse need not return a unique answer. The metamodel must represent observational or interventional equivalence and preserve underdetermination where the available experiment does not identify a unique model or construct.

## Measurement semantics

A theoretical construct should be traceable to empirical evidence without pretending that an instrument directly measures every high-level construct.

A generic chain is:

```text
theoretical property / construct
    -> measurand or operational target
    -> observing / measurement procedure
    -> instrument or observer
    -> raw observation / result
    -> representation / transformation
    -> estimator or analysis
    -> measurement / estimate + uncertainty
    -> scientific claim
```

For a simulation the instrument may be a state logger or software observer. For an empirical biological system it may be imaging, an assay, an external sensor, or a human-coded observation. The metamodel should be neutral to that distinction.

## Collective Competence as the first proving ground

The repository already has a machine-readable prospective experiment declaration. Treat that as the first substantial instance to map, not as a schema that must be preserved forever.

| Existing CC declaration | Candidate metamodel interpretation |
|---|---|
| `substrate_and_world` | system realization, environment, implementation/version, applicability limits |
| `focal_boundary_and_scale` | system/boundary plus attribution context |
| `mechanism` | model structure + behavior/dynamics + causal claim + epistemic access/status |
| `capability_claims` | bounded system-function claims; test whether these specialize a general disposition/function concept or require a richer relation/process pattern |
| `observation_contract` | access contract + observable variables + observation procedure/instrument |
| `representation_contract` | typed transformation/function from permitted observation history to analysis coordinates |
| `goal_criteria` | predicates/constraints over represented histories plus provenance and alternatives |
| `challenge_family` | experimental-condition family, sampling/coverage, opportunity/feasibility and resource conditions |
| `competence_profile` | structured analysis/measurement result containing only tested dimensions, units, uncertainty, failures, and transfer boundary |
| `intervention_contract` | controllable target + operation + timing/scope/persistence + comparator |
| `evidence` and status fields | claim/evidence/provenance/review semantics |

The current ontology already treats the relevant layers as distinct and already supports `black_box`, `white_box`, and `blind_first_reveal_later` access phases. The metamodel work should explain and generalize those distinctions rather than duplicate them.

### Competence under the candidate metamodel

`Competence` itself should initially remain a theory-level concept. Its current formal shape is approximately:

```text
K = performance_profile(
    system,
    boundary,
    representation,
    goal criterion,
    challenge family,
    resources
)
```

The metamodel should supply the more general notions needed to express this: system, boundary, representation function, predicate/criterion, experimental-condition family, resource quantities/constraints, analysis procedure, structured result, uncertainty, and evidence.

A concrete `CompetenceAssessment` is therefore better modeled as an analysis/process with typed inputs and a result than as a binary `system hasCompetence competence` assertion.

## Existing standards to reuse before inventing primitives

The purpose of the first pass is to determine how much of the candidate metamodel is already supplied by established standards.

- **KerML 1.0 / SysML v2:** primary candidate for general type/feature/association semantics, n-ary role-typed relations, structure, behavior, calculations, constraints, cases, analysis and verification. KerML is the semantic foundation; SysML v2 adds systems-modeling constructs and reusable libraries.
- **QUDT:** candidate reuse for quantity kinds, quantities, values, units, and dimensions rather than creating another units model.
- **SOSA/SSN:** candidate reuse or alignment for sensors/observers, observations, procedures, observed properties, executions, and results, especially when the model crosses from simulation into empirical instrumentation.
- **ISO/IEC/IEEE 42010:** useful discipline for viewpoints and views so conceptual, dynamical, measurement, and evidence visualizations can be projections of one model rather than competing sources of truth.
- **PROV-O:** potentially useful for result lineage and responsibility, but provenance is only one slice of the metamodel and should not determine its scientific semantics.
- **Foundational/domain standards such as BFO/IOF and statistical ontologies such as STATO:** evaluate selectively where they remove real ambiguity or duplication; do not import large ontologies merely to appear standards-based.

Current official references:

- OMG KerML 1.0: https://www.omg.org/spec/KerML/1.0
- OMG SysML 2.0: https://www.omg.org/spec/SysML/2.0
- W3C/OGC SSN/SOSA: https://www.w3.org/TR/vocab-ssn-2023/
- QUDT: https://www.qudt.org/
- ISO/IEC/IEEE 42010: https://www.iso.org/standard/74393.html

No adoption decision follows from this list. Reuse is earned by concrete model fit.

## Acceptance tests for a useful metamodel

A candidate should fail if it can only draw attractive concept graphs. At minimum it should be able to represent:

1. a nontrivial Collective Competence experiment from its system/mechanism through observation, intervention, analysis, competence result, and evidence;
2. both white-box and black-box/blind-first access to the **same** underlying system model without duplicating the theory;
3. formal equations/functions and their typed inputs/outputs, units/dimensions, assumptions, and applicability conditions;
4. direct observations, derived variables, latent/theoretical constructs, instruments/observers, measurement procedures, and uncertainty as distinct things;
5. binary and genuinely n-ary role-typed relations without losing participant meaning;
6. processes/analyses as occurrences rather than flattening them into relation tuples;
7. alternative hypotheses/models that are observationally equivalent under one access contract but distinguishable by a declared intervention;
8. `abstain` / `underdetermined` results when evidence does not identify a unique answer;
9. claims whose evidence can be traced to exact experimental results without treating schema validity as proof of scientific truth; and
10. multiple views or visualizations as recoverable projections of the same underlying model.

After a CC instance works, use a compact mature case such as classical mechanics as a cross-domain sanity check. That check is not the design driver; it tests whether CC-specific assumptions have leaked into supposedly general primitives.

## First iteration

Proceed in this order:

1. **Map the existing experiment contract, do not replace it.** Treat its fields and validators as empirical requirements for the metamodel.
2. **Select one manageable CC experiment** that has explicit mechanism, observations, intervention/control, and competence semantics. Encode its scientific content using the smallest candidate primitive set.
3. **Represent a second access phase over the same system** with internal mechanism or authored semantics hidden. Verify that the model can express what is and is not identifiable without cloning the system definition.
4. **Crosswalk every primitive against KerML/SysML v2, QUDT, and SOSA/SSN.** Reuse or align where the semantics actually fit; record mismatches rather than papering them over.
5. **Promote only repeated missing concepts into the metamodel.** A concept needed only to explain Collective Competence stays at the theory/domain-model level.
6. **Only after the model is semantically adequate choose a canonical serialization and visualization.** WebVOWL, SysML diagrams, tables, and bespoke scientific views are possible projections, not the metamodel itself.

The immediate design question is therefore not “what should the Collective Competence ontology look like?” but:

> **What minimal, reusable semantic machinery is required to express the full scientific and empirical content already present in a Collective Competence experiment, including its white-box and black-box interpretations?**
