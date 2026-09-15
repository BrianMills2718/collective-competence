---
doc-role: scientific-hypergraph-changelog
authority: historical-navigation
lifecycle: active
---
# Scientific hypergraph metamodel changelog

[Current AI IR](scientific-hypergraph-v2-ai-ir.md) · [Repository map](scientific-hypergraph-repository-map.md) · [Kernel](scientific-hypergraph-kernel.md) · [Adequacy review](scientific-hypergraph-adequacy-review.md) · [PR #79](https://github.com/BrianMills2718/collective-competence/pull/79)

This is the curated history of the scientific-hypergraph work on `docs/scientific-metamodel`. It is intentionally **phase-based**, not a replacement for Git history. Use it to understand why the current representation looks the way it does, what was superseded, and what remains open.

## Current state in one paragraph

The project now treats `scientific-hypergraph-v2` as the canonical **AI-facing scientific semantic IR**. The carrier is a typed n-ary hypergraph with first-class `RelationInstance` and addressable `RoleBinding` identity. Ordinary type membership and specialization are graph relations. Shared scientific semantics such as Equation, Measurement, Analysis, Distribution, Representation, Access, Claim, Identifiability, Experiment, and QuantityValue are reusable relation schemas. Theory-specific schemas may extend the graph locally. v0/v1 remain migration and regression inputs. The viewer is only a projection/debugging surface over the IR.

## Phase 0 — Collective Competence problem framing

### Starting problem
The work began from Collective Competence and goal-discovery studies that exposed recurring scientific-modeling distinctions:

- world/system/mechanism vs observations and evidence;
- white-box constructive studies vs black-box restricted-access inference;
- declared information contracts vs actual implementation dependencies;
- validity of a study vs truth/falsity of a hypothesis;
- method failure vs fundamental non-identifiability.

### Key source context
- `wiki/ontology.md`
- `goal-discovery/docs/hypotheses/c2_001_derived_phase.md`
- `goal-discovery/docs/hypotheses/q1_006_pairwise_relation.md`

### Result
Collective Competence became the **first proving ground**, not the scope of the metamodel.

## Phase 1 — Broad scientific metamodel exploration

### Change
The first metamodel drafts separated systems, measurement, experiment, analysis, evidence, access, equations, quantities, and related scientific concepts into conceptual families.

### Why it changed
That organization was useful for identifying semantics but risked turning presentation compartments into foundational ontology structure.

### Result
The project adopted a layered interpretation instead:

```text
carrier/kernel
  -> reusable scientific schema/profile
  -> theory/domain model
  -> study/evidence instances
```

These became **views/layers of one graph**, not separate semantic stores.

### Main records
- `scientific-model-metamodel.md`
- `scientific-model-metamodel-prior-art.md`
- CC/C2/Q1 pilot documents in this directory.

## Phase 2 — One typed n-ary hypergraph becomes the carrier hypothesis

### Change
The design collapsed to one typed, attributed, n-ary hypergraph. Relation instances became first-class model elements.

### Why
This made higher-order scientific composition natural:

```text
measurement relation -> evidence for claim
quantity-value relation -> input to equation
access relation -> governs analysis
relation instance -> participant in another relation
```

### Candidate carrier at this stage
- `ModelElement`
- `RelationInstance`
- typed roles / role bindings
- constraints, expressions, values as candidate semantic categories

### Result
Scientific concepts such as Equation, Measurement, Analysis, and Experiment moved toward **relation schemas**, not separate foundational object families.

### Main record
- `scientific-hypergraph-kernel.md`

## Phase 3 — Cross-domain stress testing

### Change
The kernel was tested outside Collective Competence rather than being refined only against the original domain.

### Initial stress tests
- classical mechanics / kinetic energy;
- harmonic oscillator ODEs;
- first-order reaction kinetics.

### Later stress tests
- Ornstein-Uhlenbeck stochastic dynamics;
- heat-equation PDE / fields;
- multiscale random-walk -> diffusion;
- correlated calibration uncertainty;
- causal Markov equivalence + intervention;
- dynamic topology / entity creation;
- gauge-equivalent representations;
- stochastic PDE / random field;
- uncertain lineage / model-dependent identity.

### Result
No stress test required a new carrier primitive. New needs generally appeared as reusable schema roles or theory-local relation types.

### Important design rule that emerged
> Add a kernel primitive only after a concrete scientific case cannot be represented cleanly using existing elements, relations, roles, typing, constraints, expressions, and views.

## Phase 4 — Generated viewer and layout work

### Change
Hand-authored visual prototypes were replaced by a generated viewer that reads the machine graph.

### Layout evolution
- unconstrained force layouts were rejected as too unstable and unreadable;
- ELK/layered ideas were explored;
- the accepted default became a deterministic **hub-and-lobes Sugiyama-style layout** with a shared semantic hub, domain lobes, semantic columns, barycentric crossing reduction, and type-edge bundling.

### Why this mattered
The viewer became a representation test: if the graph could not be navigated or projected coherently, that often exposed a modeling problem.

### Current status
The viewer is **not authoritative**. It is a debug/projection surface over v2.

### Main record
- `scientific-hypergraph-viewer.md`

## Phase 5 — Typed-role v1

### Change
Role strings such as `input:mass` were replaced by explicit typed bindings:

```text
role        = sci:eqInput
qualifier   = mass
participant = h:mass-value
```

### Why
The original representation was n-ary but only role-labelled, not truly role-typed.

### Result
`scientific-hypergraph-v1` made RoleType identity, qualifiers, cardinality, and participant restrictions explicit.

v0 fixtures were retained as frozen migration inputs, and v1 migration was made deterministic.

### Main records
- `scientific-hypergraph-typed-role-v1.md`
- `metamodel/scientific-role-schema-v1.json`

## Phase 6 — Self-hosted relation/role schema

### Change
Role contracts stopped being treated as a parallel hand-maintained JSON ontology and were represented in the graph itself using `sci:declaresRole`.

### Why
A second source of semantic truth would undermine the single-graph thesis.

### Result
The scientific role schema became self-describing above a deliberately tiny bootstrap. Generated contract caches are derived artifacts.

### Main files
- `metamodel/scientific-role-schema-v1.json`
- `scripts/generate_role_contracts_from_schema_graph.py`
- `scripts/check_role_schema_roundtrip.py`

## Phase 7 — Theory-local schemas

### Change
The validator learned to accept relation/role schemas declared locally by a theory fixture instead of requiring every relation type to be registered centrally.

### Proving cases
- dynamic topology: `DivisionRelation`, `BondChangeRelation`;
- gauge equivalence: local equivalence relation;
- uncertain lineage: local assignment/link relations.

### Why
A general metamodel must be extensible without turning the shared scientific profile into a universal registry of domain vocabulary.

### Result
Local schemas extend but do not override conflicting shared contracts.

## Phase 8 — Adequacy audit: test whether the metamodel was becoming vacuous

### Concern
A generic hypergraph can encode nearly anything. Representability alone does not prove the metamodel is useful.

### Change
The project measured shared-schema reuse and added cross-domain scientific queries.

### Result
Across the current scientific corpus, approximately 93% of scientific relation instances and typed bindings use shared scientific schemas; only a small minority use local schemas.

Generic queries recover recurring structures across unrelated domains, including measurement -> analysis flow, inferred quantities, fixed parameters, access-relative identifiability, and claims scoped to an addressable RoleBinding.

### Main records
- `scientific-hypergraph-adequacy-review.md`
- `scripts/audit_scientific_hypergraph_adequacy.py`
- `scripts/check_scientific_hypergraph_queries.py`

## Phase 9 — Kernel ablation and first-class RoleBinding

### Change
Candidate kernel categories were actively removed/demoted to see what actually broke.

### Findings
Dedicated serialization/node-kind markers for RelationType, RoleType, ElementType, Expression, Constraint, and Value were not irreducible carrier machinery. Their semantics could move into graph-level typing/profile vocabulary.

`RoleBinding`, however, demonstrated a real carrier-level capability: another relation can target one exact participant-to-role assignment.

### Result
The reduced-carrier direction became:

```text
ModelElement identity
RelationInstance
RoleBinding

plus graph/bootstrap semantics for:
  type assignment / specialization
  relation-schema identity
  role identity / declaration
```

### Main files
- `scripts/audit_kernel_ablation.py`
- `metamodel/role-binding-epistemics-hypergraph-v1.json`
- `scripts/check_first_class_role_binding.py`

## Phase 10 — Graph-native normalization

### Change
The project tested removal of ordinary `kind` and node-level `type` fields as semantic authority.

### Normalization target

```text
node.kind = expression
node.type = phys:Velocity

        becomes

instanceOf(node, sci:Expression)
instanceOf(node, phys:Velocity)
```

### Tests
- deterministic/idempotent normalization;
- query invariance;
- negative semantic typing checks;
- role schema `participantKind -> participantType` conversion;
- normalized incidence-table round trip.

### Result
The probes passed locally across the complete fixture suite. This established that ordinary type semantics can live in the graph rather than serialization discriminators.

### Late-stage commit anchors
- `6c85127` — gate normalized v2 incidence-table round trips
- `2684929` — specify import closure and normalized incidence-table v2 probe
- `9d8799c` — make viewer consume graph-native semantic IR

### Main record
- `scientific-hypergraph-normalization-v2-probe.md`

## Phase 11 — v2 becomes the canonical AI semantic IR

### Change
The target consumer was clarified: this representation is primarily for **AI systems**, not human scientist authoring.

That changed the optimization target from compactness toward:
- explicit semantics;
- canonical IDs;
- deterministic builds;
- import-resolved graph composition;
- bounded machine queries;
- mechanical validation.

### Canonical v2 shape

```text
elements[]
relations[]
  id
  relationType
bindings[]
  id?
  relation
  role
  participant
  qualifier?
```

### Import stack

```text
hypergraph-kernel-v2
  -> scientific-semantic-types-v2
  -> scientific-role-schema-v2
  -> domain/study v2 graph
```

### Result
- v2 artifacts rebuild deterministically;
- resolved import closures validate;
- canonical `sci:*` relation identities replace migration aliases in the AI IR;
- a JSON query CLI exposes summary/show/types/relation/subgraph operations;
- the viewer now projects canonical v2 rather than defining a separate semantic world.

### Commit anchor
- `2dea301` — promote graph-native v2 as AI semantic IR

### Main record
- `scientific-hypergraph-v2-ai-ir.md`

## Phase 12 — current direction: AI interaction contract

### Current question
The representation research is mature enough that the next bottleneck is no longer "can another scientific domain fit?"

The next problem is:
> How should an AI query, propose changes to, validate, diff, and commit scientific graphs safely and provenance-aware?

### Planned surface
Candidate operations include:

```text
query / inspect / traverse
proposePatch / validatePatch / applyPatch
addElement / addRelation / addBinding / removeBinding
assertClaim / attachEvidence / recordProvenance
diffModels / compareSubgraphs
```

### Next acceptance target
An AI should be able to inspect an underdetermined causal model, propose an intervention, validate the patch, apply it transactionally, and then recover the changed identifiability status from the graph.

## What is obsolete vs retained

| Artifact family | Status | Reason retained |
|---|---|---|
| v0 fixtures | historical/migration | earliest simple hypergraph shape; frozen migration regression |
| v1 fixtures | migration/regression | typed-role intermediate representation; deterministic source for v2 build |
| v2 fixtures | **canonical AI IR** | current machine-facing semantic representation |
| hand-authored viewer prototypes | superseded | replaced by generated v2-backed viewer |
| current viewer | debug/projection only | useful for inspection; not semantic authority |
| role-contract cache | derived | generated from graph schema; not independent authority |
| pilot documents | historical evidence | explain why specific semantic distinctions were introduced |

## Where to look for exact history

This file is deliberately curated. For exact chronology:

1. inspect Git history on `docs/scientific-metamodel`;
2. inspect PR #79 and its commit list;
3. use the pilot/reference documents for the scientific rationale behind each phase.

Do not reconstruct current authority from commit age alone. The current authority map is maintained in [Scientific hypergraph repository map](scientific-hypergraph-repository-map.md).
