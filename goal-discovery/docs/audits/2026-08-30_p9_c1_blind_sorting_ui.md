# P9-C1 blind sorting calibration audit

**Date:** 2026-08-30  
**Disposition:** checkpoint pass; retain as calibration UI only  
**Claim level:** engineering calibration, no automated goal-discovery claim

## Outcome

The sorting laboratory now supports a coherent blind-calibration workflow. It
starts from observable trajectories rather than narrating sorting as the known
goal, declares the focal system/environment boundary, exposes typed matched
interventions, and keeps authored truth behind a separate evidence-access
control.

## First-principles audit

| Question | Finding | Decision |
|---|---|---|
| What is the substrate? | A deterministic line of identity-bearing cells with carried values, capabilities, snapshot/restore, and a scheduler | adequate for sorting calibration; not general |
| What is inside the declared system? | cells, positions, values, and action capabilities | explicit |
| What is outside? | fixed geometry and activation scheduler | explicit but limited |
| Is the environment dynamic? | the scheduler can be changed at a branch; cells cannot change scheduler or geometry | call it limited contextual dynamics, not reciprocal environment |
| What counts as competency? | reliable achievement or recovery over a stated challenge family | one trajectory is demonstration only, not reliability |
| Are all regularities goals? | no; ledger separately labels outcomes, progress measures, mechanisms, invariants, constraints, and competencies | pass |
| Is discovery automated? | no; current candidates are a transparent calibration ledger | retain the limitation prominently |

## Intervention audit

- **Internal state:** a block swap changes arrangement once, then normal rules resume.
- **Capability/mechanism:** selected cells become moveable- or immovable-frozen.
- **Environment dynamics:** the external activation scheduler changes persistently.
- **Not represented:** topology, sensing/action interfaces, changing demand or
  task, and injected state/sensing/action noise.

The scheduler test verifies that cells, tick, comparison/swap counters, and RNG
state are unchanged at the intervention boundary. All arms share the exact
pre-intervention history.

## Observation and claim audit

Sealed mode exposes position, identity, value, visible capability, counters,
and derived trajectory measures. It withholds authored rule, internal target,
and authored outcome. The candidate ledger shows evidence and a distinguishing
test for each interpretation but does not score or promote a goal. Ground truth
is a separate calibration reveal.

The known Zhang/Goldstein/Levin confirmation remains visible as prior white-box
evidence and is explicitly excluded from blind discovery evidence.

## Verification

- Targeted sorting-laboratory suite: 15 passed.
- Full repository suite: 153 passed, 16 optional NetLogo checks skipped.
- Ruff: passed for the modified laboratory and test files.
- Live route: `http://localhost:5011/app` loaded with all seven regions.
- Live interaction: intervention family selection exposed the scheduler control,
  hid irrelevant controls, and updated the intervention contract.
- Live reveal/reseal: ground-truth table, authored rule tooltips, and privileged
  algorithm selector appeared only after reveal and disappeared after resealing.
- Cell comprehension: every card now renders explicit `VALUE`, `ID`, and
  capability labels. Browser screenshots verified readable card styling.

## Time-value review

The work reused Panel, HoloViews, Tabulator, and the validated `SortingWorld`.
No simulator, chart framework, or generalized substrate was added. Most code
went to the missing scientific distinctions and verification rather than visual
polish. The live audit found an unreliable styled reveal control; it was replaced
with the same standard select interaction already proven elsewhere in the UI.
It also found that global styles did not reach the embedded cell view; styles
are now scoped to each pane, and the two arms use full-width aligned rows.

## Next checkpoint

Freeze a held-out blinded sorting-discovery protocol with candidate generation,
abstention, confusion, and intervention-selection criteria. Only if that method
recovers the known classification prospectively should it be tested on a second
system. Keep the passive-bowl runtime reuse test separate from any scientific
goal-discovery claim.
