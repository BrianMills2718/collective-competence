# P3-002 Flocking representation discrimination — results

**STOP Flocking — neither frozen candidate representation passed.**

| Seed | Shock Δ | Late local Δ | Polarization ratio | Interaction advantage | Whole late heading error |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 24.3° | 1.2° | 91.9% | 0.41 | 94.4° |
| 2 | 21.9° | -1.0° | 165.3% | 0.78 | 82.6° |
| 3 | 22.3° | 3.3° | 86.4% | 0.39 | 100.0° |
| 4 | 22.2° | 1.7° | 97.5% | 0.51 | 88.1° |
| 5 | 26.0° | 0.1° | 87.2% | 0.49 | 106.6° |
| 6 | 20.0° | 1.4° | 82.1% | 0.33 | 90.3° |
| 7 | 15.2° | -3.0° | 100.3% | 0.74 | 94.1° |
| 8 | 22.7° | 0.8° | 60.1% | 0.19 | 98.1° |

## Integrity

- pass — `eight_complete_trajectories_per_arm`
- pass — `prebranch_trajectories_identical`
- pass — `quarter_shock_detected_in_six_seeds`
- pass — `whole_rotation_detected_in_six_seeds`
- pass — `population_and_mean_vectors_valid`

## Alignment / polarization

- pass — `late_local_alignment_in_six_seeds`
- fail — `late_polarization_in_six_seeds`
- pass — `interaction_advantage_in_six_seeds`

## Prior heading

- fail — `late_prior_heading_in_six_seeds`
- fail — `half_heading_error_closed_in_six_seeds`

## Interpretation boundary

This discovery distinguishes candidate macro-state representations. A selected manifold still requires new held-out seeds and parameters before any regulation claim; it does not establish agency or an autonomous goal.
