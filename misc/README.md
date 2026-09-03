# misc/ — expiring, non-authoritative quarantine

This directory follows project-meta's "Temporary `misc/` escape hatch" policy
(`project-meta/docs/ops/WIKI_AND_DOCS_POLICY.md`, "New Artifact and Directory
Governance"): a tracked holding area for useful material that cannot yet be
classified into a proper concern owner. It is not a permanent home.

Every item under here must declare, in an adjacent `INTENT.md`:

- `authority: none`
- `owner`
- `destination` — where this is expected to end up once classified
- `reason` — why it isn't classified yet
- `expires_at` — timezone-aware ISO-8601, default max 14 days from creation

**Note on enforcement:** this repository does not yet have
`scripts/artifact_directory_policy.yaml`, so nothing here is mechanically
checked by `enforced-planning`'s `artifact_creation.py` — these rules are
applied by hand, faithfully to the real policy schema, pending formal
onboarding. An overdue item here should be treated the same as a failing audit
would treat it: moved, archived, or deleted, not left in place.

Unshared experiments and disposable notes belong in an ignored `scratch/` or
OS temp directory, not here.
