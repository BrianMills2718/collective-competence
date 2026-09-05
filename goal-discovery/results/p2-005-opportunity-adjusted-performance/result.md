# P2-005 opportunity-adjusted performance — discovery results

**STOP — the frozen opportunity-adjusted promotion gate did not pass.**

The discovery contains 2,160 graph-oracle cases and 17,280 scheduled branches.

| Damage | Schedule | Algotype | Reachable | Opportunity | Realization | Any seed | All seeds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| immovable | index | bubble | 30 | 8.3% | 100.0% | 100.0% | 100.0% |
| immovable | index | insertion | 30 | 8.3% | 100.0% | 100.0% | 100.0% |
| immovable | index | selection | 41 | 11.4% | 100.0% | 100.0% | 100.0% |
| immovable | shuffled | bubble | 30 | 8.3% | 100.0% | 100.0% | 100.0% |
| immovable | shuffled | insertion | 30 | 8.3% | 100.0% | 100.0% | 100.0% |
| immovable | shuffled | selection | 41 | 11.4% | 100.0% | 100.0% | 100.0% |
| moveable | index | bubble | 185 | 51.4% | 100.0% | 100.0% | 100.0% |
| moveable | index | insertion | 96 | 26.7% | 100.0% | 100.0% | 100.0% |
| moveable | index | selection | 100 | 27.8% | 96.0% | 96.0% | 96.0% |
| moveable | shuffled | bubble | 185 | 51.4% | 100.0% | 100.0% | 100.0% |
| moveable | shuffled | insertion | 96 | 26.7% | 100.0% | 100.0% | 100.0% |
| moveable | shuffled | selection | 100 | 27.8% | 95.8% | 100.0% | 92.0% |

## Integrity gates

- pass — `bubble_immovable_oracle_matches_invariant`
- pass — `bubble_moveable_oracle_matches_invariant`
- pass — `zero_unreachable_successes`
- pass — `zero_time_limit_exits`
- pass — `at_least_30_reachable_cases_per_cell`

## Promotion comparisons

- moveable: fail; best {'index': None, 'shuffled': None}; worst {'index': 'selection', 'shuffled': 'selection'}; gaps {'index': 0.040000000000000036, 'shuffled': 0.07999999999999996}
- immovable: fail; best {'index': None, 'shuffled': None}; worst {'index': None, 'shuffled': None}; gaps {'index': 0.0, 'shuffled': 0.0}

## Interpretation boundary

The graph labels whether some allowed local-action sequence can reach sorted order. The scheduled runs measure whether the implemented rule realizes that opportunity. Neither quantity alone establishes agency or an autonomous goal.
