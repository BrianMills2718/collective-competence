# Infrastructure spike X02 — NetLogo visual calibration

## Decision to make

Can one off-the-shelf NetLogo environment provide the model execution,
interactive visualization, perturbation controls, repeated runs, and trajectory
export needed for rapid visual experiments without weakening the Python
laboratory's evidence boundaries?

This is a time-boxed calibration, not a migration of Experiment 001 and not a
comparison of simulation platforms. NetLogo is the only tool under evaluation.

## Governing rule

Borrow the environment instead of rebuilding it. Use NetLogo's standard world,
agents, controls, plots, monitors, deterministic seeding, and BehaviorSpace.
Write only the bubble rule, intervention semantics, measurements, and export
needed to answer the decision question.

The completed Python implementation remains the scientific reference. Do not
rewrite it, add a general simulation framework, or build a custom web viewer as
part of this spike.

## Smallest useful prototype

Build one model only:

- a 12-position one-dimensional line;
- 12 identifiable cells with value, position, and freeze state;
- bubble behavior only;
- an explicit seed and repeatable setup;
- one seeded block-swap perturbation;
- moveable-frozen and immovable-frozen behavior;
- the existing `boundary_length` observable;
- raw trajectory export for later Python analysis.

Do not implement insertion, selection, the random-swap null, Experiment 002,
confirmation runs, or a reusable NetLogo extension.

## Off-the-shelf interface

Use NetLogo's built-in Interface elements rather than a custom visualization
layer:

- `setup`, `step`, and forever `go` buttons;
- a seed input;
- controls for perturbation tick, freeze position, and freeze mode;
- a `perturb` button for an immediate manual intervention;
- a tick monitor and a `boundary_length` monitor;
- a `boundary_length` plot with the intervention tick marked or clearly
  reported;
- the NetLogo world as the live cell display.

In the world, position communicates location, color communicates value, and a
small built-in visual distinction communicates freeze mode. Prefer standard
agent shapes, labels, colors, and plots. Do not write a custom drawing system.

## Evidence export

Export one tidy trajectory table whose rows are observations rather than
screenshots. It must be sufficient to reconstruct each recorded state and must
include at least:

- run identifier;
- NetLogo version;
- model version or commit when available;
- seed;
- tick;
- cell identity;
- position;
- value;
- freeze mode;
- `boundary_length`;
- intervention type and intervention tick.

The visual interface is for understanding and manipulation. The exported
trajectory remains the evidence consumed by analysis.

## Rapid calibration

Use BehaviorSpace for one deliberately small batch:

- three unperturbed seeded runs;
- three seeded block-swap branches;
- one moveable-freeze run;
- one immovable-freeze run.

Predeclare the expected qualitative checks before inspecting the batch:

1. undamaged bubble runs reach the sorted state;
2. the block swap initially raises disorder;
3. undamaged post-perturbation runs recover;
4. moveable and immovable freezing can produce different outcomes;
5. rerunning the same NetLogo version, model, parameters, and seed reproduces
   the same NetLogo trajectory.

NetLogo and Python use different schedulers and random-number generators, so
cross-engine byte identity is not an adoption requirement. Compare declared
mechanics, measurements, and qualitative outcomes against the validated Python
reference. Within NetLogo, exact same-version replay is required.

## Python handoff gate

Add the smallest read-only Python check needed to load the exported table and:

1. validate the required columns and unique cell identity per tick;
2. reconstruct the ordered cell values for each tick;
3. recompute `boundary_length` independently;
4. reproduce one trajectory plot or summary from the exported evidence;
5. verify that intervention metadata survives the handoff.

Do not create a NetLogo/Python runtime bridge unless plain file export proves
insufficient. A stable CSV handoff is preferable for the first version.

## Execution order

Work in this order and stop when a critical gate fails:

1. Install or run the standard NetLogo distribution and record its version.
2. Build the 12-cell baseline using the standard world and interface controls.
3. Prove exact replay for one seed within NetLogo.
4. Add the block-swap intervention and both freeze semantics.
5. Export a tidy trajectory and load it in Python.
6. Run the eight-case BehaviorSpace calibration.
7. Compare the predeclared outcomes with the Python reference.
8. Record an adopt or stop decision before beginning Experiment 003.

## Adoption gate

Adopt NetLogo as the first visual prototyping environment only if all of the
following are demonstrated in the time box:

- the model is visibly understandable with NetLogo's built-in world and UI;
- setup, stepping, continuous running, reset, perturbation, and freezing work
  without custom visualization infrastructure;
- same-version seeded replay is exact;
- the two freeze modes have faithful, explicit semantics;
- BehaviorSpace produces the tiny repeated batch without manual repetition;
- raw trajectories export in a stable form that Python can validate and read;
- the calibration agrees with the reference model on the predeclared mechanics
  and qualitative outcomes;
- model-specific interface code remains smaller than the scientific model and
  intervention logic;
- no change to the validated Python experiments is required.

If the gate passes, use NetLogo for the next visual prototype: Experiment 003's
active-feedback versus passive-relaxation comparison. Keep Python as the
analysis, validation, and evidence layer.

## Stop conditions

Stop and retain the current Python approach if any of these becomes true:

- deterministic same-version replay cannot be demonstrated;
- trajectory export loses identity, ordering, intervention, or freeze state;
- Python cannot independently reproduce the exported measurement;
- activation or freezing requires opaque workarounds;
- the live display requires a custom rendering layer;
- automation requires a fragile runtime bridge rather than standard export;
- the time box expires before the end-to-end visual-to-Python loop works.

Do not respond to a failure by evaluating another platform in this spike. Write
the measured limitation first; a later plan may decide whether another tool is
warranted.

## Time box and deliverables

Stop after one focused implementation session or as soon as a critical
incompatibility is established. Produce only:

- one 12-cell NetLogo bubble model using its built-in interface;
- one exported sample trajectory;
- one tiny BehaviorSpace result set;
- one focused Python import-and-validation check;
- one short decision note: adopt NetLogo for the next prototype, or stop with a
  measured reason.

Success means reaching a platform decision quickly and learning whether the
full visual-experiment-to-Python-evidence loop works. It does not mean porting
the existing programme or building a general laboratory.
