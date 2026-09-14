---
doc-role: scientific-metamodel-adequacy-review
authority: exploratory
lifecycle: active
---
# Scientific hypergraph adequacy review

[Hypergraph kernel](scientific-hypergraph-kernel.md) · [v2 normalization probe](scientific-hypergraph-normalization-v2-probe.md) · [Generated viewer](scientific-hypergraph-viewer.md) · [Prior-art audit](scientific-model-metamodel-prior-art.md)

## Why this review exists

A typed n-ary hypergraph is an extremely general representation substrate. With sufficiently unconstrained local `RelationType` and `RoleType` declarations, it can encode almost arbitrary structured data. Therefore:

> **“A domain can be encoded without adding a kernel primitive” is necessary evidence of expressive adequacy, but weak evidence that the scientific metamodel is good.**

The evaluation standard has therefore moved from mere representability to:

- semantic economy and cross-domain reuse;
- mechanical validation power;
- higher-order compositionality;
- query invariance;
- representation independence;
- interoperability with established standards;
- authoring economy; and
- kernel minimality.

## Current architecture

The project now distinguishes four levels without splitting them into separate semantic stores:

```text
Hypergraph carrier/kernel
    ↓
Shared scientific schema/profile
    ↓
Theory/domain schema
    ↓
Study/evidence instances
```

The carrier is a meta-representation substrate. The reusable scientific profile is where Equation, Measurement, Analysis, Distribution, Representation, Access, Claim, Identifiability, Experiment, QuantityValue, and similar scientific semantics live.

## What the current tests establish

The current v1 scientific fixtures carry, in one representation:

- deterministic equations and continuous dynamics;
- stochastic processes and random fields;
- PDEs, spatial domains, operators, and boundary conditions;
- measurement, instruments, observations, derived quantities, and uncertainty;
- experimental interventions and access-conditioned analysis;
- causal observational equivalence and distinguishing interventions;
- multiscale/coarse-grained representations;
- correlated calibration uncertainty;
- dynamic topology and entity creation;
- gauge-equivalent representations with preserved invariants;
- uncertain/model-dependent lineage identity;
- higher-order composition in which relation instances participate in other relations; and
- evidence/claims targeting one specific role assignment through an addressable `RoleBinding`.

The validator rejects malformed models including shared/local role-cardinality violations, unresolved participants, unresolved binding targets, duplicate binding IDs, and node/relation/binding identity collisions.

These are real results, but they do not by themselves prove that the carrier is minimal or the profile complete.

## Local schemas: extensibility versus escape hatch

Theory-local RelationTypes are necessary for extensibility, but would make the shared profile vacuous if most difficult distinctions were solved locally.

The measured result does **not** show that failure mode.

Across the 13 scientific fixtures:

```text
scientific relation instances: 128
  shared-schema: 119 = 93.0%
  local-schema:    9 =  7.0%

scientific typed bindings: 691
  shared-schema: 640 = 92.6%
  local-schema:   51 =  7.4%
```

The local relations are concentrated in intentionally theory-specific cases:

```text
topo:DivisionRelation
topo:BondChangeRelation
gauge:GaugeEquivalenceRelation
lin:LineageAssignmentRelation
lin:LineageLinkRelation
```

Shared relation reuse is broad:

```text
EquationRelation       23 instances / 11 domains
AnalysisRelation       21 / 11
MeasurementRelation    14 / 10
QuantityValueRelation  32 / 8
DistributionRelation    6 / 5
RepresentationRelation  5 / 4
AccessRelation          6 / 3
ClaimRelation           5 / 3
IdentifiabilityRelation 5 / 3
ExperimentRelation      2 / 2
```

This does not prove optimality, but it is evidence that the shared scientific profile is doing substantial semantic work rather than merely delegating difficult cases to bespoke local schemas.

A local relation should be considered for promotion only when it recurs across independent domains, supports the same queries, has stable role semantics, maps coherently to standards, and reduces modeling/query complexity.

## Resolved design decision: RoleBinding is first-class when addressable

The earlier implementation described RoleBinding as first-class while serializing it only as nested structure. That inconsistency is now resolved.

A binding may remain anonymous when no external reference is needed. When it has an `id`:

- the ID shares the global namespace with nodes and relation instances;
- another relation may target that binding directly;
- validator connectivity includes it;
- unresolved binding references fail;
- duplicate/colliding binding IDs fail;
- the viewer materializes it as a `roleBinding` element; and
- the inspector exposes parent relation, canonical RoleType, qualifier, participant, and inbound relations.

The structural fixture demonstrates a ClaimRelation scoped to one specific `analysisModel` assignment rather than to the whole AnalysisRelation or model.

This gives RoleBinding a concrete carrier-level capability: the epistemic object can be one participant-to-role assignment.

## Kernel ablation result

Ablation now gives evidence about the proposed kernel list rather than relying on names.

Current measured result:

```text
RelationType node-kind markers demoted:  8  -> fixtures still validate
RoleType node-kind markers demoted:     21  -> fixtures still validate
ElementType/type markers demoted:       89  -> fixtures still validate

Expression/Constraint/Value kind markers erased: 85
```

Erasing Expression/Constraint/Value kinds initially breaks only scientific-schema participant-kind checks. If those checks are relaxed to generic model elements, all 13 scientific fixtures validate.

Interpretation:

