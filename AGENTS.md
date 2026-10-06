# Competence research agenda — agent bootstrap

## Start here

Read [`wiki/index.md`](wiki/index.md) before substantial work. It is the project front door and should be enough to orient you without loading the repository's history.

Then follow only the task-specific route you need:

- scientific questions → [`wiki/questions.md`](wiki/questions.md)
- current findings → [`wiki/findings.md`](wiki/findings.md)
- terminology → [`wiki/concepts.md`](wiki/concepts.md)
- current priority → [`wiki/current.md`](wiki/current.md)
- apparatus / adding a specimen → [`wiki/laboratory.md`](wiki/laboratory.md)
- audits, external-system surveys, old plans, decisions, detailed ontology, chronology → [`wiki/reference/README.md`](wiki/reference/README.md)

Do **not** read the full ontology, failure log, development log, audits, or historical plans as routine orientation. They are reference/history, not working context. If resuming after a long hiatus, `wiki/index.md` → `wiki/current.md` → `wiki/findings.md` is the intended three-page handoff.

## Project model

The project asks **which experimentally separable constraints determine goal-relative competencies and failure boundaries of dynamical systems, and which candidate goals and competence claims are identifiable from behavior under a declared observation/intervention contract**.

It has two complementary research arms:

- **Collective Competence** uses intervention and white-box analysis to explain which mechanisms/capabilities are causally load-bearing for particular dimensions and ranges of system- or collective-level competence.
- **Goal and Competence Discovery** analyzes systems under declared observation/intervention access and asks which candidate goal criteria and competence profiles are supported, contradicted, or behaviorally equivalent, and what further intervention would reduce that ambiguity.

The **Dynamical Laboratory** is shared apparatus. Black-box/white-box describes analyst access, not the two arms. A constructed specimen can be analyzed blind-first; an imported specimen can be inspected mechanistically.

The programme is now **reuse-first and interrogation-first**. Broad demonstrations of local-to-global competence, cellular competency, goal scaling, regeneration, bioelectric coordination, reachability, inverse mechanism inference, behavioral equivalence, and active discrimination have substantial prior art. Prefer independently authored executable systems and real intervention data; do not build another bespoke example merely to re-demonstrate an established primitive.

## Before modifying code or evidence

1. Read the relevant hot wiki page for orientation, then follow it to the native authority.
2. For new scientific/implementation scope, identify the accepted plan under `docs/plans/` that authorizes the work; ordinary maintenance must not silently expand scientific scope.
3. Read the native experiment README/protocol and the code you will change.
4. If the work makes a novelty claim, selects a comparator, or adds a new substrate, inspect the relevant landscape survey under `wiki/reference/` first.
5. **Pass the reuse gate before building.** For any proposed new simulator, dynamical model, analysis algorithm, or substantial visualization primitive, identify maintained/published alternatives first. Record which options were checked and why they cannot answer the experiment. "I can implement it faster myself" is not a scientific justification.
6. Read the applicable subtree instructions:

| Work scope | Additional instructions |
|---|---|
| `goal-discovery/` laboratory work | [`goal-discovery/AGENTS.md`](goal-discovery/AGENTS.md) |
| research records/docs | [`goal-discovery/docs/AGENTS.md`](goal-discovery/docs/AGENTS.md) |
| source/UI/analysis | [`goal-discovery/src/AGENTS.md`](goal-discovery/src/AGENTS.md) |
| tests | [`goal-discovery/tests/AGENTS.md`](goal-discovery/tests/AGENTS.md) |

The canonical checkout is intentionally read-only; use the repository's worktree convention for writes and runs that produce output.

## Scientific discipline

