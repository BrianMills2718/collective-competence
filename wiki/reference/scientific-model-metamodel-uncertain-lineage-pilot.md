# Uncertain lineage / model-dependent identity pilot

[Scientific hypergraph kernel](scientific-hypergraph-kernel.md) · [Generated viewer](scientific-hypergraph-viewer.md)

## Question

Does the metamodel need a universal `Identity` or `Persistence` kernel primitive when the scientifically relevant question is itself **which observed entity at a later time should be treated as the continuation/descendant of which earlier entity**?

This pilot deliberately refuses to encode that answer as node identity.

The machine-readable fixture is:

`metamodel/uncertain-lineage-hypergraph-v1.json`

## Setup

At time `t1`, two cells are observed:

```text
A
B
```

At time `t2`, two unlabeled detections are observed:

```text
U
V
```

The tracking data alone support two competing assignments under different identity criteria:

```text
nearest-motion criterion:
  A -> U
  B -> V

morphology-continuity criterion:
  A -> V
  B -> U
```

The observation nodes remain distinct. The metamodel does **not** assert `A == U` or `A == V`.

## Local theory schema

The fixture declares two local relation types:

```text
lin:LineageLinkRelation
lin:LineageAssignmentRelation
```

`LineageLinkRelation` binds:

```text
earlier entity
later entity
identity criterion
evidence
confidence?
status
```

`LineageAssignmentRelation` is a higher-order relation over exactly two lineage-link relation instances plus the assignment criterion, score, and status.

The local contracts are declared with `sci:declaresRole` and remain outside the shared scientific schema.

## Competing identity hypotheses

Each candidate lineage mapping is built from relation instances:

```text
nearest assignment
  link -> LineageLink(A,U)
  link -> LineageLink(B,V)
  criterion -> nearest motion

morphology assignment
  link -> LineageLink(A,V)
  link -> LineageLink(B,U)
  criterion -> morphology continuity
```

This is intentionally higher-order: an assignment relation takes lineage-link relations as participants.

A shared `RepresentationRelation` constructs the candidate family from both assignment relations.

## Observational identifiability

Under the unlabeled observation phase:

- both assignments are available as candidates;
- lineage-tag information is restricted;
- the comparison analysis returns an ambiguous result;
- the `IdentifiabilityRelation` records the target mapping as **underdetermined**;
- the two assignments occupy an observational lineage-equivalence class.

The key point is that uncertainty is about the scientific identity/lineage claim, not about whether the observation nodes exist.

## Distinguishing intervention

A lineage tag is applied to cell `A` before the later observation. The later data show the tag on `U` and not `V`.

The tagged analysis compares the same two candidate assignment relations and resolves the nearest assignment.

The second `IdentifiabilityRelation` records:

```text
target              -> A/B to U/V lineage mapping
candidate family    -> same two assignments
observation model   -> lineage-tag measurement
intervention family -> lineage-tag cell A
status              -> identified by intervention
evidence            -> resolved assignment result
```

Thus persistence/identity is explicitly relative to evidence, criteria, and interventions.

## Validation result

The semantic acceptance check requires:

1. the local lineage relation types are absent from the shared scientific schema;
2. the two candidate assignments contain genuinely different lineage links;
3. the observational identifiability status is underdetermined and has an equivalence class;
4. the tagged identifiability status is identified and explicitly names the intervention;
5. removing one lineage link from an assignment violates the local `min=2,max=2` contract.

## Result

**No kernel change and no shared-schema change are required.**

The current pattern is:

```text
observed entity snapshots
        ↓
local identity / lineage hypotheses
        ↓
candidate assignment relations
        ↓
analysis + access regime
        ↓
identifiability / equivalence / intervention
```

This is preferable to treating persistence as built-in equality because different scientific theories or operational criteria may disagree about what counts as the same continuing entity.

## Implication

The kernel appears able to represent model-dependent identity by keeping ontology and epistemology separate:

- nodes represent the modeled/observed entities or states;
- relations represent proposed continuity, descent, equivalence, or identity criteria;
- claims/evidence/identifiability represent warrant for those relations.

A future kernel extension would need a stronger counterexample where this relational treatment cannot express the required scientific distinction cleanly.
