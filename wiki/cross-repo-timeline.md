---
doc-role: cross-repository-timeline
authority: derived
lifecycle: active
sources:
  - development-log.md
  - ../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md
---
# Cross-repo timeline — competence / goal-discovery / Levin / platonic work

Built from git logs of: collective-competence, levin-wiki, agent_ecology,
platonic-semantics, platonic-atlas-math (263 commits), plus file mtimes for
non-git artifacts (~/code/levin/, Downloads/). All times local (-0700).

## Structural events

| When | Where | What |
|---|---|---|
| 2025-12-29 | agent_ecology | Repo initial commit (agent ecology sim v1/v2) — unrelated line |
| 08-26 15:12 | agent_ecology `ec00406` | **Experiment 1 written**: self-sorting agents with defective local components |
| 08-26 15:56 | agent_ecology `66b007c` | "Heterogeneity threshold is a headcount, not a fraction" |
| 08-26 16:05 | **collective-competence `0795072`** | **Repo founded** — experiment 01 moved in. README: "How does coupling among bounded local systems produce higher-level competence?" 7-experiment ladder, LLM agents last |
| 08-26 16:05 | Downloads | `Levin_Diverse_Intelligence_Library.md` downloaded — same minute as the founding commit |
| 08-26 16:10 | agent_ecology `c904902` | "Move the self-sorting experiment to BrianMills2718/collective-competence" |
| 08-26 19:37 | collective-competence `95b5099` | **goal-discovery imported** — 39 files, 3,497 lines, complete project (Makefile, pyproject, uv.lock, docs, src, tests, results). Its own sources/README already names the replication target: Zhang, Goldstein & Levin (2024), arXiv:2401.05375. No prior git history came across |
| 08-27 06:55 | Downloads | `Dynamical_Laboratory_Coding_Agent_Spec.md` |
| 08-27 07:24 | Downloads | `Levin_Diverse_Intelligence_Library_Expanded.md` |
| 08-27 07:35 | Downloads | `Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md` |
| 08-27 08:02 | Downloads | `Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md` |
| 08-27 | collective-competence (8 commits) | Experiments 001 (sorting replication) and 002 (passive bowl control) |
| 08-27 10:49 | **levin-wiki** (5 commits) | **Repo founded** — "build local Levin Karpathy wiki seed" |
| 08-28 | levin-wiki (1) | quiet day; collective-competence silent |
| 08-29 | collective-competence (20) | P5-000, P5-001, P5-002, P6-001 neuromast, archive-first contract, P7-002 |
| 08-30 18:33 | collective-competence `9b8666a` | **The three briefs and PROJECT.md (the charter) enter the repo** — 4 days after goal-discovery arrived. "Consolidate laboratory documentation around a linked development wiki" |
| 08-31 | collective-competence (106) | Biggest day: P10, P11, P12, P13, P14 all frozen, run, recorded |
| 08-31 22:44 | collective-competence `046f049` | **"docs: unify competence agenda and freeze P15 contract"** — `wiki/` created; the two-arm framing written |
| 09-01 | collective-competence (6) | P15 proposal layer implemented and frozen |
| 09-02 | collective-competence (7) | Governance: project membership, workspace function labels |
| 09-02 | levin-wiki (16) | Active wiki work |
| 09-03 | levin-wiki (25), platonic-atlas-math (41, new repo), platonic-semantics (6, new repo), collective-competence (10) | **Platonic day** — 82 commits across 4 repos. Ingress data quarantined into collective-competence/misc/, morphogenesis scaling law computed, ontology cross-link added |

## Per-repo per-day commit counts

```
2025-12-29  agent_ecology 1
2026-02-24  agent_ecology 2
2026-08-26  agent_ecology 3          collective-competence 2
2026-08-27  collective-competence 8  levin-wiki 5
2026-08-28  levin-wiki 1
2026-08-29  collective-competence 20
2026-08-30  collective-competence 4
2026-08-31  collective-competence 106
2026-09-01  collective-competence 6
2026-09-02  collective-competence 7  levin-wiki 16
2026-09-03  collective-competence 10 levin-wiki 25
2026-09-03  platonic-atlas-math 41   platonic-semantics 6
```

