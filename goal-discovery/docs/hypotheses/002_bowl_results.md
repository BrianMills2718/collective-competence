# Experiment 002 results — what the 001 instrument actually measures

Run `results/002-bowl`, 40 seeds (4000–4039), 8 independent damped coordinates.
Predictions from [the pre-registration](002_bowl.md), committed before the
experiment was run (`1ca5c79`).

| | prediction | |
|---|---|---|
| **D1** | approach and persistence | ⚠️ approach ✅ 1.000 · **persistence ❌ 0.000** |
| **D2** | no compensation: freezing strands the system | ✅ **PASS**, 0.000 at every k |
| **D3** | no adaptation across episodes | ✅ **PASS**, identical to the tick |
| **D4** | the C2 signal fires here too | ✅ **PASS** — as predicted, against my own interest |
| **D5** | recovery equals fresh convergence, robustly | ✅ **PASS**, and it diagnoses 001's R7 |

## D4 — the headline, and it narrows Experiment 001

I predicted my own test would fire on the passive control, and it did:

| condition | goal rate | changed a representation? |
|---|---|---|
| none | 1.000 | 0.00 |
| displace 1 coordinate by 6.0 | **1.000** | **1.00** |
| displace 3 coordinates | **1.000** | **1.00** |
| kick 1 coordinate | **1.000** | **1.00** |
| freeze 1 coordinate | **0.000** | **0.00** |
| freeze 2 | **0.000** | **0.00** |
| freeze 3 | **0.000** | **0.00** |

This is the same shape as Experiment 001's C2: damage that is invisible to every
representation destroys goal attainment, damage that is maximally visible costs
nothing. **A ball in a bowl is passive by construction.** So:

> **Experiment 001's headline is narrowed.** "Observable state is not sufficient
> to predict goal attainment" is true, and it is true of a damped oscillator
> too. The C2 signal detects that a chosen representation set omits mechanism
> variables. It does **not** distinguish an active system from a passive one,
> and 001 must not be read as though it does.

Stating this in advance is the only thing that makes it worth anything. Had I
run 002 first and reasoned backwards, the narrowing would be indistinguishable
from an excuse.

## What does separate them: redundancy

The two systems differ, but not in whether mechanism damage matters — in
whether it is survivable.

| | frozen components | goal attainment |
|---|---|---|
| **001**, bubble algotype | 3 of 40 cells, moveable | **0.97** |
| **001**, bubble algotype | 3 of 40 cells, immovable | 0.57 |
| **002**, bowl | 1 of 8 coordinates | **0.00** |
| **002**, bowl | 3 of 8 coordinates | **0.00** |

In the array a frozen cell's neighbours carry it; the collective reaches the
goal with three of its members unable to act. In the bowl no coordinate can act
on another, so one frozen coordinate is stranded and the goal is unreachable
forever. **Redundancy, not invisibility, is the discriminating quantity**, and
it is measurable without any representation-sufficiency argument.

That is the "recovery despite targeted damage" half of compensation on the
brief's ladder, now with a passive control that scores zero on it. The other
half — *more than one route* — remains unmeasured, and the claim stays parked
until it is.

## D5 — this diagnoses 001's R7 failure

Ratio of recovery time to a matched point on the unperturbed run, by
matched-point definition:

| | first crossing | last crossing | spread |
|---|---|---|---|
| **002** bowl (monotone descent) | 0.97 | 0.96 | **0.01** |
| **001** bubble (oscillating descent) | 1.10 | 1.83 | **0.73** |

On a monotone trace the two comparators agree to within 0.01 and both sit at
1.00, exactly as a true attractor should. On 001's oscillating trace they
disagree by 0.73. **R7's instability in Experiment 001 was a property of the
measure meeting an oscillating trace, not a property of the system** — which is
what the confirmation phase suspected and could not show. It is shown here.

## D1 — my persistence rule failed, and the diagnosis is mine again

Approach passed at 1.000, median 202 ticks. **Persistence failed at 0.000**: not
one run stayed inside the goal box for the following 500 ticks.

The bowl is fine. The rule was wrong. A damped oscillator *spirals* into the
target: it enters the tolerance box still carrying velocity, overshoots out the
far side, and comes back with a smaller amplitude. Measured over 20 seeds and
400 ticks after first arrival, excursions reach **2.17× the tolerance** and last
a median of **8 ticks in 400**, decaying throughout. The box is not
forward-invariant, and "reached the goal region once" is not "settled".

A correct persistence rule needs a dwell requirement — inside the box for T
consecutive ticks — or a decaying-envelope test. Choosing one now that I have
seen these numbers would be the after-the-fact threshold the brief prohibits, so
it is left as a declared defect for the next pre-registration.

This is the third time a measurement convention I wrote has been the weak point
rather than the system: v1's relative recovery criterion, R7's matched point,
and now this. The systems in this programme have been better behaved than my
instruments for measuring them.

## D2 and D3

**D2** passes at every k: freezing 1, 2 or 3 of 8 coordinates gives a goal rate
of exactly 0.000. Nothing can carry a frozen coordinate.

**D3** passes to the tick: five repetitions of the same episode take 202, 202,
202, 202, 202 ticks. No improvement, and there is no per-episode memory to
erase. The analysis does not mistake a deterministic attractor for adaptation.

## Verdict on the instrument

002 did its job. It caught an overstatement in 001's headline, diagnosed R7's
instability, and confirmed that the analysis does not read passive convergence
as compensation or adaptation. What it could not do is validate my persistence
criterion, which it falsified instead.

## Reproduce

```bash
uv run python -m src.experiments.bowl.run --suite configs/suites/bowl.yaml
```
