---
doc-role: scientific-metamodel-kernel-ablation
authority: exploratory
lifecycle: active
---
# Scientific hypergraph kernel ablation

[Kernel](scientific-hypergraph-kernel.md) · [Adequacy review](scientific-hypergraph-adequacy-review.md) · [Viewer](scientific-hypergraph-viewer.md)

## Question

The stress tests show broad expressive coverage, but a general carrier can accumulate unnecessary categories simply because they are convenient names.

This audit asks a narrower question:

> Which proposed kernel categories are actually required by the normalized incidence semantics and validator, and which can be demoted to ordinary schema/type semantics?

The executable audit is `scripts/audit_kernel_ablation.py`.

## Results

Across the current v1 fixtures:

```text
PASS RelationType marker
  8 relationType node-kind markers -> type
  local/shared role declarations still validate

PASS RoleType marker
  21 roleType node-kind markers -> type
  typed bindings/declarations still validate

PASS ElementType marker
  89 type node-kind markers -> element
  fixtures still validate structurally

PASS payload-category ablation
  85 expression/constraint/value markers -> element
  direct validation rejects 11 fixtures because shared schemas constrain those kinds
  after changing only those participant-kind contracts to generic element,
  all 13 scientific fixtures validate
```

## Interpretation

### RelationType

The **concept of a relation type remains necessary**: every relation instance must identify a reusable relation schema whose roles/cardinalities can be resolved.

However, the dedicated serialization/class marker `kind = relationType` is not what creates that semantic status. A model element behaves as a relation type because it is used as a relation's type and/or participates in `sci:declaresRole` declarations.

Candidate simplification:

```text
RelationType := ModelElement used as relation type + role declarations
```

rather than an irreducible carrier class marker.

### RoleType

Stable role identity remains necessary; bindings need a reusable role identifier and relation schemas need to declare role contracts.

But the dedicated `kind = roleType` marker is not structurally necessary. Role semantics are carried by use in `sci:declaresRole` and in bindings.

Candidate simplification:

```text
RoleType := ModelElement used as declared/bound role identity
```

### ElementType

The current validator does not structurally depend on `kind = type`. Typing relationships remain useful, but a special ElementType marker class has not demonstrated independent necessity.

This suggests treating type-ness as graph semantics—principally `instanceOf`, specialization, and type participation—rather than as a privileged serialization category.

### Expression, Constraint, Value

These distinctions matter scientifically, but the audit locates their current enforcement in the **scientific schema/profile**, not in the incidence carrier.

For example:

```text
EquationRelation.eqExpression -> participant kind expression
QuantityValueRelation.numericalValue -> participant kind value
EquationRelation.eqConstraint -> participant kind constraint|element
```

When those schema restrictions are relaxed to generic `element`, the carrier validates all fixtures after erasing the special node-kind markers.

Therefore the current evidence favors:

```text
Expression
Constraint
Value
```

as reusable scientific/data types or libraries rather than irreducible hypergraph-carrier primitives.

A principled implementation should **not simply erase these distinctions**. It should replace raw serialization-kind restrictions with semantic participant-type constraints, e.g. a role contract that states its participant must instantiate `sci:Expression` rather than requiring the JSON node field `kind: expression`.

### RoleBinding

`RoleBinding` is different. A separate acceptance fixture demonstrates a capability that disappears if bindings are only anonymous serialization records: a ClaimRelation can target one specific participant-to-role assignment.

Addressable RoleBindings therefore have concrete semantic justification in the current carrier.

## Reduced-carrier candidate

The ablation results motivate a smaller conceptual carrier:

```text
ModelElement
RelationInstance
RoleBinding

plus graph semantics for:
  type assignment / specialization
  relation-schema identity
  role identity / declaration
```

In this formulation:

- relation types are model elements recognized by their graph use/declarations;
- role types are model elements recognized by their graph use/declarations;
- ordinary element types are model elements participating in typing relations;
- Expression/Constraint/Value are scientific/data schema types;
- an addressable RoleBinding is a genuine incidence object.

This is a **candidate simplification**, not yet a v2 serialization decision.

## Why not change v1 immediately?

The current explicit `kind` markers are useful for authoring, validation messages, and visualization, even where they are semantically derivable.

Changing the serialization before defining semantic-normalization/query invariants would risk confusing:

```text
redundant convenience annotation
```

with:

```text
irreducible semantic primitive
```

Therefore v1 remains stable while the next acceptance gate tests cross-domain queries.

## Decision rule for a future v2

A v2 simplification should preserve at least:

- all current fixture validity/invalidity results;
- shared/local schema contracts;
- higher-order relation participation;
- first-class RoleBinding reference;
- the cross-domain scientific query acceptance suite;
- deterministic viewer projections after normalization.

Only then should redundant `kind` markers or primitive names be removed from the normalized format.
