# P2-005 opportunity-adjusted performance — discovery results

## Decision

**No-go. Stop the sorting line and do not generate size-5 confirmation data.**

All five integrity gates passed across 2,160 graph-oracle cases and 17,280
scheduled branches. The frozen 20-point opportunity-adjusted promotion gate did
not pass.

| Damage | Schedule | Bubble robust | Insertion robust | Selection robust | Range |
| --- | --- | ---: | ---: | ---: | ---: |
| immovable | index | 100% | 100% | 100% | 0 points |
| immovable | shuffled | 100% | 100% | 100% | 0 points |
| moveable | index | 100% | 100% | 96% | 4 points |
| moveable | shuffled | 100% | 100% | 92% | 8 points |

No graph-unreachable branch reached the target and no run stopped at the time
limit. The NetworkX bubble oracle agreed with both exact P2-003/P2-004
invariants on every case.

## What was learned

The algotypes differ more in *opportunity* than in exploiting it. Under
moveable damage, 51.4% of bubble cases were reachable, compared with 26.7% for
insertion and 27.8% for selection. Conditional on reachability, however, bubble
and insertion realized every route under every seed and schedule.

Selection left a small scheduler-dependent residue. Four of 100 reachable
moveable cases failed under index sweeps; shuffled sweeps succeeded at least
once in all 100 but were robust in 92. A NetworkX shortest-path witness exists
for the index failures, confirming that this is a route-realization difference,
not an oracle error. Its magnitude is below the frozen promotion threshold.

## Research consequence

For the present questions, sorting is mechanically complete. More sizes,
features, or dashboards would add confidence without changing the decision.
The durable result is the three-way distinction between unreachable,
reachable-but-unrealized, and robust recovery. Carry that measurement boundary
into a richer generator with motion, local interaction, multiple dynamic macro
states, and no leader.

Artifacts are in `results/p2-005-opportunity-adjusted-performance/`.
