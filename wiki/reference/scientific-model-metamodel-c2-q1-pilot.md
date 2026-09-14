---
doc-role: scientific-metamodel-pilot
authority: exploratory
lifecycle: active
sources:
  - scientific-model-metamodel.md
  - scientific-model-metamodel-cc-pilot.md
  - ../../goal-discovery/docs/hypotheses/c2_001_derived_phase.md
  - ../../goal-discovery/docs/hypotheses/c2_001_derived_phase_results.md
  - ../../goal-discovery/docs/hypotheses/q1_006_pairwise_relation.md
  - ../../goal-discovery/docs/hypotheses/q1_006_pairwise_relation_results.md
  - ../../goal-discovery/src/substrate/specimens/contended_slot.py
  - ../../goal-discovery/src/substrate/contract.py
---
# Scientific metamodel pilot — one system, white-box and black-box

[Metamodel direction](scientific-model-metamodel.md) · [First CC pilot](scientific-model-metamodel-cc-pilot.md) · [Reference index](README.md)

This note performs the next concrete test: represent the C2-001 contended-channel specimen once, then place a constructive white-box study and Q1-006's restricted black-box/reveal analysis over that same underlying model. The goal is to expose which semantic machinery is general, which is already supplied by established modeling languages, and which remains a candidate gap.

This is not a replacement schema and the SysML-shaped fragments below are **semantic sketches, not validated SysML source**.

## 1. The underlying system exists independently of analyst access

The implemented specimen is a discrete state-transition system. Its shared state includes time, horizon, per-subunit needs and obtained amounts, a shared scalar signal, and specimen-specific fields such as phase, period, collision count, idle count, and number attempting. Its run loop executes a fixed sequence:

```text
initialize
  -> replenish
  -> decide
  -> optional observer callback
  -> allocate
  -> update obtained state
  -> update shared signal
  -> repeat
  -> derive RunOutcome
```

The contended-slot realization supplies the following scientific content:

```text
System: ContendedChannel

components
  Subunit[1..N]
  ContendedSlot

state / parameters
  tick
  horizon
  need[i]
  obtained[i]
  signal
  phase[i]          when phase scheduling is used
  period            currently N
  configuration parameters

derived state
  remaining[i]       = max(need[i] - obtained[i], 0)
  remaining_ticks    = horizon - tick

behavior
  decide
  allocate
  update_signal

constraints / predicates
  feasible(config) := horizon >= N * mean_need

measurement/result
  satisfaction      = fraction_i(obtained[i] >= need[i])
  signal trace
  obtained[i]
  collision/idle/served counters
```

The key modeling rule is:

> **Do not duplicate this system definition merely because different studies receive different access to it.**

C2-001 and Q1-006 are different studies/projections over a common underlying specimen family.

## 2. The mechanism should be a selected causal submodel, not an opaque label

For the `derived_phase` arm, the operative dependencies in the implementation include:

```text
period = N
phase[i] = int(need[i]) mod period
attempt[i,t] =
    remaining[i,t] > 0
    AND phase[i] == (tick mod period)

k[t] = number of attempting subunits

gain[i,t] =
    0                    if i does not attempt
    1 / k[t]^2           if i attempts and outcomes are rival
    1                    if i attempts and outcomes are non-rival
```

This makes the proposed mechanism inspectable as a dependency graph over variables, functions and processes. `Mechanism` can remain a scientific explanatory claim selecting some of this structure, but the causal/dynamical content should live in the actual model elements rather than inside a prose field.

A general scientific metamodel therefore needs to support both:

- the **model structure itself** — variables, functions, transitions, connections, conditions; and
- an **epistemic mechanism claim** that identifies some submodel as explanatory, with status such as authored, inferred, supported, hidden, or unknown.

## 3. Declared information interfaces and actual dependencies must be different objects

