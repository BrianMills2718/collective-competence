---
doc-role: domain-ontology
authority: canonical
lifecycle: active
sources:
  - ../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md
  - ../goal-discovery/docs/sources/briefs/Dynamical_Laboratory_Coding_Agent_Spec.md
  - ../goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md
---
# Research ontology

[Project wiki](index.md) ·
[Scientific charter](../goal-discovery/docs/PROJECT.md) ·
[Current analytic-arm plan](../goal-discovery/docs/plans/current_research_plan.md)

This page is the canonical owner for the project's scientific vocabulary and
the relationships among its terms. Other current documents should link here
rather than silently redefine these concepts. Historical protocols and results
retain their original wording; interpret their claims through the definitions
and evidence distinctions below without rewriting their observations.

The ontology uses **distinct primary claim roles** so each declaration has one
clear owning question and category errors are visible. Terms can legitimately
participate in more than one relation; they are not independent physical objects.
For example, capabilities can support competence, and a maintained invariant
can be used in a goal criterion, but neither relationship makes the terms
interchangeable.

## Research architecture

The repository participates in one broader research agenda whose proper name is
still unresolved. Do not use either arm's name as the name of the whole agenda.

| Name | Ontological role | Governing question |
|---|---|---|
| **Collective Competence** | Constructive and mechanistic research arm | How can mechanisms, component capabilities, coupling, and organization be designed or varied to produce competence at system and collective scales? |
| **Goal and Competence Discovery** | Analytic and inferential research arm; **Goal Discovery** is acceptable shorthand | Given an observation and intervention contract, what goal criteria and competence profiles are supported, contradicted, or underdetermined by behavior? |
| **Dynamical Laboratory** | Shared experimental apparatus | How are systems defined or imported, executed, observed, challenged, compared, and audited for either arm? |

The constructive arm may use black-box measurements, and the analytic arm may
eventually inspect mechanisms. White-box and black-box therefore describe
analyst access, not the two research arms. A system constructed in the
laboratory can be analyzed blind-first; an imported system can be inspected
mechanistically.

## The claim stack

A scientific claim is incomplete unless the relevant roles below are declared.
Not every experiment needs to make a claim at every layer; absent or unresolved
layers remain explicit rather than being inferred from a filename or result.

| Claim role | Canonical term | Question it answers | Minimum declaration |
|---|---|---|---|
| Context and realization | **World** and **substrate** | What situation and executable realization produce the dynamics? | State/rule realization, relevant environment, version, and limitations |
| Attribution | **Focal system**, **boundary**, and **scale** | What is being treated as the system, and at what level is a property attributed? | Inside/outside split, component/collective level, and boundary rationale |
| Causal implementation | **Mechanism** | What organization or process produces transitions or behavior? | Authored, observed, inferred, hidden, or unknown mechanism status |
| Bounded system function | **Capability** | What transformation, sensing, memory, communication, representation, or control operation can the system perform? | Interface, conditions, resources, success/failure semantics, and evidence source |
| Evolution | **State**, **dynamics**, and **trajectory** | What changes through time? | Time convention, transition process, interventions, and run lineage |
| Access | **Observation contract** | What information may the analyst use? | Allowed variables/history and privileged information withheld |
| Coordinates | **Representation** or **problem space** | In what derived coordinates are patterns, criteria, and distances expressed? | Transformation from allowed observations, provenance, and information budget |
| Success semantics | **Goal criterion** | What represented histories or outcomes count as success? | Predicate/score, tolerance, temporal scope, provenance, and alternatives |
| Test conditions | **Challenge family** and **resource contract** | Across which initial states, perturbations, routes, demands, and costs is performance assessed? | Sampling/coverage, opportunities, resources, comparators, and failure cases |
| Evaluated performance | **Competence profile** | How effectively and flexibly does the system satisfy a goal criterion under the declared tests? | Dimensions, units, uncertainty, individual failures, and transfer boundary |
| Epistemic standing | **Evidence and review status** | What is supplied, observed, inferred, tested, reviewed, or still unknown? | Provenance, prospective/retrospective status, result source, alternatives, and limits |

A compact relational form is:

```text
mechanism -> capabilities -> possible dynamics and trajectories
                                ↓
observations -> representation -> goal criterion
                                ↓
             challenges and resources -> competence profile
```

