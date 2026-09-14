---
doc-role: scientific-metamodel-prior-art-audit
authority: exploratory
lifecycle: active
sources:
  - scientific-model-metamodel.md
  - scientific-model-metamodel-cc-pilot.md
  - scientific-model-metamodel-c2-q1-pilot.md
---
# Scientific metamodel prior-art deletion audit

[Metamodel direction](scientific-model-metamodel.md) · [C2/Q1 pilot](scientific-model-metamodel-c2-q1-pilot.md) · [Reference index](README.md)

## Purpose

The Collective Competence pilots exposed a large candidate vocabulary for representing scientific models. This audit has the opposite goal from ontology expansion:

> **Delete candidate primitives whenever an established standard already supplies the required semantics.**

The emerging target is not necessarily one new universal ontology. It may be a small **scientific-modeling profile/integration** over existing formal modeling, mathematical, metrological, experimental, workflow, policy, and evidence standards, with only genuinely missing cross-cutting scientific semantics added locally.

The standards below are reuse candidates, not dependencies or adoption decisions. A standard earns a place only when a concrete CC model benefits from its semantics.

## The strongest precedent: EXPO already asked a very similar question

Soldatova and King proposed **EXPO, a domain-independent ontology of scientific experiments**, in 2006. Its explicit motivation was that different sciences share generic experimental structure and should not independently redefine experimental design, methodology, and results representation.

Especially relevant to the present work, EXPO separates an experiment into:

1. a **physical level** — the real-world field of study;
2. a **model level** — knowledge/model of the experimental domain; and
3. a **design level** — parameters, target variables, and the sequence of experimental actions.

It also distinguishes physical and computational experiments and treats controllability of variables as an experimental attribute.

Reference: https://pmc.ncbi.nlm.nih.gov/articles/PMC1885356/

EXPO therefore establishes that the intuition behind a domain-independent scientific/experimental metamodel is not novel. Its limitations for the current purpose are equally informative: it predates modern SysML v2/KerML, modern workflow/provenance standards, current observation ontologies, and the project's need for explicit mathematical theory, staged information access, black-box inference, and identifiability.

The correct response is to **build on the problem decomposition, not restart it**.

## Prior art by semantic responsibility

### 1. Formal model structure and behavior — KerML / SysML v2

Use for:

- identity, types, specialization and features;
- parts, connections and system composition;
- typed and n-ary associations with role-bearing ends;
- behaviors/actions, states and transitions;
- functions/calculations and predicates/constraints;
- requirements, analysis cases and verification cases;
- model views/viewpoints and metadata extensions.

References:

- https://www.omg.org/spec/KerML/1.0
- https://www.omg.org/spec/SysML/2.0

**Deletion consequence:** do not invent generic `Entity`, `Part`, `Association`, `Role`, `Process`, `Function`, `Predicate`, `Constraint`, or `Analysis` metaclasses until a concrete mismatch is demonstrated.

### 2. Mathematical expression and mathematical-model semantics — OpenMath / MathModDB

**OpenMath** is an extensible standard for the semantics of mathematical objects. Its Content Dictionaries define symbols, descriptions, and formal properties rather than treating equations as opaque text.

Reference: https://openmath.org/standard/

**MathModDB** is a current cross-disciplinary ontology/knowledge graph for mathematical models. Its model connects research problems to mathematical models, formulations/formulas, quantities and quantity kinds, assumptions, computational tasks, and literature; its quantity semantics align with QUDT. It also supports model specialization hierarchies.

References:

- https://mardi4nfdi.github.io/MathModDB/
- https://arxiv.org/abs/2606.27933

**OMDoc** is older but remains useful prior art for the theory level above individual expressions: theories, symbols, definitions, axioms, imports, and formal mathematical statements.

Reference: https://www.omdoc.org/pubs/omdoc1.2.pdf

**Deletion consequence:** do not invent another mathematical expression tree or a bespoke `Equation` serialization merely to make formulas machine-readable. Test whether KerML/SysML calculation semantics plus OpenMath/MathML representation and MathModDB-style model metadata cover the need.

### 3. Quantities, units and measurement uncertainty — VIM/GUM + QUDT

