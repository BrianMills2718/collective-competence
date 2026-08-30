# P7-003 selector complexity audit

**Status:** next Level 1 methodology sprint  
**Time cap:** 60 minutes  
**Evidence boundary:** retrospective development only; no new scientific claim

## Decision being purchased

Did P7-002 fail because the identity-conditioned signal lacks prospective value,
or because representation families were compared with unequal and unstable
descriptive capacity?

The selected identity family transferred directionally, while removing its
mean/max duration features improved confirmation. The correct response is not to
promote the ablation or rerun Virus. It is to decide whether a simpler,
capacity-matched selector contract is coherent enough to test prospectively on
a different task.

## Bounded audit

Use P7-002 discovery and confirmation outcomes openly as development data and
label every result retrospective. Compare each family through exactly four
predeclared observable summaries and the same intervention interactions:

- temporal: checkpoint infection, infection slope, checkpoint resistance,
  resistance slope;
- relational: infection-boundary fraction, exposed-susceptible fraction, mean
  infected neighbors, same-state edge fraction;
- identity: ever-infected fraction, mean duration, late burden, degree-weighted
  burden;
- network: infected mean degree, infected degree share, largest infected
  component fraction, infected betweenness share.

Measure feature collinearity, leave-one-seed-out winner stability, coefficient
stability, and the gap between discovery and confirmation. Do not search feature
subsets or tune regularization.

## Gate

- **Freeze a revised prospective contract** only if one family wins under the
  equal-capacity rule in at least six of eight leave-one-discovery-seed analyses,
  its advantage has the same sign in confirmation, and no coefficient sign flips
  in more than two folds.
- **Stop generic family selection** otherwise and return to task-conditioned,
  scientifically specified representations.

Any revised contract must be tested on a different task with new outcomes. Virus
on a Network is closed as prospective evidence after this audit.

## Allocation

| Time | Work | Output |
|---:|---|---|
| 0–15 min | capacity and collinearity inventory | comparable feature contract |
| 15–40 min | fixed equal-capacity stability analysis | fold/winner surface |
| 40–52 min | failure attacks and claim-boundary check | stop or freeze rationale |
| 52–60 min | update plan and cockpit | one next branch |
