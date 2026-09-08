# Experiment 02 — passive relaxation vs negative-feedback regulation

This is the first qualitatively different control specimen placed on the shared
lattice after sorting. It is a **calibration/port**, not a new discovery claim:
the repository's earlier scalar thermostat already established this contrast in
NetLogo. The question here is whether the current shared substrate can express
that phenomenon cleanly without adding apparatus.

## System

One integer-valued temperature occupies a one-site, non-conserving centred
lattice. The one-site form is deliberate: this experiment distinguishes passive
convergence from feedback regulation; it does not claim collective competence.

Both arms experience passive relaxation toward ambient temperature 100. The
feedback arm additionally senses error from an authored setpoint of 100 and
applies proportional corrective control. The passive arm has no controller.

The goal criterion used for measurement is external: temperature within 3 units
of 100. For this calibration the controller's authored setpoint is known; a later
Goal Discovery analysis should withhold it from the analyst.

## Interventions

Two intervention families expose the mechanism:

- **State displacement:** add -40, -20, +20, or +40 to a settled state and measure
  first return to the tolerance band.
- **Persistent load:** add -4, -2, +2, or +4 every step and measure mean absolute
  setpoint error over the final 20 steps of a 100-step run.

Two feedback ablations are controls: block sensing by pinning the sensed value to
the setpoint, or disable actuation. Either should remove the feedback advantage.
All arms start from the same substrate snapshot.

## Result

| displacement | passive recovery | feedback recovery |
|---:|---:|---:|
| -40 | 11 | **2** |
| -20 | 8 | **2** |
| +20 | 8 | **2** |
| +40 | 11 | **2** |

Feedback therefore restores the criterion faster for every tested displacement.

| persistent load | passive late error | feedback late error |
|---:|---:|---:|
| -4 | 16.0 | **6.0** |
| -2 | 8.0 | **3.5** |
| +2 | 8.0 | **3.5** |
| +4 | 16.0 | **6.0** |

For every load, **sensor blocked = passive** and **actuator disabled = passive**
exactly. The advantage therefore depends on the feedback path rather than merely
on a different transition rate hidden elsewhere in the specimen.

This reproduces the qualitative result of the earlier thermostat calibration on
the shared lattice: ordinary convergence to a desirable state and active
regulation can look similar until displacement/load challenges reveal the
feedback mechanism.

It does **not** establish goal discovery, adaptation, agency, or collective
competence. The setpoint and controller were authored, and this result is a
white-box calibration of a known distinction.

## Reproduce

```bash
python3 experiments/02-regulation/run.py
```

The committed result is [`results/characterization.json`](results/characterization.json).
Implementation: [`goal-discovery/src/lattice/specimens/regulation.py`](../../goal-discovery/src/lattice/specimens/regulation.py).
