---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen-before-execution
---
# P11 — reject a redundant selection benchmark before running it

[Wiki](../../../roadmap/README.md) · [Current plan](../plans/current_research_plan.md)

## Decision from analytic preflight

The approved question is whether automated experiment choice earns its cost
over random and a strong fixed policy. The first proposed family cannot test
adaptive advantage: one intervention is mathematically best throughout it.
Instead of executing the proposed12/24-case discovery/held-out batch, verify
the decision machinery with two real-engine fixtures and expose the limitation.
This change occurs before any P11 simulator run or protocol freeze.

This checkpoint implements inspectable model-disagreement selection and checks
its connection to an existing simulator. It does NOT evaluate adaptive efficacy,
discover a goal, establish agency, or reject experiment selection in general.
The supplied family, menu and predicted contrast remain visible.

## Why the proposed comparison is redundant

Reuse the existing NetLogo thermostat, unchanged. Passive relaxation has rate k;
feedback has passive rate k/2 plus control gain k/2, with ambient=setpoint=q.
When unsaturated, both obey T_next=T+k(q-T)+load. Wait, displacement and ordinary
load therefore have identical predictions. Disabling actuation changes only
feedback to T_next=T+(k/2)(q-T)+load. The selector must choose disable-plus-load,
the same choice a fixed policy makes. More seeds cannot cure this design.

The original ranges q in[16,24], k in[.1,.3], initial displacement magnitude
in[2,6], subsequent displacement+3 or load+.4, limit2 keep these probes
unsaturated. For the retained fixtures q20,k.2,initial24, all predictions and
observations must remain in that regime. Confirm that bound before interpreting
equation equality; do not silently use a saturated trajectory.

## Minimal real-engine contract check

Run `src/experiments/thermostat/thermostat.nlogox` and adjacent `.nls` unchanged
in installed NetLogo7.0.4, using the existing launcher/path adapter. Python
equations provide candidate forecasts, never substitute for actual observations.
The bowl result supplies prior passive-counterexample reasoning, not another
new simulator in this checkpoint.

Two deterministic fixtures share q=ambient=setpoint20, initial temperature24,
max-control2 and max-ticks88. Passive: relaxation-rate.2, controller-gain0.
Feedback: relaxation-rate.1, controller-gain.1. Fit candidates only from
tick0..24 `{tick,temperature}` observations. Reject extra fields, nonfinite,
rank-deficient or invalid-rate fits. Ordinary least squares fits deltaT=b-kT,
then q=b/k. Parameters and mechanism labels are evaluator-only.

Supplied explanations: passive(k) and feedback(k/2,k/2), centered on fitted q,
control limit2. The 50:50 split is assumed, not discovered. No case identifier,
truth label, hidden parameter, or post-prefix observation enters selection.

At tick24, four matched probes, fixed tie order:

1. `wait`: unchanged.
2. `displace`: existing `displace-state`, magnitude+3.
3. `load`: existing `apply-load`, magnitude+.4, persistent.
4. `disable_load`: existing `disable-actuator` and `apply-load`+.4.

Forecast64 post-step values, ticks25..88. Maximize RMS disagreement between
the candidates; exact ties follow menu order. Commit the fitted candidates,
forecasts and selected actions before executing probe outcomes. Selection
gets no evaluator outcomes. Each policy observes one64-tick probe; evaluator
coverage is eight probe runs plus two prefix runs. This is a run/time budget,
not equal physical energy or equal number of intervention operations.

Support a unique candidate only when best post-step RMSE<=.05 and rival>=.15;
otherwise abstain. Evaluate correctness only after support is decided. These
are supplied numerical tolerances, not posterior probabilities. Retain errors,
all cases, and abstentions. Random comparison is exact uniform-menu expected
correct support; fixed reference always uses disable_load, selected analytically
before outcomes. These are fixture diagnostics, NOT held-out efficacy estimates.

## Integrity, provenance and stopping

Before execution commit this protocol and scientific implementation. Run
prefix-only phase, then commit selection artifact before any outcome phase.
Record Git revision, UTC, model/source/protocol/artifact hashes and backend.
Writes must refuse overwrite. All forecasts are retained, not only winners.
Matched outcome runs must reproduce all25 prefix observations exactly; verify
full64 post-step rows and unchanged model bytes. Save actual simulator output
and parsed traces. Failed checks stay visible; no dropping or imputation.

Fixture checks: inferred q,k within1e-8 of configured values; the first three
probe predictions equal within1e-8; selected/fixed actions equal; selected probe
supports the correct supplied mechanism in both fixtures; no other probe
uniquely distinguishes it; all integrity checks and unsaturation bounds pass.
Failure diagnoses the adapter/predictor/contract, not a scientific no-go.
Passing establishes a small instrument check only. There is no adaptive-value
promotion gate because the design cannot measure adaptive advantage.

Reuse Panel for an inspectable decision view: observed prefix, supplied
candidates, predicted probe differences, automatic choice, actual response,
support/abstention and why the fixed policy ties. Playback conclusions must use
only observations through the cutoff; full-batch results are separately labeled.
Missing artifacts display unavailable, never fabricated examples. Finish after
this bounded evidence and independent audit; no large batch or new framework.
Record the next design need: genuinely different live ambiguities requiring
different useful probes, justified by the research question rather than a
manufactured selector win. Compare against a strong fixed policy there too.
