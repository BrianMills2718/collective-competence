# Experiment 002 — passive convergence, as a control on the analysis

**Committed before the experiment was run.** This commit contains no results.

## What 002 is for

Experiment 001 ended with a claim: freezing cells mid-run changes no observable
value, yet costs up to 97 percentage points of goal attainment, so **observable
state is not sufficient to predict goal attainment**.

That claim is only worth something if the same test *fails to fire* on a system
that is passive by construction. 002 is not a new phenomenon to study. It is a
control on the instrument, and it is designed so that it can embarrass the
instrument.

## System

N independent damped harmonic coordinates — a ball in a bowl, one per axis, with
no coupling between them:

```
v_i  <-  (v_i  -  k * x_i) * (1 - damping)
x_i  <-  x_i + v_i
```

Deterministic, no randomness in the dynamics. The goal region is
`max|x_i| <= eps and max|v_i| <= eps`. Every coordinate descends its own bowl
and **no coordinate can act on any other**. That is the single structural
difference from the sorting array, where a cell's neighbours can move it, and it
is the difference the predictions below turn on.

A coordinate can be **frozen**: it stops updating. There is deliberately no
moveable/immovable distinction, because "moveable by a neighbour" presupposes
neighbours that can act on you, and here none can. The absence of that
distinction is itself a reportable structural fact, not an implementation
shortcut.

## Predictions

- **D1 — approach and persistence.** From varied random starts the system
  reaches the goal region in ≥ 95% of seeds, and having reached it stays for the
  remainder of the horizon in 100% of them.
- **D2 — no compensation. The load-bearing prediction.** Freezing k ≥ 1
  coordinates away from the goal drops goal attainment to **0.00**, for every k,
  because nothing can carry a frozen coordinate. Contrast, already measured in
  001: freezing three of forty cells with the bubble algotype leaves goal
  attainment at **0.97**. Predicted contrast at k = 1: bowl 0.00, array 1.00.
- **D3 — no adaptation.** Repeating the same episode with the same disturbance
  produces identical time-to-goal every time. No improvement across episodes,
  and erasing any per-episode memory changes nothing, because there is none.
- **D4 — the C2 test must behave differently here.** This is the control on
  001's headline.
  - **D4a.** State damage (displacing position, or injecting velocity) is
    *visible* to the representation set and costs **zero** goal attainment: the
    ball re-descends. Same as 001's block_swap result.
  - **D4b.** Mechanism damage (freezing coordinates) is *invisible* to the
    representation set at the instant it fires and costs **total** goal
    attainment.
  - So the raw C2 signal — "invisible damage hurts, visible damage does not" —
    **will fire here too**. I am predicting my own test fires on the passive
    control.

  That is not a failure of the test; it is the discovery of what the test
  actually measures, and stating it in advance is the only way the distinction
  is worth anything. The C2 signal shows that a chosen representation set omits
  mechanism variables. It does **not** by itself distinguish an active system
  from a passive one. **What separates 001 from 002 is not whether mechanism
  damage matters, but whether the system survives it** — 0.97 against 0.00.
  Redundancy, not invisibility, is the discriminating quantity.

  If 002 instead shows *tolerance* of frozen coordinates, the bowl is not the
  passive control I think it is and the comparison is void.
- **D5 — recovery equals fresh convergence.** For a true attractor, time from a
  displaced state to the goal equals time from a fresh start at the same
  distance. Predicted ratio 1.00, and unlike 001's R7 this should be robust to
  the matched-point definition, because the trace descends monotonically rather
  than oscillating. **If the two comparators disagree here, that is evidence
  that R7's instability in 001 was a property of the measure and not of the
  system.**

## What a failure means

- **D2 failing** — the bowl tolerates frozen coordinates — voids the 001/002
  contrast and means I have built a system with hidden coupling.
- **D4 failing in the other direction** — the C2 signal *not* firing here —
  would mean C2 discriminates active from passive after all, which would make
  001's claim stronger than I am now willing to state. I am predicting against
  my own interest and will report it either way.
- D1, D3, D5 failing means the implementation is wrong, not that the finding is
  interesting.

## Reproduction

```bash
uv run python -m src.experiments.bowl.run --suite configs/suites/bowl.yaml
```
