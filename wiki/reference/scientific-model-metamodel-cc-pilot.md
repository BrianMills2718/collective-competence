---
doc-role: scientific-metamodel-pilot
authority: exploratory
lifecycle: active
sources:
  - scientific-model-metamodel.md
  - ../../goal-discovery/docs/hypotheses/c1_002_contended_channel.md
  - ../../goal-discovery/docs/hypotheses/c1_002_contended_channel_results.md
  - ../../goal-discovery/docs/hypotheses/q1_006_pairwise_relation.md
---
# Scientific metamodel pilot — Collective Competence

[Metamodel direction](scientific-model-metamodel.md) · [Reference index](README.md)

This note performs the first concrete pass requested by the metamodel direction. It does not introduce a new schema. Its job is to discover which general semantic distinctions are actually required by existing Collective Competence experiments.

## Why start here

Two existing protocols expose complementary requirements:

- **C1-002 contended channel** is a compact constructive/white-box experiment with explicit system rules, mechanism, capability claim, goal criterion, intervention/control, resource limits, validity gate, and competence dimensions.
- **Q1-006 pairwise relation** consumes a constructed specimen under a **black-box proposal phase** followed by a **blind-first/reveal-later phase**, with mechanism labels and privileged state withheld during proposal.

Together they are more informative than inventing a toy example because they already contain prospective constraints, negative outcomes, and epistemic discipline.

## First finding: there are multiple observation/access relations

The current experiment contract uses related language for things that the metamodel should distinguish.

### 1. System-internal sensing / information access

In C1-002 each subunit observes only its own remaining need, the remaining ticks, and the shared scalar. It does not observe other subunits' quotas/accumulations/decisions or the stock directly.

This is part of the **modeled system architecture**. A subunit is an observer/participant inside the system and its information interface partly determines the dynamics.

### 2. Experimental instrumentation / recording

The experiment implementation records run state and result artifacts. This is the **measurement apparatus** used to produce data. In a simulator it may be software logging; in an empirical system it could be a camera, assay, detector, human observer, or other instrument.

Instrumentation should specify what property/variable it observes, by which procedure, with which sampling, units, calibration/error model when relevant, and what result it produces.

### 3. Analyst epistemic access

C1-002 declares white-box analyst access to the authored substrate, subunit rules, signal update law, parameters, and full run state.

Q1-006 instead declares a black-box proposal phase exposing opaque identifiers, selected per-entity observables, time ordering, field types, and intervention signatures while withholding the shared stock, coordinating signal, condition labels, and mechanism names. A later reveal phase exposes the condition mapping only after proposals are frozen.

This is neither the system's own sensor interface nor the physical/software instrument. It is a **scientific access policy over model/data elements**.

### Candidate distinction

The general metamodel therefore appears to need separate concepts or roles corresponding to:

```text
SystemObservationInterface
  what a modeled participant can sense/use

ObservationOrMeasurementProcedure + Instrument/Observer
  how empirical data are generated

AnalystAccessContract / AccessPhase
  what a scientist or inference procedure is permitted to know,
  observe, or intervene on at a particular stage
```

The current `observation_contract` field may legitimately project more than one of these concerns in different experiments; a future metamodel should make the roles explicit rather than assuming one universal observer.

## Second finding: white-box and black-box are projections of one system

Q1-006 strongly supports the proposed access semantics. The underlying specimen has authored structure and a known native condition, but the proposal procedure is intentionally denied that information.

The desired model shape is therefore:

```text
UnderlyingSystemModel
  parts
  state
  dynamics
  mechanism-relevant structure
  authored condition identity
       |
       +--> WhiteBoxAccessPhase
       |      exposes internal model/state
       |
       +--> BlackBoxProposalPhase
       |      exposes selected observation products only
       |
       +--> RevealPhase
              exposes frozen-answer comparison information
```

The system definition should not be cloned into a separate black-box ontology. Access phases select or hide model/data elements and constrain which inference procedures may consume them.

## Third finding: experiment validity is not hypothesis truth

C1-002 failed its prospective validity gate, so the downstream detector was never read. The result explicitly classifies this as an **invalid qualification run rather than a detector failure**.

That requires more than a generic `claim_assessment` property. The metamodel should support conditional experimental logic such as:

```text
ValidityCondition
   evaluatedBy -> Analysis/Check
   result -> pass | fail | indeterminate

DownstreamAnalysis
   permittedWhen -> ValidityCondition == pass
```

and distinguish at least:

- failure of a specimen/study to instantiate the intended test;
- failure of an instrument or analysis procedure;
- evidence against a scientific hypothesis;
- missing/insufficient data;
- a procedure deliberately not executed because a prerequisite failed.

This distinction is general experimental semantics, not a competence-specific concept.

