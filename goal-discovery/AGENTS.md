<!-- GENERATED from CLAUDE.md by scripts/sync_agent_context.py; do not edit. -->

# Laboratory scope

Read the repository bootstrap and project wiki first. This historically named
subtree contains the active Goal and Competence Discovery lane and much of the
shared Dynamical Laboratory implementation. It does not define the broader
research agenda or make every contained experiment a discovery study.

- Use `../wiki/ontology.md` for terms and `docs/PROJECT.md` for scientific scope.
  `docs/plans/current_research_plan.md`
  alone owns current priorities; old phase IDs and `research_state.yaml` may be historical.
- The investigation unit is a question plus competing explanations and an
  intervention, not a simulator, chart, or library chosen in isolation.
- Record which goals, features, metrics, and hypotheses were supplied by hand.
- Declare specimen origin, analyst access, and research purpose independently.
  Freeze blind-first interpretations before revealing authored mechanisms.
- For a visual artifact, connect configuration, trajectory, contrast, inference,
  and limitations. Read `docs/plans/dynamic_experiment_artifact_standard.md`.
- Before runtime claims, identify the exact checkout and code revision. The
  current plan records integration checks; a localhost URL is not a revision.
- Read `docs/CLAUDE.md`, `src/CLAUDE.md`, or `tests/CLAUDE.md` when touching that scope.
