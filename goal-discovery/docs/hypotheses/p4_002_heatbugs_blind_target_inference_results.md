# P4-002 — blind heterogeneous Heatbugs target inference results

**Decision: promote the blind per-agent target representation.** All nine
frozen criteria passed.

- The inference boundary used only persistent identity, declared probe
  temperature, and observed movement direction.
- Four discovery probes recovered 200 hidden individual targets with median
  absolute error 2.0° and mean error 2.13°.
- On the deliberately ambiguous held-out 15°, 25°, and 35° probes, inferred
  targets predicted movement direction at 71.5% accuracy versus 55.5% for the
  identity-free midpoint null, a 16-point advantage.
- Every response was interpretable; all probe/seed/identity pairs, paired
  hidden truths, initial positions, and populations passed integrity checks.

Truth values were joined only after target estimates were fixed. The completed
generator tables were not rerun when the analysis parser was corrected; the
metadata records recovery from those intact raw tables.

This validates blind recovery of explicitly authored heterogeneous micro
targets in a moving off-the-shelf system. It does not establish an emergent
collective goal. Stop the Heatbugs calibration line here rather than optimizing
its already-passing probe accuracy.

Artifacts: `results/p4-002-heatbugs-blind-target-inference-001/`.
