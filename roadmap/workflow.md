---
doc-role: context-and-maintenance-navigation
authority: derived
lifecycle: active
sources:
  - ../CLAUDE.md
  - ../goal-discovery/docs/CLAUDE.md
---
# Work from the goal, keep knowledge usable

[Wiki](README.md) · [Current plan](../goal-discovery/docs/plans/current_research_plan.md)

## Two entry layers, different jobs

The instruction hierarchy is the mandatory behavioral bootstrap. The unified
wiki is the single project-information entrypoint reached from it. Neither
replaces the other: instructions say how to orient and work; wiki topics explain
the project and connect current knowledge to evidence.

[Root CLAUDE](../CLAUDE.md) is authored; [root AGENTS](../AGENTS.md) is generated.
Read the applicable [laboratory](../goal-discovery/CLAUDE.md),
[documentation](../goal-discovery/docs/CLAUDE.md),
[source](../goal-discovery/src/CLAUDE.md), and
[test](../goal-discovery/tests/CLAUDE.md) rules explicitly.
There are no claims of automatically loaded nested instructions.

## Task-sized context

| Task | Required route, then exact evidence as needed |
|---|---|
| Strategy or next experiment | Charter -> current plan -> research topic -> relevant reviewed experiment/counterevidence |
| Interpret an experimental result | Research topic -> experiment record -> native result and protocol; examine corrections before quoting a verdict |
| Modify a simulation/analysis | Apparatus -> source instructions -> model/protocol/observation contract -> relevant tests |
| Change a visual | Usage + shared analytic contract -> source/test instructions -> exact checkout and first-user journey |
| Consolidate documentation | Documentation rules -> concern owner -> evidence relationships -> affected wiki topic |
| Recover old reasoning | Document catalog -> historical record/source lineage; never treat old next steps as present instructions |

The full catalog is a recovery route, not an instruction to read every file.
The structured register distinguishes reviewed result summaries from unreviewed
records. A result being indexed does not certify its validity.

## Maintenance loop

1. Start with first-pass root/subtree instructions preserving the complete goal.
2. Improve the native authorities and wiki synthesis around actual questions.
3. Review as a fresh reader: goal, current gap, evidence/correction, next action,
   local rule, and version boundary must be findable and correctly understood.
4. Revise the instructions to route to the improved knowledge. Keep live status
   in its owner, not duplicated in bootstrap text.
5. Regenerate projections and verify routes. Archive only through shared
   lifecycle policy; never discard unique evidence to make counts smaller.

Run from this checkout:

```bash
python3 scripts/sync_agent_context.py --write
python3 scripts/render_knowledge_index.py --write
python3 scripts/sync_agent_context.py --check
python3 scripts/render_knowledge_index.py --check
```

These tiny adapters generate navigation from authored sources. They do not
infer scientific outcomes, replace shared governance tooling, install hooks,
or prove client context loading. Shared Markdown link validation may be run
with Project Meta's existing `scripts/check_markdown_links.py --repo-root <repo>`.

## Shared policy and evidence ownership

The shared [Documentation and Context guide](https://github.com/BrianMills2718/project-meta/blob/main/docs/ops/DOCUMENTATION_PLANNING_LINKAGE_SYSTEM.md)
routes to wiki, instruction-surface, coupling, and archive authorities. For the
local checkout resolve repository ID `project-meta` through the workspace
[Project Graph](https://github.com/BrianMills2718/project-meta/blob/main/PROJECT_GRAPH.json).
These explicit repository links are fallback discovery routes when a local
workspace resolver is unavailable; access may require the owner's Git account.
The policy remains shared; this page specifies only the laboratory's routes.

[Time allocation](../goal-discovery/docs/plans/progress_allocation_protocol.md)
and [reuse selection](../goal-discovery/docs/plans/reuse_survey_protocol.md)
specialize how to advance the laboratory. Evaluate decision-changing information
and cost, not code volume, file count, or an unsupported "learning score."

Research synthesis is interpretation; result files own measurements; the current
plan owns priorities; JSON experiment records own classification and source
links; generated catalog/register pages are projections. Correct each concern
at its source.
