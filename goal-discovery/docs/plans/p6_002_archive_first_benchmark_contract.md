---
doc-role: historical-plan-or-decision
authority: historical
lifecycle: retained
---
> Historical record. Its next-step language describes the decision at the time,
> not an active assignment. See the [current plan](current_research_plan.md)
> and [evidence index](plan_completion_ledger.md).


# P6-002 archive-first benchmark contract

**Decision:** no candidate qualifies. Do not install CompuCell3D, run M9147,
or download either full result archive. The missing product is a compact,
run-level evidence package, not another simulator integration.

**Survey date:** 2026-08-29

**Time cap:** 45 minutes

**Confidence:** archive qualification, not a scientific result

## Decision to unlock

Can a specific published model archive establish, before installation, that its
recovery ensemble and causal counterfactual can support the programme's next
representation-discovery experiment?

P6-001 supplied the correction. A model page can contain many examples and a
convincing recovered image while fresh stochastic units still fail and a
mechanism-off condition becomes computationally unbounded. Therefore platform
features, mean curves, and author claims are not substitutes for run-level
qualification.

## Frozen contract

A candidate had to establish all six items from its paper, manifest, or compact
results. Unknown counts fail the preflight; they are not assumed favorable.

1. At least eight genuinely independent stochastic or layout units spanning at
   least three damage conditions.
2. At least 80% active recovery under a reproducible outcome derived from
   observable logs.
3. A mechanism-disabled control that is bounded at the common endpoint, or a
   published event/time-to-failure endpoint for an unbounded control.
4. Positions, fields, or images supporting a structural macro observable that
   is not total cell count.
5. Exact source identity and license, live visualization, and headless batch
   execution.
6. Enough compact output to produce the first discriminating analysis without
   downloading a multi-gigabyte archive or rerunning the study.

Only two exact archives could be inspected. No platform installation and no
large archive download were allowed.

## Archive scorecard

| Hard requirement | V-Cornea published archive | Morpheus M9147 liver regeneration |
|---|---|---|
| 8 independent units × 3 damage conditions | **not established**: slight, mild, and moderate injury are published with mean ± SD, but the accessible paper/repository does not state a run-level recovery denominator | **fail**: the released reproduction declares one seed and one circular lesion geometry |
| ≥80% active recovery from logs | **not established**: the paper reports complete recovery of slight/mild mean trajectories, not the fraction of independent runs that recover | **not established**: one reproduced lesion-area trajectory is shown |
| usable mechanism-off control | **fail**: module flags exist, but no matched published recovery comparison disables EGF-driven repair or another focal mechanism | **fail**: the original paper's reduced submodels are described, but the M9147 reproduction explicitly does not compare them |
| spatial macro distinct from count | **pass**: stratification, regional thickness, cell positions, and EGF fields | **pass**: lesion area, hepatocyte layers, polarization, and lobule architecture |
| provenance + live + headless | **pass in principle**: a permanent Zenodo version, CompuCell3D Player, and supplied HPC/batch scripts | **pass**: a persistent one-file Morpheus record, standard plots, logger, GUI, and CLI |
| compact first evidence artifact | **fail**: the code archive is about 229 MB and the raw result archive about 6.8 GB; no compact run-level recovery table is surfaced | **partial**: the XML and plotted trajectory are compact, but they contain no qualifying ensemble/control evidence |
| **Decision** | **no-go before install** | **no-go before run** |

## What each candidate does establish

V-Cornea is a substantive off-the-shelf tissue model, not a platform-only
example. The published model has three injury severities, complete closure in
the slight and mild mean cases, recurrent defects after moderate injury,
spatial thickness/stratification measures, a live CompuCell3D Player workflow,
and headless replicate scripts. Those facts make it scientifically interesting.
They do not reveal the run-level recovery rate or supply the matched
mechanism-off contrast required here. Its repository also points to a 6.8 GB
raw-data archive, which defeats the compact preflight condition.

M9147 is much smaller. It reproduces a published 16-day liver-regeneration
trajectory and logs pericentral lesion area while visualizing lobule structure,
cell layers, chemotaxis, adhesion, and oriented division. But the released
Morpheus model fixes `RandomSeed` to zero, uses one lesion geometry, and shows
one reproduced trajectory. More importantly, its page says the original
reduced mechanism models are not compared in the Morpheus implementation. It
therefore cannot establish ensemble robustness or the causal control without us
authoring a new study.

Primary artifacts:

- [V-Cornea paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013410)
- [V-Cornea repository](https://github.com/VaninJoel/vCornea)
- [V-Cornea permanent archive](https://doi.org/10.5281/zenodo.16764319)
- [Morpheus M9147 model record](https://morpheus.gitlab.io/model/m9147/)
- [original liver-regeneration paper](https://doi.org/10.1073/pnas.0909374107)

## Missing benchmark specification

The next benchmark should publish a small manifest plus ordinary tables or
images. A qualifying package needs no custom dashboard and no new simulator
adapter at selection time.

### Required manifest

| Field | Minimum content |
|---|---|
| source | permanent DOI/revision, simulator version, model hash, license |
| unit | one row per seed/layout/organ; repeated time rows retain that unit ID |
| conditions | at least three declared damage conditions plus active and mechanism-off arms |
| endpoint | common fixed endpoint or declared event/time-to-failure rule |
| recovery | observable formula, target/tolerance, and per-unit recovered boolean |
| structure | position/image/field reference and at least one predeclared macro statistic beyond count |
| execution | one live-view command and one headless command |
| files | sizes and hashes for every compact preflight artifact |

### Minimum compact bundle

- `manifest` in CSV, JSON, or YAML;
- a run table with at least 24 active units (8 independent units × 3 damage
  conditions) and the matched control rows;
- either tidy observable trajectories or per-run image/field references;
- one source image/field sample per condition so the structural observable can
  be checked;
- a mechanism intervention declaration and an event censoring field;
- total preflight size at most 250 MB.

The 250 MB cap is an allocation boundary, not a scientific principle. Larger
raw outputs may exist, but selecting the benchmark must not require them.

## Planning correction

The programme has now failed three different candidate lines for three
different evidentiary reasons: weak representation signal, seed-sensitive
phenomenology, and missing run-level archive evidence. More implementation
speed does not repair any of them. The highest-value next sprint is therefore
**evidence-package acquisition**: search for a compact run table that already
satisfies this manifest, then reproduce one row before installing or adapting a
new simulator.

This is not another general framework survey. Search at most three named
published packages, reject on metadata first, and stop if none exposes the
required denominator and control. If that search also fails, publish this
contract as the benchmark request and pause new simulator work; do not silently
lower the scientific bar or manufacture independence from time points.
