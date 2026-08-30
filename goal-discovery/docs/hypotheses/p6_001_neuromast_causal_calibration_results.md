# P6-001 — neuromast local-feedback causal calibration results

**Decision: no-go. Close M4377 without tuning.**

The selected off-the-shelf model produced a large, interpretable causal signal,
but it failed the frozen robustness and runtime design needed for the research
programme. Three of four fresh active seeds reconstructed a bounded, radially
ordered organ near the declared target. The fourth lost every sustentacular
cell and stalled at eight cells. Removing local stopping feedback caused
runaway growth in all four seeds and made a common 210,000-step endpoint
computationally inappropriate; the batch was stopped by the frozen allocation
rule with those partial trajectories preserved.

## What ran

The [frozen protocol](p6_001_neuromast_causal_calibration.md) used the authors'
Figure 4 E03 layout and official Morpheus 2.4.1 simulator. Fresh seeds 801–804
were run under:

- the published active local neighbor feedback;
- the same dynamics with only the neighbor-dependent stopping predicates
  disabled; and
- the same cell mechanics with proliferation probabilities set to zero.

All four active and all four proliferation-disabled runs reached the declared
210,000-step endpoint. The four feedback-disabled runs were preserved at their
latest completed 5,000-step checkpoint when the causal direction was common to
all seeds and the first run could no longer finish inside the 25-minute cap.
Eight of 12 planned trajectories therefore completed. The active replay was
not purchased after the no-go decision was fixed.

## Results

The declared E03 day-7 target was 52 cells with composition
hair/sustentacular/mantle = 14/27/11.

### Active local feedback

| Seed | Final cells | Hair | Sustentacular | Mantle | Macro distance | Radial order | Outcome |
|---:|---:|---:|---:|---:|---:|---:|---|
| 801 | 65 | 14 | 38 | 13 | 0.315 | 1.000 | recovered, oversized |
| 802 | 58 | 10 | 35 | 13 | 0.212 | 0.999 | recovered |
| 803 | 60 | 14 | 35 | 11 | 0.218 | 1.000 | recovered |
| 804 | 8 | 4 | 0 | 4 | 1.365 | 0.000 | failed; sustentacular extinction |

All active counts were unchanged over the frozen final interval, so the late-
growth measure was zero. That does not rescue seed 804: it is a stable failed
state, not successful bounded reconstruction. Full-run wall times reported by
Morpheus ranged from 90 seconds for that small failed tissue to 546–568 seconds
for the three reconstructed tissues.

### Stopping feedback disabled

| Seed | Latest time | Model days | Latest cells | Multiple of target | Macro distance |
|---:|---:|---:|---:|---:|---:|
| 801 | 80,000 | 2.67 | 558 | 10.73× | 10.501 |
| 802 | 65,000 | 2.17 | 300 | 5.77× | 5.531 |
| 803 | 70,000 | 2.33 | 394 | 7.58× | 6.870 |
| 804 | 60,000 | 2.00 | 260 | 5.00× | 4.227 |

Every mechanism-disabled trajectory was already at least five times the day-7
target by no later than model day 2.67 and was continuing to grow. Seed 801 had
consumed more than 11 minutes to reach only time 80,000, with later steps
becoming slower as cell count rose. Reaching 210,000 inside the remaining
frozen runtime budget was impossible. Continuing the four explosions could not
change the decision, so the allocation protocol stopped them.

### Proliferation disabled

All four passive controls remained at the same five cells present at time zero:
zero hair, two sustentacular, and three mantle cells. Their macro distance was
1.292 and radial-order score 0.500. Cell mechanics alone therefore did not
reconstruct the organ.

## Gate audit

| Frozen requirement | Result |
|---|---|
| all 12 runs complete | **fail** — 8 complete; four runaway controls stopped |
| identical matched initial macrostate | pass — five cells in every arm and seed |
| active macro distance advantage over both controls | not scoreable at the common frozen endpoint |
| active median late growth ≤ 0.10 | pass — 0.000 |
| feedback-disabled ≥25% above active in at least 3/4 seeds | directional pass already at partial checkpoints, but endpoint gate incomplete |
| proliferation-disabled no more than one new cell | pass — no new cells in 4/4 |
| active median radial order ≥0.70 | pass — median 0.999, with one zero-score failure |
| deterministic active replay | not run after stop |

Independent parsing confirmed that unique observed cell identities by type
equaled every logged population count at every saved time. Source and generated
variant hashes are in `metadata.json`. Morpheus automatically converted the
published v4 XML to its internal v5 schema and recorded the warnings in each
completed run log; no dynamics parameter was repaired in response.

## Interpretation

The model supplies real mechanism discrimination:

- passive relaxation cannot recover the damaged organ;
- stochastic proliferation without the local stop rule runs away; and
- the published local rule can reconstruct size, composition, and radial order.

But the research agenda needs a **robust benchmark**, not one compelling seed.
Fresh seed 804 demonstrates an absorbing failure mode in which the
sustentacular population disappears. The mechanism-off arm also demonstrates
that a fixed full-horizon endpoint is the wrong counterfactual design for an
unbounded process. These are benchmark-design failures, not reasons to tune the
published thresholds after seeing the result.

M4377 is therefore closed. The causal signal is retained as a useful model-
internal lesson, but it does not unlock held-out macro prediction or causal-
emergence tooling.

## Allocation reflection and changed plan

The sprint stopped at the point where additional computation could not change
the decision. Completing the cheap passive arm still had information value; a
fresh active replay and the remaining runaway horizon did not. This preserved
the rapid-prototyping ratio: most time produced or challenged observable
behavior, and no dashboard, simulator port, or full-paper reproduction was
built.

P6-000's package-level checklist was necessary but insufficient. It verified
that seeds and result archives existed; it did not verify fresh-seed success
rate or whether the causal control remained bounded enough for a matched
endpoint. The next qualification therefore moves **before installation** and
requires an archive-level robustness/control preflight. A candidate must show
at least 80% recovery across at least eight independent units and three damage
layouts, plus either a bounded mechanism-off endpoint or a declared
time-to-failure event. Otherwise the programme writes the missing benchmark
contract instead of adopting it.

## Reproduction and artifacts

```bash
uv run python -m src.spikes.morpheus_neuromast.run \
  --run-id p6-001-neuromast-causal-calibration
```

The original command was stopped under its frozen rule. The compact closure
artifacts are regenerated from the preserved partial and complete logs with:

```bash
uv run python -m src.spikes.morpheus_neuromast.analyze_stopped \
  results/p6-001-neuromast-causal-calibration
```

The ignored result directory contains `decision.png`, `layout_strip.png`,
`decision.json`, `stopped_metrics.csv`, `stopped_trajectories.csv`, generated
variants, raw logger tables, logs, performance records for completed runs, and
source/variant hashes.
