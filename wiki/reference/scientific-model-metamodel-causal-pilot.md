# Scientific hypergraph metamodel: causal-identifiability pilot

Status: exploratory stress test for PR #79.

## Question

Can the typed n-ary hypergraph represent a causal-inference distinction that is stronger than ordinary curve fitting without adding a new kernel primitive?

The pilot uses two three-variable structural causal models:

```text
SCM A: X -> M -> Y
SCM B: X <- M -> Y
```

These DAGs have the same skeleton and no v-structure, so they are Markov equivalent under purely observational data. Both imply the conditional-independence pattern:

```text
X ⫫ Y | M
```

An intervention on `X`, however, distinguishes them. In SCM A, `do(X=x)` can change `M` and therefore `Y`; in SCM B, intervening on `X` does not change `M` through the causal graph.

This makes the example useful for separating:

- observational fit from causal orientation;
- one analysis method from an identifiability assertion;
- observational equivalence from interventional distinguishability;
- access to observed variables from access to the authored causal mechanism.

## Representation

Fixture:

```text
wiki/reference/metamodel/causal-markov-equivalence-hypergraph-v1.json
```

The model uses only existing scientific schemas:

- `EquationRelation` for the structural equations;
- `DistributionRelation` for exogenous-noise assumptions;
- `MeasurementRelation` for observational and post-intervention data;
- `AnalysisRelation` for conditional-independence and model-comparison analyses;
- `AccessRelation` / `StudyView` for observational versus interventional access;
- `ClaimRelation` for conditional-independence and equivalence claims;
- `RepresentationRelation` for candidate-family construction and observational projection;
- `ExperimentRelation` for `do(X=x)`;
- `IdentifiabilityRelation` for the observational and interventional conclusions.

No causal-specific kernel primitive or new relation schema is introduced.

## Key epistemic distinction

The observational stage asserts:

```text
target: orientation of X--M
candidate family: {SCM A, SCM B}
access: observational
observation model: joint observations of (X,M,Y)
equivalence class: {A,B}
status: observationally underdetermined
```

The intervention stage asserts:

```text
target: orientation of X--M
candidate family: {SCM A, SCM B}
access: observational variables + do(X=x)
intervention family: do(X=x)
status: identified by intervention
```

This is the generic pattern the metamodel needs to preserve:

```text
A ≡ B under observation/access regime O
but intervention I distinguishes A from B.
```

## Result

The current kernel survives this stress test unchanged.

The important result is not that every causal concept should be encoded as free-form text. It is that the existing combination of typed relations, role bindings, formal expressions, access regimes, claims, experiments, and identifiability assertions can represent the scientific distinction without inventing a `CausalModel` or `CausalEdge` kernel primitive.

A future causal-library layer may still introduce reusable schemas for conditional-independence assertions, causal mechanisms, or graph factorizations if repeated use justifies them. Those would be schema-library additions, not evidence for expanding the kernel.

## Acceptance test

Browser CI selects the causal fixture and requires both conclusions to remain explicit:

1. observational access exposes an equivalence class and `observationally underdetermined` status;
2. the intervention relation exposes `do(X=x)` as an intervention family and `identified by intervention` status.

If either distinction disappears, the causal pilot fails even if the graph remains structurally valid.
