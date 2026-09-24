# Evidence and verification

- Test the changed scientific or user-visible boundary with the smallest useful
  positive/negative cases; preserve a falsifiable claim and realistic controls.
- Passing software tests is not scientific confirmation. Report fixture checks,
  exploratory trials, validation, and held-out confirmation separately.
- Test capability contracts separately from goal-relative competence claims.
  Robustness needs challenges; adaptation needs evidenced change after loss;
  authored targets cannot satisfy a goal-discovery assertion.
- Check leakage, matched initial state/RNG, intervention semantics, and what the
  observation contract permits when these affect the claim.
- Missing optional data is missing evidence, not a passed experiment. Retain the
  exact skip/error reason and do not retune old results to make checks green.
- Documentation checks should catch broken routes, stale instruction files,
  and duplicate experiment IDs. They cannot automatically certify useful synthesis.
