# Plan completion ledger

**Status: complete. There are zero active required plans.**

This ledger closes the ambiguity between executable plans and retained policy or
decision-history documents. `current_research_plan.md` remains the authoritative
roadmap; historical “next” language records what followed at the time and does
not create a current task.

| Plan document | Terminal disposition | Completion evidence |
|---|---|---|
| `current_research_plan.md` | authoritative roadmap; P7 route evidence-closed and P8 checkpoint ready for authorization | `docs/audits/2026-08-29_outcome_backcasting_final_audit.md` plus current user-authorized strategic review |
| `dynamic_experiment_artifact_standard.md` | retained protocol; no active deliverable | `docs/audits/2026-08-29_outcome_backcasting_final_audit.md` |
| `outcome_backcasting_protocol.md` | complete; retain with revision locally | `docs/audits/2026-08-29_ob_001_three_sprint_retrospective.md` |
| `p2_research_pivot.md` | superseded decision history | `docs/audits/2026-08-29_outcome_backcasting_final_audit.md` |
| `p3_generator_reuse_survey.md` | complete | `docs/audits/2026-08-29_p3_generator_reflection.md` |
| `p4_generator_selection.md` | complete | `docs/audits/2026-08-29_p4_target_inference_reflection.md` |
| `p5_001_reuse_survey.md` | complete-negative | `docs/hypotheses/p5_001_slime_mold_network_threshold_results.md` |
| `p6_000_phenomenon_qualification.md` | complete | `docs/hypotheses/p6_001_neuromast_causal_calibration_results.md` |
| `p6_002_archive_first_benchmark_contract.md` | complete-negative | `docs/research_state.yaml` |
| `p6_003_compact_evidence_package_acquisition.md` | complete-negative | `docs/research_state.yaml` |
| `p7_003_selector_complexity_audit.md` | complete-negative | `docs/hypotheses/p7_003_selector_complexity_audit_results.md` |
| `p7_004_ants_trail_scale_preregistration.md` | executed once; complete-negative | `docs/hypotheses/p7_004_ants_trail_scale_results.md` |
| `p7_005_network_intervention_value_preregistration.md` | executed once; complete-negative | `docs/hypotheses/p7_005_network_intervention_value_results.md` |
| `progress_allocation_protocol.md` | retained protocol; no active deliverable | `docs/audits/2026-08-29_ob_001_three_sprint_retrospective.md` |
| `reuse_survey_protocol.md` | retained protocol; no active deliverable | `docs/audits/2026-08-29_outcome_backcasting_final_audit.md` |
| `v1_phase2.md` | complete | `docs/audits/v1.md` |
| `x01_mesa_spike.md` | complete | `docs/plans/x01_mesa_decision.md` |
| `x01_mesa_decision.md` | complete decision | `docs/plans/x01_mesa_decision.md` |
| `x02_netlogo_calibration.md` | complete | `docs/plans/x02_netlogo_decision.md` |
| `x02_netlogo_decision.md` | complete decision | `docs/plans/x02_netlogo_decision.md` |
| `x03_visual_analytics_decision.md` | complete decision | `docs/plans/x03_visual_analytics_decision.md` |
| `plan_completion_ledger.md` | complete inventory | `docs/audits/2026-08-29_outcome_backcasting_final_audit.md` |

## Externally gated opportunities

The passive P6-004 evidence request and any future company-method transfer pilot
are not active required plans. Both require new external evidence or a new
explicit authorization and have evidence-backed stop decisions. Likewise, V4
can reopen only for a genuinely new causal task or qualified external bundle.
None permits another internal repair sprint.

## Completed implementation checkpoint

`docs/roadmaps/p8_sorting_laboratory_phase.md` completed at P8-C1 on 2026-08-30.
Its pass decision, live checks, timing, limitations, substrate boundary, and
selected next branch are recorded in
`docs/audits/2026-08-30_p8_c1_vertical_slice.md`. It remains outside
`docs/plans/` so the terminal plan inventory continues to distinguish retained
planning policy from bounded implementation roadmaps.

## Completion invariant

`docs/research_state.yaml` registers every Markdown document in `docs/plans/`
exactly once with a terminal disposition and evidence path. The state loader and
tests fail if a plan file is missing, duplicated, assigned a nonterminal state,
or backed by a missing evidence source.
