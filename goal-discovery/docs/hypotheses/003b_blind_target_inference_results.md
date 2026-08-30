# Experiment 003B — blind target-inference results

## Decision

**PASS: B1–B6 all passed on the 28 pre-registered new cases.**

With setpoint, ambient, sensor, error, and controller fields removed, the
trajectory-only estimator selected `20.00`. Every leave-one-displacement-out
estimate also selected `20.00`. The true target was unlocked only after those
estimates and the held-out decisions were fixed.

## What was discovered

Both systems revealed the same candidate state:

| System | Blind candidate | Discovery loss |
|---|---:|---:|
| intact feedback | 20.00 | effectively 0 |
| passive relaxation | 20.00 | 0.00794 |

That is expected and important. Return trajectories alone reveal an attractor,
not whether it is actively defended. The held-out loads supplied that missing
contrast:

| Load | Feedback late error | Passive late error | Feedback/passive |
|---:|---:|---:|---:|
| -0.37 | 1.2333 | 7.3899 | 0.1669 |
| -0.13 | 0.4333 | 2.5965 | 0.1669 |
| +0.19 | 0.6333 | 3.7948 | 0.1669 |
| +0.31 | 1.0333 | 6.1916 | 0.1669 |

Sensor-blocked and actuator-disabled runs had exactly `1.0` times passive error
under every load. Thus the inferred state was not merely the centre of passive
relaxation: its stronger preservation depended causally on sensing and acting.

## Frozen decisions

| Rule | Result | Decision |
|---|---|---|
| B1: candidate within 0.25 after unlock | 20.00 versus true 20.00 | pass |
| B2: leave-one-run-out span no more than 0.25 | span 0.00 across six estimates | pass |
| B3: feedback no more than 25% of passive error | 16.69% on every load | pass |
| B4: sensor null at least 90% of passive and fails 25% | 100% on every load | pass |
| B5: actuator null at least 90% of passive and fails 25% | 100% on every load | pass |
| B6: exact blind whitelist | six fields, no hidden mechanism fields | pass |

## Evidence and reproduction

- NetLogo: 7.0.4, run headlessly in WSL.
- Model SHA-256: `9376166947a4b41f3bbb8349b48978df9a55ac18d735a7578c13c52eb09aa590`.
- Logic SHA-256: `dbddaf727a8174ef763789d502ec8db9df054efb09b6a155379891031c180dc9`.
- Setup SHA-256: `4337093462af0608806c067796c1c0fa7885925e22511ef3fefcc92a7af5e503`.
- Analyzer SHA-256: `519ef8083ad015d009cf009e23be03d8c229f08d487409665216ded90629b946`.
- Generated raw and blind evidence: `results/003b-blind-target/` (ignored).
- Blind table: 4,508 observations plus one header, with exactly
  `run_id,tick,system_label,intervention_kind,magnitude,temperature`.

Run with:

```bash
NETLOGO_CONSOLE=/path/to/netlogo-headless.sh \
  bash src/experiments/thermostat/run_003b.sh
```

## Interpretation

This is the first experiment in the repository that actually hides a target and
recovers it. It also demonstrates why inference and attribution are separate:
both active and passive systems expose the same candidate, but only the active
system defends it strongly under new sustained disturbances, and that advantage
vanishes when sensing or actuation is removed.

The result is still constrained. The scalar variable, candidate grid,
intervention labels, and disturbance family were supplied. Experiment 004
should now ask whether a more distributed system preserves an inferred macro
condition through distinct routes after targeted component damage.