The **International Vocabulary of Metrology (VIM)** is explicitly intended to provide basic and general measurement concepts across science and engineering. The associated GUM series covers measurement uncertainty and measurement models.

References:

- https://www.bipm.org/en/publications/guides
- https://jcgm.bipm.org/vim/en/

**QUDT** supplies machine-readable quantity kinds, quantities, dimensions, units, values and related semantics.

Reference: https://www.qudt.org/

**Deletion consequence:** `Measurand`, `MeasurementResult`, `MeasurementUncertainty`, `QuantityKind`, `Unit`, and `Dimension` should align with established metrology/quantity semantics rather than receive CC-specific definitions.

### 4. Observations, procedures, instruments and results — ISO/OGC OMS + SOSA/SSN

**ISO 19156:2023 / OGC Observations, Measurements, and Samples (OMS)** is a cross-community conceptual schema for observation acts and results. It treats an observation as an act evaluating a property using a procedure and producing a result; the procedure may be an instrument, algorithm, process chain, or simulation.

Reference: https://www.ogc.org/standards/om/

**SOSA/SSN** provides RDF/ontology semantics for sensors/observers, procedures, observations, samples, actuations, features of interest, observed properties and results.

Reference: https://www.w3.org/TR/vocab-ssn/

**Deletion consequence:** the CC metamodel should not invent generic `Observation`, `Instrument`, `Procedure`, `ObservedProperty`, or `ObservationResult` semantics. The simulator's read-only observer hook can be represented as one software observation procedure; an empirical camera or assay can use the same observation layer.

### 5. Variable descriptions — I-ADOPT

The RDA **I-ADOPT Framework** deliberately provides a small cross-domain model for describing observed or mathematically derived variables in terms of a property, object of interest, context/matrix entities, constraints, and statistical modifiers.

Reference: https://i-adopt.github.io/ontology/

This is notably close to the metamodel's need to distinguish a symbol/variable from the property/entity/context it denotes.

**Deletion consequence:** do not invent a rich variable-description ontology. Test I-ADOPT as a semantic description layer attached to KerML/SysML variables and calculations.

### 6. Simulation experiment specification — SED-ML

**SED-ML** is a model-language-independent format for reproducible simulation experiments. It already separates:

- referenced model;
- changes made to the model;
- simulation procedure/algorithm;
- task binding model to simulation;
- input data;
- data generators/post-processing; and
- outputs.

Reference: https://sed-ml.org/

It is biology-originated but intentionally independent of the underlying model implementation.

**Deletion consequence:** a generic `SimulationStudy` should not be invented before testing whether SED-ML concepts cover the computational-experiment subset of the desired metamodel.

### 7. Planned procedure versus actual execution — P-Plan / ProvONE / PROV-O

**P-Plan** extends PROV-O to represent a plan's steps and variables and to link planned steps/variables to the activities/entities that actually occurred. Its motivating distinction is exactly the difference between the procedure that was supposed to happen and retrospective provenance of what did happen.

References:

- https://www.opmw.org/model/p-plan/
- https://www.w3.org/TR/prov-o/

**ProvONE** similarly covers prospective workflow specification, retrospective execution provenance, and process provenance for scientific workflows.

Reference: https://jenkins-1.dataone.org/jenkins/job/ProvONE-Documentation-1.0.0/ws/provenance/ProvONE/v1/provone.html

**Deletion consequence:** the candidate `ScientificDeclaration` versus `ExecutableRealization` distinction should not become bespoke workflow/provenance machinery. Use plan/specification and execution concepts, then add a scientific conformance claim only where necessary.

### 8. Scientific claims and evidence — SEPIO

The **Scientific Evidence and Provenance Information Ontology (SEPIO)** is explicitly a domain-agnostic model for scientific claims, lines of evidence, supporting information, and the methods/tools/agents that generated them.

References:

- https://obofoundry.org/ontology/sepio.html
- https://github.com/monarch-initiative/SEPIO-ontology

**Deletion consequence:** do not create a new generic Claim/Evidence ontology. CC-specific assessment statuses may be profiles/vocabularies over a reusable claim/evidence model.

### 9. Permission/prohibition over model and data assets — ODRL

The **W3C Open Digital Rights Language (ODRL)** provides a generic policy information model for permissions, prohibitions and obligations on identified assets, with parties/roles, actions and constraints.

