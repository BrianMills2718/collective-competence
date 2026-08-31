# Evidence and verification

- Test the changed scientific or user-visible boundary with the smallest useful
  positive/negative cases; preserve a falsifiable claim and realistic controls.
- Passing software tests is not scientific confirmation. Report fixture checks,
  exploratory trials, validation, and held-out confirmation separately.
- Check leakage, matched initial state/RNG, intervention semantics, and what the
  observation contract permits when these affect the claim.
- Missing optional data is missing evidence, not a passed experiment. Retain the
  exact skip/error reason and do not retune old results to make checks green.
- Documentation checks should catch broken routes, stale generated instructions,
  and duplicate experiment IDs. They cannot automatically certify useful synthesis.