Every arrow is a claim to test, not an identity. In particular, observed
behavior can underdetermine mechanism, representation can manufacture apparent
regularity, and convergence can occur without goal-directed competence.

## Core entities and relations

### World, substrate, focal system, environment, boundary, and scale

- A **world** is the modeled or empirical situation relevant to a study,
  including contextual dynamics.
- A **substrate** is the executable or physical realization sufficient to
  produce the studied dynamics. The laboratory may adapt existing engines; it
  does not presume a universal substrate.
- A **focal system** is the state and components selected for attribution.
- A **boundary** declares what is inside and outside the focal system. It may be
  authored, empirically motivated, or itself compared as a candidate.
- The **environment** is what lies outside that boundary and interacts with it.
- A **scale** is the level or aggregation at which observations, mechanisms,
  capabilities, goals, or competence are described. Scale never substitutes
  for a boundary or representation.

These declarations are relational: the same component can be system or
environment under different, explicitly compared boundaries.

### Mechanism

A **mechanism** is the causal organization or implementation that produces
transitions, behavior, or capabilities. It includes update rules, feedback,
memory, morphology, coupling topology, communication, learning, or other causal
structure.

Mechanism knowledge can explain a capability or competence result, but does not
itself establish either. Conversely, behavioral evidence may support a bounded
capability or competence claim without uniquely identifying its mechanism.

### Capability

A **capability** is a bounded transformation, operation, or control affordance
that a declared system can perform under a stated contract. A capability
contract identifies:

```text
(system boundary, interface/input, transformation/output,
 operating conditions, resource bounds, failure semantics, evidence source)
```

Capabilities can be:

- **specified** from architecture or mechanism;
- **demonstrated** by a behavioral test under the contract;
- **inferred candidates** when behavior suggests but does not yet isolate them;
- **unsupported or unknown** when the required test or access is absent.

A demonstrated capability may have a local acceptance test. That does not make
capability synonymous with competence. When the study attaches a goal criterion
and evaluates graded performance over a challenge family, it has additionally
posed a competence question.

### Observation, representation, and metric

An **observation** is information available under the declared analyst-access
contract. It need not expose the full state. A **representation** transforms
allowed observation history into coordinates used for comparison or inference:

```text
o_t = H(x_t, access contract)
z_t = phi(o_0:t)
```

The representation may contain instantaneous state, history, relations,
aggregates, learned features, morphology, network structure, or any other
testable function of allowed observations. “Arbitrary” means the candidate
family is not restricted to familiar physical coordinates; it does not permit
post-hoc, unrecorded functions chosen only because they make a preferred result
look true.

A **metric** is a measurement on a declared representation, with units and
interpretation. A metric is not automatically a goal, progress measure, or
competence score.

### Goal criterion

A **goal criterion** is a predicate, set, or graded condition on represented
states or histories that specifies what counts as success for a declared focal
system. Here “goal” does not by itself imply consciousness, intention, planning,
or an internal symbolic objective.

In analytic records, **goal** is shorthand for a candidate goal criterion unless
the record explicitly identifies an authored or system-internal goal object.

A criterion may concern:

- a point or target value;
- a region, set, or tolerance band;
- a relation among entities;
- an invariant or maintained condition;
- a finite or continuing trajectory predicate;
- a distribution over states or histories;
- morphology, topology, or network organization;
- a metastable regime or recurrent set;
- remaining inside a viability set; or
- modifying reachability, such as preserving multiple routes to acceptable states.

Formally, a criterion can be written as `G(z_0:T, context)`, not merely as a
point in raw simulator state. A point target is one special case. An observed
attractor, invariant, low-disorder state, or viability boundary is not
automatically a goal; evidence must distinguish active achievement or
maintenance from passive dynamics and artifact explanations.

Goal provenance must be explicit:

- **authored** — supplied as a design target or known task;
- **analyst-supplied** — proposed manually for calibration or exploration;
- **method-proposed candidate** — generated from allowed observations by the
  declared procedure;
- **retrospectively interpreted** — formulated after viewing outcomes;
- **unknown or underdetermined** — no supported criterion has been isolated.

