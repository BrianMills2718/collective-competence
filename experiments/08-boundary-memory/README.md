# Experiment 08 — composing “how much” with “which edge”

Experiment 07 showed that a tissue-produced inhibitor can restore total size while leaving historical position ambiguous. This experiment adds a deliberately tiny second information channel: each current tissue boundary carries one local **sealed / unsealed** bit.

A normal edge is sealed. End amputation removes that boundary and exposes an ordinary unsealed interior cell. The endogenous inhibitor still decides **whether more structure is needed**; the boundary bit decides **which edge is eligible to grow**. When the inhibitor returns to its quiet band, exposed edges seal again.

No absolute coordinate, target-site list, or left/right morphogen gradient is supplied.

## Unilateral regeneration

Left- and right-side amputations of 1, 4, 8, 12, or 18 cells were each run for **2000 fixed seeds**. Across all **20,000 trials**, the combined controller restores both size 24 and the exact pre-damage interval, using exactly one birth per removed cell.

The resealed boundary supports repeated damage as well: right-8, left-6, right-12, and left-4 amputations applied sequentially each return exactly to the same pre-damage tissue before the next challenge.

A translation control rules out a hidden pull toward the repository reference coordinates: tissues at intervals **40–63** and **120–143** each repair left-8 and right-8 amputations exactly in **1000/1000** trials. The controller uses size and boundary state, not absolute arena position.

## Orthogonal ablations

The two information channels can be removed separately.

**Remove boundary memory, keep size sensing.** After an 8-cell right amputation, size returns to 24 in **2000/2000** trials but the exact pre-damage interval returns in only **5/2000**. This reproduces Experiment 07's amount-without-historical-location behavior.

**Keep boundary memory, clamp the inhibitor at its pre-damage quiet value.** After the same amputation, no structural operation occurs; the tissue remains at size **16**. The wound marker says where growth would belong but supplies no evidence that growth is needed.

**Keep boundary memory, eliminate inhibitor secretion.** The exposed right edge remains the only eligible growth edge, so growth remains on the wounded side, but the stop is lost. After the fixed 50-operation window the tissue has grown from 16 to **66 cells**.

So the channels solve different problems in this controller: boundary state identifies an exposed edge; endogenous inhibitor supplies the amount/stop condition.

## Bilateral damage: what the data actually show

If both ends are amputated, both boundaries are unsealed. The inhibitor reports only the **total** missing amount, so each replacement event chooses randomly between the two wounded sides. Size still recovers in **5000/5000** trials for every declared bilateral challenge, while exact return to the historical interval occurs only when the random birth allocation happens to match the numbers removed from each side.

| cells removed left/right | exact pre-damage interval | binomial expectation |
|---|---:|---:|
| 2 / 6 | 571 / 5000 | 0.1094 |
| 4 / 4 | 1331 / 5000 | 0.2734 |
| 4 / 8 | 619 / 5000 | 0.1208 |
| 8 / 8 | 981 / 5000 | 0.1964 |

The observed frequencies are consistent with the authored random-edge rule.

A previous interpretation called this a failure to recover “anatomy” because the controller lacks the left/right allocation split. **That was too strong for this specimen.** The tissue is homogeneous and contiguous; every 24-cell interval is a translation of every other 24-cell interval. Once size 24 is restored, all bilateral outcomes are therefore equivalent under translation. What is sometimes not restored is the **historical arena position**, not an intrinsic morphology represented in this model.

This distinction matters. If position relative to an external landmark or remembered pre-damage frame is part of the declared goal, then the information deficit is real: total deficit plus two wound bits does not specify how many births belong on each side. If translations are admissible, however, the present bilateral trials already restore the modeled morphology. The data themselves do not choose between those goal criteria.

## Scope and interpretation

This is an engineered composition result, not a claim that real tissues use a literal boundary bit. The quiet thresholds still encode target size, tissue is one-dimensional, contiguous, and internally homogeneous, and boundary sealing is an authored local state transition driven by the inhibitor.

The useful positive result remains: two small, separately ablatable information channels compose cleanly for unilateral restoration and repeated damage. The bilateral runs add a different lesson: **do not manufacture an allocation problem by privileging one translation of an otherwise translation-invariant morphology.** This is the same many-state caution already exposed by Experiment 05 in another form.

Before adding a bilateral-allocation mechanism, the next specimen should make allocation matter intrinsically—for example by adding non-translation-equivalent internal compartments, proportions, polarity, or a declared external landmark. Only then is failure to divide repair correctly a genuine morphology/function failure rather than failure to recover a privileged historical microstate.

## Reproduce

```bash
python3 experiments/08-boundary-memory/run.py
python3 -m pytest -q experiments/08-boundary-memory/test_model.py
```

Evidence: [`results/characterization.json`](results/characterization.json).
