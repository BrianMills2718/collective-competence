---
doc-role: implementation-receipt
authority: historical
lifecycle: completed
---
> Historical implementation receipt; its original checks and next-step advice
> are preserved as recorded. Runtime integration has its own verification in the
> [current plan](../plans/current_research_plan.md); this receipt does not set priorities.

# P8-C1 sorting-laboratory vertical-slice audit

**Date:** 2026-08-30  
**Decision:** checkpoint pass; recommend the extract-and-test-on-passive-bowl
branch as the next separately authorized phase.  
**Scientific authority:** unchanged. This is an engineering and method
checkpoint over existing validated evidence, not a new scientific result.

## Outcome

P8-V0 through P8-V3 now form one runnable desktop laboratory. A user can
configure the elementary cell-view sorting system, use a standard timeline
player, inspect persistent identities and local activation events, branch from
an exact snapshot, compare state or mechanism damage against the matched
baseline, change synchronized representation lenses, and inspect the frozen
published-result comparison and its claim boundary.

The active surface is the first tab of the existing cockpit at
`http://localhost:5011/app`. A standalone entry point is also available in
`src/experiments/sorting/lab_app.py`, but the checkpoint was exercised through
the documented cockpit URL.

## C1 gate audit

| Gate | Evidence | Result |
|---|---|---|
| Configure and run without terminal commands | Desktop controls for cell count, initial arrangement, algotype, activation order, seed, horizon, branch tick, and damage mode. Changing a control automatically rebuilds and resets the trajectory; a manual build button is also present. | pass |
| Understand local action and global progress | Every cell shows value, persistent identity, and capability; its tooltip and microscopic table expose rule, internal target, and last local activation. Tick, comparisons, swaps, and aggregate measures remain visible. | pass |
| Compare matched futures on one screen | Baseline and perturbed arrays share one timeline and are rendered side by side from an exact common snapshot. | pass |
| One tick controls every view | Player changes both worlds, counters, explanation, metric plot, microscopic table, neighbour table, capability table, and aggregate table. | pass |
| Explanations and tooltips state meaning and limits | Each region names its question. PASSIVE and BLOCKED status use text plus dashed/double borders, not color alone. Claim text distinguishes state damage, mechanism damage, convergence, and competence. | pass |
| Deterministic replay and intervention integrity | `tests/test_sorting_laboratory.py`, `tests/test_snapshots.py`, and model tests cover identical replay, common past, full snapshot identity, block-swap conservation, freeze semantics, and counter definitions. | pass |
| No invented outcome or silent model change | Live frames call the authoritative `SortingWorld`; metrics call `sorting.representations.evaluate`; the replication table is recomputed from the frozen CSV and metadata. Added event instrumentation records actions but does not alter rule execution. | pass |
| Documented launch works | The exact command below started Bokeh/Panel and served `/app`; a fresh browser session rendered the laboratory. | pass |
| Interface improves inspectability | Live checks showed that a reverse-order choice regenerated tick 0, scrubbing to tick 12 synchronized all views, and immovable freezing exposed 83% active cells, 73% traversable edges, and the frozen identities. This demonstrates reduced integration effort; moderated novice comprehension remains unmeasured. | pass with stated limit |

## Live interaction and defect record

The first live load exposed a render-blocking key mismatch in the analytical
measure selector. Component construction tests had not exercised the server
document path. The selector mapping was repaired, the server was restarted,
and the live page then rendered.

The initial form also consumed the entire first viewport. Configuration and
transport were compacted into a paired desktop layout so the perturbation
surface begins immediately below them. Controls now rebuild automatically,
which prevents a visible configuration choice from coexisting with a stale
trajectory.

Final browser checks:

- loaded `http://localhost:5011/app` in a fresh Panel session;
- selected reverse initial order and observed the baseline reset to tick 0 with
  values 11 through 0;
- selected immovable mechanism damage and observed the intervention contract
  change to `freeze_cells(count=2,mode=immovable,positions=[4, 5])`;
- scrubbed to tick 12 and observed synchronized baseline/branch counters,
  BLOCKED cells, capability values, and frozen identities; and
- inspected the accessible DOM for the five question regions, cell tooltips,
  four synchronized lenses, and the published-result boundary.

## Verification

```text
uv run pytest -q
147 passed, 16 skipped

uv run ruff check src tests
All checks passed

git diff --check
passed
```

The 16 skips are optional NetLogo-backed checks and are not part of the P8
Python/Panel vertical slice.

## Time against caps

The goal clock recorded 22 minutes 38 seconds through implementation, live C1
checks, documentation, and authoritative-state closure.
Because the versions were built as one vertical slice, the per-version split is
reconstructed from the work sequence rather than separate timers:

