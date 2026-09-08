# Competence research agenda — agent bootstrap

## Start here

Read [`wiki/index.md`](wiki/index.md) before substantial work. It is the project front door and should be enough to orient you without loading the repository's history.

Then follow only the task-specific route you need:

- scientific questions → [`wiki/questions.md`](wiki/questions.md)
- current findings → [`wiki/findings.md`](wiki/findings.md)
- terminology → [`wiki/concepts.md`](wiki/concepts.md)
- current priority → [`wiki/current.md`](wiki/current.md)
- apparatus / adding a specimen → [`wiki/laboratory.md`](wiki/laboratory.md)
- audits, old plans, decisions, detailed ontology, chronology → [`wiki/reference/README.md`](wiki/reference/README.md)

Do **not** read the full ontology, failure log, development log, audits, or historical plans as routine orientation. They are reference/history, not working context. If resuming after a long hiatus, `wiki/index.md` → `wiki/current.md` → `wiki/findings.md` is the intended three-page handoff.

## Project model

The project studies how component capabilities and interactions produce robust, goal-relative competencies of systems, and what can be inferred about those competencies and candidate goals from behavior.

It has two complementary research arms:

- **Collective Competence** constructs systems and explains how their mechanisms produce system- or collective-level competency.
- **Goal and Competence Discovery** analyzes systems under declared observation/intervention access and asks which candidate goals and bounded competence claims behavior supports, contradicts, or leaves underdetermined.

The **Dynamical Laboratory** is shared apparatus. Black-box/white-box describes analyst access, not the two arms. A constructed specimen can be analyzed blind-first; an imported specimen can be inspected mechanistically.

## Before modifying code or evidence

1. Read the relevant hot wiki page.
2. Read the native experiment README/protocol and the code you will change.
3. Read the applicable subtree instructions:

| Work scope | Additional instructions |
|---|---|
| `goal-discovery/` laboratory work | [`goal-discovery/CLAUDE.md`](goal-discovery/CLAUDE.md) |
| research records/docs | [`goal-discovery/docs/CLAUDE.md`](goal-discovery/docs/CLAUDE.md) |
| source/UI/analysis | [`goal-discovery/src/CLAUDE.md`](goal-discovery/src/CLAUDE.md) |
| tests | [`goal-discovery/tests/CLAUDE.md`](goal-discovery/tests/CLAUDE.md) |

The canonical checkout is intentionally read-only; use the repository's worktree convention for writes and runs that produce output.

## Scientific discipline

- Separate **what happened**, **what the system can do**, **what counts as success**, **why it happened**, and **how strongly the interpretation is supported**.
- An authored goal criterion is legitimate in constructive work. Do not relabel it as discovered.
- Goal Discovery does not require one unique true goal. Multiple candidate criteria or `underdetermined` are valid outcomes.
- Do not assume a universal scalar notion of "more competent." Report the performance dimensions the experiment actually measures.
- Convergence, prediction, low disorder, or an attractive visualization do not by themselves establish goal-directed competence.
- Robustness, recovery, and adaptation are distinct. Adaptation requires a change that restores or improves performance.
- State important boundaries, observations, interventions, comparators, resources/costs, and evidence limits.
- Prefer the smallest experiment that can change the scientific conclusion. Useful negative results count.
- Add substrate capability, metrics, UI, or governance only when a concrete experiment needs them.

## Evidence discipline

- Native protocols, code, raw/result packages, and committed observations are the authority for what was actually done.
- Preserve counterevidence and material corrections. Never rewrite historical results to fit a newer interpretation.
- A test passing is evidence about what that test covers, not automatic evidence for the scientific claim.
- For important Goal Discovery demonstrations, use a simple information barrier where possible: construct the specimen in one context, give the analyst only the permitted interface, record the inference, then reveal implementation for audit.

## Documentation discipline

Documentation should **reduce the amount an agent must read**.

Keep current working knowledge in the six hot wiki pages. Detailed experiment records and technical documents are warm reference. Audits, chronology, closed failures, and superseded plans are cold history.

After material work, update the smallest owning hot page plus the native evidence/record that actually changed. Do not create another status surface when [`wiki/current.md`](wiki/current.md) can be updated.

Historical mistakes belong in current narrative only when they materially constrain the current scientific interpretation. Git and the reference layer preserve the rest.

`AGENTS.md` is generated from this file by `scripts/sync_agent_context.py`; keep the pair synchronized.
