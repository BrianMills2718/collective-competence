# Experiment 003: passive relaxation versus feedback regulation

This is the first new experiment built directly in the off-the-shelf NetLogo
laboratory. It contrasts a scalar system that passively relaxes toward ambient
temperature with the same system plus bounded proportional negative feedback.

Open `thermostat.nlogox` in NetLogo 7.0.4. Its adjacent `thermostat.nls` file
contains the model logic.

## What is visible

The interface uses only standard NetLogo components:

- a passive/feedback arm chooser;
- visible physical and controller parameters;
- Setup, Step, and Go controls;
- state-displacement and persistent-load interventions;
- sensor block and actuator disable/restore controls;
- a vertical temperature display;
- state/target and dynamics plots;
- monitors for temperature, error, control, load, and the last intervention;
- one-click flat CSV trajectory export.

The orange level is actual temperature, the green line is the setpoint, and the
blue line is ambient temperature.

## Model

Every deterministic tick applies:

```text
passive_term = alpha * (ambient_temperature - temperature)
error = sensed_temperature - setpoint
commanded_control = clip(-gain * error, -control_limit, control_limit)
temperature_next = temperature
                 + passive_term
                 + applied_control
                 + external_load
```

The passive arm commands zero. Disabling the actuator preserves the command in
the record but makes applied control zero. Blocking the sensor pins its report
to the setpoint, so the controller cannot see later state error. A persistent
load remains active on every tick until removed.

## Frozen calibration

The embedded BehaviorSpace design fixes:

- initial, ambient, and target temperature: `20`
- ambient relaxation rate: `0.05`
- feedback gain: `0.25`
- control limit: `2`
- horizon: `160` ticks
- intervention: tick `20`
- held-out displacements: `[-8, -4, 4, 8]`
- held-out persistent loads: `[-0.4, -0.2, 0.2, 0.4]`

Ten embedded BehaviorSpace experiments define exactly 34 cases:

- two undisturbed controls, passive and intact feedback;
- displacement and load families for passive and intact feedback;
- displacement and load families with the feedback sensor blocked;
- displacement and load families with the feedback actuator disabled.

The frozen confirmation suite has been executed and passed all five declared
regulation gates. The full decision table is in
`docs/hypotheses/003_thermostat_results.md`.

Experiment 003B reuses the frozen dynamics with new intervention magnitudes but
hides the target and controller fields from analysis. Its external BehaviorSpace
setup is `003b-behaviorspace.xml`; `run_003b.sh` generates the 28 runs and calls
`goal_inference.py`. The preregistration and result are in
`docs/hypotheses/003b_blind_target_inference.md` and
`docs/hypotheses/003b_blind_target_inference_results.md`.

## Recorded evidence

Each trajectory row contains:

```text
tick, event, arm, temperature, setpoint, ambient_temperature,
sensed_temperature, error, passive_term, commanded_control,
applied_control, external_load, load_active, sensor_blocked,
actuator_disabled, distance_to_setpoint
```

BehaviorSpace supplies the same principal metrics in its standard table output.
Use the interface Export button for the in-model flat CSV log.