Only the third category can support a discovery claim, and only after
distinguishing tests. Authored and analyst-supplied criteria remain legitimate
for constructive studies and calibration.

### Competence and competency

**Competence** is the graded, goal-relative performance of a declared system
across a declared challenge and resource family. It asks not only whether one
success occurred, but how reliably, flexibly, efficiently, and recoverably the
criterion is satisfied and where performance fails.

A competence claim can be represented as:

```text
K = performance_profile(system, boundary, representation,
                        goal criterion, challenge family, resources)
```

The profile can include:

| Dimension | Question |
|---|---|
| Attainment or maintenance | Does the system reach or preserve criterion-satisfying histories? |
| Reliability | Across what fraction or distribution of eligible cases? |
| Reachability/opportunity | Was success possible from the tested condition, and was opportunity accounted for? |
| Flexibility | Can different routes, configurations, or means achieve the criterion? |
| Efficiency | What time, energy, actions, information, or other resources are consumed? |
| Robustness | How does performance change across declared perturbations or uncertainty? |
| Recovery | How quickly and completely does performance return after loss? |
| Adaptation | What behavioral or organizational change restores or improves performance? |
| Generalization/transfer | Does the profile hold outside the fitting or calibration conditions? |

No universal scalar is assumed. A study may report only the dimensions it
actually measures, with others marked untested or unknown.

Use **a competency** only as a count noun for a particular operationally
demonstrated case, such as competence toward one criterion under one declared
challenge contract. It is not a separate theoretical primitive. Prefer
*capability* when naming an operation and *competence* when naming graded
goal-relative performance.

### Robustness, recovery, adaptation, and viability

- **Robustness** is the portion of a competence profile describing performance
  across a declared perturbation or uncertainty family.
- **Recovery** describes return toward prior performance after disruption.
- **Adaptation** requires a change in behavior, policy, organization, or
  mechanism that restores or improves performance. Remaining unchanged and
  unaffected is robustness, not adaptation.
- **Viability** describes remaining within conditions compatible with continued
  operation. A viability set may supply a goal criterion, but viability is not
  automatically evidence of a discovered goal.

These concepts require a time window, baseline, challenge, and failure rule.

### Collective competence

**Collective competence** is competence attributed at a declared boundary that
contains multiple interacting components. “Collective” identifies the proposed
level of attribution; it does not guarantee emergence, superiority, or agency.

A strong collective-competence claim states:

1. the collective boundary and candidate goal criterion;
2. component capabilities and component-level competence baselines;
3. the coupling or organizational mechanism being varied;
4. matched resource, environment, and information conditions;
5. uncoupled, ablated, centralized, or simpler controls as applicable;
6. the collective competence profile and individual failures; and
7. what the collective achieves that components do not, or achieve less
   reliably, flexibly, efficiently, or robustly.

System size, coordination-looking motion, aggregate prediction, or improvement
over an unmatched component baseline is insufficient on its own.

## Goal and competence may be jointly assessed from behavior

An authored goal criterion can exist even when competence is zero. But when the
criterion is not supplied and must be inferred from behavior, evidence for a
goal normally depends on observing some discriminating competence toward it.
With no reliable achievement, maintenance, recovery, or selective response,
behavior may provide no basis for preferring one candidate goal over another.

Therefore the analytic arm should normally return a structured result:

```text
(candidate goal criterion,
 competence profile,
 focal boundary and scale,
 observation/representation contract,
 evidence status, alternatives, and confidence limits)
```

It may return `abstain` or `underdetermined`. Goal discovery is not a requirement
to force a goal label onto every system.

## Independent study dimensions

Every prospective experiment declares these separately:

| Dimension | Canonical values | Question answered |
|---|---|---|
| **Specimen origin** | constructed · imported · empirical · mixed · unknown | Where did the system and its organization come from? |
| **Analyst access** | black-box · white-box · blind-first/reveal-later · mixed · unknown | Which state, rules, mechanisms, targets, and provenance may be used at each phase? |
| **Research purpose** | Collective Competence/constructive-mechanistic · Goal and Competence Discovery/analytic-inferential · calibration; one primary plus optional secondary purposes | What claim is the study designed to change? |

