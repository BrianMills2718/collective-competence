---
doc-role: scientific-metamodel-kernel
authority: exploratory
lifecycle: active
sources:
  - scientific-model-metamodel.md
  - scientific-model-metamodel-prior-art.md
  - scientific-hypergraph-adequacy-review.md
---
# Scientific hypergraph kernel

[Metamodel direction](scientific-model-metamodel.md) · [Adequacy review](scientific-hypergraph-adequacy-review.md) · [Reference index](README.md)

## Working hypothesis

Represent the normalized scientific model as **one typed, attributed n-ary hypergraph**. Terms such as system, equation, process, measurement, experiment, access policy, analysis, claim, and evidence should normally be reusable relation/type schemas over this graph rather than independent foundational compartments.

An n-ary relation may be visualized as a relation node with role-labelled spokes. That incidence graph is a rendering of one hyperedge.

This document distinguishes the **hypergraph carrier/kernel** from the **scientific schema/profile** built on top of it. The carrier supplies identity, typing, n-ary relations, roles, incidence, and higher-order reference. The scientific profile supplies reusable semantics such as Equation, Measurement, Analysis, Access, Claim, Distribution, Representation, and Identifiability.

## Candidate carrier/kernel

The current candidate machinery is:

- `ModelElement` — anything that can participate in the normalized model.
- `ElementType` — a type of model element; still subject to ablation/minimality review.
- `RelationType` — an element type/pattern whose instances are n-ary relations; whether this requires independent primitive status is still under review.
- `RoleType` — a stable participant-role identity declared by a relation type.
- `RelationInstance` — one typed relation occurrence or assertion; relation instances are themselves model elements.
- `RoleBinding` — one assignment of a participant to a role in a relation instance.
- `Constraint`, `Expression`, `Value` — currently represented as model-element categories, but their status as irreducible carrier primitives is **not established** and is under ablation review.

The important change from the earlier prototype is that this is a **candidate kernel**, not a claim that every item listed above is irreducible.

## First-class RoleBinding semantics

A role binding is not merely an edge label.

Normalized incidence has the conceptual form:

```text
RelationInstance
      |
      | contains / owns incidence
      v
RoleBinding
   |        \
   | role    \ participant
   v          v
RoleType   ModelElement
```

In the compact v1 serialization a binding lives inside its parent relation:

```json
{
  "id": "binding:analysis-model",
  "role": "sci:analysisModel",
  "participant": "study:ModelA"
}
```

The `id` is optional. Anonymous bindings are appropriate when nothing needs to refer to the assignment itself.

When an `id` is present, the binding is a first-class addressable model element:

- its ID shares the global identity namespace with nodes and relation instances;
- other relations may use that binding ID as a participant;
- evidence, provenance, uncertainty, or a claim may target that specific assignment;
- validator connectivity includes the binding;
- the viewer materializes and inspects the binding as a semantic element.

The structural acceptance fixture `metamodel/role-binding-epistemics-hypergraph-v1.json` proves that a `ClaimRelation` can scope itself to one `analysisModel` binding rather than to the whole AnalysisRelation or model.

## Core relations and bootstrap

Core relations are themselves relation types. Representative carrier/meta relations include:

```text
instanceOf(instance, type)
specializes(subtype, supertype)
declaresRole(relationType, role, cardinality/qualifier constraints...)
```

`scientific-role-schema-v1.json` self-hosts shared scientific `RelationType -> RoleType` declarations using `sci:declaresRole`. Only that bootstrap relation and its small trusted role set must be understood before reading the rest of the schema graph.

The older conceptual `roleBinding(relation, role, participant)` form should be read as the abstract incidence semantics. v1 serializes that incidence compactly as binding records, optionally addressable by ID.

The machine-readable early kernel fixture is [`metamodel/hypergraph-kernel.jsonld`](metamodel/hypergraph-kernel.jsonld); the active typed-role semantics are exercised by `scientific-hypergraph-v1` fixtures and the self-hosted role schema.

## One connected model

