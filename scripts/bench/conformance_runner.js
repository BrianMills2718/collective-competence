// Emit trajectories for the configurations named on stdin, as JSON on stdout.
// Driven by `tests/test_bench_matches_python.py`, which compares them to the
// Python substrate's own. This file is a test fixture, not part of the bench.
require("./pyrandom.js");
const S = require("./lattice.js");

let input = "";
process.stdin.on("data", (d) => (input += d));
process.stdin.on("end", () => {
  const cases = JSON.parse(input);
  const out = cases.map((c) => {
    if (c.kind === "sorting") {
      const { lat, rule } = S.makeSorting(c.n, c.seed, c.faults || {}, c.nTypeB || 0);
      const drive = S.controller(c.controller, lat, rule);
      const trace = [];
      for (let step = 0; step < c.steps; step++) {
        if (!drive.step()) break;
        trace.push([lat.ops, lat.occupants.slice()]);
      }
      return trace;
    }
    if (c.kind === "ca") {
      const { lat, rule } = S.makeCA(c.rule, c.size, true, 0);
      const trace = [[lat.ops, lat.occupants.slice()]];
      for (let step = 0; step < c.steps; step++) {
        S.stepSynchronous(lat, rule);
        trace.push([lat.ops, lat.occupants.slice()]);
      }
      return trace;
    }
    throw new Error("unknown case kind: " + c.kind);
  });
  process.stdout.write(JSON.stringify(out));
});
