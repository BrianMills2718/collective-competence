# X02 decision — adopt NetLogo for the next visual prototype

## Decision

**Adopt NetLogo for Experiment 003's visual prototype.** Keep Python as the
analysis, validation, and evidence layer. Do not migrate completed experiments
and do not build a general NetLogo framework.

The decision concerns rapid visual prototyping, not the scientific superiority
of one simulation engine.

## What was built

One NetLogo 7.0.4 model provides:

- twelve persistent cells with identity, value, position, and freeze state;
- index and shuffled activation;
- the local bubble rule;
- setup, step, continuous run, perturb, freeze, and unfreeze controls;
- separate model and intervention seeds;
- moveable and immovable freezing;
- a standard NetLogo world, labels, colors, monitors, and plot;
- flat trajectory export;
- four embedded BehaviorSpace experiments.

No custom web interface or rendering layer was added.

## Calibration results

- All 18 baseline arms sorted and became quiescent.
- All 6 post-sort block swaps raised boundary length from 0 to 2 and then
  recovered to 0.
- Matched moveable-freeze runs ended with boundary length 1.
- Matched immovable-freeze runs ended with boundary length 2 or 3.
- Rerunning the same model, version, parameters, and seeds produced identical
  BehaviorSpace measurements.
- Python read every output table, reconstructed cell order, verified unique
  identities, and independently recomputed every boundary length.

Nine focused headless gates pass against the portable NetLogo runtime. The raw
calibration tables are generated under `results/x02-netlogo/`.

These are infrastructure calibration observations, not claims about agency,
regulation, or compensation.

## Why the gate passed

The complete visual-to-evidence loop used standard NetLogo facilities:

1. the world displays the cells;
2. standard widgets control the run and interventions;
3. a standard plot shows the representation;
4. BehaviorSpace performs seeded repeated runs;
5. CSV-compatible tables cross into Python;
6. Python independently checks the measurements.

The completed Python experiments were unchanged. Cross-engine byte identity was
not required because NetLogo and Python use different random generators; exact
same-version replay inside NetLogo was required and passed.

## Operating rule

Use NetLogo for the smallest visible executable world. Put only model rules,
interventions, observations, and necessary controls in the model. Export raw
trajectories and use Python for confirmatory analysis, figures, metadata
assembly, and held-out decisions.

Do not add another simulation platform unless a recorded NetLogo limitation
blocks a required experiment. Do not generalize the NetLogo code before two
experiments require the same abstraction.

## Next experiment

Experiment 003 should contain only:

- one controlled variable;
- one declared setpoint;
- one passive relaxation arm;
- one negative-feedback arm;
- state displacement and persistent-load interventions;
- sensor-block and actuator-disable interventions;
- live plots of state, setpoint, error, and control action;
- seeded BehaviorSpace runs exported for Python analysis.

The result sought is whether feedback produces disturbance-opposing action that
separates active regulation from passive convergence. Nothing richer is needed
until that contrast is measured.