## Fourth finding: a mechanism is probably not one primitive object

C1-002's mechanism consists of system structure and dynamics: a shared scalar, its update law, per-subunit urgency, decision rules, contention resolution, and the way those pieces interact.

Representing that as one opaque `Mechanism` node would lose the scientific content. A more useful general representation is likely a **causal/dynamical submodel** composed of:

- parts/components and their roles;
- state variables/parameters;
- functions/equations/constraints;
- processes/actions/transitions;
- connections/flows/coupling;
- initial/boundary/operating conditions.

`mechanism` can then be a **scientific claim or selected explanatory submodel** over those structures, with a separate epistemic status such as authored, observed, inferred, hidden, or unknown.

This is a candidate place where SysML/KerML structure/behavior may remove substantial homemade ontology work.

## Fifth finding: capability is conditional/modal

C1-002 defines `scarcity_tracking_coordination` by:

- a bearer/attribution boundary;
- an input/output interface;
- an operation/transformation;
- operating conditions;
- resource bounds;
- failure semantics; and
- an evidence source/status.

So `System hasCapability Capability` is too weak. The scientific claim is closer to:

```text
under conditions C and resource bounds R,
system S can perform transformation T
from interface/input I to output O,
with declared failure semantics F
```

Whether the metamodel should call this a disposition, function, modal relation, or a specialized capability contract remains open. The important result of the pilot is that its participant roles and conditions must be explicit.

## Sixth finding: goal criteria and competence dimensions map naturally to formal analysis

For C1-002:

- `quota_satisfaction` is a score/predicate over the collective state at a declared horizon;
- the challenge family defines seeds, heterogeneous needs, feasibility, routes, and one indivisible slot per tick;
- the intervention removes the signal for the entire run under a matched-seed comparator;
- attainment is a derived result over eligible trials;
- robustness is explicitly **not measured** because no perturbation family was applied.

This supports a generic separation:

```text
Criterion / Predicate / ScoreFunction
ExperimentalConditionFamily
ResourceConstraint
Intervention
Comparator
AnalysisProcedure
DerivedMeasurement / Result
```

`CompetenceProfile` is then a theory-level structured interpretation of whichever performance dimensions were actually measured, rather than a metamodel primitive that every scientific domain must adopt.

## Provisional model skeleton

The following is semantic scaffolding, not proposed syntax:

```text
ScientificModel
  SystemDefinition
    parts/components
    variables/parameters
    equations/functions/constraints
    processes/transitions
    boundaries/environment

  StudyDesign
    subject/focal system
    access phases
    observation/measurement procedures
    instruments/observers
    interventions
    condition families
    comparators
    validity conditions / stop conditions

  AnalysisDefinition
    inputs
    representation/transformation
    estimator/statistic/predicate
    assumptions
    outputs/results
    prerequisite gates

  EpistemicLayer
    hypotheses/claims
    predictions
    evidence
    uncertainty
    provenance
    identifiability/equivalence
    assessment/review status
```

Each item above must still be justified against established standards; none is promoted to a bespoke class merely because it appears in this sketch.

## Immediate standards questions exposed by the pilot

1. **KerML/SysML v2:** Can one underlying system definition be projected through multiple access phases while keeping behavior, calculations, constraints, cases, and n-ary participant roles explicit?
2. **SOSA/SSN:** Does its distinction among observer/sensor, procedure, execution, observed property, feature of interest, and result cleanly cover the instrumentation layer without confusing it with analyst epistemic access?
3. **QUDT:** Can quantities/units/dimensions be reused directly for resource, urgency, time, and measured result semantics?
4. **Identifiability/access:** Which existing standard, if any, already models allowed-information contracts, hidden variables, observational equivalence, and distinguishing interventions? This currently looks less obviously covered than system structure or measurement.
5. **Validity/conditional inference:** Do SysML analysis/verification cases or another scientific workflow standard capture the semantics of prospective gates that determine whether downstream analyses are interpretable or even permitted to execute?

## Next concrete test

Use the **C2-001/Q1-006 pairing** as the next instance because it naturally exercises one underlying constructed system through a restricted black-box proposal phase and a later reveal phase.

The test should encode, without duplicating the specimen:

1. the full authored system/dynamics;
2. the system's own information interfaces;
3. the instrumentation that records entity trajectories;
4. the black-box analyst access projection;
5. the proposal/analysis procedure and candidate family;
6. the frozen result before reveal;
7. the reveal mapping and subsequent evidence assessment; and
8. the fact that different latent mechanisms may remain observationally equivalent under the restricted access contract.

If this requires CC-specific metamodel machinery merely to express access, observation, analysis, or evidence, record that as a candidate gap. If established constructs express it cleanly, reuse them and keep CC-specific semantics at the model/theory level.
