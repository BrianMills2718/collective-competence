---
authority: none
owner: collective-competence (Brian)
destination: >
  Either (a) a registered experiments/NN-.../ entry once validated, or
  (b) permanent external-reference-only status (cross-linked from the wiki,
  never native code here) — undecided until both conditions below resolve.
reason: >
  Raw output (CSV/PNG/JSON) from an external, independent research thread —
  a separate ChatGPT-based conversation exploring "Platonic ingress" toy
  automata (computational-boundary tests, causal abstraction, representation
  scrambling, metastability/dissipative-adaptation experiments). No native
  runnable source code exists in this repo for any of it; the narrative
  descriptions live outside this repo at
  /home/brian/code/algorithmic_ingress*.md (parts 1-5). The generating
  agent's own part5 document explicitly states its central enrichment
  numbers (up to ~181x) should not yet be treated as benchmark results —
  positive controls were proposed but had not been run as of this import.
  Specimen origin per this repo's own ontology: constructed/imported, not
  empirical — but analyst access and evidentiary status are unresolved
  until (1) the source agent's own validation pass completes, and (2) a
  landscape survey (in progress, run by the same source agent) checks
  whether this duplicates existing published work.
expires_at: "2026-09-17T00:00:00Z"
---

# Platonic ingress toy automata — imported, unvalidated

> **Relevance changed 2026-09-05, before the 09-17 expiry.** The substrate design
> discussion turned to *capability composition* — elements differing in
> computational class, one contributing memory, one contributing learning — and
> this holding's `computational_capacity_ladder_summary.csv` measures exactly that
> axis: `3-state DFA -> one counter` on Dyck-1, `pushdown -> two counters` on
> a^n b^n c^n, with `abc_capacity_boundary.csv` showing a modular PDA degrading
> 1.0 -> 0.33 while two counters hold at 1.0.
>
> **This does not change its evidentiary status**, which remains as stated above:
> no native runnable source here, headline enrichment numbers its own author said
> should not be treated as benchmark results, positive controls proposed and not
> run. It is **design input, not evidence.**
>
> **Narrative copied in 2026-09-05.** The six documents this INTENT describes as
> living *"outside this repo at /home/brian/code/algorithmic_ingress*.md"* existed
> in exactly one place, untracked, on a directory that is not a repository. They
> are now copied to [`narrative/`](narrative/README.md) — 5,496 lines, bytes
> unmodified — so the disposition decision is not also a race against losing
> them. Evidentiary status is unchanged: design input, not evidence.
>
> The open disposition question is therefore no longer "does this expire" but "is
> this the capability axis the substrate should be built around" — see
> [the substrate design discussion](../../wiki/substrate-design.md). Do not let
> it lapse on the date without answering that.

39 files (`.csv`, `.png`, one `.json` per major result) covering: static vs.
dynamic ("metastable") occupancy of abstract patterns in a 5,832-machine toy
automaton universe, drive-dependent selection under periodic forcing,
computational-capacity boundaries (regular/context-free language separations,
a morphogenesis finite-horizon analogue), and representation-scrambling
controls.

**Do not cite these as findings.** They are raw output from a different
codebase, reviewed at the summary/claims level (not full independent
reproduction) in the `levin-wiki` living document
[`platonic-space-and-ingression.md`](../../../../levin-wiki/wiki/concepts/platonic-space-and-ingression.md)
and in the source narrative documents themselves. One general mathematical
claim underlying the metastability results (the stationary-distribution
formula for a state-dependent-escape-rate process on a regular graph) was
independently verified correct by direct construction; the specific reported
numbers were not independently reproduced.

See `misc/README.md` for the quarantine convention this follows.
