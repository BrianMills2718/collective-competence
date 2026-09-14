---
doc-role: scientific-metamodel-composition-probe
authority: exploratory
lifecycle: active
sources:
  - scientific-model-metamodel.md
  - scientific-model-metamodel-c2-q1-pilot.md
  - scientific-model-metamodel-prior-art.md
  - ../../goal-discovery/docs/hypotheses/c2_001_derived_phase.md
  - ../../goal-discovery/docs/hypotheses/q1_006_pairwise_relation.md
---
# Scientific metamodel composition probe — how little new semantics are needed?

[Metamodel direction](scientific-model-metamodel.md) · [Prior-art deletion audit](scientific-model-metamodel-prior-art.md) · [C2/Q1 pilot](scientific-model-metamodel-c2-q1-pilot.md)

## Question

The prior-art audit removed most proposed primitives from the “invent” column. This probe asks a stricter question:

> **Can the C2-001 / Q1-006 proving ground be represented by composing established model, measurement, workflow, policy, provenance and evidence semantics, with only a very small scientific extension?**

The answer appears to be **mostly yes**. The principal unresolved semantic object is not `System`, `Experiment`, `Observation`, `Mechanism`, `Capability`, `Claim`, or even `AccessPolicy`. It is the **identifiability/equivalence statement made relative to a model, observation/intervention regime, and access policy**.

This document is a semantic composition test, not a commitment to RDF, SysML, JSON-LD, or any other canonical serialization.

## 1. Give each scientific thing one stable identity

The first integration requirement is mundane but essential: the same scientific object must be referable from several semantic layers.

For example:

```text
cc:c2-contended-channel               underlying system/model
cc:c2-need                            model variable / quantity
cc:c2-period                          model variable / parameter
cc:c2-derived-phase                   calculation/function
cc:q1-006-restricted-package          data product
cc:q1-006-proposal-step               planned analysis step
cc:q1-006-proposal-output             frozen result artifact
cc:q1-006-proposal-access-policy      access policy
```

The profile may project those identifiers into different standards. It should not create duplicate “SysML system”, “PROV system”, “SOSA system”, and “ontology system” identities unless the distinction is scientifically real.

## 2. Underlying theory/system model — KerML/SysML + mathematical semantics

The underlying C2 specimen is represented once using general model semantics:

```text
ContendedChannelSystem
  parts
    Subunit[1..N]
    ContendedSlot
  variables
    tick, horizon
    need[i], obtained[i]
    signal
    phase[i]
    period
  calculations / predicates
    remaining[i] = max(need[i] - obtained[i], 0)
    remaining_ticks = horizon - tick
    feasible := horizon >= N * mean_need
    phase[i] = int(need[i]) mod period
  behavior
    decide -> observe(optional) -> allocate -> update state -> update signal
```

Use **KerML/SysML v2** for the model graph, typed/n-ary roles, behavior, calculations and constraints. Use **OpenMath/MathML** if expressions require portable mathematical semantics beyond the modeling tool's native expression representation. Align quantities/units with **QUDT** and mathematical-model metadata with **MathModDB** where useful.

No `Mechanism` metaclass is required. A mechanism claim selects some of this model structure as explanatory.

## 3. Observations — OMS/SOSA, not analyst access

The software observer in the shared run loop is an observation procedure over the modeled execution:

```text
ObservationExecution
  procedure    = software observer hook
  feature      = contended-channel run
  observed     = tick, attempted actions, selected state
  timing       = after decide / before allocate
  result       = recorded observation product
  constraint   = read-only; no random draw; no state mutation
```

Map this to **ISO/OGC OMS and/or SOSA/SSN** concepts. The same pattern should support a camera, assay, sensor or human-coded procedure in an empirical system.

The observation product is data. It is **not** the same as permission for an analyst to inspect all or part of that data.

## 4. Study plan and execution — P-Plan/ProvONE/PROV

Q1-006 has a prospective order that matters scientifically. Represent the plan with steps and variables/artifacts, then bind actual executions to those planned steps.

Conceptually:

```text
Plan: Q1-006

PackageRestrictedObservations
    -> Proposal
    -> FreezeProposalOutput
    -> RevealConditionMapping
    -> AssessAgainstReveal
```

A P-Plan-style representation supplies planned `Step` and input/output `Variable` structure. PROV/ProvONE supplies actual `Activity` and generated/used `Entity` relationships.

