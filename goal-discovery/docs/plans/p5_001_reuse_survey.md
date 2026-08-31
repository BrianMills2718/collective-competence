---
doc-role: historical-plan-or-decision
authority: historical
lifecycle: retained
---
> Historical record. Its next-step language describes the decision at the time,
> not an active assignment. See the [current plan](current_research_plan.md)
> and [evidence index](plan_completion_ledger.md).


# P5-001 reuse survey — field to network

**Decision: reuse the standard NetLogo model, scikit-image, and NetworkX.**

The installed NetLogo 7.0.4 Models Library supplies the unmodified
`Slime Mold Network.nlogox` generator and its native interactive visualization.
Its SHA-256 is
`93b05eeb698936369e66dd81fba1aaa23ccf21978a5af4b7d081e6dc81ae3e1b`.

The model does not contain explicit links. Its network is a two-dimensional
`cp-fluid` patch field traversed by cytoplasm agents. That makes this an image-
to-graph problem, not a reason to add a graph simulator.

## Adopted components

- [scikit-image global Otsu thresholding](https://scikit-image.org/docs/stable/api/skimage.filters.html)
  supplies a deterministic, off-the-shelf field-to-mask boundary.
- [scikit-image skeletonization](https://scikit-image.org/docs/stable/api/skimage.morphology)
  reduces each connected binary tube region to a one-pixel-wide topology.
- [NetworkX connected components and shortest paths](https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html)
  operate on the eight-neighbor skeleton graph. NetworkX is already a project
  dependency.

The adapter is deliberately removable: one BehaviorSpace setup file exports a
final patch field; one Python module reshapes it, calls the standard algorithms,
and computes frozen metrics.

## Rejected for this sprint

- modifying the NetLogo generator to create links;
- a custom segmentation, skeletonization, or graph library;
- Mesa or another agent framework, which would duplicate the adopted generator;
- deep image embeddings, graph neural networks, or automated threshold tuning;
- a new dashboard—the NetLogo interface is the animation and one static figure
  is the decision surface.

## Replacement boundary

If global Otsu thresholding yields no usable skeleton in at least 80% of frozen
runs, stop P5-001. That failure identifies an observation/segmentation mismatch;
it does not authorize tuning thresholds on the outcomes.