| Version | Approx. actual | Cap | Audit |
|---|---:|---:|---|
| P8-V0 outcome shell and state reconciliation | 2 min | 30–45 min | all five question regions mapped to real sources |
| P8-V1 authoritative motion and transport | 4 min | 60–90 min | deterministic motion, identity, actions, counters, reset/replay |
| P8-V2 exact branch and damage modes | 3 min | 90 min | common snapshot, block swap, moveable/immovable freeze |
| P8-V3 synchronized lenses and replication boundary | 4 min | 90–120 min | six frozen metrics plus micro/relational/capability views |
| P8-C1 tests, live defect repair, audit, and state closure | about 10 min | checkpoint | one live defect found and repaired; no open high-priority defect |

The unusually short time reflects aggressive reuse of Panel's Player,
HoloViews/Bokeh, Tabulator, the validated sorting model, snapshot protocol,
interventions, representation functions, and existing confirmation evidence.

## Version-by-version value audit

| Version | Goal alignment | Fidelity and replay | Comprehension | Reuse decision | Next-value decision |
|---|---|---|---|---|---|
| V0 | Five regions each name the research question they answer and the real source that will fill them. | No mock outcome was introduced. | Mature flow was visible before extra machinery. | Panel cards and the existing cockpit route were reused. | Motion remained the highest-value missing evidence, so advance to V1. |
| V1 | The interface exposes the elementary substrate rather than a programme-status abstraction. | Frames come from `SortingWorld`; identical configuration and seed reproduce every snapshot. | Persistent ID, value, capability text, last activation, counters, and standard transport are visible together. | Panel Player replaced a custom animation loop; a small event trace was added without changing dynamics. | A matched intervention was the next discriminating interaction, so advance to V2. |
| V2 | State versus mechanism damage directly tests the recovery questions. | Both arms restore one full snapshot; block swap conserves cells and counters; freeze changes only capability. | Baseline and branch share a timeline, intervention label, boundary marker, and side-by-side worlds. | Existing snapshot and intervention functions were reused; no branching framework was created. | Representation linkage was the remaining explanation gap, so advance to V3. |
| V3 | Micro, neighbour, capability, aggregate, and publication views answer the specified questions without new science. | Frozen metrics call the authoritative representation set; publication values are recomputed from measured CSV and metadata. | One tick updates all lenses; terse limits explain what each result does not establish. | HoloViews/Bokeh and Tabulator supply plots and tables; no visualization framework was built. | The complete vertical slice was ready for C1; stop feature development. |
| C1 | The slice now tests the UI-first method and the smallest substrate boundary. | Full suite, lint, whitespace, and live server checks passed after repairing one render-blocking defect. | Configuration, automatic rebuild, scrubbing, damage status, capability evidence, and publication boundary were exercised live. | Only a seven-point boundary appears reusable; all cell semantics stay local. | Stop at C1 and recommend one passive-bowl second-use test under separate authorization. |

## Correctness and scientific limits

- A tick is one activation sweep. Comparisons are shown as primitive steps
  minus swaps; steps are not mislabeled as comparisons.
- The branch event occurs at a tick boundary. The baseline frame at that tick is
  the common pre-intervention snapshot; the branch frame at the same tick is
  explicitly labeled post-intervention.
- Cell identity is `cell_id`, not value or position. Freeze positions are
  resolved at the branch boundary, so the resulting frozen identities may
  differ from the selected position numbers.
- The interactive laboratory is deliberately small (6–24 cells, 15–120 ticks).
  It does not regenerate the N=100, 40-seed publication comparison for display;
  it reads the frozen measured rows and metadata instead.
- The published ranking inversion reproduced directionally. Immovable means
  agree to about 0.1; moveable errors remain lower than published. This is only
  a partial quantitative replication.
- The local event stream reports each cell's last activation within an atomic
  sweep. It is not a sub-tick animation of every comparison.
- No moderated novice comprehension session was performed. The checkpoint
  proves coherent interaction and evidence linkage, not a population-level
  usability claim.

## Earned substrate boundary

P8 exposed one small boundary worth testing, not a generalized simulator:

1. configuration creates a deterministic system;
2. snapshot and restore preserve full state and RNG;
3. one declared step advances the system;
4. observation produces a presentation frame;
5. intervention changes only declared fields at a boundary;
6. representation functions evaluate the same selected observation; and
7. provenance identifies rules, representations, seed, and evidence source.

Cells, algotypes, arrays, freeze semantics, local actions, graphs, spatial
fields, and learning remain model-local. P8 has not demonstrated that those are
universal substrate concepts.

## Selected next branch

**Extract only the seven-point boundary above and test it on the existing
passive ball-in-bowl system as the second use.** This recommendation does not
authorize that work. If the bowl needs a materially different contract, retain
the sorting adapter locally and do not force a common abstraction.

## Launch and walkthrough

```bash
cd /home/brian/code/collective-competence/goal-discovery
uv run --extra visual-workbench panel serve src/cockpit/app.py --show --port 5011
```

Open `http://localhost:5011/app`; the first tab is **Sorting laboratory · P8**.
Choose initial conditions, press Build or let a changed control rebuild
automatically, use the standard timeline transport, select a damage mode and
branch tick, compare the two cell rows, change the analytical measure and lens,
then open **Published-result boundary** for the replication table and limit.
