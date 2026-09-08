# Experiment 04 — route learning across episodes

This is a small **adaptation calibration in a different dynamical setting** from the repository's older thermostat-gain Experiment 005. It keeps one idea from that calibration — retained experience must matter, and frozen/reset controls must remove the advantage — but applies it to repeated allocation between two routes.

## System

Each episode allocates 100 work units between two routes. Route quality is an exogenous property of the current environment. The system starts each run with an equal 50/50 preference. There is **no within-episode feedback**: allocation is fixed for the episode, outcomes are observed, and only then may the next episode's preference change.

The adaptive arm has one persistent variable, the preference for route A. After an episode it updates by the experienced quality difference and clips the preference to `[0.1, 0.9]`. The exact update is authored in advance; this is not open-ended learning or learning-rule discovery.

Two controls isolate retained experience:

- **frozen:** the preference never changes;
- **reset:** the same update is computed, but preference is restored to 0.5 before the next episode.

## White-box characterization

In a stationary environment where either A or B is better, all arms begin at **75 delivered units**. The adaptive arm then improves **75 → 87.5 → 95** and remains there, while frozen and reset stay at **75**.

In reversal histories, the adaptive arm first reaches 95 under the initial environment. When route qualities swap, its retained preference is temporarily wrong: delivery falls to **55**, then recovers **67.5 → 80 → 92.5 → 95** as the preference moves toward the newly better route.

The strongest history test compares two cases with the same current environment. At block 4 with identical `(quality_A, quality_B) = (0.5, 1.0)`, a system previously trained under A-good allocates **90** units to A, while one with B-good history allocates **10**. Current inputs and block number are the same; prior history differs.

This is genuine history-dependent adaptation in the operational sense used here: prior experience changes a persistent variable, which changes later behavior and performance. It is still an engineered learner with a supplied update rule and objective context.

## Blind adaptation check

`blind.py` packages three anonymous arms, two known exogenous inputs per block, and three anonymous outputs. It withholds policy meanings, field/domain semantics, objective, learning rule, and implementation. The two interventions are generically described as holding one component fixed or restoring it before each block.

A separate zero-context reader found that the unmodified arm is inconsistent with a memoryless current-input → output mapping. It used the reversal histories to show that the previously developed asymmetry persists after the environment changes and is gradually replaced. It also identified the decisive same-current-input comparison: identical exogenous inputs at the same block produce different outputs depending on prior history.

The reader concluded that the hold and restore interventions support a causal role for a component that can **change and carry state between blocks**. It explicitly did **not** identify the learning rule, a unique goal, a memory-specific molecular/mechanical implementation, or even semantic action labels for the anonymous fields. Stateful fixed-parameter feedback, hidden initialization, intervention side effects, sparse sampling, and many alternative update laws remain live explanations.

So the bounded result is: **retained history-dependent adaptation is behaviorally recognizable here, and it disappears when change or cross-block persistence is prevented.**

## Mixed contrast stopping check

A final one-off zero-context read placed compact opaque evidence from passive attraction, feedback regulation, compensation and this adaptation case in the same prompt. The reader separated **attraction**, **bounded substitution**, and **history-dependent adaptation** cleanly. It treated the feedback case as a stronger **regulation-like behavioral signature** but correctly refused to claim that behavior alone uniquely proves an active feedback mechanism; a passive system with different restoring dynamics remains a rival unless the causal feedback-path ablations are supplied.

That is the useful stopping result. The calibration cases show distinct behavioral signatures, but they are not four exclusive mechanism labels recoverable from arbitrary trajectories. Rather than tune the toys until every label is inevitable, the programme should now test these distinctions while constructing genuinely new phenomena.

Evidence: [`results/mixed_contrast_reader.md`](results/mixed_contrast_reader.md).

## Reproduce

```bash
python3 experiments/04-route-learning/run.py
python3 -m pytest -q experiments/04-route-learning/test_model.py
python3 experiments/04-route-learning/blind.py
```

Evidence:
- [`results/characterization.json`](results/characterization.json)
- [`results/summary.json`](results/summary.json)
- [`results/blind_case.json.gz`](results/blind_case.json.gz)
- [`results/blind_manifest.json`](results/blind_manifest.json)
- [`results/blind_reader.md`](results/blind_reader.md)
