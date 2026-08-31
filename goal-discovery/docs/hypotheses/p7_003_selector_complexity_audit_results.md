# P7-003 selector complexity audit — results

**STOP: equal descriptive capacity did not produce a stable generic family
selector. No family won the frozen six-of-eight leave-one-seed gate.**

## Evidence boundary and method

This is retrospective Level 1 development evidence. Both P7-002 discovery and
confirmation outcomes were already open. Nothing here repairs the failed
prospective claim or licenses selecting a model from confirmation performance.

Each family used exactly the four summaries frozen in the P7-003 protocol, the
same three intervention-only columns, and the same summary-by-intervention
interactions. For each of the eight discovery seeds, the model was fit on the
other seven seeds and scored on all five arms of the held-out seed. The family
with the lowest held-seed log loss was that fold's winner. Coefficient signs were
recorded from the same eight fits. The untouched label no longer applies to the
confirmation split; it was used only to describe the retrospective
discovery-to-confirmation gap.

## Frozen gate result

| Family | Held-seed wins | Required | Gate |
|---|---:|---:|---|
| Identity-conditioned | 3 | 6 | fail |
| Network | 3 | 6 | fail |
| Temporal | 2 | 6 | fail |
| Relational | 0 | 6 | fail |

The winner varied materially by seed. Two of the eight winning families even
performed worse than the intervention-only null on their held-out seed. Because
no family reached six wins, the protocol does not nominate a family for the
confirmation-sign or coefficient-sign gates. The decision is therefore fixed
before any retrospective confirmation comparison: **stop generic family
selection**.

## Retrospective diagnostics

| Family | Discovery log loss | Confirmation log loss | Confirmation improvement over null |
|---|---:|---:|---:|
| Identity-conditioned | 0.600 | 0.556 | +15.7% |
| Temporal | 0.651 | 0.725 | −9.9% |
| Network | 0.719 | 0.599 | +9.2% |
| Relational | 0.742 | 0.563 | +14.7% |

These opened-data scores are diagnostics, not selection evidence. Their rank
changes reinforce the stop: relational was worst on discovery but nearly tied
identity on confirmation, while temporal moved in the wrong direction.

Collinearity remained substantial despite matching summary counts. Temporal had
rank three across four standardized summaries because checkpoint resistance and
resistance slope were perfectly correlated in these eight seeds. Relational's
maximum pairwise absolute correlation was 1.000 (rounded), identity's 0.968, and
network's 0.872. Across deletion fits, temporal had two coefficients with more
than two modal-sign disagreements and network had one. Identity and relational
did not exceed that coefficient threshold, but neither earned entry to the sign
gate because neither was a stable winner.

## Decision and next branch

Unequal feature count was not the sole cause of P7-002's instability. Four
generic family labels are too coarse to choose a representation reliably from
this evidence. Retire the generic automated-family leaderboard and return to
task-conditioned, scientifically specified representations. A future sprint
should start from a concrete prediction/intervention question and compare a
small representation justified for that question against simpler nulls; it
should not run another generic family tournament.

Virus on a Network remains closed as prospective evidence. Do not add seeds,
retune regularization, search feature subsets, or promote the retrospective
identity or relational scores.

## Reproduction

With the regenerable P7-002 feature table present:

```bash
uv run python -m src.experiments.prospective_network_selector.audit
uv run pytest -q tests/test_prospective_network_selector.py
```

The audit writes `fold_winners.csv`, `fold_scores.csv`, `full_scores.csv`,
`collinearity.csv`, coefficient tables, and `summary.json` under
`results/p7-003-selector-complexity-audit/`. Result artifacts are ignored by git
under the repository's existing regenerable-results policy.

## OB-001 sprint observation 1 of 3

The mature-outcome trace helped enforce the abstention path: a strong-looking
retrospective identity score could not replace the frozen stability question.
It also prevented work on a new visual leaderboard or generator. The audit did
not instrument wall-clock planning overhead or time-to-first-evidence, so those
quantities remain unmeasured rather than estimated. For the next two pilot
sprints, capture timestamps at sprint start, first artifact, and decision so the
retain/revise/stop retrospective has quantitative evidence.
