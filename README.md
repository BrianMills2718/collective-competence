# collective-competence

How does coupling among bounded local systems produce higher-level competence?

The point is to find out whether *goal*, *perturbation*, *recovery*, *coupling*
and *collective competence* are actually measurable in systems small enough to
be understood completely, before introducing anything as confounding as a
language model.

## Where the work is

**[`goal-discovery/`](goal-discovery/)** is the current programme. It replaces
the experiment ladder this README used to list, with a stricter one: a
replication of a published system, pre-specified representations, a
discovery/validation/confirmation split, snapshot-exact branching, and null
models that have to be beaten before anything stronger than "it converges" may
be claimed. Start at its
[README](goal-discovery/README.md) and
[experiment 001](goal-discovery/docs/hypotheses/001_sorting.md).

**[`experiments/01-self-sorting/`](experiments/01-self-sorting/)** is the pilot
that came first and motivated it. Kept because its results still stand and
because the way it went wrong is the reason the new programme is built the way
it is: three of its first findings turned out to be implementation asymmetries
rather than properties of the system, and one measure ("holds the goal") was a
single sample of a fluctuating process. Those are exactly the failures the
freeze-before-confirming and snapshot-exact-branching rules exist to prevent.

## What the pilot found

Local action noise barely affects whether a goal is reached — feedback, not
decentralization, is the dividing line, and a controller that halts on "nothing
left to fix" stays goal-directed for a window only 5–20 operations wide.
Heterogeneous local rules break the collective by **headcount, not proportion**:
two opposing agents are as fatal at 4% of the population as at 20%. One
opposing agent is tolerated for reachability but drops goal occupancy to about
1/N.

Details, including the three implementation artifacts that had to be fixed
before any of it was believable, are in
[experiments/01-self-sorting/README.md](experiments/01-self-sorting/README.md).
None of it has been through validation or confirmation in the sense
`goal-discovery/` now defines, so read it as exploratory.

## Setup

The current programme:

```bash
cd goal-discovery && make dayone
```

The pilot:

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
