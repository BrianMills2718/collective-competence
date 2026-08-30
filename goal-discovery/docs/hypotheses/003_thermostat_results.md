# Experiment 003 — confirmation results

## Decision

**PASS: R1–R5 all passed on the 34 pre-registered held-out cases.**

This supports one narrow conclusion: in this scalar calibration, the declared
trajectory measurements distinguish bounded negative feedback from matched
passive relaxation. It does not establish autonomous goal discovery, agency,
adaptation, or compensation. The controller's target was supplied explicitly.

## Results

| Rule | Frozen requirement | Held-out result | Decision |
|---|---|---|---|
| R1 | Feedback recovers faster after every displacement | feedback 8–10 ticks; passive 55–68 ticks | pass |
| R2 | Feedback late load error <= 25% of passive | 16.69% for all four nonzero loads | pass |
| R3 | Blocking sensing removes the advantage | blocked late error was 100% of passive; displacement recovery was no faster | pass |
| R4 | Disabling actuation removes the advantage | all disabled temperature trajectories equaled their passive pairs within `1e-9`; applied control was zero | pass |
| R5 | Applied control opposes sensed error on >= 95% of active ticks | 796 / 796 active ticks, 100% | pass |

The detailed paired measurements were:

| Displacement | Passive recovery | Feedback recovery |
|---:|---:|---:|
| -8 | 68 | 10 |
| -4 | 55 | 8 |
| +4 | 55 | 8 |
| +8 | 68 | 10 |

| Persistent load | Passive late error | Feedback late error | Feedback/passive |
|---:|---:|---:|---:|
| -0.4 | 7.9891 | 1.3333 | 0.1669 |
| -0.2 | 3.9946 | 0.6667 | 0.1669 |
| +0.2 | 3.9946 | 0.6667 | 0.1669 |
| +0.4 | 7.9891 | 1.3333 | 0.1669 |

Recovery is measured from the intervention at tick 20 to the first tick inside
the `0.25` tolerance followed by the full 10-tick dwell. Late error is the mean
absolute error over ticks 140–159.

## Execution record

- Runtime: NetLogo 7.0.4 portable Linux distribution, run headlessly in WSL.
- Model: `src/experiments/thermostat/thermostat.nlogox`.
- Included logic: `src/experiments/thermostat/thermostat.nls`.
- Model SHA-256: `d45c70525ad7acf813e44c0c0aef6bdcdfbf83019a2baf6cc47b424d3d3627c0`.
- Logic SHA-256: `dbddaf727a8174ef763789d502ec8db9df054efb09b6a155379891031c180dc9`.
- Raw BehaviorSpace tables: `results/003-thermostat/` (ignored generated evidence).
- Independent gate: `tests/test_thermostat.py`; 9 tests passed.

The first attempted confirmation was rejected before interpretation because an
implementation check found that disturbances were being installed during
setup instead of at tick 20. The event timing was repaired without changing
the frozen cases, parameters, thresholds, or decisions. A new timing regression
gate verifies the complete undisturbed ticks 0–20 prefix. Only the subsequent
batch reported above is accepted evidence.

## What this changes

Experiment 003 calibrates the **regulation** rung of the programme's evidence
ladder. The next experiment should not add more thermostat polish. It should
move to the pre-declared compensatory-controller contrast: damage one route and
test whether a distinct remaining route restores the same macro condition.
