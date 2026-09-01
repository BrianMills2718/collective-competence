---
doc-role: source-provenance-index
authority: canonical
lifecycle: active
---
# Sources and original specifications

[Development wiki](../../../wiki/index.md) ·
[Research ontology](../../../wiki/ontology.md) · [Current charter](../PROJECT.md)

## Supplied research briefs

These are retained source inputs, not live execution plans. The current user
clarification and [charter](../PROJECT.md) govern the destination; the
[current plan](../plans/current_research_plan.md) governs next actions.
An original source calling itself "current" does not override either.

| Preserved source | What it contributes |
|---|---|
| [Consolidated laboratory specification](briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md) | Full agenda, shared apparatus, observation/white-box separation, staged discovery |
| [Coding-agent specification](briefs/Dynamical_Laboratory_Coding_Agent_Spec.md) | Experimental candidate-goal discovery, minimal engine, classical analysis baseline |
| [Robinson-Crusoe addendum](briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md) | Progressive construction, candidate boundaries, entropy/information distinctions |

Originals were supplied in the user's Windows Downloads directory and retained
there unchanged. The repository snapshots add source-role headers and normalize
line endings; they are not claimed to be byte-identical copies.

Original SHA-256 fingerprints:

- `Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md`:
  `bc06cefa faf3975c 697f3117 e27c45b9 34250529 88475d6f 80ceb35c ec8c64ff`
- `Dynamical_Laboratory_Coding_Agent_Spec.md`:
  `54806f72 1efc2ed3 dba5574f 6dda1eb8 9ef6b1d9 2acf60cc b2167811 b909a0b7`
- `Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md`:
  `43bdfbb6 4050b986 7d093117 1236fd98 b4edba14 b1e66738 53c54e80 2545a04a`

Spaces above group hash digits for reading. These fingerprints identify original
files, not the wrapped repository snapshots.

## Authority reconciliation

The original briefs deliberately start with manual observables and simple
systems. That is a sequencing decision, not a restriction of the destination
to predefined tasks. Their immediate-task lists are historical.

The user's clarified goal integrates two directions already present in these
briefs: the Collective Competence constructive arm and the Goal and Competence
Discovery analytic arm. Common visual analytics are part of the shared
Dynamical Laboratory, conditional on each run's supported observations and
interventions. The [ontology](../../../wiki/ontology.md) owns their current
terminology. No claim is made that all of that machinery has already been
implemented.

## Experiment 001 rule provenance


The replication target is:

> Taining Zhang, Adam Goldstein, Michael Levin (2024). *Classical Sorting
> Algorithms as a Model of Morphogenesis: self-sorting arrays reveal unexpected
> competencies in a minimal model of basal intelligence.*
> arXiv:2401.05375v1.

with its own reference implementation at
`github.com/Zhangtaining/cell_research`, commit
`1fd2bd5921c1f6b423a71f691d5189106a8a1020` (2024-10-30).

Neither is vendored here. The PDF is 2.3 MB and the reference repository is
third-party code under no license we have checked; copying either into this
repository would add weight and a licensing question without adding
reproducibility, since both are fetched by identifier in one command:

```bash
curl -sL -o zgl2024.pdf https://arxiv.org/pdf/2401.05375v1
git clone https://github.com/Zhangtaining/cell_research.git \
  && git -C cell_research checkout 1fd2bd5921c1f6b423a71f691d5189106a8a1020
```

## Which source settled which rule

| Rule | Settled by |
|---|---|
| Cell-view bubble: move left if smaller than left neighbour, right if bigger than right neighbour | Paper, Methods, "Implementation of Cell-View Sorting Algorithm" |
| Bubble picks *which* neighbour to look at by a coin flip each activation | Reference, `modules/multithread/BubbleSortCell.py`, `move()` — `check_right = random.random() < 0.5`. The paper does not mention this and it materially changes the dynamics. |
| Cell-view insertion: view all cells to the left, swap only with the left neighbour, move only when the prefix is sorted | Paper, Methods |
| Insertion's prefix check skips frozen cells rather than failing on them | Reference, `InsertionSortCell.is_enable_to_move()` |
| Cell-view selection: hold an ideal position, initially leftmost; swap with its occupant when smaller | Paper, Methods |
| **Selection advances its ideal position by one when it loses the comparison, and also when the occupant is frozen** | Reference, `SelectionSortCell.should_move_to()`. The paper states the swap condition but never says what happens otherwise, so the replication would have been guesswork without the code. |
| A sorting step is one comparison *or* one swap | Paper, "Total Sorting Steps" |
| Monotonicity Error = count of adjacent pairs violating order | Paper, "Monotonicity and Monotonicity Error" |
| Sortedness Value = percentage of cells following the designated order | Paper, "Sortedness Value" |
| Frozen cells come in moveable and immovable kinds, reported separately | Paper, Results, "Error tolerance" |

## Deliberate deviations

Both are forced by this program's determinism requirement, and both are
implemented so the deviation is visible rather than silent.

1. **Activation order.** The reference gives every cell its own Python thread,
   so ordering is whatever the OS scheduler does and no run reproduces. Here a
   tick is one explicit sweep in which every cell acts once, in an order named
   by config (`index`, `reverse_index`, `shuffled`). `shuffled` is the default
   as the closest deterministic stand-in for concurrency.
   `tests/test_reproducibility.py::test_activation_order_changes_the_history`
   exists to keep this from being hidden: the order demonstrably changes the
   trajectory, so it is a declared experimental variable, not an accident.
2. **Randomness.** The reference calls the global `random`. Here every draw
   comes from a seeded generator whose state is part of every snapshot, so a
   branch resumes the same stream it would have seen.

## Where the brief and the paper disagree

The brief specifies Experiment 001 as "a small 2-D grid or graph" with "two or
more object/cell types". Zhang/Goldstein/Levin is a **1-D array of distinct
integers**. Fidelity to the named publication was treated as the binding
constraint, since the brief also says to treat the publication's rules as
authoritative; a 1-D array is a path graph, so this satisfies the "or graph"
half of that sentence. The three day-one measures are named in grid vocabulary
and are implemented as their direct 1-D analogues, documented in
`src/experiments/sorting/representations.py`.

The reference repository does contain 2-D work (`modules/Cell2D.py`,
`sorting_cells_2d.py`) which is not part of the paper's headline results. If a
genuine 2-D grid is wanted, that is a second experiment with its own hypothesis
document, not a change to this one.
