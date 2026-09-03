# Results: N_max scaling for the bilateral-morphogen midpoint task

Baseline unless swept: λ=4.0, SNR=30.0 (relative to source concentration
1.0, i.e. σ=1/30 as an absolute sensor-noise floor), t_eq=5τ where
τ=λ²/D. Accuracy computed exactly (normal-CDF closed form on the true
field separation at the hardest cell), not by Monte Carlo. Both
regression checks against the known exact-arithmetic identity pass.

## λ (decay length) sweep, fixed SNR=30, t_eq=5τ(λ)

| λ | N_max |
|---|---|
| 1 | 6 |
| 2 | 8 |
| 4 | 8 |
| 8 | undefined (< 2) |
| 16 | undefined (< 2) |

**Finding, not an artifact**: N_max does *not* increase monotonically
with λ, and past a threshold it collapses to below the smallest testable
tissue size (2 cells). At λ=8, the hardest-cell separation is only 0.015
(accuracy 0.63); at λ=16 it's 0.004 (accuracy 0.53, barely better than
chance) — even at N=2. This is the opposite of what the idealized
exact-arithmetic result (which only checks the *sign* of the separation,
never its magnitude) would suggest. Mechanism: at fixed absolute sensor
noise, a longer decay length spreads both fields out more evenly across
a small reflecting domain, shrinking their absolute difference
everywhere, including at the midpoint — the sign identity stays exact,
but the signal becomes unresolvably small against a fixed noise floor.

## SNR sweep, fixed λ=4, t_eq=80 (=5τ)

| SNR | N_max |
|---|---|
| 3 | undefined (< 2) |
| 10 | undefined (< 2) |
| 30 | 8 |
| 100 | 18 |
| 300 | 28 |

Monotonic and roughly consistent with N_max growing with SNR — expected,
since higher SNR directly shrinks the noise floor the field separation
must clear.

## Equilibration time sweep, fixed λ=4, SNR=30 (t_eq expressed as multiples of τ=16)

| t_eq/τ | N_max |
|---|---|
| 0.1 | 6 |
| 0.3 | 10 |
| 1.0 | 10 |
| 3.0 | 8 |
| 10.0 | 8 |

**Finding, not an artifact**: this is non-monotonic, with an interior
maximum around t_eq/τ ≈ 0.3–1.0. Too little equilibration time means the
fields haven't built up much of a spatial gradient yet (weak signal
everywhere); too much time lets both fields approach the finite,
reflecting-domain steady state, which — on a small domain — is flatter
and less differentiated than the transient profile at intermediate
times. "Let it settle longer" is not simply better for this task.

## Honest limitations

- Only one accuracy threshold (95%, at the single hardest cell) was
  tested; the CSV/script can be rerun at other thresholds but this pass
  didn't.
- The λ-sweep's collapse to "undefined" past λ=8 means that curve has
  only 3 usable points on the N_max-vs-λ relationship, not a clean
  scaling law across the full tested range.
- Gaussian additive noise only (no quantization), by design (see
  `INTENT.md`/the adopted design brief).
- Not independently reproduced — one script, one run, checked against
  two regression tests, not against a second independent implementation.
- The reflecting-boundary finite-domain steady state differs materially
  from the idealized semi-infinite exponential profile once λ approaches
  or exceeds the domain size — this is exactly the regime where the
  λ-sweep's "undefined" results appear, and is a real physical effect of
  the finite domain, not a modeling shortcut.
