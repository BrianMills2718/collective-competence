# P3-005 Slime interaction discrimination — results

**PROMOTE — recovery depends on chemical sensing under the frozen gate.**

Late active aggregation: **24.104**. Late sensing-disabled aggregation: **1.743**. Matched advantage: **22.362**.

| Seed | Shock loss | Active late | Disabled late | Active advantage | Disabled field |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 21.945 | 22.719 | 1.728 | 20.991 | 1.097 |
| 2 | 30.009 | 27.280 | 1.768 | 25.511 | 1.097 |
| 3 | 28.160 | 21.245 | 1.771 | 19.473 | 1.097 |
| 4 | 25.622 | 25.175 | 1.704 | 23.471 | 1.097 |

## Frozen criteria

- pass — `four_complete_paired_trajectories`
- pass — `prebranch_trajectories_identical`
- pass — `population_preserved`
- pass — `shock_detected_in_three_seeds`
- pass — `active_recovered_in_three_seeds`
- pass — `disabled_dispersed_in_three_seeds`
- pass — `interaction_advantage_in_three_seeds`
- pass — `disabled_field_regenerated_all_seeds`

## Interpretation boundary

A pass identifies interaction-dependent reconstruction of a collective state. It does not establish an internal target representation, an evolved goal, or generality beyond this generator.
