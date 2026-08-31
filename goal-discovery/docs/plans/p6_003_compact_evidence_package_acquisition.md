---
doc-role: historical-plan-or-decision
authority: historical
lifecycle: retained
---
> Historical record. Its next-step language describes the decision at the time,
> not an active assignment. See the [current plan](current_research_plan.md)
> and [evidence index](plan_completion_ledger.md).


# P6-003 compact evidence-package acquisition

**Decision:** no selection. Stop internal simulator search and trajectory
generation. The near-term dependency is an external run-level evidence bundle.

**Survey date:** 2026-08-29

**Time cap:** 60 minutes

**Execution:** metadata, paper, and file-list inspection only; zero candidate
archives downloaded and zero platforms installed

## Decision to unlock

Does a published model package already expose enough compact run-level evidence
to test multiscale recovery representations without first reproducing the
authors' entire simulation study?

Candidates had to clear the frozen
[P6-002 contract](p6_002_archive_first_benchmark_contract.md). In particular,
the package—not an inference from a mean figure—had to identify independent
units, three damage conditions, an observable recovery result, and a matched
mechanism control.

## Frozen shortlist and scorecard

| Candidate | What makes it promising | Decisive contract failure | Decision |
|---|---|---|---|
| CompuCell3D muscle regeneration with microvascular remodeling | published spatial muscle-repair ABM; many cell identities and cytokine fields; 100 replicates for each of eight biological perturbations; 3.5 MB versioned code archive; Player visualization | the published study uses one acute-injury design rather than three damage conditions, does not publish a per-run recovered denominator, and the permanent archive contains code/initialization rather than the 100-replicate run table | no-go before install |
| axonal pathfinding during zebrafish spinal-cord regeneration | plain-text particle snapshots import directly into OVITO; multiple stiffness profiles; spatial neurite trajectories; figure-grouped simulation outputs | 44.2 GB total archive; 26 axons inside a simulation are agents, not independent stochastic/layout units; the study is qualitative path reconstruction rather than a three-damage recovery/control comparison | no-go before download |
| PhysiCell extracellular-matrix framework results | versioned open model and data; fibrosis/wound, collective-migration, and invasion examples; explicit stochastic-replicate archives and standard PhysiCell visual outputs | the examples are different phenomena rather than three damage conditions on one recovery task; no compact recovery/control run table; the general stochastic archive is 971.8 MB and the full deposit 9.3 GB | no-go before download |

Primary artifacts:

- [muscle-regeneration paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11147512/)
  and [versioned model archive](https://zenodo.org/records/10569972)
- [zebrafish axon simulation-data archive](https://zenodo.org/records/20748788)
  and [preprint record](https://doi.org/10.64898/2026.04.17.719187)
- [PhysiCell ECM paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11821717/)
  and [simulation-results archive](https://zenodo.org/records/13770006)

## Candidate-specific findings

### Muscle regeneration

This was the strongest candidate. The model simulates muscle fibers, satellite
stem cells, fibroblasts, immune cells, vessels, seven cytokines, and spatial
coordinates over 28 days. The paper reports 100 replicates for each altered
cell/cytokine/angiogenesis condition and a 300-point sensitivity study run in
triplicate. This is substantially better ensemble practice than the earlier
candidates.

It still does not answer the frozen preflight question. Injury percentage is an
input, but the reported validation varies biological mechanisms around one
acute-injury design. The compact Zenodo release contains 3.5 MB of source and
histology initialization, not the run-level outputs from those replicates. Its
figures show confidence intervals and mean changes rather than a recover/not-
recover row for each unit. Selecting it would therefore require installing
CompuCell3D and creating our own damage ensemble—the work this sprint was meant
to avoid funding on incomplete evidence.

### Axonal pathfinding

This archive is unusually transparent about raw spatial output: each snapshot
is plain text with particle position, type, radius, and identifier, and it can
be viewed in OVITO. But the archive totals 44.2 GB, while even one supplementary
figure bundle is 217.5 MB. The study grows roughly 25–26 axons under stiffness
profiles to qualitatively reproduce observed trajectory shapes. Those axons
share a simulated environment; they do not establish independent recovery
units. No matched mechanism-off recovery denominator is defined.

### PhysiCell ECM framework

The deposit contains raw results and stochastic replicates for fibrosis,
invasive carcinoma, collective migration, and several ECM orientations. This
is good reproducibility practice, but it is a framework demonstration across
different phenomena. It is not one recovery phenomenon tested across three
damage conditions with a matched mechanism control. The stochastic-replicate
bundle alone is 971.8 MB and no compact manifest supplies the missing outcome
table, so the 250 MB selection boundary also fails.

## First-principles conclusion

The off-the-shelf software problem is solved repeatedly: CompuCell3D,
PhysiCell, Morpheus, OVITO, and their standard viewers/batch runners can already
represent the cells, fields, movement, and spatial views we need. The limiting
artifact is the **study-level evidence interface** between published simulators
and downstream systems analysis.

The missing interface has three columns of meaning that papers commonly leave
implicit:

1. which rows are independent units;
2. which observable rule declares recovery or failure;
3. which intervention is the matched causal control and how unbounded runs are
   censored.

Without those, fast code merely generates another bespoke dataset whose
robustness must be purchased from scratch. The rational allocation is therefore
to circulate a concise
[benchmark evidence request](../requests/multiscale_recovery_benchmark_request.md)
and stop internal simulator work until a candidate satisfies it. This is a
genuine dependency boundary, not an invitation to lower the gate or continue
searching indefinitely.
