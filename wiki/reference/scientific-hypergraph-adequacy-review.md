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

The evaluation standard must now move from *representability* to *semantic economy, reuse, validation power, compositionality, interoperability, and scientific queryability*.

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
- higher-order composition in which relation instances participate in other relations.

The validator also rejects concrete malformed models, including violations of shared and theory-local role cardinalities. The viewer derives multiple projections from the same graph and keeps fixture-local identities isolated.

These are real results.

## What the current tests do **not** establish

### 1. The hypergraph kernel is not yet a scientific metamodel by itself

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

Calling the carrier universal does not make its scientific semantics universal.

### 2. Local schemas are both a feature and an escape hatch

Theory-local `RelationType` declarations are necessary for extensibility. But if every difficult distinction is solved by inventing a local relation, the shared scientific schema becomes vacuous.

A local schema is justified when the relation is genuinely theory-specific. A relation should be considered for promotion into the shared scientific schema when it:

1. recurs across independent domains;
2. supports the same scientific queries in those domains;
3. has stable role semantics and constraints;
4. maps coherently to established standards; and
5. reduces authoring/query complexity rather than merely centralizing vocabulary.

No promotion should occur merely because a relation is interesting.

### 3. Current success says little about semantic compression

A good metamodel should let heterogeneous sciences reuse a relatively small set of scientific relations. We therefore need to measure:

- how many relation instances use shared versus local schemas;
- how many domains reuse each shared relation type;
- how many local relation types are introduced per fixture;
- how many typed bindings are explained by shared roles;
- whether shared schemas remain stable as new domains arrive.

The accompanying adequacy audit reports these statistics. They are initially diagnostic, not pass/fail thresholds.

### 4. Kernel minimality has not been demonstrated

The current list is:

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

Some of these may be reducible to schemas/types over a smaller carrier.

In particular:

- `RelationType` may simply be a specialization of `ElementType` with declared roles;
- `Constraint`, `Expression`, and `Value` may belong in reusable libraries or payload semantics rather than the irreducible carrier;
- `RoleBinding` is conceptually central, but its implementation is currently inconsistent with the prose kernel (see below).

The next minimality test should be **ablation**, not another domain fixture: remove or demote a proposed primitive and determine exactly which required semantics become impossible or materially worse.

## Concrete implementation inconsistency: RoleBinding is not fully first-class yet

The kernel document says:

> `RoleBinding` binds one relation instance, one role type, and one participant.

and treats relation/binding structure as first-class semantic machinery.

However, `scientific-hypergraph-v1` currently serializes bindings as nested objects inside a hyperedge:

```json
{
  "role": "sci:eqInput",
  "qualifier": "mass",
  "participant": "h:mass-value"
}
```

A binding may carry an optional `id`, but the current validator's participant-resolution graph includes node and hyperedge IDs, not binding IDs. Therefore another relation cannot yet say, for example:

```text
ClaimRelation
  proposition -> “this particular role assignment is uncertain”
  evidence    -> tracking result
  scope       -> binding-123
```

This matters scientifically. Sometimes the epistemic object is not the participant or the whole relation but the **assignment of a participant to a role**:

- uncertain entity-to-track association;
- disputed causal-role assignment;
- inferred parameter-to-model correspondence;
- provenance for one input binding of a calculation;
- confidence in one component-to-function assignment.

The current fixtures often avoid this by reifying the disputed assignment as another relation instance. That is legal, but it does not prove that `RoleBinding` is genuinely first-class.

### Decision gate

We should choose one of two coherent designs:

**A. First-class RoleBinding**

- every binding may have a stable ID;
- binding IDs are valid relation participants;
- evidence/provenance/claims can target a binding directly;
- the viewer can inspect inbound relations to a binding;
- validator connectivity and identity rules include bindings.

**B. RoleBinding is serialization structure, not a kernel ModelElement**

- remove `RoleBinding` from the irreducible kernel claim;
- require scientifically meaningful assignments to be represented as relation instances when they need identity/evidence/provenance.

The current design implicitly claims A while implementing something closer to B. This should be resolved before claiming kernel stability.

## Stronger adequacy gates

Future acceptance should evaluate these dimensions separately.

### A. Expressive adequacy

Can the model state the required scientific distinction without lossy hacks?

Current evidence: strong.

### B. Constraint power

Can malformed/invalid instances be rejected mechanically rather than by prose convention?

Current evidence: improving; role/cardinality enforcement is real, but many scientific assumptions remain opaque nodes/expressions.

### C. Semantic compression

Do heterogeneous domains reuse stable scientific schemas rather than inventing equivalent local relations?

Current evidence: unmeasured until the adequacy audit is run consistently.

### D. Compositionality

Can outputs/results/relations become inputs/evidence/models for other relations without wrapper-specific machinery?

Current evidence: strong; many fixtures exercise higher-order relation participation.

### E. Query invariance

Can important scientific questions be asked generically across domains?

Examples:

```text
Which analyses consumed measured rather than authored quantities?
Which claims rely on a restricted access regime?
Which parameters were inferred rather than fixed?
Which equivalence classes can be broken by an intervention?
Which measurements contribute to this derived quantity?
```

Current evidence: partial. Named viewer projections are a start, but a query/test API should eventually make this explicit.

### F. Representation independence

Can equivalent serialization/layout choices preserve semantic identity and query results?

Current evidence: partial. v0→v1 migration equivalence and view projections help, but canonical semantic normalization is not yet formally specified.

### G. Interoperability

Can the scientific schemas map to mature external standards without semantic distortion?

Current evidence: conceptual prior-art mappings exist; executable mappings are still limited.

### H. Authoring economy

Can a scientist/modeler express a normal study without excessive relation boilerplate?

Current evidence: weak. The fixtures are intentionally explicit and may be too verbose for authoring. A higher-level authoring syntax may be needed while retaining the hypergraph as normalized form.

### I. Minimality

Does each claimed kernel primitive enable something that cannot be cleanly reduced to the others?

Current evidence: weak. This requires ablation tests.

## Recommended next work

Stop expanding the domain catalogue temporarily.

1. Run a cross-fixture **schema-reuse / semantic-compression audit**.
2. Resolve the `RoleBinding` first-classness inconsistency with a targeted test.
3. Perform kernel **ablation tests** for `RoleBinding`, `Constraint`, `Expression`, `Value`, and possibly `ElementType`.
4. Define a small cross-domain **query acceptance suite**.
5. Only then decide whether the current carrier deserves to be called the stable kernel of the scientific metamodel.

## Current conclusion

The evidence supports the following narrower claim:

> A typed n-ary hypergraph is a promising normalized carrier for the scientific metamodel, and the current shared scientific schemas compose across a broad set of adversarial examples.

The evidence does **not yet** support:

> The current list of kernel primitives is proven minimal, or the current schema layer is proven scientifically sufficient.

That distinction should remain explicit in PR #79 and subsequent design decisions.