- Separate **what happened**, **what the system can do**, **what counts as success**, **why it happened**, and **how strongly the interpretation is supported**.
- An authored goal criterion is legitimate in constructive work. Do not relabel it as discovered.
- Goal Discovery does not require one unique true goal. Multiple candidate criteria, an equivalence class, or `underdetermined` are valid outcomes.
- Do not assume a universal scalar notion of "more competent." Report only the performance dimensions the challenge family actually measures.
- **Specification satisfaction is not automatically competence.** A passive attractor, invariant, one-shot controller, and active regulator can satisfy the same nominal criterion on ordinary trajectories; use challenges/interventions to distinguish them.
- Convergence, prediction, low disorder, a latent variable, an error-like signal, a reward, or an attractive visualization do not by themselves establish a semantic goal or goal-directed competence.
- Robustness, recovery, compensation, and adaptation are distinct. Adaptation requires a change that restores or improves performance under a relevant challenge.
- State important boundaries, observations, interventions, comparators, resources/costs, and evidence limits.
- On external systems, prefer **prospective risky predictions**: state the expected intervention/failure-boundary ordering and what outcome would count against the explanation before running the test.
- When an established neighboring method fits the assumptions, use it as a baseline rather than inventing project-specific vocabulary for the same task. If the competence layer adds no validated value, report an application/comparison, not a new framework.
- When discussing Levin/TAME, preserve the source vocabulary. Do not mechanically translate *competency* to project *capability*, reduce all *intelligence/goal-directedness* language to the flexibility row, or call persistent latent state *memory* without a history-dependent test. Use the project-specific refinements in experiment records when their evidentiary precision is needed.
- Prefer the smallest experiment that can change the scientific conclusion. Useful negative results count.
- Add substrate capability, metrics, UI, or governance only when a concrete experiment needs them.
- Before implementing a new dynamical/developmental system, check whether an externally authored executable model or corpus already supplies the phenomenon. Default to **wrap, intervene, compare**.

## Evidence discipline

- Native protocols, code, raw/result packages, and committed observations are the authority for what was actually done.
- Preserve counterevidence and material corrections. Never rewrite historical results to fit a newer interpretation.
- A test passing is evidence about what that test covers, not automatic evidence for the scientific claim.
- For important Goal Discovery demonstrations, use a real information barrier where possible: declare the candidate family and access contract, give the analyst only the permitted interface, freeze the inference, then reveal implementation/intent for audit.
- For discovery claims, record rival criteria that remain compatible with the evidence and the intervention that would discriminate them.
- A method's success is not "it guessed the author's label." It should recover only the resolution supported by the evidence and abstain from stronger claims.

## Documentation, plans, and repository discipline

Documentation should **reduce the amount an agent must read**.

The wiki is **derived progressive-disclosure navigation and synthesis**. It is the front door, not a second native authority. Follow consequential claims to the owning decision, accepted plan, experiment record, code/test contract, or result artifact.

Use one owner per mutable fact:
- `docs/decisions/` — durable repository-level choices;
- `docs/plans/` — accepted bounded future-work authorization;
- native experiment README — experiment interpretation, scope, and limits;
- experiment code — executed procedure;
- tests — software/intervention contract verification;
- committed result artifacts — observations;
- `wiki/` — derived navigation/synthesis over those owners.

A plan must begin from an explicit gap, constrain the intended artifacts/tests/evidence, and state stop rules/non-goals. **Plan completion never establishes a scientific finding or closes a scientific gap by itself**; fresh evidence and re-characterization do.

Historical `goal-discovery/docs/plans/`, audits, generated status views, chronology, and superseded records remain provenance. Do not reactivate imperative language from them without a new accepted plan.

Do not create another roadmap, status, handoff, research-state, or conceptual surface when a native owner or derived wiki route already covers the concern. General-purpose infrastructure whose scope is independent of Collective Competence belongs in its own repository; the general Scientific Hypergraph IR is one such extracted authority.

Long-form exploratory/philosophical discussion is not working-project authority. Promote only a compact falsifiable question, conjecture, decision, or intervention implication when it changes live research.

Keep `.agentic/relationships.yaml` synchronized when a current decision/plan/experiment changes its code, test, evidence, or navigation relationships. Prefer explicit relationships over asking future agents to infer them from prose.

`AGENTS.md` is the authored instruction source for Claude Code and Codex; update the nearest file directly.
