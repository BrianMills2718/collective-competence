# Provenance of the Experiment 001 rules

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
