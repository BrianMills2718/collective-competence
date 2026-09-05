---
doc-role: context-and-maintenance-navigation
authority: derived
lifecycle: active
sources:
  - ../CLAUDE.md
  - ../goal-discovery/docs/CLAUDE.md
---
# Work from the goal, keep knowledge usable

[Project wiki](../wiki/index.md) · [Research roadmap](README.md) ·
[Current plan](../goal-discovery/docs/plans/current_research_plan.md)

## Two entry layers, different jobs

The instruction hierarchy is the mandatory behavioral bootstrap. The project
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
| Strategy or next experiment | Ontology -> charter -> current plan's selected evidence -> native result/protocol; research topic only when wider context is needed |
| Construct or compare a competent system | Ontology -> charter -> roadmap -> apparatus -> authored mechanism/capability contract -> challenge and ablation evidence |
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

Record material changes in the [development log](../wiki/development-log.md),
referencing the current owner and evidence. The log replaces stale narrative
snapshots, not native protocols or observations. Superseded authored material
moves outside active search only through the shared manifest, semantic preflight,
stable repository identity, and recovery-log procedure; never create another
project-local archive directory. Archiving here is **deletion plus a row in**
[**the archive recovery index**](../wiki/archive-index.md): Git is the recovery
route, and `scripts/check_archive_index.py` verifies every entry is genuinely
recoverable and genuinely gone from the tree. Evidence — preregistrations,
results, packages, briefs, historic audits — is preserved by rule and is never
an archive candidate.

Run from this checkout:

```bash
python3 scripts/sync_agent_context.py --write
uv run --project goal-discovery python scripts/render_knowledge_index.py --write
python3 scripts/sync_agent_context.py --check
uv run --project goal-discovery python scripts/render_knowledge_index.py --check
uv run --project goal-discovery python -m unittest scripts.test_documentation_tools
python3 scripts/check_evidence_custody.py
python3 scripts/render_status_page.py --write
python3 scripts/render_status_page.py --check
python3 scripts/check_archive_index.py
```

The last one is the evidence-custody guard, added 2026-09-05. It fails when a
result package that a tracked document or module references is not itself
tracked, which is how thirteen packages backing the live conjectures stayed
outside Git while `git status` reported clean. It also fails when the scan finds
no citations at all, or none from a source type that
[its baseline](../scripts/evidence_custody_baseline.json) records as
contributing — a scan that finds nothing has reported that it is broken, not that
custody is clean. `goal-discovery/tests/test_evidence_custody.py` runs it as part
of the suite and includes the negative controls that prove each of those paths
fires.

`scripts/render_status_page.py` renders [the visual status page](../wiki/status.html) from committed result packages and the experiment register. It is generated for the same reason the scoreboard is: a hand-maintained status surface goes stale, and this repository already had three that must move in lockstep, two of which were stale when an outside reader looked. `--check` fails when the page and the evidence disagree, and the renderer refuses a live record with no `outcome_class`.

These tiny adapters generate navigation from authored sources. They do not
infer scientific outcomes, replace shared governance tooling, install hooks,
or prove client context loading. Shared Markdown link validation may be run
with Project Meta's existing `scripts/check_markdown_links.py --repo-root <repo>`.
A successful index build is not a usability test; verify reported broken links
relative to the containing file before changing them.

Reviewed intent for documentation added after the current baseline is recorded
in [`scripts/artifact_intents.yaml`](../scripts/artifact_intents.yaml) and checked
with Project Meta's shared `scripts/check_artifact_intents.py`; this repository
does not fork the shared checker or claim retrospective coverage of the legacy
corpus.

### Check retrieval after structural changes

Ask an independent reader to recover the project goal, latest finding and its
limits, next scientific question, relevant counterevidence, and priority owner
starting from the root instructions. Record sources opened and ambiguities;
repair failed routes, not the answers. Disclose prior context if the reviewer
is reused. A single successful read does not establish optimal retrieval.
Keep execution receipts in the change review, not another recurring audit file.

### Fresh-agent handoff acceptance

Do not create a separate handoff narrative. Update the existing concern owners,
then verify that a reader starting at root instructions can recover, with links:

- the broader agenda, its two named research arms, and what is shared apparatus;
- why specimen origin, analyst access, and research purpose are independent;
- the latest accepted result, its strongest alternatives, and its claim limits;
- the current scientific bottleneck and the one next decision—not a backlog;
- explicit unknowns, integrity concerns, quarantined evidence, and stop rules;
- the exact native protocol/result and relevant source/test routes; and
- which local branches, running services, or generated files are authoritative;
  and which ignored result/receipt paths must be preserved rather than broadly cleaned.

If two current pages disagree, repair the concern owner and its projections.
Do not paper over the conflict with another summary.

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

The ontology owns terminology and conceptual relationships; the charter owns
purpose and scientific boundaries; research synthesis owns cross-experiment
interpretation; result files own measurements; the current
plan owns priorities; JSON experiment records own classification and source
links; generated catalog/register pages are projections. Correct each concern
at its source.