C2-001 is especially useful because the later audit found that the preregistered anti-smuggling claim did not match the actual implementation. The intended derivation was described as depending on one local scalar and not seeing population size, while the implemented phase calculation uses `period = cfg.n_subunits`.

This is not merely a documentation bug. It exposes a general modeling requirement.

The metamodel should distinguish:

```text
DeclaredInformationContract
    what a specification says a function/agent/procedure may depend on

ActualDependencyGraph
    which model variables/inputs the realized function actually reads

ConformanceClaim
    ActualDependencyGraph satisfies DeclaredInformationContract

VerificationEvidence
    check/audit/test supporting or refuting that conformance claim
```

The same distinction applies in physics or biology when an estimator is claimed to be blind to a variable but the implementation leaks that variable through preprocessing, calibration, a covariate, or an instrument channel.

This suggests a high-value invariant for any executable scientific model:

> **Information-access claims should be checkable against declared or extracted dependency structure, not only prose.**

## 4. There are three different observers in this one example

### System participant

A subunit is part of the modeled system. Its information access changes the dynamics. The phase arm's actual behavior depends on local remaining need/state plus clock/period/phase information; the level arm uses urgency and a shared scalar.

This is an architectural/causal interface:

```text
SystemInformationInterface
  bearer/participant : Subunit
  permits             : selected system variables/signals
  constrains          : DecisionBehavior inputs
```

### Experimental instrument / software observer

The shared execution loop optionally invokes an observer callback once per tick after `decide` and before `allocate`, passing tick, attempted actions, and state. It is declared read-only and must not draw randomness. Run outcomes then record selected aggregate and trace information.

This is measurement/instrumentation semantics:

```text
ObservationProcedure
  observes     : modeled state/action at a defined stage
  instrument   : software observer/logger
  timing       : after decision, before allocation
  noninvasive  : required
  produces     : recorded observation package
```

### Analyst / inference procedure

Q1-006 deliberately exposes a restricted package to the proposal procedure while withholding the shared signal, stock, native condition label, mechanism language and other privileged information. A later reveal phase exposes frozen-answer comparison information without permitting the proposal path to change.

This is epistemic access:

```text
AnalystAccessContract
  principal      : analysis/proposal procedure
  phase          : proposal | reveal
  mayConsume     : selected observations/model metadata
  mayNotConsume  : privileged model/data elements
  mayIntervene   : declared operation signatures only
  freezeBoundary : outputs fixed before reveal
```

These three relations must not collapse into one generic `observes` edge.

## 5. Black-box access is not just a SysML view

SysML v2 views/viewpoints are useful for selecting and rendering model information, but Q1-006 requires a stronger semantic property:

> the proposal analysis is **not permitted to depend on hidden information**.

A rendered projection can hide an element from a person while an analysis still depends on it. Scientific black-box semantics therefore need an enforceable or at least checkable **information-flow/access constraint** on the analysis inputs/dependencies.

A candidate general representation is:

```text
AccessPhase
  principal          : Agent | AnalysisProcedure
  sourceModel        : ScientificModel
  permittedKnowledge : ModelElement[*]
  permittedData      : ObservationProduct[*]
  permittedActions   : InterventionType[*]
  forbiddenInputs    : ModelElement[*]
  start/end/freeze conditions
```

The concrete black-box data package can be a projection of the full model/run data, but the access contract is a scientific constraint on admissible inference, not merely a visualization query.

## 6. One underlying model, multiple access phases

The C2-001 / Q1-006 pairing can be represented conceptually as:

```text
                        ContendedChannelSystem
                       /         |          \
                      /          |           \
             system dynamics   run data    authored semantics
                    |              |               |
                    |              |               |
          C2 constructive       instrument      native labels
          white-box study        output         and mechanism
                    |              |
                    +------ full access --------+

                    Q1-006 proposal phase
                             |
                 AccessContract: black-box
                             |
               only packaged entity-time data
                             |
                   Proposal / inference
                             |
                       frozen output
                             |
                    Q1-006 reveal phase
                             |
               reveal native condition mapping
                             |
                    Evidence assessment
```

