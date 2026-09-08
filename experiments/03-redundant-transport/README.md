# Experiment 03 — redundant-route compensation

This is a deliberately small **topology-different compensation specimen**. The
repository already contains an older thermostat-family two-actuator compensation
calibration (Experiment 004). Repeating that scalar result would add little. This
experiment asks whether the same distinction is clean in a discrete transport
setting and whether it remains recognizable when the semantics are hidden.

## System

A source receives a fixed number of jobs per tick and has two distinct routes to
a sink. Each route can carry at most **2 jobs/tick**. At tick 20, route A, route
B, both routes, or neither may be disabled. The run lasts 60 ticks.

The external success criterion is **zero accumulated backlog**.

Two policies use identical physical routes and capacities:

- **reroute:** when one route is unavailable, new jobs are reassigned to the
  survivor up to its physical capacity;
- **fixed:** the original equal assignment is retained, so work assigned to a
  disabled route is lost rather than reassigned.

The rerouting rule is authored in advance. This is engineered compensation, not
learning or adaptation.

## Characterization

At the compensable input of **2 jobs/tick**:

| condition | reroute final backlog | fixed final backlog | post-fault survivor flow |
|---|---:|---:|---:|
| no failure | 0 | 0 | 1 + 1 |
| A disabled | **0** | 40 | reroute 2; fixed 1 |
| B disabled | **0** | 40 | reroute 2; fixed 1 |
| both disabled | 80 | 80 | 0 |

So physical redundancy alone is not the result: with the same routes and spare
capacity, the fixed-assignment control fails after either single cut while the
rerouting policy preserves the criterion by shifting all traffic to the survivor.

The result has a hard tested boundary. At **4 jobs/tick**, each intact system can
carry the load, but either single-route cut leaves only 2 jobs/tick of physical
capacity. Both policies then accumulate **80 jobs** of backlog by tick 60. A
policy cannot compensate for capacity that no longer exists.

This white-box result is largely derivable from the declared allocation and
capacity rules. Its value is therefore calibration and cross-system structure,
not surprise.

## Blind compensation check

`blind.py` packages two anonymous systems with three anonymous integer fields,
the known exogenous input, and channel-disable operations. It withholds policy
meaning, field semantics, transport semantics, macro criterion, and implementation.

A separate zero-context reader inferred that one system shows **complete bounded
substitution** at input 2: disabling either channel makes the other observed
channel double while the conserved/accumulating quantity remains at zero. It
correctly distinguished the second system, where the survivor does not increase
and the accumulating quantity grows. At input 4 it identified the shared
single-channel ceiling of 2 and the resulting compensation failure.

The reader also retained important limits: a pre-existing switch rule, feedback,
or passive coupling could all generate the observed substitution; the observed
accumulating field could be derived rather than independently causal; and the
disable operation might have hidden effects. It explicitly found **no evidence
of learning or persistent adaptation** and did not infer a unique goal.

This is a bounded positive Goal Discovery result: compensation/substitution and
its resource boundary are behaviorally recognizable in a system structurally
different from the scalar regulation example. It is not a general compensation
analyzer and not evidence of agency.

## Reproduce

```bash
python3 experiments/03-redundant-transport/run.py
python3 -m pytest -q experiments/03-redundant-transport/test_model.py
python3 experiments/03-redundant-transport/blind.py
```

Evidence:
- [`results/characterization.json`](results/characterization.json)
- [`results/blind_case.json.gz`](results/blind_case.json.gz)
- [`results/blind_manifest.json`](results/blind_manifest.json)
- [`results/blind_reader.md`](results/blind_reader.md)
