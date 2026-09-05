---
doc-role: archive-recovery-index
authority: canonical
lifecycle: active
sources:
  - ../scripts/check_archive_index.py
---
# Archive recovery index

[Project wiki](index.md) · [Failure log](failure-log.md) ·
[Development log](development-log.md)

**Archiving in this repository is deletion plus an entry here.** The shared
policy requires archived material to be *"reached through the archive index and
recovery route on demand, not injected as current instructions"* — it leaves
active navigation, and it stays reachable. Git is the recovery route; this table
is the index.

The bytes are not moved. Moving a stale document into an `archive/` directory
keeps it inside grep and inside the generated document catalog, which is the
opposite of leaving current instructions, and
[workflow](../roadmap/workflow.md) forbids creating another project-local
archive directory in any case.

## How to archive a document

1. `git rm` it.
2. Add a row below with the **commit that still contains it** — normally the one
   immediately before the deletion — and a reason a reader can act on.
3. `python3 scripts/check_archive_index.py` must pass. It verifies the recorded
   commit really contains the file at that path, that the file is really gone
   from the tree, and that a reason is recorded.

Recover with `git show <commit>:<path>`.

**This does not apply to evidence.** Preregistrations, result records, result
packages, original briefs and historic audits are preserved by rule and are not
archive candidates. This index is for superseded narrative, plans and guidance.

## Archived

| Archived path | Recover from | Date | Reason |
|---|---|---|---|
| `goal-discovery/docs/archive/pre-consolidation-readme.md` | `f2e1d02` | 2026-09-05 | Pre-consolidation snapshot, `lifecycle: superseded` since the documentation consolidation. Superseded by its live counterpart; retained only because the plan was waiting on a mover that does not exist. |
| `goal-discovery/docs/archive/pre-consolidation-research-plan.md` | `f2e1d02` | 2026-09-05 | Pre-consolidation snapshot, `lifecycle: superseded` since the documentation consolidation. Superseded by its live counterpart; retained only because the plan was waiting on a mover that does not exist. |
| `goal-discovery/docs/archive/pre-consolidation-allocation-protocol.md` | `f2e1d02` | 2026-09-05 | Pre-consolidation snapshot, `lifecycle: superseded` since the documentation consolidation. Superseded by its live counterpart; retained only because the plan was waiting on a mover that does not exist. |

## Why this exists

The [current research plan](../goal-discovery/docs/plans/current_research_plan.md)
recorded that three superseded pre-consolidation snapshots *"remain physically
present until the shared archive system can perform the registered, logged
move,"* and instructed that they not be moved or deleted by hand.

Checked 2026-09-05: **no such mover exists.** Nothing in `project-meta/scripts`
or `enforced-planning/scripts` moves documents to an archive.
`archive_registered_repository.py` archives whole repositories,
`archive_coordination_records.py` archives coordination claims, and
`generate_archive_preflight.py` produces preflight evidence for project-meta's
own two archive roots. `archive_lifecycle.py` describes itself as a *"CLI wrapper
for report-only document lifecycle and archive blockers"* — it was never going to
move anything — and it cannot run against this repository at all, exiting with
`relationship config does not exist:
/home/brian/code/collective-competence/scripts/relationships.yaml`.

So the plan was waiting on a capability that was never built and never
scheduled, and the wait was unnecessary: the policy asks for an index and a
recovery route, not a move.
