# P3-003 — off-the-shelf Fireflies synchrony spike results

**Decision: stop.** The standard model completed every paired trajectory and
preserved the intervention boundary, but it failed all three frozen scientific
criteria.

- Mean baseline phase order before the branch was 0.249; no seed reached the
  required 0.5.
- The mean matched shock gap was 0.076; only one of four seeds reached 0.15.
- No seed closed half its shock gap by the late window.

The failure is not a software failure. It says this default Fireflies
configuration is a weak testbed for the current agenda: its baseline is not
synchronized enough for the frozen perturbation to create a large,
interpretable loss-and-recovery trajectory. Do not tune the model around this
gate. Continue to the preselected field-mediated Slime fallback.

Artifacts: `results/p3-003-fireflies-spike/`.
