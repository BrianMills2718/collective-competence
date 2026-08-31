# Reuse survey protocol

**Status:** retained operating protocol; no capability survey is currently
licensed.

Every new scientific capability begins with this protocol. Its purpose is to
move quickly by discovering what already exists, not to turn tool selection into
an open-ended research project.

Time allocation and confidence are governed by
`progress_allocation_protocol.md`. A reuse survey is itself discovery work and
must not consume more time than the capability decision warrants.

## 1. Capability card

Before looking at packages, write five items:

1. the scientific question the capability must answer;
2. the smallest input and output contract;
3. the evidence that would prove the capability useful;
4. the failure conditions that would make us stop;
5. the maximum discovery-spike budget.

If the capability is merely attractive rather than required by a scientific
question, defer it.

## 2. Survey order

Search in this order:

1. tools already installed or already used by the repository;
2. reference implementations attached to relevant papers;
3. mature open-source packages with current official documentation;
4. adapters around established external software;
5. new custom code only after the preceding options fail a named requirement.

Prefer primary sources: official documentation, source repositories, release
history, licenses, and papers. Record version, maintenance recency, license,
data model, extension mechanism, reproducibility support, and the cost of
removal if the choice fails.

## 3. Bounded candidate set

Evaluate at most three serious candidates plus the current baseline. Score only
requirements that affect the active experiment:

- scientific fit;
- time to first useful result;
- compatibility with the trajectory boundary;
- deterministic/reproducible operation;
- scale required by the next two experiments, not hypothetical future scale;
- maintenance and exit cost.

Do not reward generality that the active experiment does not need.

## 4. Thin spike

Use one real existing trajectory and implement the hardest required interaction,
not a generic tutorial. Time-box the spike to one focused work session. A spike
must end with:

- a runnable artifact;
- measured setup and interaction latency;
- missing requirements;
- a keep, fallback, or reject decision.

Delete or isolate spike code that is not adopted.

## 5. Adoption gate

Adopt a tool only if it:

- answers the active scientific question faster than the baseline;
- preserves the black-box/white-box boundary;
- keeps analysis independent of the simulator;
- can regenerate evidence from stored trajectories;
- has a clear path to removal or replacement.

Record the decision and rejected alternatives. Revisit it only when a concrete
requirement fails, not whenever another package looks interesting.

## 6. Rapid learning loop

Each research cycle is:

```text
question
→ reuse survey
→ existing-data discovery spike
→ go/no-go
→ frozen prediction
→ smallest new held-out batch
→ mechanism unlock
→ audit and decide
```

No polished interface, new simulator feature, or generalized framework is built
before the existing-data go/no-go passes.

Record time to first artifact and time to tool decision in the sprint review.