Construction is an activity and usually an origin; it is not itself a research
arm or evidence of collective competence. Open construction of a system does
not count as Goal and Competence Discovery unless the analysis withholds or
controls authored answers and actually tests an inference procedure.

## Evidence vocabulary

Keep three status families separate:

| Status family | Machine values |
|---|---|
| **Provenance** | `authored` · `analyst_supplied` · `method_proposed` · `observed` · `retrospectively_interpreted` · `unknown` · `not_reviewed` |
| **Claim assessment** | `not_tested` · `candidate` · `supported` · `qualified` · `mixed` · `contradicted` · `abstain` · `underdetermined` · `unknown` · `not_reviewed` |
| **Record review** | `not_reviewed` · `result_reviewed` · `independently_reproduced` |

Prose may use human-readable hyphens and slashes. Machine fields use the
`snake_case` values above and the explicit values in the prospective contract.

`Unknown`, `mixed`, and `not_reviewed` are not interchangeable:

- **unknown** means the relevant fact or value is genuinely unavailable or
  unresolved under the current evidence;
- **mixed** means multiple declared values or outcomes apply and cannot be
  honestly reduced to one; list the contributing values when possible;
- **not_reviewed** means the native evidence has not been examined sufficiently
  to classify the field and therefore forbids an inferred scientific verdict.

Evidence strength remains claim-specific. A run can establish that a trajectory
occurred without establishing a mechanism, and a reviewed result can still be
exploratory, internally reproduced only, or contradicted by a later test.

## Non-equivalences and common category errors

| Do not equate | Why |
|---|---|
| Capability = competence | An operation under a local contract is not a graded goal-relative profile across challenges. |
| Goal = target point | Criteria may concern regions, relations, histories, distributions, or regimes. |
| Goal = attractor or invariant | Passive dynamics can converge or preserve structure without active goal-directed performance. |
| Goal = metric | A measurement can describe behavior without defining success. |
| Robustness = adaptation | Robustness can require no change; adaptation specifically involves restorative or improving change. |
| Viability = discovered goal | Continued operation may be passively constrained or analyst-defined. |
| Mechanism = goal | Causal implementation explains transitions; it does not define what counts as success. |
| White-box = constructive arm | Access and research purpose are independent dimensions. |
| Black-box = discovery arm | A black-box study can measure an authored task, and discovery can include a later mechanism reveal. |
| Constructed = authored answer | A constructed specimen can be analyzed blind-first with intent withheld. |
| Collective = emergent or superior | Collective attribution requires boundary, component, coupling, and matched-control evidence. |
| Prediction = competence | Predictability can arise from passive regularity and does not show achievement, maintenance, or recovery. |
| Intelligence/viability/self-preservation = autopoiesis | Distinct empirical properties; a system can show strong directed behavior while destroying its own organization. Autopoiesis specifically requires that a system's constituting processes recursively participate in maintaining/reconstituting the organization that defines the system — do not infer it from the presence of an attractor or a merely persistent boundary. |

