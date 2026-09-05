# P3-006 Slime bidirectional target discrimination — results

**STOP — stable bidirectional target regulation was not supported.**

Classification: **interaction-dependent attractor reconstruction**.

Mean candidate center: **41.134** neighbors. Mean late dispersed state: **21.950**. Mean late compressed state: **227.997**.

| Seed | Center ± tolerance | Slope | Baseline late | Dispersed shock → late | Compressed shock → late | Both return |
| ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 5 | 54.98 ± 8.25 | 0.025 | 55.67 | 1.82 → 22.20 | 222.71 → 226.83 | no |
| 6 | 35.50 ± 5.33 | 0.000 | 36.27 | 1.77 → 25.03 | 237.49 → 227.12 | no |
| 7 | 40.08 ± 6.01 | 0.032 | 51.85 | 1.67 → 21.47 | 235.40 → 230.16 | no |
| 8 | 33.98 ± 5.10 | -0.001 | 37.65 | 1.77 → 19.10 | 228.96 → 227.88 | no |

## Eligibility

- fail — `slope_stable_in_three_seeds`
- pass — `half_windows_stable_in_three_seeds`
- pass — `baseline_remains_in_band_in_three_seeds`

## Frozen criteria

- pass — `four_complete_triplets`
- pass — `prebranch_trajectories_identical`
- pass — `population_preserved`
- fail — `candidate_band_eligible`
- pass — `dispersal_valid_in_three_seeds`
- pass — `compression_valid_in_three_seeds`
- fail — `dispersed_returned_in_three_seeds`
- fail — `compressed_returned_in_three_seeds`
- fail — `bidirectional_return_in_three_seeds`

## Interpretation boundary

A no-go leaves P3-005 intact as interaction-dependent collective reconstruction, while stopping target/setpoint language for this representation.
