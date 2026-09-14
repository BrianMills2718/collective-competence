# Scientific hypergraph typed-role v1

[Scientific hypergraph kernel](scientific-hypergraph-kernel.md) · [Scientific relation schemas](metamodel/scientific-relation-schemas.jsonld)

## Why v1 is needed

The current `scientific-hypergraph-v0` fixtures correctly model **n-ary relation instances**, but their serialization still represents participant roles as string keys:

```json
{
  "id": "h:ke-equation",
  "type": "schema:Equation",
  "roles": {
    "input:mass": "h:mass-value",
    "input:velocity": "h:velocity-value",
    "output": "h:ke-value"
  }
}
```

That is role-*labelled*, but not yet fully role-*typed*.

The metamodel claim is stronger: each incidence should identify a `RoleType` declared by the relation type, and validators should be able to enforce role cardinality and participant constraints.

## Proposed v1 serialization

```json
{
  "model": "scientific-hypergraph-v1",
  "imports": [
    "hypergraph-kernel",
    "scientific-relation-schemas",
    "scientific-quantity-schemas"
  ],
  "nodes": [
    {"id": "...", "type": "..."}
  ],
  "hyperedges": [
    {
      "id": "h:ke-equation",
      "type": "sci:EquationRelation",
      "bindings": [
        {
          "role": "sci:eqInput",
          "qualifier": "mass",
          "participant": "h:mass-value"
        },
        {
          "role": "sci:eqInput",
          "qualifier": "velocity",
          "participant": "h:velocity-value"
        },
        {
          "role": "sci:eqOutput",
          "participant": "h:ke-value"
        }
      ]
    }
  ]
}
```

The qualifier is not a new role type. `mass` and `velocity` specialize the human/scientific meaning of two bindings that both instantiate the declared `eqInput` role.

## Role declaration

A `RelationType` declares its admissible roles through the same hypergraph machinery. Conceptually:

```text
DeclaresRole(
    relationType -> EquationRelation,
    roleType     -> eqInput,
    min          -> 0,
    max          -> many,
    qualifiable  -> true,
    participantConstraint -> ModelElement
)
```

Representative Equation declarations:

```text
eqInput                0..*   qualifiable
eqOutput               1..*   qualifiable
eqExpression           1..1
eqParameter            0..*   qualifiable
eqIndependentVariable  0..*   qualifiable
eqInitialCondition      0..*   qualifiable
eqDriver               0..*   qualifiable
eqDomain               0..*   qualifiable
eqBoundaryCondition    0..*   qualifiable
eqOperator             0..*   qualifiable
eqAssumption            0..*   qualifiable
eqRegime                0..*   qualifiable
eqContext               0..*   qualifiable
```

The exact cardinalities are schema claims and should remain revisable. They are **not** kernel primitives.

## RoleBinding as incidence

A binding is the typed incidence between one relation instance and one participant:

```text
RoleBinding(
    relation    -> relation instance,
    role        -> RoleType,
    participant -> ModelElement,
    qualifier?  -> Value
)
```

Serialization may keep a binding inline for compactness. If provenance or another scientific relation must refer to one particular incidence, the binding can receive a stable `id` and become directly referenceable.

## Validation levels

### Kernel validity

- IDs are unique;
- relation types resolve;
- role types resolve;
- participants resolve;
- relations/bindings are legal model elements;
- the intended model component is connected.

### Schema validity

- the relation type declares each bound role;
- cardinalities hold;
- qualifiers are allowed where used;
- participant type constraints hold where declared;
- required roles are present.

### Scientific adequacy

Still separate. Passing schema validation does not establish that an equation, measurement, access declaration, inference, or scientific claim is correct.

## Migration from v0

For v0 keys such as:

```text
input:mass
parameter:diffusivity
context:frame
boundaryCondition:left
```

migration splits the key at the first colon:

```text
base role = input
qualifier = mass
```

and resolves the base role using the relation type's declared role vocabulary.

Examples:

```text
Equation + input:mass
    -> role sci:eqInput, qualifier mass

Measurement + context:locations
    -> role sci:measurementContext, qualifier locations

Distribution + randomObject:slope
    -> role sci:distributionRandomObject, qualifier slope
```

This means the existing stress-test fixtures are useful migration inputs rather than throwaway prototypes.

## Compatibility aliases exposed by the pilots

Formal role typing also surfaces places where prototype names and general schema names differ. These should become explicit aliases or specializations rather than silent string conventions. Examples include:

```text
StudyView.consumer   -> Access.accessor
StudyView.included   -> Access.allowed
StudyView.excluded   -> Access.restricted
StudyView.phase      -> Access.phase

Identifiability.studyView   -> Identifiability.access
Identifiability.observation -> Identifiability.observationModel
```

## Acceptance gate

Before calling the hypergraph metamodel structurally mature:

1. encode relation-type role declarations machine-readably;
2. migrate at least one existing fixture to v1 typed bindings;
3. validate declared roles and cardinalities;
4. support v0 -> v1 normalization for the remaining fixtures;
5. make the viewer inspect RoleType identity, not only display labels;
6. only then decide whether v0 can be retired.

This is a structural metamodel task. It does not require changing any scientific domain concepts or adding a kernel primitive.