The important point is not the vocabulary name. It is that **prospective procedure and retrospective execution remain distinct but linked**.

### Freeze does not require a new metaclass

A freeze boundary can be a pattern:

```text
Proposal activity
  generates -> ProposalArtifact(hash = H)

Reveal step
  isPrecededBy -> Proposal step

Post-reveal assessment
  uses -> exact ProposalArtifact(hash = H)
```

If a post-reveal activity uses a different artifact identity/hash, the freeze contract fails. No universal `FreezeBoundary` class is required unless repeated examples show added semantics beyond ordered stages + immutable artifact identity.

## 5. Black-box access — ODRL policy bound to a study step

The Q1-006 proposal phase can be treated as a permission/prohibition policy over identified model/data assets.

Semantic sketch:

```text
Policy: q1-006-proposal-access
  assignee = PairwiseRelationInference

  permit read:
    opaque case identifiers
    per-entity cumulative accumulation
    per-tick draw
    within-run ordering
    field types
    intervention operation signatures

  prohibit read:
    shared stock
    coordinating signal
    native condition label
    mechanism names / authored semantic labels
```

Use **ODRL** for generic permissions/prohibitions, preferably as a small scientific profile rather than a new access-control language.

Bind the policy to the proposal study step. The reveal step then uses a different policy that additionally permits the frozen condition mapping.

### White-box is just a less restrictive policy

C2's constructive study can use a policy permitting the full authored system structure and state. White-box and black-box therefore do not need separate model types; they are named policy/access regimes over the same model.

## 6. Declared dependencies versus actual dependencies

C2-001 supplies a concrete negative case.

The intended phase derivation was described as local to each subunit's own need, but the realized calculation is effectively:

```text
period = n_subunits
phase[i] = int(need[i]) mod period
```

Therefore:

```text
DeclaredPermittedDependencies(DerivePhase)
  = { ownNeed }

ActualDependencies(DerivePhase)
  = { ownNeed, nSubunits }
```

and the conformance predicate is false:

```text
ActualDependencies ⊆ DeclaredPermittedDependencies
```

The metamodel does not need to define a new static-analysis engine. It needs only to make the **declared dependency contract**, the **actual/extracted dependency graph**, and the **conformance claim/evidence** addressable.

Potential reuse:

- SysML/KerML calculation inputs and dependency relationships for declared structure;
- FMI-style input/output/local/dependency semantics for executable model boundaries where applicable;
- a generated dependency artifact from language-specific static/dynamic analysis;
- a constraint/verification case evaluating the subset relation;
- SEPIO-like claim/evidence representation for the conformance conclusion.

No generic `DependencyConformanceClaim` metaclass is required unless the reusable claim/evidence model cannot express a proposition of this form.

## 7. Validity gates — constraint + planned control flow, not a new scientific object

C2's P0 and C1-002's validity gate are scientifically important, but their semantics can be composed from existing constructs:

```text
GateCheck
  evaluates -> Boolean constraint/predicate
  produces  -> pass | fail | indeterminate

DownstreamStep
  permitted/executed only if GateCheck == pass
```

The plan records the prospective dependency. The retrospective execution records whether the downstream activity occurred. The evidence layer distinguishes:

- gate failed, so downstream test invalid/not executed;
- downstream analysis executed and falsified a hypothesis;
- execution itself failed;
- data were insufficient.

That is a reusable **study-design pattern**, not necessarily a new metamodel primitive.

## 8. Claims and evidence — SEPIO + PROV rather than a new epistemology graph

Represent statements such as:

- “the phase derivation conformed to the declared input restriction”;
- “the coordination statistic discriminates the tested conditions”;
- “this stronger mechanism interpretation is not warranted”;

as scientific claims with evidence/provenance, not as properties baked into the system model.

Use **SEPIO-like** assertion/evidence structure, with PROV links to the observation/result artifacts and analyses that produced the evidence.

CC's controlled statuses (`supported`, `qualified`, `contradicted`, `underdetermined`, `not_tested`, etc.) can remain a project profile unless a broader evidence-status vocabulary fits exactly.

## 9. What cannot yet be delegated cleanly: identifiability

Q1-006 and the Goal Discovery arm require statements whose truth is indexed by the experimental/epistemic regime.

General form:

```text
Identifiability(
  target,
  candidate family,
  underlying model family,
  observation mapping,
  intervention family,
  access policy,
  noise/error assumptions
) -> status / equivalence class
```

