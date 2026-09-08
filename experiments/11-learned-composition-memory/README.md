# Experiment 11 — learned extracellular composition memory

Experiment 10 replaced hard count measurements with tissue-generated A/B signals, but the controller still contained authored target thresholds. This experiment removes those target-count constants from the **repair** controller. Instead, a slow extracellular memory learns the healthy A and B signal levels before damage and retains them as setpoints.

The question is narrow: can information learned from the tissue's own healthy history survive loss of the lineage that originally generated it, and for how long is that memory useful?

## System

A and B compartments use the same endogenous exponential signals as Experiment 10. During an undamaged training phase, two extracellular memory variables follow the healthy A and B signals by a simple exponential moving average:

```text
M' = M + alpha * (signal - M)
```

with `alpha = 0.2` for 100 training steps. Repair receives **no target A count or target B count**. A wounded boundary grows while its current compartment signal is below 99% of the remembered healthy signal. Daughter-fate plasticity is available in the principal arm so a completely lost lineage can be recreated from surviving tissue.

After damage, the memory is no longer trained from the damaged state. It persists extracellularly but may decay by a fixed retention factor after each birth. This is an authored toy memory mechanism, not a biological claim.

## The same controller learns several healthy compositions

The identical controller is tested on healthy compositions:

- `A^6 B^18`
- `A^8 B^16`
- `A^10 B^14`

For each, memory starts at zero and converges to the healthy endogenous signal. The largest relative setpoint error after training is below `2.1e-10`.

With non-decaying learned memory, the plastic repair controller restores all **12/12** declared challenges: for each healthy composition, one partial bilateral loss, complete A loss, complete B loss, and a larger bilateral-half loss.

Thus the repair rule is not relying on hard-coded 8/16 target counts; the healthy state itself supplies the remembered setpoint.

## Memory retention is a capability boundary

The same 12 challenges were repeated while the extracellular trace decayed after each birth:

| memory retained per birth | exact repairs / 12 |
|---:|---:|
| 1.0000 | **12** |
| 0.9995 | **12** |
| 0.9990 | 11 |
| 0.9980 | 8 |
| 0.9950 | 4 |

Longer missing compartments fail first because they require more births while the remembered setpoint is decaying. The direction is expected from the construction; the useful result is the explicit **memory-horizon boundary** rather than the numerical values themselves.

Lineage extinction remains a separate capability requirement. Across complete A and B loss for all three healthy compositions, the same learned memory with **no fate plasticity restores 0/6** cases. Remembering the target does not create the missing cell type.

## Reporter failure is only partly disambiguated

The boundary/wound state from the preceding regeneration work provides one useful orthogonal cue.

If A secretion fails in an otherwise healthy `A^8 B^16` tissue **without a wound**, the A signal collapses but no boundary is marked wounded, so the learned-memory controller performs **0 births**. It does not mistake an isolated reporter fault for structural loss in that challenge.

But if A secretion fails **at the same time as an A wound**, the ambiguity remains. Current A signal stays near zero even as new A cells are produced, so the controller cannot tell that structural repair has completed. In a fixed 40-birth observation window:

- partial A wound + A reporter failure ends at **A=44, B=16**;
- complete A extinction + A reporter failure ends at **A=40, B=16**.

So persistent setpoint memory solves loss of the *target reference* but does not make the current-state reporter self-authenticating.

## Fault-identifiability analysis

The next limitation can be stated without another simulation. Let `N` be current A abundance, `H` indicate whether the A reporter is healthy, and let the observed A signal be

```text
S = H * f(N)
```

where `f` is the increasing endogenous-signal function and `f(0)=0`. The controller also observes the wound bit `W` and retains the learned healthy setpoint `M`.

At wound onset, every state with `W=1`, broken reporter `H=0`, and any possible `N` produces the same pair `(W,S) = (1,0)`. Complete A extinction with a healthy reporter also initially produces `(1,0)`.

One **diagnostic A birth** can separate the last case from reporter failure: if the reporter is healthy, a newly created A cell makes `S>0`; if the reporter is broken, `S` remains zero. So reporter health itself is experimentally identifiable with the available plastic action.

But after reporter failure is established, current A abundance is not. Further A births change `N` while the observation remains `S=0`. Different initial wounded abundances therefore generate the same observation history under the same birth sequence, yet require different numbers of births to return to the remembered target. No controller using only `{W, S, M, its own birth history}` can guarantee exact repair for all such initial states.

That gives a precise requirement for any next information channel: it must distinguish the **remaining-current-amount / deficit classes** that require different actions. Merely duplicating “reporter healthy/broken” is insufficient.

For a finite declared challenge set containing `K` reporter-failed deficit classes that require different exact birth counts, a perfect discrete side channel needs enough capacity to distinguish those `K` classes—at least `ceil(log2 K)` bits in the ordinary noiseless counting sense. Calling an analog quantity “one scalar” is not a minimal-information statement unless its precision/range is also specified.

Several mechanisms would be sufficient in principle, but they answer different questions:

- an independent current-abundance reporter not sharing A's failure mode;
- an exact wound-loss counter that records how many A cells were removed;
- a persistent structural landmark from which current A extent can be read;
- repairing/replacing the broken reporter before using it to close the growth loop.

An exact wound-loss counter is especially important as a control: for one-shot end amputations it can solve the declared problem by adding exactly the recorded number of cells, but that simply moves current-state information into the damage sensor. It should be challenged by unobserved loss, pre-existing composition error, internal damage, or ongoing loss if used in future work.

## Scope

This is a deterministic white-box memory calibration. The memory update rule, wound bits, signal identities, 99% matching tolerance, fate plasticity, and extracellular persistence are authored. It does not show that real tissues store analog setpoints this way, and the retention sweep is not an empirical estimate of biological memory lifetime.

The durable distinctions are:

1. a target setpoint can be **learned from healthy history** rather than hard-coded;
2. that information can persist outside a lineage and support regeneration after the lineage is lost;
3. memory lifetime limits the amount of repair it can support;
4. memory and generative plasticity remain independent requirements;
5. remembering the desired state does not by itself diagnose failure of the sensor reporting the current state;
6. once a reporter is known to be broken, exact current amount is unidentifiable without an additional independent observation or historical deficit record.

Do not add another reporter inside this experiment. The next mechanism should be chosen to test which kind of **independent current-state information** is actually useful, with explicit joint-failure challenges.

## Reproduce

```bash
python3 experiments/11-learned-composition-memory/run.py
python3 -m pytest -q experiments/11-learned-composition-memory/test_model.py
```

Evidence: [`results/characterization.json`](results/characterization.json).