Nothing about the underlying specimen needs to be cloned to create the black-box study.

## 7. Forward and inverse models become explicit

### Forward model

C2-001 primarily exercises the generative direction:

```text
configuration + initial state + mechanism/behavior
    -> trajectory
    -> obtained amounts / action traces / counters
    -> quota-satisfaction result
```

The constructive scientific question is whether a particular causal organization supports the declared performance under the challenge/resource family.

### Inverse model

Q1-006 exercises the inverse direction:

```text
restricted entity-time observations
    -> representation / residual construction
    -> relation statistic / proposal procedure
    -> candidate/disposition
    -> reveal comparison
    -> evidence about detectability / identifiability
```

The metamodel should not treat the inverse model as a special case of the forward dynamics. It is another model/procedure whose subject is evidence produced from the system.

## 8. The study must represent prospective dependency ordering

Both experiments rely on ordering constraints that carry epistemic meaning:

- protocol frozen before implementation/outcome;
- parameters selected without consulting protected downstream readouts;
- proposal path frozen before the specimen/package in Q1-006;
- proposal outputs frozen before reveal;
- a failed precondition/validity gate can prevent downstream interpretation.

This is stronger than provenance timestamps. The study design contains a **partial order of permitted information and decisions**.

Candidate structure:

```text
StudyStage
  consumes        : declared information available at this stage
  produces        : artifact/result
  precedes        : StudyStage
  freezes         : artifact/model element
  unlocks         : later information/access

Gate
  predicate       : Boolean-valued analysis
  evaluatedAt     : StudyStage
  onPass          : permit downstream stage/interpretation
  onFail          : disposition / stop / invalidation rule
```

This is likely general across preregistration, blinded trials, train/test splits, holdouts, staged model selection, and reveal-later studies.

## 9. A scientific model needs declaration, realization and evidence relations

C2-001 demonstrates why a single `model` layer is insufficient. We need to distinguish at least:

```text
ScientificDeclaration
  what the protocol/theory says should hold

ExecutableRealization
  the code, physical apparatus or other realization that actually generates behavior

ConformanceClaim
  realization implements/satisfies declaration

ConformanceEvidence
  tests, dependency audits, code inspection, calibration, etc.

EmpiricalResult
  observations produced by executing the realization
```

The anti-smuggling correction is precisely a refuted conformance claim: the empirical numbers remain what they were, but the stronger interpretation no longer follows because the implementation depended on information the declaration claimed to exclude.

This distinction is fundamental enough to test as a metamodel feature rather than a CC-specific convention.

## 10. SysML/KerML fit after this pilot

The following is a provisional reuse assessment, not an adoption decision.

| Requirement exposed by C2/Q1 | SysML/KerML fit | Remaining issue |
|---|---|---|
| Parts, state, parameters, connections | strong | none obvious |
| Behaviors/processes/transitions | strong | none obvious |
| Functions/equations | strong (`calc` / KerML functions) | scientific applicability metadata still needed |
| Predicates/constraints/gates | strong (`constraint`, requirements) | gate disposition semantics may need a study pattern |
| N-ary typed participant relations | strong in KerML associations | choose relation vs occurrence carefully |
| Analysis/inference procedure | strong (`analysis case`) | scientific estimator/identifiability vocabulary remains external/domain extension |
| Variants/conditions | good | experiment-family sampling/coverage semantics still need explicit treatment |
| Multiple views/projections | strong for presentation/query | **not sufficient for epistemic access enforcement** |
| Domain metadata/extensions | strong mechanism exists | metadata tags alone do not prove information-flow constraints |
| Quantities/units | standard SysML library exists; QUDT remains an interchange candidate | empirical uncertainty/calibration semantics need testing |
| Instrument/observation semantics | representable generically as parts/actions/cases | dedicated scientific measurement semantics likely benefit from SOSA/SSN alignment |
| White-/black-box access | partial | candidate metamodel extension/pattern required |
| Blind-first/reveal-later ordering | partial | candidate study-stage/freeze/access pattern required |
| Identifiability/equivalence/abstention | weak as a built-in scientific concept | likely general scientific extension |
| Declaration vs realization conformance | representable through requirements/verification | needs an explicit scientific pattern linking theory/protocol, executable realization and evidence |

