---
doc-role: historical-plan-or-decision
authority: historical
lifecycle: retained
---
> Historical record. Its next-step language describes the decision at the time,
> not an active assignment. See the [current plan](current_research_plan.md)
> and [evidence index](plan_completion_ledger.md).


# P6-000 phenomenon-first benchmark qualification

**Decision:** select Morpheus model M4377, *Neuromast Regeneration in
Zebrafish*, for one bounded causal calibration. Do not build another generator
or visualizer.

**Survey date:** 2026-08-29  
**Time cap:** 45 minutes  
**Confidence:** tool and benchmark qualification, not a new scientific result

## Decision to unlock

Can a mature, published, off-the-shelf benchmark supply a robust perturbation
and recovery phenomenon, independent experimental layouts, a causal
counterfactual, standard visualization, and headless batch execution quickly
enough to support the next research sprint?

The fixed hard requirements came from the
[current research plan](current_research_plan.md). Platform capability alone
does not count; the candidate must include a concrete qualifying phenomenon.

## Shortlist

| Candidate | Published recovery phenomenon | Independent units | Macro structure | Causal control | Visual + batch | Sprint fit | Decision |
|---|---|---|---|---|---|---|---|
| Morpheus M4377 neuromast regeneration | yes: severe ablation followed by recovery of size, composition, and radial architecture | yes: nine experimental post-ablation tissues and stochastic replicates | yes: cell counts, type proportions, neighborhoods, and radial organization | yes: the local stopping switch is an explicit two-threshold rule; proliferation-off is a direct matched passive control | yes: Morpheus GUI/Gnuplotter and standalone CLI | yes: small static binary, one-file model plus three TIFFs | **select** |
| CompuCell3D V-Cornea | yes: graded corneal injury and recovery | yes: replicated scenarios | yes: layered tissue structure and healing | plausible, but no minimal packaged mechanism-off comparison was identified in the bounded survey | yes: Player plus headless/HPC scripts | weaker: a 229 MB code archive, 6.8 GB result archive, Conda/CC3D environment, and a larger multi-mechanism model | reserve; too much setup and causal surface for the first sprint |
| Artistoo example gallery | no qualifying packaged published regeneration benchmark found | framework supports seeds, but no candidate data design | framework supports fields and browser views | would have to be authored | yes: browser plus Node | excellent platform fit, insufficient phenomenon fit | stop; would recreate the benchmark |

Primary sources:

- [M4377 model record](https://morpheus.gitlab.io/model/m4377/) documents
  90–95% cell loss, experimental image initialization, stochastic division,
  the homotypic-neighbor stopping thresholds, recovery of proportions and
  radial architecture, and the peer-reviewed source.
- [M4377 data and code archive](https://zenodo.org/records/13922477) supplies
  example XML, experimental data, notebooks, 45 with-delay and 45 without-delay
  trajectories across experimental tissue identities, and an MIT license file.
- [Morpheus software structure](https://morpheus.gitlab.io/faq/general/software-structure/)
  documents separate GUI and command-line executables; the
  [2.4.1 release](https://morpheus.gitlab.io/download/2.4.1/) supplies a static
  Linux simulator and command-line random-seed override. Morpheus is BSD-3-Clause.
- [V-Cornea](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013410)
  and its [repository](https://github.com/VaninJoel/vCornea) document the
  published injury scenarios, open code, Player workflow, and headless batch
  scripts.
- The [Artistoo gallery](https://artistoo.net/examples.html) and
  [manual](https://artistoo.net/manual/your-first-simulation.html) document its
  browser and Node execution surfaces, but the gallery contains building-block
  CPM examples rather than a packaged published regeneration-and-control study.

## Qualification checks on the selected candidate

The official inputs were inspected without altering the repository or treating
their published outputs as new evidence.

| Artifact | Identity |
|---|---|
| Morpheus 2.4.1 static Linux simulator | SHA-256 `06a9b44dca3195536907657348e5c6882711f9ce6e60f39af71fef2362e093c7` |
| M4377 repository `model.xml` | SHA-256 `7a75a08c86dad0dee64023568bfbbc7d68b3c361d41ffa0052e140727937e9ca` |
| Zenodo `xml_examples.zip` | SHA-256 `03aae512a6d299593a45db46ae4946867993be3b8144528399cf81e9271417f1` |
| Zenodo with-delay trajectories | 45 CSVs; archive SHA-256 `7fbbad2028387fd4cbc5767f3b596d78857943bc5b1130d6f7919c97da8fa626` |
| Zenodo without-delay trajectories | 45 CSVs; archive SHA-256 `876031c3d6d57a516786907710550ca2dc88a9f0a4e89c0a0a63e8f2edd61975` |

The representative model has a declared random seed, a 65,000-step horizon,
three image-derived cell populations, local neighbor reporters, stochastic
division, an off-the-shelf spatial plot, and a tabular logger. A diagnostic run
on WSL shortened only the horizon to 1,000 steps and disabled Gnuplot; it
finished in 3.49 seconds with the official simulator and seed 801. This is a
runtime/setup check, not experimental evidence. It makes a first full causal
comparison comfortably feasible inside a 90-minute sprint.

## Why this moves the programme

M4377 supplies the combination the earlier standard NetLogo models lacked:

- recovery begins from measured, materially different damaged tissue layouts;
- local stochastic cell behavior reconstructs bounded organ-level composition
  and spatial architecture;
- the proposed control mechanism can be disabled without replacing the rest of
  the generator;
- cell count, composition, neighborhood structure, and spatial organization can
  be kept separate rather than collapsing every outcome to one scalar;
- standard visualization and batch execution are already part of the package.

This does not establish autonomous goals. The local neighbor thresholds are
authored into the published model. It does provide a calibrated multiscale
case on which to ask the programme's actual question: can an observable macro
description predict and causally distinguish successful recovery across held-
out damaged tissues better than count-only or intervention-only alternatives?

## Allocation

Fund one 90-minute P6-001 causal calibration, then stop or promote. Do not port
M4377 into the laboratory, reproduce the paper's entire analysis, download the
143 MB neighborhood archive, or build a custom viewer.

P6-001 must use the unmodified published dynamics for the active condition,
generate only thin logger/control variants, compare active feedback with both
feedback-disabled and proliferation-disabled conditions, and save one decision
surface. A successful calibration licenses a separately frozen held-out
layout prediction; it does not unlock broad causal-emergence tooling by itself.
