# P4-001 — off-the-shelf Heatbugs recovery spike results

**Decision: adopt Heatbugs for one blind heterogeneous-target inference
experiment.** All eight frozen criteria passed.

- Mean settled baseline unhappiness was 4.208.
- Deep freeze created a 12.388-point matched unhappiness gap.
- By ticks 470–500, mean gap closure was 98.1%; every seed exceeded the frozen
  half-closure requirement.
- Paired pre-branch trajectories, population, mean ideal temperature, installed
  source, and the unmodified-generator boundary all passed.

This is bridge-calibration evidence only. The standard generator explicitly
assigns an ideal temperature to every bug. P4-002 must hide those values and
the generator's unhappiness calculation, infer targets from observable motion,
and predict held-out probe responses.

Artifacts: `results/p4-001-heatbugs-spike/`.