Metamodel, theory, study, execution, and evidence should remain connected through typing, relation participation, and role bindings. A domain term such as `Competence` or `KineticEnergy` is normally a theory-level specialization, not a universal carrier primitive.

Relation instances and addressable RoleBindings may participate in higher-order relations. Examples now exercised in CI include:

- a measured/inferred QuantityValue relation becoming an equation input;
- a DistributionRelation becoming the stochastic driver of a PDE EquationRelation;
- a transformation relation becoming the transformation participant of a gauge-equivalence relation;
- a specific `analysisModel` RoleBinding becoming the scope of a scientific claim.

## Reusable scientific schema/profile

Representative shared relation schemas include:

```text
EquationRelation
ProcessRelation
MeasurementRelation
QuantityValueRelation
DistributionRelation
AnalysisRelation
ExperimentRelation
AccessRelation
RepresentationRelation
ClaimRelation
IdentifiabilityRelation
```

They are libraries expressed with the carrier, not new foundational compartments. Existing standards should supply or refine their semantics where possible.

Theory-specific relations may be declared locally with the same RoleType machinery. Current local examples include cell division/bond change, gauge equivalence, and lineage assignment/link relations. Local declarations extend but cannot override conflicting shared contracts.

A cross-fixture adequacy audit currently finds that roughly **93% of scientific relation instances** and **92.6% of scientific typed bindings** use the shared scientific schemas, so local extension is not presently the dominant representation mechanism.

## Views are projections

The connected hypergraph is the semantic source model. Human views are graph queries: metamodel schema, theory, study design, measurement, probability, causal structure, access-conditioned projection, evidence, representation/coarse-graining, dependency conformance, or identifiability.

A view may hide, bundle, or rearrange structure for readability but should remain derivable from the source graph.

## Collective Competence as a test

C2/Q1 appears in the same graph machinery as the other scientific cases:

- CC theory elements specialize/use general schemas;
- concrete study objects instantiate those concepts;
- actual observations, analyses, and evidence are relation instances;
- declared and realized dependencies are separate relations whose conformance can be checked;
- white-box and restricted-access studies operate over the same underlying system model.

CC remains a proving ground, not the scope of the metamodel.

## Acceptance tests

The carrier/profile combination should express in one formalism:

1. equations with typed roles and applicability conditions;
2. n-ary participant roles and cardinality/type constraints;
3. processes and relation instances that can themselves participate in evidence/provenance;
4. addressable RoleBindings when one assignment needs evidence/provenance/uncertainty;
5. measurement from target through procedure/instrument to result and uncertainty;
6. deterministic, stochastic, ODE, PDE, and field models;
7. multiple access conditions over one model;
8. planned stages and realized execution;
9. declaration-versus-realization conformance;
10. validity gates controlling downstream interpretation;
11. claims supported by relation or binding instances;
12. equivalence and identifiability relative to access/intervention conditions;
13. dynamic entity creation and contested identity through time;
14. metamodel, theory, study, and evidence as one connected component; and
15. multiple visualizations/projections generated from that graph.

## Current evidence and next gate

The current scientific fixture set has survived deterministic mechanics, continuous dynamics, stochastic processes, PDEs/random fields, multiscale representation, calibration covariance, causal equivalence/intervention, dynamic topology, gauge equivalence, and uncertain lineage without adding a carrier primitive.

That demonstrates broad **expressive adequacy**, not kernel minimality.

Next work should therefore focus on:

1. **kernel ablation** — determine whether `Constraint`, `Expression`, `Value`, `ElementType`, and independent `RelationType` status can be demoted or derived;
2. **cross-domain query acceptance** — prove important scientific questions can be asked generically over unrelated fixtures;
3. **interoperability mappings** — connect reusable schemas to established standards where that adds semantic precision;
4. **authoring economy** — separate a concise authoring syntax from the explicit normalized hypergraph representation.

A new carrier primitive should require a concrete semantic capability that cannot be represented cleanly by the surviving carrier plus reusable relation schemas.
