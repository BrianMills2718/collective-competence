# P4-002 — blind heterogeneous Heatbugs target inference

**Frozen after P4-001 and before generating P4-002 data.**

## Claim under test

A supplied candidate family plus observable one-step movements under controlled
thermal gradients can recover useful per-agent target-temperature estimates
without exposing the standard generator's `ideal-temp`, `unhappiness`, or
decision calculation to inference.

## Generator and counterfactual probes

Use the installed, unmodified NetLogo 7.0.4 Heatbugs model with 25 bugs, ideal
temperature bounds 10–40, heat-output bounds 5–25, zero evaporation, zero
diffusion, and zero random movement. Use paired seeds 5–12.

After standard setup, place bug `who` at `(50, (4 × who) mod 100)` so occupied
neighborhoods do not overlap. Set a left-to-right temperature gradient centered
on one of seven probe temperatures: 10, 15, 20, 25, 30, 35, or 40. Run exactly
one standard model step.

The observable export contains only persistent identity and positions before
and after the step. A separate truth field containing `ideal-temp` is sealed
from inference and opened only for frozen scoring.

## Frozen inference

Use probes 10, 20, 30, and 40 for discovery. For each bug:

- movement toward hotter patches implies target temperature above the probe;
- movement toward cooler patches implies target below the probe;
- no horizontal movement at a probe implies equality;
- otherwise estimate the target as the midpoint of the tightest discovered
  lower and upper bounds, using the declared 10–40 candidate range.

Do not fit coefficients or inspect truth values while constructing estimates.

## Held-out test and null

Predict movement direction at probes 15, 25, and 35 from the inferred target.
Compare against observed direction. The frozen identity-free null assigns every
bug the midpoint target 25 and makes the same directional prediction.

## Frozen promotion gate

Promote blind heterogeneous-target inference only if:

- all seven probes contain ticks 0 and 1 for all eight paired seeds and all 25
  persistent bug identities;
- paired hidden targets and initial positions agree across probes;
- at least 95% of movement responses are horizontally interpretable or exact
  no-move responses;
- inferred target median absolute error is at most 5 degrees when truth is
  unsealed;
- held-out movement-direction accuracy is at least 70% overall and at least 65%
  in seven of eight seeds; and
- held-out accuracy exceeds the midpoint null by at least 15 percentage points.

The deliberately coarse 10-degree discovery grid makes the 15, 25, and 35
degree held-out probes maximally ambiguous within each inferred bracket; 70% is
therefore the frozen resolution-aware gate, not a post-result relaxation.

Passing validates blind recovery of explicitly authored heterogeneous micro
targets in a moving off-the-shelf system. It does not establish an emergent
collective target.