Reference: https://www.w3.org/TR/odrl-model/

For a black-box study, a scientific access contract could potentially be represented as an ODRL profile in which:

```text
principal / analysis procedure  -> Party
model or data element           -> Asset
read / inspect / execute        -> Action
allowed                         -> Permission
hidden / forbidden              -> Prohibition
study phase                     -> Constraint
```

This does **not** by itself prove that an analysis did not depend on prohibited information. It covers the normative access policy, not information-flow conformance.

**Deletion consequence:** do not invent generic permission/prohibition semantics. Retain only the scientific binding between access policy, study stage, model elements and dependency verification if needed.

### 10. Executable black-box model interfaces and dependencies — FMI

The **Functional Mock-up Interface (FMI)** is useful prior art for executable-model boundaries. FMI explicitly classifies exposed variables by causality (`parameter`, `input`, `output`, `local`, `independent`) and records variable dependencies. Local variables are internal and are not intended for model connections.

Reference: https://fmi-standard.org/docs/3.0.2/

This is not an epistemic model of blinded science, but it demonstrates that a machine-readable distinction between externally available model variables, internal state and dependency structure is mature engineering practice.

**Deletion consequence:** the candidate access/dependency layer should align with executable-interface concepts where appropriate instead of inventing an incompatible notion of input/output/hidden state.

### 11. Physically oriented integrated ontology — EMMO

The **Elementary Multiperspective Material Ontology (EMMO)** explicitly aims to integrate fundamental physics/materials concepts, modelling, characterization and metrology.

Reference: https://emmo-repo.github.io/

EMMO is strong prior art for connecting physical systems, models and measurement, but its development is intentionally grounded in physics/materials modelling. It is therefore more useful as a comparison and source of reusable patterns than as the presumptive universal metamodel for arbitrary empirical disciplines.

## Revised candidate set after deletion

The first metamodel note listed many candidate primitive families. After this audit, most should be delegated to established semantics rather than treated as new primitives.

| Earlier candidate | Current disposition | Likely reuse |
|---|---|---|
| Type / instance / `is-a` | delegate | KerML |
| System / part / connection / boundary structure | delegate except scientific attribution semantics | KerML / SysML v2 |
| N-ary relation / participant role / cardinality | delegate | KerML |
| Process / behavior / state / transition | delegate | KerML / SysML v2 |
| Function / calculation / predicate / constraint | delegate | KerML / SysML v2 |
| Mathematical expression / symbols | delegate | OpenMath / MathML |
| Mathematical model / formula / assumptions / task | align/reuse | MathModDB |
| Quantity / quantity kind / unit / dimension | delegate | QUDT / SysML Quantities & Units |
| Measurand / result / uncertainty / measurement model | align to standards | VIM / GUM |
| Observation / procedure / instrument / observed property | delegate | OMS and/or SOSA/SSN |
| Semantic variable description | delegate/profile | I-ADOPT |
| Computational simulation experiment | delegate/profile | SED-ML |
| Planned steps versus actual execution | delegate | P-Plan / ProvONE / PROV-O |
| Generic claim / supporting evidence | delegate/profile | SEPIO |
| Permission / prohibition / obligation | delegate | ODRL |
| Executable model inputs/outputs/locals/dependencies | align where executable | FMI |
| View / viewpoint / projection | delegate | SysML v2 + ISO 42010 discipline |
| Validity gate | **pattern, not primitive** | predicate/constraint + planned conditional stage + result |
| Freeze/reveal boundary | **pattern, not primitive** | plan/stage ordering + immutable artifact/provenance + access-policy change |
| Declaration-realization conformance | **pattern, not primitive** | requirement/specification + verification + prospective/retrospective provenance |
| Mechanism | theory-level explanatory submodel/claim, not metamodel primitive | system model + SEPIO-like claim |
| Capability | theory/foundational-level modal construct; evaluate separately | SysML behavior/requirements + possible disposition/function alignment |
| Competence | CC theory-level construct | CC model |

## What still appears genuinely under-covered

The audit leaves a much smaller candidate scientific extension.

### A. Scientific access regime

We need to bind, in one scientific statement:

