# collective-competence

How does coupling among bounded local systems produce higher-level competence?

Each experiment is a self-contained directory under `experiments/`, with its own
script, writeup, and results. They are meant to be small: the point is to find
out whether concepts like *goal*, *perturbation*, *recovery*, *coupling* and
*collective competence* are actually measurable, before introducing anything as
confounding as a language model.

## Experiments

| | | |
|---|---|---|
| 01 | [self-sorting agents with local defects](experiments/01-self-sorting/) | done |
| 02 | tiny production / specialization world | not started |
| 03 | dispersed information | not started |
| 04 | communication | not started |
| 05 | persistent organization | not started |
| 06 | causal-emergence analysis of the transition systems above | not started |
| 07 | LLM agents, only once the measurables hold up without them | not started |

## What experiment 01 found

Local action noise barely affects whether a goal is reached — feedback, not
decentralization, is the dividing line, and a controller that halts on "nothing
left to fix" stays goal-directed for a window only 5–20 operations wide.
Heterogeneous local rules break the collective by **headcount, not proportion**:
two opposing agents are as fatal at 4% of the population as at 20%. One
opposing agent is tolerated for reachability but drops goal occupancy to about
1/N.

Details, including three implementation artifacts that had to be fixed before
any of it was believable, are in
[experiments/01-self-sorting/README.md](experiments/01-self-sorting/README.md).

## Setup

```bash
python3 -m venv .venv && .venv/bin/pip install numpy matplotlib
.venv/bin/python experiments/01-self-sorting/selfsort.py test
.venv/bin/python experiments/01-self-sorting/selfsort.py all
```

## History

Experiment 01 was first written in `BrianMills2718/agent_ecology` (commits
`ec00406` and `66b007c`) and moved here so this research line has its own home;
that repository is about tool-calling agent ecologies and is a different
subject. The original commits remain in its history.