SysML v2 formally supplies calculations, constraints, requirements, cases including analysis/verification cases, views/viewpoints and user-defined metadata extensions; KerML supplies the more general type/feature/function/predicate/association semantics beneath it. The current pilot suggests using those capabilities as infrastructure while keeping scientific epistemic/access semantics explicit rather than pretending a systems-engineering view automatically supplies them.

## 11. SysML-shaped sketch

This is intentionally **not claimed to parse**. It is a compact test of semantic fit against SysML concepts.

```text
part def ContendedChannelSystem {
    part subunits[1..*] : Subunit;
    part slot : ContendedSlot;

    attribute tick;
    attribute horizon;
    attribute signal;
    attribute period;

    action decide;
    action allocate;
    action updateSignal;
}

calc def DerivePhase {
    in ownNeed;
    in period;
    return phase;
}

constraint def FeasibleConfiguration {
    in horizon;
    in nSubunits;
    in meanNeed;
    // horizon >= nSubunits * meanNeed
}

analysis def QuotaSatisfactionAnalysis {
    subject system : ContendedChannelSystem;
    // consume eligible run outcomes
    // return satisfaction / competence result
}

analysis def PairwiseRelationInference {
    subject observations : RestrictedObservationPackage;
    // hidden system fields are not legal inputs under proposal access
    // return frozen candidate/disposition
}
```

What is conspicuously absent from native SysML syntax here is the semantic force of comments such as “hidden system fields are not legal inputs under proposal access.” That is exactly the point the metamodel extension/pattern must make first-class and checkable.

## 12. Candidate kernel additions exposed by this pilot

Do **not** promote these into a new standard yet. They are candidate scientific semantics that should now be searched against existing prior art.

### Access contract

A relation/policy binding a principal and study phase to permitted model/data dependencies and interventions.

### Information interface

A causal interface specifying which information a modeled participant receives as part of the system architecture.

### Scientific observation execution

A procedure/instrument execution that samples a property/state/event at a declared stage and produces an observation product without being conflated with analyst access.

### Study stage / freeze boundary

A prospective ordering construct specifying which artifacts are fixed before later information becomes accessible.

### Validity gate

A prospective predicate whose result controls whether a later analysis or interpretation is admissible.

### Declaration-realization conformance claim

A claim that an executable/physical realization respects a declared scientific interface, dependency restriction, law, procedure or protocol, supported by explicit verification evidence.

### Identifiability assertion

A claim that a target construct/model distinction is identifiable, partially identifiable, equivalent or underdetermined under a specified observation/intervention/access contract.

These may turn out to be patterns composed from existing constructs rather than metamodel primitives. The proving-ground criterion is whether repeated scientific cases need the same semantics and whether existing standards already supply them precisely.

## 13. Immediate next test

The next pass should **not add another CC concept**. It should search these newly exposed candidate semantics against established work on:

- scientific workflow/protocol and preregistration models;
- information-flow and access-control semantics;
- measurement/observation models;
- system identification and identifiability representations;
- model/implementation conformance and verification;
- experimental design and staged/blinded studies.

Then revise the candidate primitive list by deleting anything already captured well elsewhere.

The metamodel is successful if C2-001 and Q1-006 can share one system definition while the model can still state, mechanically and without prose-only caveats, **who can know what, when; what generated each observation; what each analysis was allowed to use; what was frozen before reveal; and which conclusions are warranted by the resulting evidence**.