Examples:

```text
Candidate A and Candidate B
  observationally equivalent
  under access policy X

but

Intervention Y
  distinguishes A from B
```

or:

```text
Goal criterion G
  underdetermined
  from observation package O
  under candidate family C
```

System identification, inverse problems and statistics have rigorous mathematical notions of structural/practical identifiability, observability and equivalence, but the prior-art audit did not surface a widely used general **semantic representation** for these claims across arbitrary scientific domains.

This is the strongest candidate for a thin extension.

## 10. Minimal scientific extension — candidate v0

Instead of a large bespoke metamodel, test whether the following **small vocabulary/profile** is enough on top of the reused standards.

### Identifiability assertion

```text
IdentifiabilityAssertion
  target                  ModelElement | Parameter | Construct | ModelDistinction
  candidateSet            Candidate[*]
  underModelFamily        ModelFamily
  underObservationMapping ObservationModel
  underInterventionFamily InterventionFamily
  underAccessPolicy       Policy
  underErrorModel         ErrorModel? 
  status                  identifiable
                          | partially_identifiable
                          | equivalent
                          | underdetermined
                          | not_tested
  resultingClass          EquivalenceClass?
  distinguishingAction    Intervention? 
```

This need not be one RDF class. It is the semantic information that must be representable.

### Scientific access profile

Do **not** introduce `AccessRegime` as a parallel policy language yet. Instead define a profile/convention for binding:

```text
ODRL Policy
  + study-stage identity
  + scientific model/data element identities
  + intervention/action identities
```

Only add a bespoke access object if this composition proves unable to express a real study.

### Dependency conformance pattern

Keep as a reusable validation pattern:

```text
actual dependencies
  subset-of
permitted dependencies under policy/stage
```

with a scientific claim/evidence record for the result.

## 11. Query acceptance tests on the C2/Q1 case

A concrete integrated representation should answer these mechanically.

### Q1 — What was the proposer allowed to know before reveal?

Join:

```text
Proposal study step
  -> bound access policy
  -> permissions/prohibitions
  -> model/data element identities
```

Expected answer: opaque case IDs, selected entity-time observables, ordering/types and operation signatures; not the shared signal, stock, native condition or mechanism labels.

### Q2 — Did a realized calculation actually obey its declared information restriction?

Join:

```text
calculation/procedure
  -> declared input/dependency contract
  -> realized/extracted dependency graph
  -> subset/conformance check
```

For C2's original anti-smuggling statement, the answer is **no** because `n_subunits` enters through `period`.

### Q3 — Was the proposal frozen before reveal?

Join:

```text
planned stage order
  + actual activity order
  + exact generated proposal artifact/hash
  + reveal activity
  + later use of same frozen artifact
```

### Q4 — What supports a scientific conclusion?

Join:

```text
claim
  -> evidence line
  -> result/observation artifacts
  -> analysis activity
  -> underlying study plan
  -> exact model/run identity
```

### Q5 — Which candidate distinctions are identifiable under this black-box contract?

This is the key remaining extension:

```text
IdentifiabilityAssertion
  -> candidate set/equivalence class
  -> observation mapping
  -> intervention family
  -> access policy
  -> evidence
```

## 12. Revised hypothesis

The work started with the hypothesis that Collective Competence might need a general scientific metamodel containing many new primitives.

After the first two pilots and the prior-art deletion audit, the stronger working hypothesis is now:

> **A general scientific-modeling metamodel may be mostly a disciplined composition/profile of existing formal-model, mathematics, metrology, observation, workflow, policy, provenance, and evidence semantics. The genuinely thin missing layer may concern epistemic access and identifiability relative to observations/interventions—and even access policy itself may be profile-level rather than a new ontology.**

That is a much smaller and more testable design claim.

## Next falsification test

Do not add another standard to the stack merely because it exists. Instead build a tiny machine-readable C2/Q1 instance sufficient to execute the five queries above.

A candidate implementation should fail if:

- stable identity cannot be maintained across semantic layers;
- expressing access requires copying the system model;
- policy says information is hidden but dependency verification cannot detect leakage;
- plan/execution semantics cannot establish the freeze-before-reveal claim;
- claim/evidence trace cannot distinguish invalid/unexecuted from falsified; or
- the identifiability assertion cannot distinguish observational equivalence from successful discrimination.

Only those failures justify new metamodel semantics.