See the founding briefs
([Automated Dynamical Systems Discovery Laboratory Spec](../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md#55-viability-and-autopoiesis),
[Dynamical Laboratory Coding Agent Spec](../goal-discovery/docs/sources/briefs/Dynamical_Laboratory_Coding_Agent_Spec.md#14-viability-and-autopoiesis))
for the fuller early-stage treatment of viability and autopoiesis, including the
separately-tracked measures (boundary persistence, survival, maintenance of
organization, environmental control) — not yet folded into the active Goal and
Competence Discovery scope.

A separate, unrelated project (`levin-wiki`, not part of this repository) is
running an independent discussion on whether Michael Levin's "Platonic
ingression" framework could explain the emergence of increasingly competent
prebiological matter, including a dynamical/metastability account structurally
similar to this project's own driven-system apparatus — see its living
document,
[`platonic-space-and-ingression.md`](../../levin-wiki/wiki/concepts/platonic-space-and-ingression.md).
Unvalidated raw output from a related external toy-automaton experiment sits
in `misc/platonic-ingress-toy-automata/` (see that directory's `INTENT.md`) —
not yet a registered experiment here, not evidence for anything in this
repository's own ontology.

## Prospective experiment declaration

New experiment protocols should declare the following vocabulary. Native
protocols own the scientific meanings; native results and run metadata own
observations and provenance. The experiment register remains navigation and
review metadata, not a second scientific narrative.

The identifiers below are normalized machine values. Prose uses **Goal and
Competence Discovery** on first reference, with **Goal Discovery** only as later
shorthand.

| Field | Required content |
|---|---|
| `primary_research_purpose` | `constructive_mechanistic`, `goal_competence_discovery`, or `calibration` |
| `secondary_research_purposes` | Zero or more additional purposes; do not collapse them into `mixed` when they can be named |
| `specimen_origin` | `constructed`, `imported`, `empirical`, `mixed`, `unknown`, or `not_reviewed` |
| `analyst_access_phases` | Ordered phases naming `black_box`, `white_box`, or `blind_first_reveal_later`, plus the information allowed in each phase |
| `substrate_and_world` | Engine/physical realization, version, environment, and known limitations |
| `focal_boundary_and_scale` | Inside/outside split, attribution level, and rationale |
| `mechanism` | Summary plus `access_status`: `known`, `hidden`, `partially_known`, `unknown`, or `not_reviewed`; inferred mechanisms also carry provenance and claim assessment |
| `capability_claims` | For each operation: capability contract, attribution boundary, provenance, and claim assessment from the evidence vocabulary |
| `observation_contract` | Allowed variables/history, cutoff, units, privileged exclusions, and lineage |
| `representation_contract` | Transformation from observations, candidate-family provenance, information budget, and fitting boundary |
| `goal_criteria` | For each criterion: form, focal boundary, provenance, temporal scope, tolerance, claim assessment, and rival explanations |
| `challenge_family` | Initial conditions, perturbations, routes, demands, resources, opportunity rules, and `coverage_status`: `not_tested`, `partial`, `complete`, `mixed`, `unknown`, or `not_reviewed` |
| `competence_profile` | For each measured dimension: value/units, uncertainty, claim assessment, individual failures, and transfer boundary; retain untested or unknown dimensions explicitly |
| `intervention_contract` | Target, operation, scope, timing, persistence, and counterfactual comparator |
| `evidence` | Structured object with separate `provenance`, `claim_assessment`, and `review_status`, plus result source, counterevidence, abstention, and limitations |

This contract applies prospectively. Historical records remain valid evidence
with their original fields. They must be reviewed against their native protocol
and result before ontology metadata is added; otherwise use `not_reviewed`
rather than inferring classifications from filenames.

Scientific adequacy remains human-reviewed. P15 and every record outside the
register's closed `legacy_unversioned_record_ids` inventory must declare
`ontology_contract_version: 1` and carry a complete machine-readable
`experiment_declaration` in its native protocol frontmatter. The registry
renderer checks the required shape, controlled vocabulary, linked protocol, and
agreement of review status. This structural check does not certify the
experiment, infer missing values, or backfill historical records.

## Observability rule

Prefer **maximum useful observability**: retain the state, events, configuration,
randomness, provenance, timing, and failure information needed to reproduce and
audit a run when doing so is proportionate. Preserve privileged white-box data
separately even when an analysis is black-box, so a later reveal can audit
leakage and mechanisms without contaminating the frozen inference.

More collection is not automatically more scientific information. Additional
signals can increase storage and analysis cost, introduce researcher degrees of
freedom, or leak authored targets. Therefore every analysis declares its allowed
view and cutoff; unselected retained data remains inaccessible to that analysis.
Record missing, unsupported, not-applicable, and ambiguous fields rather than
silently omitting them or replacing them with synthetic values.

## Naming and writing rules

- Use **Collective Competence** only for the constructive arm or for the property
  being studied, not as the umbrella name of the whole agenda.
- Use **Goal and Competence Discovery** on first reference to the analytic arm;
  **Goal Discovery** may be used afterward as shorthand.
- Use **Dynamical Laboratory** for the shared apparatus, not as a third research
  objective or a claim that one universal simulator exists.
- Prefer **competence** for the graded property and **capability** for a bounded
  operation. Use **a competency** sparingly for an operationally demonstrated
  case and preserve the wording inside historical titles or quotations.
- Qualify every goal, capability, competence, robustness, adaptation, and
  collective-level claim with its boundary, conditions, evidence status, and
  relevant alternatives.
