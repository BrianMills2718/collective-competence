---
doc-role: scientific-metamodel-kernel
authority: exploratory
lifecycle: active
sources:
  - scientific-model-metamodel.md
  - scientific-model-metamodel-prior-art.md
---
# Scientific hypergraph kernel

[Metamodel direction](scientific-model-metamodel.md) · [Reference index](README.md)

## Working hypothesis

Represent a scientific model as **one typed, attributed n-ary hypergraph**. Terms such as system, equation, process, measurement, experiment, access policy, analysis, claim, and evidence should normally be reusable relation/type schemas over this graph rather than independent foundational compartments.

An n-ary relation may be visualized as a relation node with role-labelled spokes. That incidence graph is a rendering of one hyperedge.

## Minimal kernel v0

- `ModelElement` — anything that can participate in the model; relation instances are also model elements.
- `ElementType` — a type of model element.
- `RelationType` — an element type whose instances are n-ary relations.
- `RoleType` — a named participant role declared by a relation type.
- `RelationInstance` — one typed relation occurrence or assertion.
- `RoleBinding` — binds one relation instance, one role type, and one participant.
- `Constraint` — a condition over elements, roles, bindings, values, or relations.
- `Expression` / `Value` — formal or literal content used by constraints and scientific schemas.

Core relations are themselves relation types:

```text
instanceOf(instance, type)
specializes(subtype, supertype)
declaresRole(relationType, role)
roleBinding(relation, role, participant)
constrainedBy(subject, constraint)
expressedBy(subject, expression)
```

The machine-readable fixture is [`metamodel/hypergraph-kernel.jsonld`](metamodel/hypergraph-kernel.jsonld).

## One connected model

Metamodel, theory, study, execution, and evidence should remain connected through typing, specialization, and role bindings. A domain term such as `Competence` or `KineticEnergy` is normally a theory-level specialization, not a universal kernel primitive.

Relation instances must also be model elements so they can participate in higher-order relations. For example, a measurement relation may be evidence for a claim relation, and an access relation may govern an analysis relation.

## Reusable schema layer

Representative relation schemas include:

```text
EquationRelation(
  input*, output*, expression,
  assumption*, regime*, referenceFrame?
)

ProcessRelation(
  participant*, input*, output*,
  precondition*, effect*, startTime?, endTime?
)

MeasurementRelation(
  subject, measurand, procedure, instrument*,
  observation*, result, uncertainty?, conditions*
)

ExperimentRelation(
  subject*, intervention*, condition*, comparator*,
  observation*, analysis*, validityGate*, result*
)

AccessRelation(
  accessor, phase, allowed*, restricted*, allowedAction*
)

ClaimRelation(
  proposition, evidence*, counterevidence*, scope*, status
)

IdentifiabilityRelation(
  target, candidateFamily, access, observationModel,
  interventionFamily?, equivalenceClass?, status, evidence*
)
```

These are libraries expressed with the kernel. Existing standards should supply or refine them where possible.

## Views are projections

The giant connected hypergraph is the semantic model. Human views are graph queries: metamodel schema, theory, study design, measurement, causal structure, access-conditioned projection, evidence, dependency conformance, or identifiability. A view may hide detail for readability but should remain derivable from the source graph.

## Collective Competence as a test

C2/Q1 should appear in the same graph under the metamodel:

- CC theory elements specialize general types/relation schemas;
- concrete study objects instantiate those CC/general types;
- actual observations, analyses, and evidence are relation instances;
- declared and realized dependencies are separate relations whose conformance can be checked;
- white-box and restricted-access studies operate over the same underlying system graph.

## Acceptance tests

The kernel should express in one formalism:

1. equations with typed roles and applicability constraints;
2. n-ary participant roles and cardinality/type constraints;
3. processes that can themselves participate in evidence/provenance;
4. measurement from target through procedure/instrument to result and uncertainty;
5. multiple access conditions over one model;
6. planned stages and realized execution;
7. declaration-versus-realization conformance;
8. validity gates controlling downstream interpretation;
9. claims supported by relation instances;
10. equivalence and identifiability relative to access/intervention conditions;
11. metamodel, theory, study, and evidence as one connected component; and
12. multiple visualizations generated from that graph.

## Next

Re-express the C2/Q1 fixture with explicit relation instances and role bindings, then render a single interactive incidence graph with layer filters for metamodel, CC theory, study instance, and evidence. After that, instantiate the same kernel with a compact classical-mechanics example as a cross-domain check.
