---
doc-role: scientific-hypergraph-repository-map
authority: navigation-and-authority
lifecycle: active
---
# Scientific hypergraph repository map

[Current AI IR](scientific-hypergraph-v2-ai-ir.md) · [Changelog](scientific-hypergraph-changelog.md) · [Kernel](scientific-hypergraph-kernel.md) · [Adequacy review](scientific-hypergraph-adequacy-review.md) · [PR #79](https://github.com/BrianMills2718/collective-competence/pull/79)

This page answers two questions:

1. **Where are the scientific-hypergraph files?**
2. **Which files are authoritative now?**

The project is on branch `docs/scientific-metamodel`, PR #79. The intended consumer is an AI system. `scientific-hypergraph-v2` is the canonical machine-facing semantic IR.

## Read this first

For a new AI agent or coding agent, read in this order:

1. `wiki/reference/scientific-hypergraph-v2-ai-ir.md` — current representation and AI-facing contract.
2. `wiki/reference/scientific-hypergraph-repository-map.md` — where everything lives and what is authoritative.
3. `wiki/reference/scientific-hypergraph-changelog.md` — how the design evolved and what was superseded.
4. `wiki/reference/scientific-hypergraph-kernel.md` — carrier hypothesis and surviving structural concepts.
5. `wiki/reference/scientific-hypergraph-adequacy-review.md` — skeptical evidence that the shared schema is doing real work.

Then inspect the relevant v2 graph and use the query/validator tooling rather than inferring semantics from prose.

## Authority summary

| Concern | Current authority | Status |
|---|---|---|
| AI semantic representation | `wiki/reference/metamodel/*-v2.json` | **canonical** |
| v2 serialization shape | `wiki/reference/metamodel/hypergraph-v2.schema.json` | **canonical** |
| carrier/bootstrap | `wiki/reference/metamodel/hypergraph-kernel-v2.json` | **canonical** |
| shared semantic types | `wiki/reference/metamodel/scientific-semantic-types-v2.json` | **canonical** |
| shared scientific relation/role schema | `wiki/reference/metamodel/scientific-role-schema-v2.json` | **canonical** |
| v2 deterministic generation | `scripts/build_scientific_hypergraph_v2.py` | **canonical build path** |
| v2 closure validation | `scripts/validate_scientific_hypergraph_v2.py` | **canonical validation path** |
| AI bounded graph queries | `scripts/query_scientific_hypergraph_v2.py` | **canonical query surface** |
| v1 | `*-v1.json` | migration/regression input |
| v0 | `*-v0.json` / older unversioned fixtures | historical/migration input |
| viewer | `hypergraph-viewer*.js/html` | debug/projection only |
| pilot/reference prose | `wiki/reference/scientific-model-metamodel-*.md` | rationale/history |

## 1. Canonical v2 shared graph

Directory:

```text
wiki/reference/metamodel/
```

### Kernel

```text
hypergraph-kernel-v2.json
```

Contains the minimal machine bootstrap needed to read the graph representation.

### Semantic type profile

```text
scientific-semantic-types-v2.json
```

Contains graph-level semantic/profile types such as ModelElement, RelationType, RoleType, Expression, Constraint, Value, Method, Instrument, etc. These are **semantic graph vocabulary**, not separate carrier object classes.

### Scientific role schema

```text
scientific-role-schema-v2.json
```

Contains reusable scientific RelationType/RoleType declarations and participant/cardinality constraints. Shared relation schemas include Equation, Measurement, Analysis, Distribution, Representation, Access, Claim, Identifiability, Experiment, QuantityValue, and related infrastructure.

### Serialization schema

```text
hypergraph-v2.schema.json
```

Defines the physical v2 JSON incidence representation:

```text
elements[]
relations[]
bindings[]
```

## 2. Canonical v2 scientific/domain graphs

Also under `wiki/reference/metamodel/`:

```text
c2-q1-hypergraph-v2.json
classical-mechanics-hypergraph-v2.json
harmonic-oscillator-hypergraph-v2.json
first-order-reaction-hypergraph-v2.json
ornstein-uhlenbeck-hypergraph-v2.json
heat-equation-hypergraph-v2.json
random-walk-diffusion-multiscale-hypergraph-v2.json
calibration-covariance-hypergraph-v2.json
causal-markov-equivalence-hypergraph-v2.json
dynamic-topology-hypergraph-v2.json
gauge-equivalence-hypergraph-v2.json
stochastic-heat-equation-hypergraph-v2.json
uncertain-lineage-hypergraph-v2.json
role-binding-epistemics-hypergraph-v2.json
```

The first thirteen are scientific proving grounds. `role-binding-epistemics-hypergraph-v2.json` is a structural proof that a claim/evidence relation can target one exact RoleBinding.

## 3. AI build / validation / query tooling

Directory:

```text
scripts/
```

### Build canonical v2

```text
build_scientific_hypergraph_v2.py
```

Deterministically generates the canonical v2 corpus from the retained migration inputs and shared semantic/profile definitions.

### Reproducibility gate

```text
check_scientific_hypergraph_v2_build.py
```

Rebuilds the canonical v2 artifacts and requires byte-identical results.

### Validate one resolved v2 import closure

```text
validate_scientific_hypergraph_v2.py
```

Checks identity resolution, relation/role/participant references, cardinality, qualifier permissions, semantic participant types, specialization, first-class RoleBinding references, imports, and connected root semantics.

### Validate all v2 roots

```text
validate_scientific_hypergraph_v2_suite.py
```

### AI query interface

```text
query_scientific_hypergraph_v2.py
```

Machine-oriented JSON queries include:

```text
summary
show <id>
types <id>
relations --type <RelationType>
subgraph <id> --depth N
```

AI agents should prefer bounded query results/subgraphs to loading entire graphs into context without need.

### Query acceptance

```text
check_scientific_hypergraph_v2_queries.py
```

Checks canonical relation identities, graph-native typing, causal/access semantics, and first-class RoleBinding behavior.

## 4. Representation research and regression tooling

These scripts are evidence for why the canonical v2 design was selected. They remain useful regression tests but are not the primary AI API.

Important examples:

```text
audit_kernel_ablation.py
audit_scientific_hypergraph_adequacy.py
probe_semantic_participant_types.py
probe_graph_native_typing.py
probe_semantic_role_schema.py
materialize_graph_native_v2_probe.py
measure_graph_native_normalization.py
check_scientific_hypergraph_queries.py
check_first_class_role_binding.py
check_local_relation_schema.py
check_gauge_equivalence.py
check_stochastic_pde.py
check_uncertain_lineage.py
```

These answer questions such as:

- which proposed kernel concepts are actually structural;
- whether shared schemas are reused across domains;
- whether type semantics survive removal of `kind` fields;
- whether higher-order RoleBinding reference is real;
- whether difficult scientific distinctions can be represented without kernel growth.

## 5. v0 and v1 migration/regression files

Directory:

```text
wiki/reference/metamodel/
```

You will see older generations beside v2, for example:

```text
c2-q1-hypergraph-v0.json
c2-q1-hypergraph-v1.json
c2-q1-hypergraph-v2.json
```

Interpretation:

- **v0** — early simple hypergraph fixtures; retained for historical/migration tests.
- **v1** — explicit typed RoleBindings; important intermediate representation and deterministic migration source.
- **v2** — canonical AI semantic IR.

Do not infer authority from file age or shortest filename. Prefer `*-v2.json` unless a migration/regression task explicitly requests an older generation.

## 6. Viewer / projection tooling

Directory:

```text
wiki/reference/metamodel/
```

Main entry point:

```text
hypergraph-viewer.html
```

Related modules include:

```text
hypergraph-viewer-core.js
hypergraph-viewer-fixtures.js
hypergraph-viewer-semantic-ir.js
hypergraph-viewer-layout.js
hypergraph-viewer-multidomain.js
hypergraph-viewer-render.js
hypergraph-viewer-role-schema.js
hypergraph-viewer-typed-inspector.js
hypergraph-viewer-main.js
```

Purpose:

- visualize canonical v2;
- inspect roles and higher-order participation;
- project Theory, Measurement, Probability, Representation, Access, Evidence, Identifiability, and Typing views;
- debug identity/layout/schema problems.

**The viewer is not the semantic authority.** Never change the scientific meaning merely to make a diagram prettier.

Browser regression scripts live under `scripts/smoke_*.mjs`.

## 7. Scientific rationale / design-history documents

Directory:

```text
wiki/reference/
```

### Current architecture/evidence

```text
scientific-hypergraph-v2-ai-ir.md
scientific-hypergraph-kernel.md
scientific-hypergraph-adequacy-review.md
scientific-hypergraph-viewer.md
scientific-hypergraph-changelog.md
```

### Historical normalization/design records

```text
scientific-hypergraph-normalization-v2-probe.md
scientific-model-metamodel.md
scientific-model-metamodel-prior-art.md
scientific-model-metamodel-composition-probe.md
```

### Domain pilots

```text
scientific-model-metamodel-cc-pilot.md
scientific-model-metamodel-c2-q1-pilot.md
scientific-model-metamodel-classical-mechanics-pilot.md
scientific-model-metamodel-dynamics-pilot.md
scientific-model-metamodel-causal-pilot.md
scientific-model-metamodel-dynamic-topology-pilot.md
scientific-model-metamodel-gauge-equivalence-pilot.md
scientific-model-metamodel-stochastic-pde-pilot.md
scientific-model-metamodel-uncertain-lineage-pilot.md
```

These documents explain why distinctions entered the graph. They do not override canonical v2 machine semantics.

## 8. Original Collective Competence / experiment context

The metamodel work is general, but some motivating evidence lives elsewhere in the repository.

Important context:

```text
wiki/ontology.md
goal-discovery/docs/hypotheses/c2_001_derived_phase.md
goal-discovery/docs/hypotheses/c2_001_derived_phase_results.md
goal-discovery/docs/hypotheses/q1_006_pairwise_relation.md
goal-discovery/docs/hypotheses/q1_006_pairwise_relation_results.md
goal-discovery/src/substrate/specimens/contended_slot.py
goal-discovery/src/substrate/contract.py
```

Use these when checking whether the metamodel faithfully represents the original scientific case. Do not promote CC-specific concepts into the carrier merely because they appear in the motivating domain.

## 9. CI / regression gate

```text
.github/workflows/scientific-hypergraph.yml
```

The intended workflow covers:

- v0/v1 migration regressions;
- v2 deterministic rebuild;
- v2 import-closure validation;
- v2 AI query acceptance;
- adequacy and kernel-ablation audits;
- difficult semantic stress tests;
- v2-backed browser/viewer regressions.

Hosted runner availability is an infrastructure concern; semantic pass/failure should be determined from executed steps, not from jobs that never receive a runner.

## 10. Current branch / review unit

```text
repo:   BrianMills2718/collective-competence
branch: docs/scientific-metamodel
PR:     #79
```

PR #79 is the active review unit for this exploratory work. Do not merge it without explicit approval.

## 11. What an AI should mutate

For the current project phase:

- treat canonical v2 semantics as the target model;
- use builders/validators rather than hand-editing generated corpus files when a deterministic source path exists;
- preserve stable IDs;
- validate proposed graph changes before commit;
- record provenance for future AI-originated changes;
- avoid adding carrier primitives unless a concrete semantic capability cannot be represented with the existing carrier + graph schemas.

The next planned layer is an explicit **AI graph interaction contract** for query, patch, validation, transactional apply, provenance, and model diff operations.

## Quick commands

From repository root:

```bash
python scripts/check_scientific_hypergraph_v2_build.py
python scripts/validate_scientific_hypergraph_v2_suite.py
python scripts/check_scientific_hypergraph_v2_queries.py
```

Example bounded query:

```bash
python scripts/query_scientific_hypergraph_v2.py \
  wiki/reference/metamodel/causal-markov-equivalence-hypergraph-v2.json \
  subgraph h:obs-identifiability --depth 2
```

For history, read [the changelog](scientific-hypergraph-changelog.md). For the current architecture, read [the v2 AI IR document](scientific-hypergraph-v2-ai-ir.md).
