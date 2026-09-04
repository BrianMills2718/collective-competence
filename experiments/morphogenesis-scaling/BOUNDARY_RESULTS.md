# Results: boundary-comparison test for the morphogenesis midpoint case

Tests whether the ingress-category classification of one case
(morphogenesis midpoint task, previously classified as "informational
ingress") is robust to redrawing the agent/system boundary, per
levin-wiki's platonic-space-and-ingression.md open question. Baseline
parameters: N=8, λ=4.0, SNR_Z=30.0, t_eq=80.0 (=5τ), matching the
existing scaling-law sweep's own baseline. Regression check (Boundary C
must collapse exactly to Boundary A at SNR_O=0) passes.

## Boundary A (baseline, unchanged)

O = empty, Z = sensed bilateral field values. Classified: informational
ingress, I(Y;Z|O) > 0. Already established in the main scaling-law work;
not recomputed here.

## Boundary B: relabel the sensing channel as "inside the agent"

**Classification unchanged (informational ingress) — a genuine
prediction that held, not a definitional dodge.** Z still refers to the
same external field concentration regardless of which side of the
boundary the transduction machinery sits on; the joint distribution of
(Y, Z, O) doesn't change, only which resource bucket (`B_A` vs. `B_I`)
pays for the transduction. This is a logical argument, not a new
simulation — checked here only for the one way it could have gone
wrong (a hidden change to what Z actually refers to under the
relabeling); none found. This is the "invariant" half of the boundary
question: expanding the boundary to include mere sensing/transduction
apparatus doesn't change what information exists, so it can't change
the informational-ingress verdict.

## Boundary C: agent already has crude baseline sensing "for free"

**Classification is not binary-invariant here — it's a smooth function
of how much baseline access is already inside the boundary, with no
sharp jump or pathological collapse.**

| SNR_O (baseline, already "in" the agent) | accuracy(O alone) | accuracy(O+Z) | marginal gain from Z |
|---|---|---|---|
| 0 (= Boundary A) | 0.500 | 0.969 | 0.469 |
| 3 | 0.574 | 0.970 | 0.396 |
| 10 | 0.734 | 0.976 | 0.242 |
| 20 | 0.894 | 0.988 | 0.094 |
| 27 | 0.954 | 0.994 | 0.040 |
| 29 | 0.965 | 0.995 | 0.031 |
| 30 (= SNR_Z, agent's baseline matches Z's own precision) | 0.969 | 0.996 | 0.027 |

At SNR_O=0 this is unambiguous informational ingress (Z takes the agent
from chance to 97% accuracy). As SNR_O rises toward SNR_Z, the marginal
contribution of Z shrinks smoothly and continuously toward a small
residual — by SNR_O=30 (agent's own baseline already matches the
"external" signal's own precision), Z is contributing a 2.7-point
accuracy nudge, more naturally described as noise-averaging than
"bringing in new information." No sharp threshold, no discontinuity —
the category isn't a fact that flips under this boundary redraw, it's a
matter of degree that depends continuously on how much access is
already counted as inside the boundary.

## What this actually establishes about the boundary-arbitrariness worry

Two different kinds of boundary expansion behave differently, and that
difference is itself the finding:

- Expanding the boundary to include **sensing/transduction apparatus**
  (Boundary B) leaves the classification untouched, because it doesn't
  touch what information exists in the world — only who's charged for
  producing it.
- Expanding the boundary to include **baseline access to the same
  information source** (Boundary C) does change the picture, smoothly
  and continuously, with no pathological jump — exactly what a sound
  information-theoretic account should do, not evidence the framework is
  gerrymanderable. The classification wasn't chosen to fit a boundary;
  the boundary choice changes a well-behaved, monotonic quantity.

This is one case, computed once, not independently reproduced. It
doesn't establish that every ingress classification on the page is
boundary-robust in this same well-behaved way — only that this specific,
concrete test of the specific worry raised didn't turn up evidence of
arbitrariness or collapse for this case.