## Notes on provenance limits

- agent_ecology2 (1,387 commits) and agent_ecology3 (158) are a different
  project ("Agent Ecology" simulation); no sorting/Levin/competence content.
- ~/code/levin is not a git repo — file mtimes only.
- Downloads mtimes may reflect re-downloads, not first receipt; one brief has a
  duplicate `(1).md.crdownload`.
- Addenda 1 and 2 are referenced by Addendum 3 but exist nowhere on disk.
- goal-discovery has no separate repo on disk or on the BrianMills2718 GitHub
  account; whether it ever had its own git history is not determinable here.

The 263 merged commits behind this are not vendored; regenerate with
`git -C <repo> log --all --format='%ad|<repo>|%h|%s' --date=format:'%Y-%m-%d %H:%M'`
across the five repositories named above, then sort.

---

## CORRECTION (later in session): the Aug 26 founding, from the session transcript

Source: Claude Code session `a9350e56-4374-4a1d-8aaa-1a3453b32837`
(`~/.claude/projects/-home-brian-code/`), running 08-26 14:49 -> 08-27 07:43 local.
Earlier searches missed it because they filtered on file mtime, which is 08-27.

| Local time | Event |
|---|---|
| 08-26 14:49 | Brian pastes advice from another conversation: "For the **very first experiment** I would go much simpler than Minecraft, economics, or even a full ABM framework. I'd start with a **Levin-style self-sorting system with defective local agents**." Sorting is chosen as the simplest entry point, not the subject |
| 08-26 15:12 | Experiment 1 committed — into agent_ecology |
| 08-26 15:49 | Brian: "why did you put this in agent ecoloyg?" |
| 08-26 16:04 | Brian: "i want a fresh repo ... why did you continue when yu dneed somethign form me?" |
| 08-26 16:05 | **collective-competence founded** |
| 08-26 19:16 | Brian runs a re-anchor prompt: "Brian has lost the thread of what we are doing" |
| **08-26 19:22** | **Brian pastes a 23,471-char document: "First-Wave Implementation Brief: Goal Discovery and Goal Attribution in Tiny Deterministic Systems"** |
| **08-26 19:37** | **goal-discovery imported — 39 files, 3,497 lines, 15 minutes after the brief** |
| 08-27 07:42 | Brian: "actually before we go further can we think about a ui for this?" |

### Consequences

- goal-discovery never had a separate repository. Its "prior history" is one
  pasted design brief and a 15-minute generation. Nothing was lost in the merge.
- **That founding brief is not in collective-competence.** Recovered to
  `goal_discovery_founding_brief.md`. The three later briefs were preserved in
  `goal-discovery/docs/sources/briefs/` on 08-30; this one never was.
- The agent_ecology entanglement was flagged by Brian within 37 minutes and
  fixed by founding the fresh repo. It was not unnoticed drift.

### Searches behind the negative claims (all completed, none truncated)

- Full filesystem sweep of /home/brian: the only copies of goal-discovery's
  files anywhere are inside collective-competence.
- All 4,142 Codex sessions, matched on strings unique to this work
  (`cell-view sorting`, `Zhang, Goldstein`, `sortedness value`): earliest hit
  08-27, after the founding.
- 459 exported ChatGPT conversations: no match.
- An earlier filesystem search reported here as empty had in fact been
  **terminated by its own timeout**; it was re-run to completion.

### agent_ecology2 / 3

AE2's README states its goal as "emergent collective capability - a system where
agents produce more together than the sum of what they could produce alone",
for LLM agents. collective-competence's original ladder ended at "07 LLM agents,
only once the measurables hold up without them". AE2 is the destination that
ladder was climbing toward. collective-competence references AE2 and AE3
nowhere - zero mentions in the entire repository.
