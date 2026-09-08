# Experiment 09 — composition information and lineage extinction

Experiment 08's bilateral result was corrected after noticing that a homogeneous size-24 interval has no intrinsic left/right allocation target: different allocations merely translate the same modeled morphology. This experiment makes allocation meaningful without using arena coordinates by giving the tissue an internal pattern.

The target is a contiguous two-compartment tissue, **`A^8 B^16` modulo translation**. A wrong repair split now changes the A/B composition and cannot be repaired conceptually by translating the tissue.

## System

End damage removes cells from the left A compartment, the right B compartment, or both. Wounded boundaries can proliferate locally. In the lineage-conserving arm, a daughter inherits the type of its boundary parent.

The experiment deliberately uses **perfect composition information as an oracle control**: the repair controller is told the target counts A=8 and B=16. That is not proposed as a biological mechanism. It removes uncertainty about *what is missing* so the experiment can isolate a different question: does the surviving action repertoire contain a way to make the missing thing?

Three comparisons are kept separate:

1. **Total-only random edge choice.** Amount can be restored, but the controller has no composition-allocation information.
2. **Composition oracle + lineage conservation.** The controller knows the exact A and B deficits, but daughters must preserve parent type.
3. **Composition oracle + daughter-fate plasticity.** The same information is available, and a surviving boundary lineage may produce the missing terminal type.

## Partial damage: information is enough when both lineages survive

For unilateral partial loss and four partial bilateral cases, both A and B remain represented. With perfect composition information, lineage-conserving repair restores the exact `A^8 B^16` pattern in **6/6 declared cases**.

The total-only random policy provides a matched negative control. In a partial bilateral challenge removing `L` A cells and `R` B cells, with `D=L+R`, exact composition is recovered only if exactly `L` of the `D` random births occur at the A edge. Its exact probability is therefore `C(D,L) / 2^D` while both lineages survive. This combinatorial result is derivable from the authored policy and is not presented as an empirical discovery.

## Lineage extinction: information is not sufficient

The stronger boundary appears when an entire compartment is removed.

| damage | start A/B | oracle + lineage | oracle + plasticity |
|---|---:|---:|---:|
| all 8 A removed | 0 / 16 | 0 / 16 | **8 / 16** |
| all 16 B removed | 8 / 0 | 8 / 0 | **8 / 16** |
| all A + 4 B removed | 0 / 12 | 0 / 16 | **8 / 16** |
| 4 A + all B removed | 4 / 0 | 8 / 0 | **8 / 16** |

The lineage-conserving controller has perfect knowledge that A or B is missing but cannot create a type for which no parent remains. It repairs **0/4** lineage-extinction cases. Adding daughter-fate plasticity repairs **4/4**.

This is the useful result: **information about the goal is not sufficient when the system lacks a generative action capable of reaching it.** Plasticity changes which damage challenges are feasible; it is not merely another measurement channel.

## Complete extinction

Removing all 24 cells defeats both controllers. Even the plastic arm has no surviving parent from which local proliferation can begin. Thus the declared capability boundary has three levels:

- both lineages survive: composition information is sufficient for the authored repair rule;
- one lineage is extinct: fate plasticity is additionally required;
- every cell is gone: parent-dependent local regrowth is impossible even with perfect information and plasticity.

## Scope

This is a white-box diagnostic, not a biological model of differentiation. Target counts are supplied by oracle, terminal A/B polarity is authored, and plasticity is an explicit capability rather than an evolved or discovered process. The result is intentionally about **information versus action repertoire**, not about which controller is universally “more competent.”

Do not build a blind Goal Discovery layer for this oracle toy. The next constructive question is how a tissue could generate and maintain composition information itself—and whether a biologically suggestive local signal can support repair without simply handing cells the target counts.

## Reproduce

```bash
python3 experiments/09-composition-lineage/run.py
python3 -m pytest -q experiments/09-composition-lineage/test_model.py
```

Evidence: [`results/characterization.json`](results/characterization.json).
