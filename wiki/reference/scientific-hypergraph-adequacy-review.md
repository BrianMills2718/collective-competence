---
doc-role: scientific-metamodel-adequacy-review
authority: exploratory
lifecycle: active
---
# Scientific hypergraph adequacy review

[Hypergraph kernel](scientific-hypergraph-kernel.md) · [Generated viewer](scientific-hypergraph-viewer.md) · [Prior-art audit](scientific-model-metamodel-prior-art.md)

## Why this review exists

The current stress-test record is encouraging, but it is also easy to overinterpret.

A typed n-ary hypergraph is an extremely general representation substrate. With sufficiently unconstrained local `RelationType` and `RoleType` declarations, it can encode almost arbitrary structured data. Therefore:

> **“A domain can be encoded without adding a kernel primitive” is necessary evidence of expressive adequacy, but it is weak evidence that the scientific metamodel is good.**

The evaluation standard must move from *representability* to *semantic economy, reuse, validation power, compositionality, interoperability, scientific queryability, and minimality*.

## What the current tests do establish

The v1 fixtures demonstrate that one representation can carry, without duplicating the semantic substrate:

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
- higher-order composition in which relation instances participate in other relations;
- evidence/claims that target one specific role assignment through an addressable `RoleBinding`.

The validator rejects malformed models, including violations of shared and theory-local role cardinalities, unresolved binding targets, duplicate binding IDs, and node/relation/binding identity collisions. The viewer derives multiple projections from the same graph and keeps fixture-local identities isolated.

These are real results.

## Carrier versus scientific semantics

`ModelElement + typed n-ary relation + roles` is closer to a **meta-representation substrate** than a complete scientific metamodel. Scientific value comes from the stable reusable schemas, constraints, queries, and alignments layered over it.

The project should therefore distinguish explicitly:

```text
Hypergraph carrier/kernel
    ↓
Scientific schema/profile
    ↓
Theory/domain schema
    ↓
Study/evidence instance
```

Calling the carrier general does not make its scientific semantics general. The shared schema/profile is what must demonstrate scientific reuse.

## Local schemas: extensibility versus escape hatch

Theory-local `RelationType` declarations are necessary for extensibility. But if every difficult distinction were solved by inventing a local relation, the shared scientific schema would become vacuous.

A local schema is justified when the relation is genuinely theory-specific. A relation should be considered for promotion into the shared scientific schema when it:

1. recurs across independent domains;
2. supports the same scientific queries in those domains;
3. has stable role semantics and constraints;
4. maps coherently to established standards; and
5. reduces authoring/query complexity rather than merely centralizing vocabulary.

No promotion should occur merely because a relation is interesting.

### Measured result: local schemas are not dominating

`audit_scientific_hypergraph_adequacy.py` currently reports across the 13 scientific fixtures:

```text
scientific relation instances: 128
  shared-schema: 119 = 93.0%
  local-schema:    9 =  7.0%

scientific typed bindings: 691
  shared-schema: 640 = 92.6%
  local-schema:   51 =  7.4%
```

The local relations are concentrated in the deliberately theory-specific tests:

```text
topo:DivisionRelation
topo:BondChangeRelation
gauge:GaugeEquivalenceRelation
lin:LineageAssignmentRelation
lin:LineageLinkRelation
```

Meanwhile the reusable scientific relations show broad cross-domain reuse:

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

This does **not** prove the schema is optimal, but it materially weakens the concern that representability is being purchased mainly through bespoke local relations.

## Resolved design decision: RoleBinding is first-class when addressable

The earlier implementation contradicted the kernel prose: `RoleBinding` was described as a first-class `ModelElement`, while v1 serialized bindings only as nested objects and did not allow other relations to target a binding ID.

We chose the first-class design and implemented it.

A binding may remain anonymous when no scientific object needs to refer to it. When a binding has an `id`:

- the ID shares the global identity namespace with nodes and relation instances;
- another relation may use the binding ID as a participant;
- validator connectivity includes the binding as incidence structure;
- missing binding references fail validation;
- duplicate binding IDs fail validation;
- node/relation/binding identity collisions fail validation;
- the viewer materializes the binding as a `roleBinding` element;
- the inspector exposes parent relation, canonical `RoleType`, qualifier, participant, and inbound relations targeting the binding.

The structural fixture `role-binding-epistemics-hypergraph-v1.json` demonstrates:

```text
AnalysisRelation
  analysisModel -> ModelA
      ^
      |
  addressable RoleBinding
      ^
      |
ClaimRelation.scope
```

This is scientifically useful when the epistemic object is not a whole relation or participant, but one assignment of a participant to a role—for example a disputed causal-role assignment, uncertain entity-to-track association, parameter-to-model correspondence, or provenance for one calculation input.

The prose and implementation now agree on `RoleBinding`.

## What the current tests still do **not** establish

### Kernel minimality has not been demonstrated

The current claimed list is:

```text
ModelElement
ElementType
RelationType
RoleType
RelationInstance
RoleBinding
Constraint
Expression
Value
```

Some items may be reducible to schemas/types over a smaller carrier.

In particular:

- `RelationType` may be a specialization/pattern of `ElementType` plus role declarations rather than an independent irreducible category;
- `Constraint`, `Expression`, and `Value` may belong in reusable libraries or payload semantics rather than the irreducible carrier;
- `ElementType` may itself be representable through a more uniform typing relation, depending on what metamodel-level guarantees we actually require.

`RoleBinding` now has stronger evidence for retention because direct epistemic reference to one role assignment is both implemented and tested.

The next minimality test should be **ablation**, not another domain fixture: remove or demote a proposed primitive and determine exactly which required semantics become impossible or materially worse.

## Stronger adequacy gates

### A. Expressive adequacy

Can the model state the required scientific distinction without lossy hacks?

Current evidence: strong across the current domain set.

### B. Constraint power

Can malformed/invalid instances be rejected mechanically rather than by prose convention?

Current evidence: meaningful role/cardinality/type/reference enforcement exists; many domain assumptions still remain expressions or assertions rather than executable checks.

### C. Semantic compression

Do heterogeneous domains reuse stable scientific schemas rather than inventing equivalent local relations?

Current evidence: encouraging. About 93% of scientific relations and bindings in the current fixture set use shared schemas.

### D. Compositionality

Can outputs/results/relations/bindings become inputs, evidence, models, drivers, or claim targets without wrapper-specific machinery?

Current evidence: strong. Relation instances and now addressable RoleBindings participate directly in higher-order relations.

### E. Query invariance

Can important scientific questions be asked generically across domains?

Examples:

```text
Which analyses consumed measured rather than authored quantities?
Which claims rely on a restricted access regime?
Which parameters were inferred rather than fixed?
Which equivalence classes can be broken by an intervention?
Which measurements contribute to this derived quantity?
Which claims target a particular role assignment rather than a whole relation?
```

Current evidence: partial. Named viewer projections are useful, but a machine-tested cross-domain query API is still needed.

### F. Representation independence

Can equivalent serialization/layout choices preserve semantic identity and query results?

Current evidence: partial. Exact v0→v1 migration regression and derived viewer projections help, but canonical semantic normalization is not yet formally specified.

### G. Interoperability

Can the scientific schemas map to mature external standards without semantic distortion?

Current evidence: conceptual prior-art mappings exist; executable mappings remain limited.

### H. Authoring economy

Can a scientist/modeler express a normal study without excessive relation boilerplate?

Current evidence: weak. The fixtures are intentionally explicit and are probably too verbose as an authoring format. A higher-level authoring syntax may be desirable while retaining v1 as normalized form.

### I. Minimality

Does each claimed kernel primitive enable something that cannot be cleanly reduced to the others?

Current evidence: unresolved. `RoleBinding` now has a concrete retained capability; the other questionable primitives need ablation tests.

## Recommended next work

Stop expanding the domain catalogue temporarily.

1. Perform kernel **ablation tests** for `Constraint`, `Expression`, `Value`, `ElementType`, and the independent status of `RelationType`.
2. Define a small cross-domain **query acceptance suite** and run it against multiple fixtures.
3. Use the query suite to judge whether a local relation should be promoted to shared schema.
4. Add executable external-standard mappings only where they improve interoperability or validation.
5. Revisit authoring syntax separately from normalized representation.

## Current conclusion

The evidence supports:

> A typed n-ary hypergraph is a promising normalized carrier for the scientific metamodel, and the current shared scientific schema is doing substantial cross-domain work rather than merely delegating semantics to local extensions.

The evidence still does **not** support:

> The current list of kernel primitives is proven minimal, or the current schema layer is proven scientifically complete.

That distinction remains a deliberate design constraint for PR #79.
