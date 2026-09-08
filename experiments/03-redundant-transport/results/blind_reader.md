# Zero-context reader — opaque redundant-route case

This is the verbatim answer from an ephemeral Codex session run outside the repository. It received only `blind_case.json.gz` after decompression plus the bounded analysis prompt. System meanings, field semantics, route/transport semantics, macro criterion, and implementation were withheld.

---

The package supports **symmetric, input-dependent behavior with bounded substitution in `s000`**. It does not identify physical mechanisms, a unique goal, or learning.

1. **Stable behavioral structure — observation**

   Write the recorded state as `(f000, f001, f002)` and let \(k=t-20\) after intervention. Both systems remain at `(0, u000/2, u000/2)` before intervention and throughout the no-operation controls.

   Every post-intervention trajectory, for \(k=1,\ldots,40\), is summarized below:

   | System | `u000` | Disable channel 0 | Disable channel 1 | Disable both |
   |---|---:|---|---|---|
   | `s000` | 2 | `(0, 0, 2)` | `(0, 2, 0)` | `(2k, 0, 0)` |
   | `s001` | 2 | `(k, 0, 1)` | `(k, 1, 0)` | `(2k, 0, 0)` |
   | Both | 4 | `(2k, 0, 2)` | `(2k, 2, 0)` | `(4k, 0, 0)` |

   Across all recorded consecutive samples, the following numerical relation holds:
   \[
   f000(t)-f000(t-1)=u000-f001(t)-f002(t).
   \]
   This is an observed arithmetic regularity, not an established physical conservation law.

   **Inference:** The trajectories exhibit channel-exchange symmetry and a common relation between the two-field sum and change in `f000`. Some conditions preserve a constant state; others preserve a constant growth rate. Constant trajectories alone do not establish attraction, recovery from arbitrary disturbances, or indefinite stability.

2. **Compensation/substitution — bounded inference**

   At `u000=2`, disabling either channel in `s000` makes one field zero and raises the other from 1 to 2 at the first subsequent sample. The sum `f001+f002` remains 2 and `f000` remains zero through \(t=60\).

   Under the same intervention, `s001` leaves the other field at 1. Its sum falls to 1 and `f000` increases by 1 each step, reaching 40.

   Thus, **`s000` exhibits complete numerical substitution relative to preserving that sum and the zero trajectory of `f000` at the lower tested input**. `s001` exhibits no corresponding increase. Its remaining nonzero field still accompanies less growth than disabling both, but that is retained contribution rather than an observed compensatory increase.

   At `u000=4`, the systems are indistinguishable: neither preserves the baseline sum or zero `f000` after a single disable. The substitution claim is therefore conditional on input, intervention, measured quantities, and observation window. It does not imply that preserving these quantities is either system’s goal.

3. **Causal conclusions and limits**

   **Conditional causal inference:** If the listed operations are controlled interventions and the matching conditions otherwise differ only by operation, they establish effects of those operations on the recorded trajectories. The unchanged controls and identical pre-intervention records support that comparison.

   In `s000` at input 2, either single channel remaining enabled is sufficient, within the tested background, to preserve `f000=0`; neither particular channel is individually necessary. Disabling both destroys that preservation. At input 4, both enabled channels are required among the tested configurations. In `s001`, both are required at both tested inputs.

   These are contextual necessity/sufficiency statements. The package does **not** establish that a field is itself a channel, that changes in `f001` or `f002` directly cause changes in `f000`, or that the operation has no other effects. It does not identify mediation, internal architecture, feedback, intentions, or behavior under untested interventions.

4. **Strongest capacity/resource boundary**

   **Observation:** With one channel disabled in `s000`, the remaining nonzero field equals 2 at both tested inputs. This suffices to preserve `f000=0` at input 2, but at input 4, `f000` grows by 2 per step to 80. With both channels enabled, the sum reaches 4 without such growth.

   **Inference:** This supports an effective single-channel limit of 2 **in the tested conditions**, and a boundary between successful preservation at input 2 and failure at input 4.

   **Speculation:** A hard capacity ceiling of 2 is one explanation. A fixed intervention rule, allocation constraint, or measurement ceiling could produce the same records. No particular scarce resource is identified, and total capacity beyond input 4 is untested.

5. **Rival interpretations and limitations**

   - A fixed, pre-existing switching rule could explain `s000`; feedback regulation or passive coupling could also fit. The sampled trajectories do not distinguish them.
   - `f000` could be a derived cumulative quantity calculated from the other values. The arithmetic relation does not prove an independently evolving physical state.
   - An operation could directly modify several recorded quantities. Its label alone does not establish a selective intervention on one internal component.
   - Only two inputs, one intervention time, and one trajectory per condition are supplied. Reproducibility, variability, other initial states, and longer-term behavior remain unknown.
   - **Learning is not demonstrated.** There is no observed improvement across experience, retention, or changed response on re-exposure. “Adaptation” is defensible only in the weak descriptive sense of an immediate condition-dependent adjustment; learned or persistent adaptation is unsupported. Changes faster than the sampling interval are unresolved.

6. **Observation, inference, and speculation**

   **Observation:** Exact states, slopes, symmetry, the numerical difference equation, and the low-input difference between systems.

   **Inference:** `s000` has bounded behavioral substitution under single-channel disable; this preservation fails at the higher input. Causal attribution applies to the operations under the controlled-comparison assumptions above.

   **Speculation:** Physical meanings, a particular resource, a unique objective, a specific controller, learning, or universal capacity limits. None is identified by this package.