# Competence research agenda — agent bootstrap

## Goal: preserve the integrated research agenda

Develop one integrated, currently unnamed research agenda with two arms. The
**Collective Competence** arm constructs and explains how mechanisms and
component capabilities produce system- or collective-level competence. The
**Goal and Competence Discovery** arm infers candidate goals and competence from
allowed observations, interventions, and challenges. The **Dynamical
Laboratory** is shared apparatus for both arms.

Specimen origin (constructed/imported/empirical), analyst access
(black-box/white-box/blind-first reveal-later), and research purpose are
independent. Do not call white-box construction an arm or treat a known authored
target as a discovery. Sorting, thermostats, flocking, networks, and composition
are tests or enablers, not alternative project goals. The UI is apparatus, not
the destination.

## Read before interpreting or changing the project

1. Enter through [the project wiki](wiki/index.md).
2. Read the canonical [research ontology](wiki/ontology.md) for terminology and
   the [charter](goal-discovery/docs/PROJECT.md) for purpose and scientific scope;
   the [current plan](goal-discovery/docs/plans/current_research_plan.md) owns
   priorities for the active Goal and Competence Discovery lane, not the full
   agenda and not historical plans or a dashboard's cached status.
   For the next experiment, use that plan's selected evidence and counterexample
   links before expanding into the full research history.
3. Follow the task's topic to native evidence/code and the applicable subtree
   instructions below. Read mandatory context; do not load the entire archive.
4. State the checkout/revision and any local changes before claiming what runs.
   Separate an implemented feature, an observed run, and a scientific finding.

For "what have we learned?", read [research synthesis](roadmap/research.md),
then its [experiment register](roadmap/experiments.md) and exact result/protocol.
Unreviewed metadata is not a finding. Corrections and failed confirmation constrain
earlier headlines; a stop applies to its tested route, not the project's goal.

| Work scope | Additional instructions to read explicitly |
|---|---|
| Laboratory work under `goal-discovery/` | [Laboratory rules](goal-discovery/CLAUDE.md) |
| Documentation or research records | [Documentation rules](goal-discovery/docs/CLAUDE.md) |
| Simulation, analysis, or UI source | [Source rules](goal-discovery/src/CLAUDE.md) |
| Tests and validation | [Test rules](goal-discovery/tests/CLAUDE.md) |

Nested instructions add local rules, not another project narrative. This table
requires explicit reading; it does not claim any client automatically loads
nested `CLAUDE.md` files. A task naming an exact source can go directly there
after orientation; that source must remain discoverable through the wiki.

## Scientific and execution constraints

- Apply the [canonical ontology](wiki/ontology.md). Distinguish authored targets,
  mechanisms, and capabilities from inferred
  candidate goals and measured competence. Convergence, prediction, low disorder,
  or an attractive animation does not establish a goal.
- Use *competence* for goal-relative effectiveness and flexibility under a
  declared challenge family. Treat robustness as performance across perturbations
  and adaptation as change that restores or improves performance after loss.
- State the substrate, focal boundary, allowed observations, intervention,
  comparisons, and evidence limits. Current models do not imply a universal substrate.
- Prioritize the next decision-changing experiment per unit effort. Enabling
  work must name the research question it unlocks; useful negative results count.
- Preserve protocols, original observations, counterevidence, and dirty work.
  Never revise historical outcomes to make a current interpretation look stronger.
- Ignored result packages and local execution receipts do not make the tracked
  checkout dirty. Never use a broad clean command to improve appearances;
  classify and verify an exact target before removing reproducible material.
- Update the owning wiki topic and native authority after material work. Avoid
  separate current narratives, repeated strategy docs, and unindexed evidence.
- Use [the development log](wiki/development-log.md) for a compact referenced
  account of material changes. Superseded narratives leave active search through
  the shared archive procedure; native protocols and observations remain evidence
  until their active obligations and relationships are explicitly dispositioned.
- Shared policy lives in Project Meta's Documentation and Context guide and its
  linked authorities, reachable from [workflow](roadmap/workflow.md#shared-policy-and-evidence-ownership);
  do not fork it into project-local policy machinery.

## Maintain this bootstrap

Follow **instructions first -> improve wiki/docs -> fresh-reader review -> revise
instructions**. Test whether a reader can recover the goal, current state,
evidence limits, and next action without reconstructing history.
Keep volatile status in the current plan. Each first-party `CLAUDE.md` is
authored; its adjacent `AGENTS.md` is generated by
`python3 scripts/sync_agent_context.py --write`. Check every discovered
first-party instruction pair with `python3 scripts/sync_agent_context.py --check`.
