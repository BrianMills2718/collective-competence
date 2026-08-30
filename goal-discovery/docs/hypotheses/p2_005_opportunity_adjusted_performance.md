# P2-005 — opportunity-adjusted performance across local rules

**Frozen before generating P2-005 outcomes.**

## Question

Conditional on the sorted target being reachable under a damaged rule's own
available actions, do bubble, insertion, and selection cells differ in whether
they actually realize and robustly retain that opportunity?

## Opportunity graph

A graph node is the complete observable cell sequence: value, identity, freeze
mode, and rule-specific internal state (`ideal_position`). A directed edge is
one state-changing activation allowed by the existing local rule:

- any active cell may be selected next;
- bubble exposes both possible left/right observations;
- insertion and selection use their existing deterministic activation rule;
- frozen cells never initiate;
- immovable cells cannot be swapped;
- moveable frozen cells may be swapped by an active cell.

The graph deliberately omits fixed sweep order. It asks whether *some* allowed
local-action path exists, not whether the actual scheduler will find it. A
branch is reachable when NetworkX finds a directed path from its initial node to
any node whose values are sorted. Shortest path length is recorded as a
descriptive opportunity cost.

## Exhaustive discovery design

Enumerate:

- all 24 permutations of four distinct values;
- all 15 nonempty freeze masks;
- moveable and immovable freeze modes;
- homogeneous bubble, insertion, and selection rules.

This creates 2,160 graph-oracle cases. For performance, run every case under
index and shuffled sweep schedules with four deterministic seeds and a horizon
of `30 * n` ticks: 17,280 actual branches.

For each algotype × damage mode × schedule report:

- opportunity rate: graph-reachable cases / all cases;
- realization rate: successful runs / graph-reachable runs;
- realized-case rate: reachable cases with at least one successful seed;
- robust-case rate: reachable cases with all four seeds successful.

Do not score success on unreachable cases as incompetence.

## Frozen integrity gates

All must pass:

- the bubble oracle agrees with the P2-003 immovable invariant on every case;
- the bubble oracle agrees with the P2-004 moveable invariant on every case;
- no actual branch reaches the goal when its graph says unreachable;
- no branch exits at the time limit without becoming quiescent;
- every reported comparison cell contains at least 30 reachable cases.

## Frozen discovery promotion gate

Promote only if at least one damage mode has the same unique best and worst algotype
under both schedules, and their robust-case rates differ by at least 20
percentage points under each schedule. Schedule-only differences are reported
but do not unlock confirmation because they may reflect the laboratory's sweep
semantics rather than collective organization.

If the gate passes, freeze a new size-5 sampled confirmation design before
generating it. If it fails, stop this sorting line and select a richer generator.

## Interpretation boundary

Reachability is opportunity, not agency. Realizing a reachable route is
policy-level performance, not by itself a discovered goal. A stable held-out
algotype difference would justify carrying opportunity-adjusted competence into
the next system; it would not establish emergence or autonomous goals.
