# Experiment 08 — composing “how much” with “which edge”

Experiment 07 showed that a tissue-produced inhibitor can restore total size while leaving anatomical position ambiguous. This experiment adds a deliberately tiny second information channel: each current tissue boundary carries one local **sealed / unsealed** bit.

A normal edge is sealed. End amputation removes that boundary and exposes an ordinary unsealed interior cell. The endogenous inhibitor still decides **whether more structure is needed**; the boundary bit decides **which edge is eligible to grow**. When the inhibitor returns to its quiet band, exposed edges seal again.

No absolute coordinate, target-site list, or left/right morphogen gradient is supplied.

## Unilateral regeneration

Left- and right-side amputations of 1, 4, 8, 12, or 18 cells were each run for **2000 fixed seeds**. Across all **20,000 trials**, the combined controller restores both size 24 and the exact reference interval, using exactly one birth per removed cell.

The resealed boundary supports repeated damage as well: right-8, left-6, right-12, and left-4 amputations applied sequentially each return exactly to the same reference tissue before the next challenge.

A translation control rules out a hidden pull toward the repository reference coordinates: tissues at intervals **40–63** and **120–143** each repair left-8 and right-8 amputations exactly in **1000/1000** trials. The controller uses size and boundary state, not absolute arena position.

## Orthogonal ablations

The two information channels can be removed separately.

**Remove boundary memory, keep size sensing.** After an 8-cell right amputation, size returns to 24 in **2000/2000** trials but exact reference position returns in only **5/2000**. This reproduces Experiment 07's amount-without-location behavior.

**Keep boundary memory, clamp the inhibitor at its pre-damage quiet value.** After the same amputation, no structural operation occurs; the tissue remains at size **16**. The wound marker says where growth would belong but supplies no evidence that growth is needed.

**Keep boundary memory, eliminate inhibitor secretion.** The exposed right edge remains the only eligible growth edge, so location is constrained correctly, but the stop is lost. After the fixed 50-operation window the tissue has grown from 16 to **66 cells**, extending only on the wounded side.

So the channels solve different problems: boundary state says **where**, endogenous inhibitor says **how much**. Neither substitutes for the other in this controller.

## Bilateral damage exposes the next boundary

If both ends are amputated, both boundaries are unsealed. The inhibitor reports only the **total** missing amount, so each replacement event chooses randomly between the two wounded sides. Size still recovers in **5000/5000** trials for every declared bilateral challenge, but exact position depends on accidentally assigning the correct number of births to each side.

| cells removed left/right | exact reference interval | binomial expectation |
|---|---:|---:|
| 2 / 6 | 571 / 5000 | 0.1094 |
| 4 / 4 | 1331 / 5000 | 0.2734 |
| 4 / 8 | 619 / 5000 | 0.1208 |
| 8 / 8 | 981 / 5000 | 0.1964 |

The observed frequencies are consistent with the authored random-edge rule. The scientific point is the information deficit: two wound bits identify **which edges are damaged**, but do not encode how the total missing amount should be divided between them.

## Scope and interpretation

This is an engineered composition result, not a claim that real tissues use a literal boundary bit. The quiet thresholds still encode target size, tissue is one-dimensional and contiguous, and boundary sealing is an authored local state transition driven by the inhibitor.

The useful result is that two small, separately ablatable information channels compose cleanly for unilateral regeneration while retaining a predictable failure on bilateral damage. This is stronger than calling the combined system “more competent”: it identifies which information solves which challenge.

A natural next question is whether any equally small mechanism can resolve the **bilateral allocation** ambiguity without encoding a complete coordinate map—for example, side-specific deficit signals, persistent boundary-specific state, or local growth history.

## Reproduce

```bash
python3 experiments/08-boundary-memory/run.py
python3 -m pytest -q experiments/08-boundary-memory/test_model.py
```

Evidence: [`results/characterization.json`](results/characterization.json).
