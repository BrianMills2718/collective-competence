# Experiment 10 — endogenous composition signals

Experiment 09 made the target morphology intrinsically non-translation-equivalent (`A^8 B^16`) but supplied perfect A/B target counts as an oracle control. This experiment replaces that oracle with tissue-generated information while keeping the lineage-extinction challenge intact.

## System

A and B cells each secrete their own distinguishable inhibitory field. For a contiguous compartment of `n` cells, the boundary signal uses the same steady-state exponential sum as Experiment 07:

```text
I(n) = sum(exp(-d / lambda), d=0..n-1)
```

with decay length `lambda = 12`. Each compartment has a growth threshold halfway between the signal expected at target count and target-minus-one: A targets 8 cells; B targets 16.

A wounded A-side boundary grows A while the sensed A signal is below its threshold. The B side behaves analogously. In the lineage-conserving arm, a missing type can only be produced if a parent of that type remains. In the plastic arm, a surviving wounded pole may produce the missing terminal fate.

No total cell count, target-site list, or arena coordinate is supplied during repair. The target thresholds remain authored.

## Partial composition repair

Across the same six declared partial-loss challenges used in Experiment 09—two unilateral and four asymmetric bilateral cases—the endogenous lineage-preserving controller restores `A^8 B^16` in **6/6** cases.

This replaces the composition oracle with a causal tissue-generated measurement: as a compartment regrows, its own inhibitor rises until the growth condition closes.

## Lineage extinction remains a capability boundary

When an entire compartment is removed, its signal is zero but lineage-conserving growth still has no parent capable of producing the absent type. The endogenous lineage arm therefore repairs **0/4** declared lineage-extinction cases. Adding daughter-fate plasticity restores **4/4**.

This reproduces Experiment 09's information-versus-action separation with endogenous information: a low/absent signal can indicate what is missing, but that information does not itself create a missing fate.

## The signal is causal—and fallible

Two controls on the A channel expose opposite information failures after A loss.

**Clamp the A signal at its healthy target value.** After removing 4 of 8 A cells, the controller performs **0** A births and remains at A=4, B=16. After complete A extinction, the plastic controller likewise performs 0 births. A false high signal hides a real deficit.

**Eliminate A secretion.** After removing 4 A cells, the lineage controller never sees the signal recover and grows for the entire fixed 40-operation window, ending at **A=44, B=16**. After complete A extinction, the plastic arm similarly grows to **A=40, B=16** in 40 operations instead of stopping at A=8. A broken signal source looks like a permanent deficit.

So the endogenous signal is not merely correlated with repair; altering it changes whether growth starts and stops. But the controller cannot assume that the channel is truthful: source failure can mimic extreme tissue loss.

## Complete extinction

Removing all 24 cells still yields no repair, even with plasticity, because the model permits only parent-dependent local births. No surviving cell remains to execute the plastic rule.

## Scope

This is an engineered signaling analogue, not a biological claim about compartment-specific inhibitors. It assumes instant steady-state fields, perfectly distinguishable A/B signals, fixed terminal polarity, noiseless sensing, and authored thresholds. The secretion-failure controls are intentionally adversarial and should not be interpreted as evidence that real tissues confuse those conditions.

The durable result is narrower: **tissue-generated composition information can support partial repair, but its reliability depends on the integrity of the cells/source that generate the information; information and generative plasticity remain separately ablatable requirements.**

Do not add a blind Goal Discovery pass here. The next constructive question is whether composition information can be stored redundantly outside the lineage it describes, so loss of that lineage does not simultaneously erase the structure and its own measurement channel.

## Reproduce

```bash
python3 experiments/10-endogenous-composition/run.py
python3 -m pytest -q experiments/10-endogenous-composition/test_model.py
```

Evidence: [`results/characterization.json`](results/characterization.json).
