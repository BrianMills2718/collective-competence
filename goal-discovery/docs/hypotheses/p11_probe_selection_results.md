---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# P11 — a working selector, but not a useful adaptive benchmark

[Wiki](../../../roadmap/README.md) · [Frozen protocol](p11_probe_selection.md) ·
[Frozen choices](../../results/p11-probe-selection/selection.json) ·
[Real-engine responses](../../results/p11-probe-selection/evaluation.json)

## Decision

**Retain the small inspectable selection instrument; reject this family as a
test of adaptive advantage.** The rejection was analytic, before simulation.
The planned 12/24-case batch was canceled, not run and reported as a negative
efficacy result. Two deterministic fixtures subsequently checked the instrument
against the unchanged NetLogo thermostat. They are not held-out research cases.

## What ran and what was observed

Passive and feedback fixtures shared setpoint/ambient 20, initial temperature 24
and effective return rate 0.2. Their different mechanism decompositions were
withheld from fitting and selection. Twenty-five prefix temperatures recovered
q=20, k=0.2 within 1e-8. The 50:50 feedback decomposition, two explanations,
four-probe menu and numerical support thresholds were supplied.

For both fixtures, the first three probes had identical candidate predictions.
Disable-actuation plus load had predicted RMS disagreement about 1.67019.
The selector chose that probe and froze its forecasts before outcomes.

| Probe | Passive fixture | Feedback fixture |
|---|---|---|
| Wait | Abstain | Abstain |
| Displace temperature+3 | Abstain | Abstain |
| Persistent load+.4 | Abstain | Abstain |
| Disable actuation + load+.4 | Supports passive | Supports feedback |

The chosen candidate's response RMSE was below 4e-14 in both distinguishing
probes; the rival's error was about 1.67019. Support is a numerical model-fit
decision, not a probability, goal discovery, or agency attribution.

Selected policy: 2/2 correct supports. Analytically chosen fixed policy: 2/2.
Uniform-menu random expectation: 0.5 correct supports across two fixtures,
or 25%. These are fixture diagnostics with no sampling/error-bar claim. Each
policy gets one 64-tick probe; evaluator coverage used two prefix runs and
eight outcome runs. Equal run/time cost does not mean equal physical energy
or intervention-operation count.

All recorded source, selection, matched-prefix, tick-count and unsaturation
checks passed. Every outcome reproduced its 25-row prefix exactly and retained
64 post-step observations. All eight raw CSVs and generated experiment XMLs
are versioned beside the two prefix runs, staging receipts and JSON records.

## Why this does not demonstrate adaptive value

Without saturation, passive(k) and feedback(k/2+k/2) obey the same observed
equation. Only disabling the control pathway changes one explanation. There
is no context-dependent choice to learn in this menu: a strong fixed policy
already knows the useful experiment. Beating random cannot establish adaptive
advantage when the fixed policy ties by construction.

This is a new functioning observation -> fitted explanations -> predicted
interventions -> chosen probe -> real response -> qualified conclusion path.
It does not prove that the laboratory can propose unexpected hypotheses,
invent interventions, transfer generally, or choose better experiments than
simple policies. Do not promote the canceled benchmark into a scientific claim.

## Provenance and verification boundaries

- Protocol and analytic stop committed at `41b68aa` before execution.
- Initial adapter `043bfd7` failed on a Windows/WSL UNC URI before observations;
  its original XML/log are preserved in
  [launch-failure evidence](../../results/p11-probe-selection-launch-failure/).
- Adapter `cc75bcc` stages byte-identical model/include/XML files on Windows-local
  temporary storage. Pre/post hashes verify unchanged inputs; actual observations
  are NetLogo output, never Python forecasts masquerading as simulation.
- Prefix-derived choices committed at `38e6e85` before the guarded outcome phase.
  First outcome evidence committed at `8f233a6`; no post-outcome threshold tuning.
- Selection SHA256:
  `5755110fdf87b5b6a434e62c9be08c5edcb8502fcdd54c64582f83bdbf3f3b60`.
- Windows CSV timestamps and WSL/Git timestamps are different clock domains.
  Review observed roughly 82 seconds of offset; do not compare them as an
  independent common-clock chronology proof. Commit ancestry, recorded hashes
  and the runner's committed-selection prerequisite support execution ordering.
- Independent synthetic/mocked model and UI checks passed 55 tests; the focused
  cockpit integration set passed 67 with two unrelated missing-data skips.
  These check implementation boundaries, not scientific efficacy. Independent
  review recalculated support from raw CSVs and verified all staging/source hashes.
- Live browser inspection checked both fixture conclusions, abstention on an
  ordinary load, cutoff resets, native scrubbing and automatic playback through
  a Playing/Paused selector. Original button/keyboard activation could not be
  verified in this browser; the replacement selector was exercised directly.
  No repair of other tabs or the shared browser input bridge is claimed.

To inspect, open **Which probe? · P11** in the laboratory. Change fixture/probe
and choose Playing/Paused or scrub the observations. Dashed curves were forecast before outcomes;
the actual curve and online support use only the chosen cutoff. Final results
are separately labeled retrospective. This is saved evidence, not a new run.

Reproduction requires the recorded scientific revision and a fresh output path;
both CLI phases refuse overwrite and scientific inputs/choices must be committed.
Set `P11_NETLOGO_STAGING` to an existing Windows-local temporary directory when
running Windows NetLogo from WSL. Do not rewrite the preserved first evidence.

## Next decision

Find a research-motivated ambiguity where different observations call for
different informative interventions. Freeze that justification before evaluation
and retain a strong fixed baseline. If a fixed probe suffices, use it. Do not
build a general agent framework or fabricate case diversity to make this selector
look useful. The current plan owns any subsequent experimental authorization.