- a **principal** (human analyst, algorithm, estimator, proposal procedure);
- a **study stage**;
- the underlying scientific model and data products;
- what model knowledge/data may be consumed;
- what interventions may be invoked; and
- what remains hidden until a later stage.

ODRL can express the permission/prohibition policy. SysML views can define projections. P-Plan/ProvONE can model stages and execution. FMI can distinguish executable external/internal variables.

The missing piece may therefore be only a **scientific profile that binds those standards together**, not a new access-control ontology.

### B. Dependency/access conformance

C2-001 shows that a declared blind or local dependency claim is scientifically meaningful only if the realized procedure actually obeys it.

General form:

```text
DeclaredPermittedDependencies(P, stage)
ActualDependencies(realization)

conforms iff
ActualDependencies ⊆ DeclaredPermittedDependencies
```

This resembles information-flow/noninterference verification more than ordinary ontology classification. The metamodel may only need a standardized **conformance assertion and evidence hook**; static/dynamic analysis tools can perform the actual verification.

### C. Identifiability under an access/intervention regime

Identifiability is established mathematical territory in system identification, statistics and inverse problems, but this audit did not find a mature general semantic standard that represents statements of the form:

```text
target distinction T
is identifiable / partially identifiable / equivalent / underdetermined
under
  model family M
  observation mapping H
  intervention family I
  access regime A
  error/noise assumptions E
```

Nor did a standard surface for first-class statements such as:

```text
Model A and Model B are observationally equivalent under AccessRegime X
but distinguishable by Intervention Y.
```

This remains the strongest candidate for genuinely general new scientific semantics.

### D. Epistemic linkage between theory, study and access

Existing standards separately cover model structure, experiment plans, observations and claims. The scientific question frequently depends on **which model elements are treated as known, assumed, hidden, measured, estimated or inferred in a particular study**.

These should probably be contextual roles/relations, not intrinsic classes:

```text
EpistemicStatus(
  modelElement,
  principal,
  studyStage,
  status = known | assumed | observable | measured | inferred | hidden | unknown
)
```

The point is not to create another vocabulary of labels; it is to make the status explicitly relative to a principal and stage so that white-box and black-box analyses can share one underlying theory model.

## Resulting architecture — v1 hypothesis

A plausible architecture after the deletion audit is:

```text
                 Scientific-modeling profile
                           |
        +------------------+------------------+
        |                  |                  |
  formal/system      empirical/study      epistemic layer
      model              semantics          (thin extension)
        |                  |                  |
 KerML/SysML         VIM + OMS/SSN       access regime
 OpenMath            I-ADOPT             identifiability
 MathModDB           SED-ML              contextual known/
 QUDT                P-Plan/ProvONE      hidden/inferred roles
 FMI                  SEPIO
                      ODRL
```

This should be interpreted as a semantic crosswalk, **not** a proposal to import every ontology wholesale. A practical implementation can use a much smaller canonical representation and map to external vocabularies where interoperability matters.

## What this means for Collective Competence

The CC experiment contract should remain the current working scientific declaration while this investigation proceeds. It is valuable precisely because it already tests many of the seams:

- system realization and dynamics;
- internal information access;
- analyst access phases;
- observation/representation transformations;
- interventions and matched controls;
- prospective gates and stop conditions;
- theoretical constructs such as goal and competence;
- black-box inference and abstention/equivalence;
- claim/evidence status;
- cases where declared information restrictions did not match actual executable dependencies.

The metamodel work should eventually make those semantics **more general and more mechanically checkable**, not merely rename the fields.

## Next implementation-oriented probe

Before proposing any new core class:

1. encode the C2/Q1 pilot as a small typed graph using **existing** categories from KerML/SysML-shaped structure, OMS/SOSA observation, P-Plan/PROV plan/execution, ODRL-style permissions, and SEPIO-like claims;
2. express the phase derivation's declared and actual dependencies separately;
3. ask whether the graph can query: “what was Q1-006 allowed to know before reveal?” and “did the executable inference depend only on allowed inputs?”;
4. represent the candidate-equivalence/identifiability conclusion;
5. add a new metamodel term only where the answer cannot be expressed faithfully using the reused semantics.

If that succeeds, the result is closer to a **general scientific-modeling profile** than a new ontology stack—which is a better outcome than inventing another wheel.