- **relation-schema identity remains necessary**, but `kind: relationType` is not an irreducible carrier feature;
- **role identity/declaration remains necessary**, but `kind: roleType` is not an irreducible carrier feature;
- `ElementType` as a dedicated serialization/node-kind category is not currently structurally necessary;
- Expression, Constraint, Value, Instrument, Method, Procedure, etc. behave like shared scientific/profile types, not incidence machinery;
- first-class RoleBinding has stronger evidence for retention because direct epistemic reference to one assignment is both useful and mechanically tested.

### Reduced-carrier candidate

The evidence now motivates a smaller carrier candidate:

```text
ModelElement identity
RelationInstance
RoleBinding

plus graph/bootstrap semantics for:
  type assignment / specialization
  relation-schema identity
  role identity / declaration
```

`RelationInstance.type` and `RoleBinding.role` remain structural pointers in the current proposal because they are needed to interpret incidence records without an infinite bootstrap regress.

v1 has **not** been rewritten to this candidate. Its explicit kind markers remain useful authoring/diagnostic annotations while semantic normalization is tested.

## Cross-domain query acceptance

Queryability is now machine-tested rather than inferred from diagrams.

The current query suite finds:

```text
analyses consuming direct measurement results: 9 domains
inferred QuantityValue outputs:                 7 domains
fixed equation-parameter QuantityValues:        6 domains
intervention-breakable equivalence:             2 domains
restricted-access-scoped claims:                causal observational case
addressable-RoleBinding-scoped claims:          structural binding fixture
```

The intervention/equivalence query exposed an important modeling rule:

> observational and interventional identifiability should remain separate access-relative assertions.

The generic query joins them by common `(target, candidate family)` rather than forcing observational equivalence and a distinguishing intervention into one overloaded IdentifiabilityRelation.

This is a useful acceptance invariant for future normalization or serialization changes.

## Graph-native semantic typing probe

Ablation shows that authoring `kind` categories should not automatically be carrier primitives. The next probe therefore asks whether they can compile into graph-native semantic types.

The target transformation is:

```text
v1 authoring:
  node.kind = expression
  node.type = phys:Velocity

normalized semantic graph:
  instanceOf(node, sci:Expression)
  instanceOf(node, phys:Velocity)
```

The branch now contains an exploratory semantic type profile graph whose nodes include:

```text
sci:ModelElement
sci:Expression
sci:Constraint
sci:Value
sci:Uncertainty
sci:DataArtifact
sci:Instrument
sci:Method
sci:Procedure
sci:Operator
sci:Assumption
...
```

These are explicitly **profile/schema types, not carrier primitives**.

Two executable probes are staged:

1. `probe_semantic_participant_types.py` removes node `kind` from an in-memory form and validates participant constraints against semantic type identities.
2. `probe_graph_native_typing.py` goes further: it removes both node `kind` and node-level `type`, materializes them as ordinary `sci:instanceOf` relations, and requires selected scientific query outputs to remain identical before/after normalization.

The old authoring category `element` is interpreted as the carrier top `sci:ModelElement`, which every node, RelationInstance, and addressable RoleBinding inhabits structurally.

### Current execution status

The first semantic-index run correctly exposed a missing authoring-category mapping (`assumption`), which led to moving the canonical mapping into the graph-native semantic type profile rather than maintaining a brittle Python enumeration.

Subsequent GitHub Actions runs have been unable to execute because GitHub is creating both jobs with zero steps and `runner_id: 0`; this is runner allocation failure, not a semantic-test result. v1 therefore remains authoritative until the executable normalization gates run successfully.

## Adequacy dimensions

### Expressive adequacy

Current evidence: strong across the current domain set.

### Constraint power

Current evidence: meaningful role/cardinality/reference/type enforcement; many domain assumptions are still declarative expressions rather than executable checks.

### Semantic compression

Current evidence: encouraging; about 93% of scientific relations and bindings use shared schemas.

### Compositionality

Current evidence: strong. Relations and addressable RoleBindings can participate directly in higher-order scientific relations.

### Query invariance

Current evidence: now meaningful. Several cross-domain scientific queries are executable and will serve as normalization invariants.

### Representation independence

Current evidence: improving. Exact v0→v1 migration is tested, viewer projections are derived, and graph-native v2 normalization probes are staged. Full normalized equivalence is not yet green.

### Interoperability

Current evidence: conceptual crosswalks exist; executable external-standard mappings remain limited.

### Authoring economy

Current evidence: weak. v1 is intentionally explicit and likely too verbose as an authoring surface. A higher-level syntax should be considered separately from normalized semantics.

### Minimality

Current evidence: substantially improved. Ablation argues against treating ElementType/RelationType/RoleType markers and Expression/Constraint/Value categories as irreducible carrier syntax. The graph-native normalization probe is the next decisive test.

## Recommended next work

1. Get both semantic-typing probes green once CI runner allocation recovers.
2. Require graph-native normalization to preserve the cross-domain query signatures.
3. If green, define a concrete reduced-carrier v2 normalized form while keeping v1 as authoring/backward-compatibility input.
4. Make the viewer consume normalized form through the same projection API.
5. Add executable external-standard mappings only where they improve interoperability or validation.
6. Design a higher-level authoring syntax separately; do not pollute the normalized carrier for convenience.

## Current conclusion

The evidence now supports a stronger but still bounded claim:

> Typed n-ary incidence with first-class relation and binding identity is a promising normalized carrier, and the current shared scientific profile demonstrates substantial cross-domain reuse, validation, compositionality, and queryability.

The evidence does **not yet** support:

> The reduced carrier has completed executable graph-native normalization, or the scientific profile is complete/optimal.

That remaining distinction is the current design gate for PR #79.
