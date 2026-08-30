# P3-001 standard NetLogo Flocking spike

This spike runs the installed NetLogo 7.0.4 Models Library `Flocking.nlogox`
without changing its generator code. The original model supplies the standard
interactive animation; `behaviorspace.xml` supplies a paired headless baseline
and deterministic heading displacement.

Run from WSL with:

```bash
uv run python -m src.spikes.netlogo_flocking.run
```

The runner uses the Windows NetLogo installation at
`C:\Program Files\NetLogo 7.0.4` or `NETLOGO_HOME`, preserves the raw
BehaviorSpace tables, and creates a normalized trajectory, adoption decision,
and static evidence figure under `results/`.

To see the off-the-shelf live visualization, open **Models Library → Biology →
Flocking** inside NetLogo. The source model is Uri Wilensky's NetLogo Flocking
model (1998), distributed in the Models Library under CC BY-NC-SA 3.0. This
repository stores only the external experiment adapter and records the exact
installed model hash with each run.
