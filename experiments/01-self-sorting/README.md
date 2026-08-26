# Experiment 1 — self-sorting agents with local defects

`selfsort.py`. Plain Python plus matplotlib for the figures. Seeded and
reproducible; `python selfsort.py test` checks the substrate itself.

Ten integers on a line. Each integer is an agent that can see only itself and
one adjacent neighbour, and whose only action is "attempt to exchange with that
neighbour". The global target is the sorted array; distance to it is the
inversion count. Nothing in the system holds the target — it exists only in the
measurement.

Everything is priced in one currency: **one attempted inspection of an adjacent
pair, which may lead to an exchange**. Centralized, decentralized and random
controllers all spend that same primitive, including the coordinator's
monitoring scans, so operation counts compare directly.

## What is varied

**Controllers** — who decides which pair is touched next, and whether anyone is
still watching afterwards.

| | |
|---|---|
| `decentralized` | A random adjacent pair acts; a random one of the two is the initiator and applies its own rule. No coordinator, no halting condition. |
| `central_open` | A coordinator runs the textbook schedule of *n* passes and then declares completion. Has a plan and no feedback. |
| `central_closed` | Re-scans until a full pass finds no inversion, then halts. |
| `central_watchdog` | The same coordinator that never concludes it is finished. |
| `null_random` | Same locality, no rule: exchange with a random neighbour regardless. The control for "is it the coupling or just the locality?" |

**Defects** — `p_fail` (every attempted action fails with probability *p*),
`unreliable` (one agent fails 90% of its own actions), `frozen` (an agent never
initiates but can still be moved), `dead` (never initiates and cannot be moved,
so it blocks the line).

**Perturbations** — applied once, the moment the goal is first reached, or a
chosen number of operations later: swap two positions, move one element
elsewhere, or damage a member *and* the state together.

## What came out (N=10, 300 trials per cell)

**Local action noise is nearly irrelevant to whether the goal is reached.**
Decentralized, `central_closed` and `central_watchdog` all sort 100% of the time
at p=0.7, where 7 of every 10 attempted actions silently fail. Only the
open-loop plan degrades — 100% → 54% → 0% across p=0, 0.3, 0.7. The dividing
line is feedback, not centralization. `null_random` never sorts, so the
competence comes from the local rule and not from the locality.

**The decentralized version is robust but not cheap.** It pays about 1.6× the
coordinator's operation count to reach the goal, and about 1.7× to recover from
a disturbance, at every noise level. Robustness here is bought, not free.

**The sharpest result is about *when*, not *whether*.** Disturb the array
D operations after it first reaches sorted:

| D | decentralized | central_closed | central_watchdog |
|---|---|---|---|
| 0 | 1.00 | 1.00 | 1.00 |
| 5 | 1.00 | 1.00 | 1.00 |
| 20 | 1.00 | **0.00** | 1.00 |
| 200 | 1.00 | **0.00** | 1.00 |

At D=0 every closed-loop controller looks equally competent, which is what the
naive version of this experiment measures. `central_closed` is goal-directed for
a window roughly 5–20 operations wide and is merely goal-*shaped* thereafter.
The decentralized collective has no such window because it has no
representation of "done" to be wrong about. That distinction — being at the goal
versus still steering toward it — is the thing worth carrying forward.

**A degraded member is routed around; a blocking member is not.** Freezing an
agent or making it fail 90% of its actions costs some operations and changes
nothing else: recovery stays at 100%. A dead agent that will not move partitions
the line, and recovery drops to 52% for every controller equally. That is the
honest boundary of the competence.

**Heterogeneous rules break it by headcount, not by proportion.** The first
sweep at N=10 said "one agent in ten is tolerated, two in ten is not", which
described the result as a fraction. At N=10 a count and a fraction are the same
number, so that sweep could not tell them apart. Growing the population while
holding the count fixed settles it:

| opposing agents | N=10 | N=20 | N=30 | N=50 |
|---|---|---|---|---|
| 0 | 1.00 | 1.00 | 1.00 | 1.00 |
| 1 | 1.00 | 1.00 | 0.99 | 0.94 |
| 2 | **0.08** | **0.03** | **0.07** | **0.08** |
| 3 | 0.00 | 0.00 | 0.00 | 0.00 |

(probability the goal is ever reached). Two opposing agents break the collective
just as completely at 4% of the population as at 20%. Plotted against headcount
the four curves lie on top of each other; plotted against fraction they fan out
by an order of magnitude. The proportion was never the operative quantity.

**Reaching the goal and holding it break at different headcounts.** A single
opposing agent is tolerated for reachability but destroys the goal as an
attractor. Measuring occupancy — the fraction of the back half of a run spent
sorted, rather than one sample at the final operation — gives 0.097, 0.049,
0.033 and 0.024 for N = 10, 20, 30 and 50. That is about 1/N: one contrarian
reduces the collective to visiting its goal as often as it visits any single
configuration. It also costs: median operations to first reach the goal rise
from 2,635 to 20,248 at N=50. So one defector is survivable but expensive and
non-absorbing; two are fatal. Why the boundary sits exactly at two is not
tested here.

**The single-point-of-failure number is true by construction.** Kill one unit at
random: decentralized 1.000, centralized 0.913 = exactly 10/11, the
coordinator's share of the units. Freezing any one *agent* is survivable by
everyone. This is arithmetic from the model, not a discovery, and should be
reported that way.

## Three things I had to fix before believing any of it

Each of these made the decentralized controller look better than it is.

1. The coordinator always asked the **left** agent to act, while the
   decentralized rule asked a random one of the two. A single defective agent
   therefore stalled the centralized controllers permanently. That was an
   asymmetry in my code, not a structural property.
2. Freezing an agent at the moment the array is already sorted changes no state,
   so "recovery" was trivially instant and measured nothing. Member defects now
   damage the substrate and the state together.
3. Monitoring scans were free, so `central_watchdog` looped forever without
   spending anything, and a coordinator that never halts appeared to cost
   nothing. Looking is now charged at the same rate as acting.

## Running it

```bash
python selfsort.py test           # substrate self-checks, ~1s
python selfsort.py all            # every experiment + four figures, ~2min
python selfsort.py window         # the goal-directedness window on its own
python selfsort.py scale          # headcount vs fraction, N up to 50, ~3min
```

Outputs land in `results/` as one CSV and one PNG per experiment.

## Next

The mechanism behind the two-agent boundary is the first open question: one
opposing agent presumably ends up parked somewhere the majority can contain, and
two can hand a defect back and forth, but nothing here tests that. After that,
feed the transition system to
coarse-graining / causal-emergence tooling now that the state space is small and
well defined; then the two-resource production network with specialization,
which is the smallest bridge from this to an economics question.
