# Zero-context mixed contrast check

A separate ephemeral Codex session received compact opaque evidence from four cases together: the passive scalar case, the feedback-regulation scalar case, redundant-route compensation, and route-learning adaptation. Case names, field semantics, authored criteria, mechanisms, and implementations were withheld. No mixed-case analyzer or benchmark framework was added; this was a one-off stopping test for the calibration sequence.

The answer is preserved verbatim below.

---

The evidence separates several behavioral signatures, but does **not** uniquely distinguish passive mechanisms from active regulation. Here, “preservation” and “recovery” describe observed values, without assigning them purpose or desirability.

**x000 — Convergence/attraction supported; passivity underdetermined.**

- **Observations:** Negative displacements approach 97; positive displacements approach 103. Persistent inputs produce different terminal plateaus: 84, 92, 111, and 119 as `u` increases.
- **Inference:** The observed variable returns toward a narrow region after displacement and settles into input-dependent plateaus under sustained forcing. This supports attraction-like behavior over the tested range.
- **Rivals/limits:** Passive relaxation and active feedback with residual offsets can both produce these trajectories. The observations do not establish one exact attractor: opposite displacement directions retain different terminal values. Finite duration, rounding, deadbands, or multiple equilibria remain possible. No substitution or history-dependent adaptation is demonstrated.

**x001 — Stronger disturbance attenuation; active regulation compatible, but underdetermined.**

- **Observations:** Displacements return faster and closer to 100 than in x000, terminating at 99 or 101. Persistent-input endpoints lie between 94 and 106, with small alternating values for `u = ±2`.
- **Inference:** Relative to x000, this case shows faster restoration and less endpoint sensitivity to the same supplied inputs. It supports a stronger regulation-like behavioral signature, alongside convergence/attraction.
- **Rivals/limits:** Faster return and smaller offsets do not identify active regulation. A passive system with different restoring properties could reproduce them. There is no intervention on sensing, feedback, or an independently identified corrective process. The small oscillations do not resolve that ambiguity. Compensation and adaptation are untested.

**x002 — Compensation/substitution directly supported in s000, with a demonstrated operating limit; channel-dependent maintenance in both systems.**

- **Observations:** With both channels available, both systems preserve `f000 = 0` at both tested inputs. At `u = 2`, disabling either channel in s000 makes the surviving channel’s associated output increase from 1 to 2, while `f000` remains zero. In s001, the surviving output remains 1 and `f000` reaches 40. Disabling both channels makes `f000` reach 80 in both systems.

  At `u = 4`, either single-channel disablement leaves the surviving output at 2 and `f000` reaches 80; disabling both produces 160.
- **Inference:** s000 exhibits functional substitution at the lower input: an increased contribution from the remaining channel preserves an otherwise disrupted observable. The higher-input trials establish a limit to successful compensation in the tested conditions. Both systems’ baseline maintenance of `f000` depends on channel availability.
- **Rivals/limits:** Channel-dependent maintenance and compensatory redistribution support an operational regulation interpretation, but do not uniquely establish active feedback. Passive redistribution, input-driven balancing, or a fixed intervention-responsive rule remain compatible. A channel ceiling of 2 is consistent with the data, but not independently established. s001 shows no substitution under these tests; that does not establish its impossibility elsewhere. No adaptation across repeated exposure is demonstrated.

**x003 — History-dependent adaptation supported behaviorally; its mechanism and functional meaning remain underdetermined.**

- **Observations:** In a000, constant inputs accompany progressive changes from `f001/f002 = 50/50` toward either `90/10` or `10/90`, with `f000` increasing from 75 to 95. Following input reversal, the previous split initially persists, `f000` falls to 55, and subsequent blocks progressively reverse the split while `f000` returns to 95.

  At block 4, c001 and c002 have identical current inputs but different outputs because their preceding inputs differ; c000 and c003 provide the mirrored comparison. Holding component_000 fixed or restoring it before every block eliminates these changes: all conditions remain at `75, 50, 50`.
- **Inference:** Current inputs alone do not determine the outputs. The reversal behavior supports history-dependent adjustment, and both interventions implicate the ability of component_000 to change or retain changes in producing that adjustment.
- **Rivals/limits:** The evidence does not distinguish learning from ordinary stateful relaxation, lagged tracking, or another fixed dynamical rule. Intervention specificity is unspecified, so component_000 cannot be identified uniquely as a memory or learning mechanism. An increase in anonymous `f000` cannot be called improved performance. The changing output split resembles redistribution, but no channel-loss test establishes substitution as directly as in x002.

**Are the four concepts behaviorally separable here?**

**Partly, as signatures; not as four exclusive mechanism classes.**

- **Attraction:** Demonstrated by displacement recovery in x000 and x001.
- **Active regulation:** Not uniquely identified. x001 shows stronger attenuation, and x002 provides stronger causal evidence for channel-dependent maintenance, but neither excludes passive or feedforward alternatives.
- **Compensation/substitution:** Specifically demonstrated by s000’s successful single-channel replacement at `u = 2`, contrasted with s001 and the higher-input failures.
- **History-dependent adaptation:** Demonstrated by x003’s different responses under identical current inputs after different histories, reinforced by the hold/reset interventions.

These signatures can coexist. None establishes one true goal, agency, or internal representation.

- **Done:** Classified all four cases using supplied evidence.
- **Policy:** Used no external evidence or semantic assumptions about identifiers.
- **Concerns:** Mechanism identity and generalization beyond the tested conditions remain unresolved.
- **Learnings:** None; no cross-session operational finding arose.
- **Decisions:** None; no ADR-shaped decision occurred.
- **Recommended next:** Analysis complete.
- **Need anything from human:** No.
