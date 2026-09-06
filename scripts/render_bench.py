#!/usr/bin/env python3
"""Render `wiki/bench.html`: an interactive laboratory bench for the substrate.

This script is an ASSEMBLER, not a simulator. It reads `scripts/bench/pyrandom.js`
and `scripts/bench/lattice.js` and inlines them verbatim, adds the bench's own
CSS and UI script, stamps the page with the generating revision, and writes one
self-contained file. It precomputes no trajectory. Every run the page shows is
executed live, in the browser, by the same substrate the laboratory uses.

That is the difference between this page and `wiki/lattice.html`. The older page
renders three fixed experiments: the Python substrate runs them here, the frames
are embedded as data, and the browser only paints. It is a picture of runs
somebody else chose. This page ships the substrate itself, so the configuration
space is the instrument's, not the author's -- the presets are starting points
that the controls can also reach by hand, never special cases.

Two implementations of a simulator is normally a correctness hazard. It is safe
here for the reason `lattice.js` states in its own header: `pyrandom.js`
reproduces CPython's random stream exactly, so the two can be compared for
EQUALITY, and `tests/test_bench_matches_python.py` requires identical
trajectories across a matrix of configurations. Drift is a red test.

Run it from the project directory so the project environment is active:

    cd goal-discovery && uv run --frozen --all-extras python ../scripts/render_bench.py
"""

from __future__ import annotations

import hashlib
import subprocess
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BENCH = REPO / "scripts" / "bench"
OUTPUT = REPO / "wiki" / "bench.html"


# --- Provenance --------------------------------------------------------------


def git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=REPO, capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# --- Page ---------------------------------------------------------------------

CSS = r"""
:root {
  color-scheme: light dark;
  --bg: #fbfaf8;
  --surface: #ffffff;
  --sunk: #f4f2ee;
  --line: #d8d4cc;
  --line-soft: #e8e5de;
  --text: #1c1b19;
  --muted: #5d594f;
  --ink: #15150f;
  --paper: #ffffff;
  --unrun: #e9e6e0;
  --accent: #7a3b1f;
  --warn: #8a2f2f;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #131417;
    --surface: #191b1f;
    --sunk: #101115;
    --line: #33363c;
    --line-soft: #26282d;
    --text: #e6e3dd;
    --muted: #a09b91;
    --ink: #eae7e0;
    --paper: #0e0f12;
    --unrun: #2a2d33;
    --accent: #d99a6c;
    --warn: #e08585;
  }
}
* { box-sizing: border-box; }
[hidden] { display: none !important; }
html, body { max-width: 100%; overflow-x: hidden; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 15px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}
main { max-width: 1280px; margin: 0 auto; padding: 36px 20px 64px; }
h1 { font-size: 26px; line-height: 1.25; margin: 0 0 6px; font-weight: 620; letter-spacing: -0.01em; }
h2 {
  font-size: 12px; text-transform: uppercase; letter-spacing: 0.09em;
  font-weight: 700; color: var(--muted); margin: 0 0 12px;
  padding-bottom: 7px; border-bottom: 1px solid var(--line);
}
h3 { font-size: 15px; margin: 0 0 4px; font-weight: 620; }
p { margin: 0 0 12px; }
a { color: inherit; }
code, .mono { font: 12.5px var(--mono); }
.prov {
  font: 12px/1.5 var(--mono); color: var(--muted);
  margin: 0 0 26px; padding-bottom: 16px; border-bottom: 1px solid var(--line);
  overflow-wrap: anywhere;
}
section { margin: 0 0 34px; }
.lede { max-width: 74ch; }
.lede p + p { margin-top: 12px; }
.lede strong { font-weight: 640; }

/* ---- legend ---- */
dl.legend { margin: 0; display: grid; gap: 0; }
dl.legend > div {
  display: grid; grid-template-columns: 170px minmax(0, 1fr); gap: 3px 20px;
  padding: 9px 0; border-bottom: 1px solid var(--line-soft);
}
dl.legend > div:last-child { border-bottom: 0; }
@media (max-width: 620px) { dl.legend > div { grid-template-columns: minmax(0, 1fr); } }
dt { font-weight: 640; }
dd { margin: 0; color: var(--muted); }
.swatches { display: flex; align-items: center; gap: 0; margin: 4px 0 3px; max-width: 300px; }
.swatches i { display: block; height: 13px; flex: 1 1 0; }
.swatch-ends { display: flex; justify-content: space-between; max-width: 300px; font: 11px var(--mono); color: var(--muted); }

/* ---- bench layout ---- */
.bench { display: grid; grid-template-columns: 336px minmax(0, 1fr); gap: 22px; align-items: start; }
@media (max-width: 960px) {
  .bench { grid-template-columns: minmax(0, 1fr); }
  .arena { order: -1; }
}

.rack { display: grid; gap: 14px; min-width: 0; }
.card {
  background: var(--surface); border: 1px solid var(--line); border-radius: 4px;
  padding: 13px 14px 15px; min-width: 0;
}
.card > h2 { margin-bottom: 10px; }
.hint { font-size: 12px; line-height: 1.5; color: var(--muted); margin: 8px 0 0; }
.hint:first-of-type { margin-top: 0; }

/* ---- controls ---- */
.field { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 2px 10px; align-items: center; margin: 0 0 11px; }
.field:last-child { margin-bottom: 0; }
.field > label { font-size: 12.5px; font-weight: 600; grid-column: 1 / -1; }
.field > .sub { grid-column: 1 / -1; font-size: 11.5px; color: var(--muted); margin: -1px 0 3px; line-height: 1.45; }
.field > input[type=range] { grid-column: 1; width: 100%; min-width: 0; accent-color: var(--accent); }
.field > output { grid-column: 2; font: 12px var(--mono); color: var(--text); min-width: 3.4em; text-align: right; }
.field > select, .field > input[type=number] { grid-column: 1 / -1; width: 100%; min-width: 0; }
.field.row2 > input[type=number] { grid-column: 1; }
select, input[type=number], input[type=text] {
  font: inherit; font-size: 13px; padding: 4px 7px; border-radius: 3px;
  border: 1px solid var(--line); background: var(--bg); color: var(--text);
}
.radios { display: grid; gap: 5px; margin: 0 0 11px; }
.radios label { display: flex; gap: 8px; align-items: flex-start; font-size: 13px; cursor: pointer; }
.radios input { margin: 4px 0 0; accent-color: var(--accent); }
button {
  font: inherit; font-size: 12.5px; font-weight: 600;
  padding: 5px 11px; cursor: pointer; text-align: center;
  background: var(--bg); color: var(--text);
  border: 1px solid var(--line); border-radius: 3px;
}
button:hover:not(:disabled) { border-color: var(--muted); }
button:disabled { opacity: 0.42; cursor: not-allowed; }
button.primary { background: var(--accent); border-color: var(--accent); color: var(--paper); }
@media (prefers-color-scheme: dark) { button.primary { color: #17181c; } }
.btnrow { display: flex; flex-wrap: wrap; gap: 6px; }
.btnrow > button { flex: 1 1 auto; min-width: 0; }
.btngrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(96px, 1fr)); gap: 6px; }
.presets { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 8px; }

/* ---- selection strip ---- */
.selbox {
  font: 12px var(--mono); color: var(--muted); background: var(--sunk);
  border: 1px solid var(--line-soft); border-radius: 3px; padding: 6px 8px; margin: 0 0 9px;
  overflow-wrap: anywhere;
}
.selbox b { color: var(--text); font-weight: 700; }

/* ---- arena ---- */
.arena { display: grid; gap: 14px; min-width: 0; }
.strip-label { font-size: 11.5px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); margin: 0 0 6px; font-weight: 700; }
.currentrow {
  display: flex; gap: 0; width: 100%; min-width: 0;
  background: var(--line-soft); border: 1px solid var(--line); border-radius: 3px; padding: 1px;
}
.cell {
  flex: 1 1 0; min-width: 0; height: 40px; position: relative; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font: 11px var(--mono); color: #fff; border: 0; padding: 0; border-radius: 0;
  appearance: none; -webkit-appearance: none;
  text-shadow: 0 1px 1px rgba(0,0,0,0.45);
}
.cell.narrow { font-size: 0; }
.cell:hover { outline: 2px solid var(--text); outline-offset: -2px; z-index: 3; }
.cell.sel { outline: 3px solid var(--text); outline-offset: -3px; z-index: 4; }
.cell.contrarian::before {
  content: ""; position: absolute; left: 0; right: 0; top: 0; height: 4px;
  background: var(--warn);
}
.cell.frozen {
  background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.75) 0 2px, rgba(255,255,255,0) 2px 5px);
}
.cell.unreliable::after {
  content: ""; position: absolute; left: 12%; right: 12%; bottom: 3px; height: 3px;
  background: repeating-linear-gradient(90deg, #fff 0 2px, transparent 2px 5px);
}
.cell.dead { color: #fff; }
.cell.dead::after {
  content: "\00d7"; position: absolute; inset: 0; display: flex; align-items: center;
  justify-content: center; font-size: 20px; line-height: 1; color: #fff; text-shadow: 0 0 3px #000;
}
.axis { display: flex; justify-content: space-between; font: 11px var(--mono); color: var(--muted); margin: 4px 0 0; }

/* ---- readouts ---- */
.readouts { display: grid; grid-template-columns: repeat(auto-fit, minmax(132px, 1fr)); gap: 1px; background: var(--line-soft); border: 1px solid var(--line); border-radius: 3px; overflow: hidden; }
.ro { background: var(--surface); padding: 9px 11px; min-width: 0; }
.ro .k { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); font-weight: 700; line-height: 1.35; }
.ro .v { font: 19px/1.3 var(--mono); margin-top: 2px; overflow-wrap: anywhere; }
.ro .v.yes { color: var(--accent); }
.ro .n { font-size: 11px; color: var(--muted); line-height: 1.4; margin-top: 1px; }

/* ---- arms ---- */
.arms { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); min-width: 0; }
.arm { border: 1px solid var(--line); border-radius: 4px; background: var(--surface); padding: 11px 12px 12px; min-width: 0; }
.arm.live { border-color: var(--accent); }
.armhead { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; margin: 0 0 3px; }
.armhead .name { font-weight: 700; font-size: 14px; }
.badge { font: 10px var(--mono); text-transform: uppercase; letter-spacing: 0.06em; border: 1px solid var(--line); border-radius: 2px; padding: 1px 5px; color: var(--muted); }
.badge.live { border-color: var(--accent); color: var(--accent); }
.armdesc { font: 11.5px/1.5 var(--mono); color: var(--muted); margin: 0 0 8px; overflow-wrap: anywhere; }
.cvwrap { width: 100%; min-width: 0; background: var(--sunk); border: 1px solid var(--line-soft); border-radius: 2px; }
canvas { display: block; width: 100%; max-width: 100%; }
.armfoot { font: 11.5px/1.6 var(--mono); color: var(--muted); margin: 7px 0 0; overflow-wrap: anywhere; }
.armfoot b { color: var(--text); font-weight: 600; }
.log { margin: 6px 0 0; padding: 0; list-style: none; font: 11.5px/1.55 var(--mono); color: var(--muted); max-height: 120px; overflow-y: auto; }
.log li { padding: 1px 0; overflow-wrap: anywhere; }
.log li::before { content: "\25b8 "; color: var(--accent); }
.log li.empty::before { content: ""; }

.note { font-size: 12.5px; line-height: 1.55; color: var(--muted); margin: 10px 0 0; max-width: 82ch; }
footer { margin-top: 10px; padding-top: 16px; border-top: 1px solid var(--line); font-size: 12.5px; color: var(--muted); }
footer p { max-width: 82ch; }
"""


BENCH_JS = r"""
// The bench. It owns no rule, no schedule and no fault model -- all of that is
// `Substrate`, inlined above from `scripts/bench/lattice.js` and gated by
// `tests/test_bench_matches_python.py` against the Python laboratory. This file
// is a control surface, a recorder and a painter.
(function () {
  "use strict";

  var S = globalThis.Substrate;
  var $ = function (id) { return document.getElementById(id); };

  // ---- palette ------------------------------------------------------------
  // A hue sweep at roughly constant lightness, so a sorted line reads as one
  // smooth left-to-right sweep and a jumbled one reads as speckle, on both a
  // white and a near-black background. Ordinal data, ordinal ramp.
  var RAMP = [[59,95,191],[47,143,168],[63,154,95],[176,144,48],[201,106,58],[182,69,107]];
  function palette(count) {
    var out = [];
    for (var i = 0; i < count; i++) {
      if (count < 2) { out.push("rgb(59,95,191)"); continue; }
      var pos = (i / (count - 1)) * (RAMP.length - 1);
      var lo = Math.min(Math.floor(pos), RAMP.length - 2), f = pos - lo;
      var c = [0,1,2].map(function (k) {
        return Math.round(RAMP[lo][k] + (RAMP[lo + 1][k] - RAMP[lo][k]) * f);
      });
      out.push("rgb(" + c[0] + "," + c[1] + "," + c[2] + ")");
    }
    return out;
  }

  // ---- configuration ------------------------------------------------------
  // Everything a rebuild needs. Nothing is read from anywhere else.
  var lastSystem = null;
  var cfg = {
    system: "sorting",
    n: 24, seed: 1, controller: "decentralized", nTypeB: 0,
    caRule: 110, caSize: 121, caInit: "seed",
    pFail: 0, frozen: [], dead: [], unreliable: {}
  };

  // ---- live state ---------------------------------------------------------
  var lat = null, rule = null, ctrl = null, typeB = new Set(), colors = [];
  var arms = [], active = null, armSeq = 0;
  var running = false, rafId = 0, steps = 0, halted = false, haltNote = "";
  var selected = null;          // sorting: entity identity. CA: site index.
  var snap = null;              // captured state + the recording prefix
  var theme = null;
  var ROWH = 2, DIAG_ROWS = 210, GUTTER = 11, GAP = 9, STRIP = 58;

  function readTheme() {
    var cs = getComputedStyle(document.documentElement);
    var g = function (n) { return cs.getPropertyValue(n).trim(); };
    return {
      ink: g("--ink"), paper: g("--paper"), line: g("--line"),
      lineSoft: g("--line-soft"), accent: g("--accent"), muted: g("--muted"),
      unrun: g("--unrun"), surface: g("--surface"), warn: g("--warn")
    };
  }

  // ---- recording ----------------------------------------------------------
  // An arm is one recorded trajectory. Rows accumulate downward. When the
  // recording outgrows the diagram it is decimated -- every other row is kept
  // and the steps-per-row doubles -- so the WHOLE run always fits and the
  // branch point never scrolls out of sight. The readout prints the current
  // steps-per-row, because a coarsening time axis that does not say so is a lie.
  function newArm(prefix) {
    var a = {
      label: String.fromCharCode(65 + (armSeq++)),
      rows: [], ops: [], met: [], rowStep: 1,
      marks: [], log: [], branchRow: null,
      canvas: null, drawn: 0, dirty: true, desc: describe()
    };
    if (prefix) {
      a.rows = prefix.rows.slice();
      a.ops = prefix.ops.slice();
      a.met = prefix.met.slice();
      a.rowStep = prefix.rowStep;
      a.marks = prefix.marks.map(function (m) { return { row: m.row, label: m.label }; });
      a.log = prefix.log.slice();
      a.branchRow = prefix.rows.length - 1;
    }
    return a;
  }

  function metric() {
    if (cfg.system === "sorting") return S.observe.inversions(lat);
    var n = 0;
    for (var i = 0; i < lat.occupants.length; i++) if (lat.occupants[i]) n++;
    return n;
  }

  function metricMax() {
    if (cfg.system === "sorting") return Math.max(1, (cfg.n * (cfg.n - 1)) / 2);
    return Math.max(1, lat.size);
  }

  function pushRow() {
    var a = active;
    var row = new Uint8Array(lat.size);
    for (var i = 0; i < lat.size; i++) {
      var v = lat.occupants[i];
      row[i] = (v === null || v === undefined) ? 255 : v;
    }
    a.rows.push(row);
    a.ops.push(lat.ops);
    a.met.push(metric());
    if (a.rows.length > DIAG_ROWS) decimate(a);
  }

  function record() {
    if (steps % active.rowStep === 0) pushRow();
  }

  function decimate(a) {
    var keep = function (_, i) { return i % 2 === 0; };
    a.rows = a.rows.filter(keep);
    a.ops = a.ops.filter(keep);
    a.met = a.met.filter(keep);
    a.rowStep *= 2;
    a.marks.forEach(function (m) { m.row = Math.floor(m.row / 2); });
    if (a.branchRow !== null) a.branchRow = Math.floor(a.branchRow / 2);
    a.dirty = true;
  }

  // An intervention is an analyst action, not a substrate step. It records its
  // own row so the change is visible even while paused, and marks the diagram
  // at that row so recovery can be read off the picture.
  function intervene(label) {
    pushRow();
    active.marks.push({ row: active.rows.length - 1, label: label });
    active.log.push("step " + steps + ": " + label);
    active.dirty = true;
    renderAll();
  }

  // ---- building -----------------------------------------------------------
  function describe() {
    if (cfg.system === "sorting") {
      // Per-entity defects belong in this line, not only on the live row. Two
      // arms of a counterfactual are compared by these summaries; one that
      // omitted a frozen entity read as identical to one without it, which is
      // the difference the comparison exists to show.
      var defects = [];
      if (cfg.frozen && cfg.frozen.length) defects.push("frozen=[" + cfg.frozen.join(",") + "]");
      if (cfg.dead && cfg.dead.length) defects.push("dead=[" + cfg.dead.join(",") + "]");
      var degraded = Object.keys(cfg.unreliable || {});
      if (degraded.length) defects.push("unreliable=[" + degraded.join(",") + "]");
      return "sorting  n=" + cfg.n + "  seed=" + cfg.seed + "  " + cfg.controller +
             "  contrarians=" + cfg.nTypeB + "  p_fail=" + cfg.pFail.toFixed(2) +
             (defects.length ? "  " + defects.join("  ") : "  no per-entity defects");
    }
    return "elementary CA  rule=" + cfg.caRule + "  size=" + cfg.caSize +
           "  init=" + (cfg.caInit === "seed" ? "single cell" : "random(seed=" + cfg.seed + ")");
  }

  function faultSpec() {
    return {
      pFail: cfg.pFail,
      frozen: cfg.frozen.slice(),
      dead: cfg.dead.slice(),
      unreliable: Object.assign({}, cfg.unreliable)
    };
  }

  function build() {
    stop();
    steps = 0; halted = false; haltNote = ""; selected = null;
    snap = null; arms = []; armSeq = 0;

    if (cfg.system === "sorting") {
      var made = S.makeSorting(cfg.n, cfg.seed, faultSpec(), cfg.nTypeB);
      lat = made.lat; rule = made.rule;
      typeB = new Set();
      made.preferences.forEach(function (pref, ident) {
        if (pref === S.RULE_DESCEND) typeB.add(ident);
      });
      ctrl = S.controller(cfg.controller, lat, rule);
      colors = palette(cfg.n);
    } else {
      var ca = S.makeCA(cfg.caRule, cfg.caSize, cfg.caInit === "seed", cfg.seed);
      lat = ca.lat; rule = ca.rule; ctrl = null;
      typeB = new Set(); colors = null;
    }
    active = newArm(null);
    arms.push(active);
    pushRow();
    buildCurrentRow();
    renderArms();
    renderAll();
  }

  // ---- the run loop -------------------------------------------------------
  function doStep() {
    if (halted) return false;
    if (cfg.system === "sorting") {
      ctrl.step();
      if (ctrl.halted) {
        halted = true;
        haltNote = "the closed-loop controller has stopped: a full sweep found nothing " +
          "to swap. It cannot restart, so damage injected from here on goes uncorrected. " +
          "Reset to run again.";
      }
    } else {
      S.stepSynchronous(lat, rule);
    }
    steps++;
    record();
    return !halted;
  }

  function frame() {
    if (!running) return;
    var speed = parseInt($("speed").value, 10);
    for (var k = 0; k < speed; k++) if (!doStep()) break;
    renderAll();
    if (halted) { stop(); return; }
    rafId = requestAnimationFrame(frame);
  }

  function play() {
    if (running || halted) return;
    running = true;
    rafId = requestAnimationFrame(frame);
    renderRunButtons();
  }

  function stop() {
    running = false;
    if (rafId) cancelAnimationFrame(rafId);
    rafId = 0;
    renderRunButtons();
  }

  // ---- interventions ------------------------------------------------------
  // Analyst randomness deliberately uses Math.random, NOT `lat.rng`. Drawing
  // from the substrate's stream would advance it, so the counterfactual arms
  // would differ by the draw as well as by the intervention, and the comparison
  // would no longer isolate what was done.
  function pick(n) { return Math.floor(Math.random() * n); }

  function swapRandom() {
    if (lat.size < 2) return;
    var i = pick(lat.size), j = pick(lat.size);
    while (j === i) j = pick(lat.size);
    var t = lat.occupants[i];
    lat.occupants[i] = lat.occupants[j];
    lat.occupants[j] = t;
    intervene("swapped the entities at sites " + i + " and " + j);
  }

  function teleport() {
    if (selected === null) return;
    var from = lat.occupants.indexOf(selected);
    if (from < 0) return;
    var to = pick(lat.size);
    while (to === from && lat.size > 1) to = pick(lat.size);
    var t = lat.occupants[from];
    lat.occupants[from] = lat.occupants[to];
    lat.occupants[to] = t;
    intervene("teleported entity " + selected + " from site " + from + " to site " + to);
  }

  function setFault(kind) {
    if (selected === null) return;
    var f = lat.faults;
    if (kind === "frozen") { f.frozen.add(selected); f.dead.delete(selected); }
    if (kind === "dead") { f.dead.add(selected); f.frozen.delete(selected); }
    if (kind === "unreliable") {
      var p = Math.min(1, Math.max(0, parseFloat($("degp").value) || 0));
      f.unreliable.set(selected, p);
    }
    if (kind === "clear") {
      f.frozen.delete(selected); f.dead.delete(selected); f.unreliable.delete(selected);
    }
    mirrorFaults();
    var words = {
      frozen: "froze entity " + selected + " (it never acts, but can be acted upon)",
      dead: "killed entity " + selected + " (it blocks every interaction touching it)",
      unreliable: "degraded entity " + selected + " to failure probability " + $("degp").value,
      clear: "cleared every defect on entity " + selected
    };
    intervene(words[kind]);
  }

  function clearAllFaults() {
    lat.faults.frozen.clear();
    lat.faults.dead.clear();
    lat.faults.unreliable.clear();
    lat.faults.pFail = 0;
    $("pfail").value = "0";
    cfg.pFail = 0;
    mirrorFaults();
    intervene("cleared every defect on every entity, and set p_fail to 0");
  }

  function flipCell() {
    if (selected === null) return;
    lat.occupants[selected] = lat.occupants[selected] ? 0 : 1;
    intervene("flipped the cell at site " + selected + " to " + lat.occupants[selected]);
  }

  function scramble() {
    var width = Math.min(9, lat.size);
    var at = pick(Math.max(1, lat.size - width));
    for (var k = 0; k < width; k++) lat.occupants[at + k] = pick(2);
    intervene("randomised " + width + " cells starting at site " + at);
  }

  // Keep cfg's fault sets equal to the lattice's, so Reset rebuilds the run
  // with the damage the user has actually inflicted rather than silently
  // undoing it. `Clear all defects` is the way back.
  function mirrorFaults() {
    cfg.frozen = Array.from(lat.faults.frozen);
    cfg.dead = Array.from(lat.faults.dead);
    cfg.unreliable = {};
    lat.faults.unreliable.forEach(function (p, ident) { cfg.unreliable[ident] = p; });
  }

  // ---- snapshot and counterfactual branch ---------------------------------
  function capture() {
    snap = {
      snap: lat.snapshot(),
      steps: steps,
      from: active.label,
      prefix: {
        rows: active.rows.slice(),
        ops: active.ops.slice(),
        met: active.met.slice(),
        rowStep: active.rowStep,
        marks: active.marks.map(function (m) { return { row: m.row, label: m.label }; }),
        log: active.log.slice()
      }
    };
    active.log.push("step " + steps + ": snapshot captured here");
    renderAll();
  }

  function branch() {
    if (!snap) return;
    stop();
    lat.restore(snap.snap);
    steps = snap.steps;
    halted = false; haltNote = "";
    mirrorFaults();
    if (cfg.system === "sorting") ctrl = S.controller(cfg.controller, lat, rule);
    active = newArm(snap.prefix);
    active.log.push("step " + steps + ": branched from arm " + snap.from + "'s snapshot");
    arms.push(active);
    renderArms();
    renderAll();
  }

  function dropBranches() {
    if (arms.length < 2) return;
    arms = [active];
    active.dirty = true;
    renderArms();
    renderAll();
  }

  // ---- the current row (DOM, because it is clickable) ---------------------
  var cells = [];
  function buildCurrentRow() {
    var host = $("currentrow");
    host.textContent = "";
    cells = [];
    for (var i = 0; i < lat.size; i++) {
      var b = document.createElement("button");
      b.className = "cell";
      b.type = "button";
      b.dataset.site = String(i);
      b.addEventListener("click", onCellClick);
      host.appendChild(b);
      cells.push(b);
    }
    $("axis-right").textContent = "site " + (lat.size - 1);
  }

  function onCellClick(ev) {
    var site = parseInt(ev.currentTarget.dataset.site, 10);
    var next = cfg.system === "sorting" ? lat.occupants[site] : site;
    selected = (selected === next) ? null : next;
    renderAll();
  }

  function paintCurrentRow() {
    var narrow = lat.size > 34;
    for (var i = 0; i < cells.length; i++) {
      var v = lat.occupants[i];
      var c = cells[i];
      var cls = "cell" + (narrow ? " narrow" : "");
      if (cfg.system === "sorting") {
        c.style.background = colors[v] || "var(--unrun)";
        c.textContent = String(v);
        if (typeB.has(v)) cls += " contrarian";
        if (lat.faults.frozen.has(v)) cls += " frozen";
        if (lat.faults.dead.has(v)) cls += " dead";
        if (lat.faults.unreliable.has(v)) cls += " unreliable";
        if (selected === v) cls += " sel";
        c.title = "site " + i + " holds entity " + v +
          (typeB.has(v) ? " (contrarian: prefers descending)" : "") +
          (lat.faults.frozen.has(v) ? " (frozen)" : "") +
          (lat.faults.dead.has(v) ? " (dead)" : "") +
          (lat.faults.unreliable.has(v) ? " (unreliable p=" + lat.faults.unreliable.get(v) + ")" : "");
      } else {
        c.style.background = v ? "var(--ink)" : "var(--unrun)";
        c.textContent = "";
        cls += " narrow";
        if (selected === i) cls += " sel";
        c.title = "site " + i + " = " + v;
      }
      c.className = cls;
    }
  }

  // ---- diagrams -----------------------------------------------------------
  function cellColour(v) {
    if (cfg.system === "sorting") return colors[v] || theme.unrun;
    return v ? theme.ink : theme.unrun;
  }

  function drawArm(a) {
    var cv = a.canvas;
    if (!cv) return;
    var W = Math.max(160, Math.floor(cv.parentElement.clientWidth));
    var H = DIAG_ROWS * ROWH;
    var dpr = window.devicePixelRatio || 1;
    var want = Math.round(W * dpr), wantH = Math.round(H * dpr);
    if (cv.width !== want || cv.height !== wantH) {
      cv.width = want; cv.height = wantH;
      cv.style.height = H + "px";
      a.dirty = true;
    }
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    var dW = Math.max(40, W - GUTTER - GAP - STRIP);
    var stripX = GUTTER + dW + GAP;
    var cols = a.rows.length ? a.rows[0].length : 1;
    var mmax = metricMax();

    var from = a.dirty ? 0 : a.drawn;
    if (a.dirty) { ctx.clearRect(0, 0, W, H); }

    for (var r = from; r < a.rows.length; r++) {
      var row = a.rows[r], y = r * ROWH;
      for (var c = 0; c < cols; c++) {
        var x0 = GUTTER + Math.floor((c * dW) / cols);
        var x1 = GUTTER + Math.floor(((c + 1) * dW) / cols);
        ctx.fillStyle = cellColour(row[c]);
        ctx.fillRect(x0, y, Math.max(1, x1 - x0), ROWH);
      }
      // metric strip: same vertical time axis, value grows to the right
      ctx.fillStyle = theme.lineSoft;
      ctx.fillRect(stripX, y, STRIP, ROWH);
      ctx.fillStyle = theme.accent;
      ctx.fillRect(stripX, y, Math.max(1, Math.round((a.met[r] / mmax) * STRIP)), ROWH);
    }
    a.drawn = a.rows.length;

    if (a.dirty) {
      if (a.branchRow !== null) {
        var by = a.branchRow * ROWH;
        ctx.fillStyle = theme.muted;
        for (var x = 0; x < W; x += 6) ctx.fillRect(x, by, 3, 1);
      }
      a.marks.forEach(function (m) {
        var y2 = Math.min(DIAG_ROWS - 1, m.row) * ROWH;
        ctx.fillStyle = theme.warn;
        ctx.fillRect(GUTTER, y2, W - GUTTER, 1);
        ctx.beginPath();
        ctx.moveTo(1, y2 - 3.5); ctx.lineTo(GUTTER - 3, y2 + 0.5); ctx.lineTo(1, y2 + 4.5);
        ctx.closePath(); ctx.fill();
      });
      a.dirty = false;
    }
  }

  function renderArms() {
    var host = $("arms");
    host.textContent = "";
    arms.forEach(function (a) {
      var box = document.createElement("div");
      box.className = "arm" + (a === active ? " live" : "");

      var head = document.createElement("div");
      head.className = "armhead";
      var name = document.createElement("span");
      name.className = "name";
      name.textContent = "Arm " + a.label;
      head.appendChild(name);
      var badge = document.createElement("span");
      badge.className = "badge" + (a === active ? " live" : "");
      badge.textContent = a === active ? "recording" : "held";
      head.appendChild(badge);
      if (a.branchRow !== null) {
        var b2 = document.createElement("span");
        b2.className = "badge";
        b2.textContent = "branched from a snapshot";
        head.appendChild(b2);
      }
      box.appendChild(head);

      var desc = document.createElement("p");
      desc.className = "armdesc";
      desc.textContent = a.desc;
      box.appendChild(desc);

      var wrap = document.createElement("div");
      wrap.className = "cvwrap";
      var cv = document.createElement("canvas");
      cv.setAttribute("role", "img");
      cv.setAttribute("aria-label",
        "Space-time diagram for arm " + a.label + ". Each row is one recorded sample of the " +
        "lattice; time runs downward. The narrow band on the right is the tracked measurement.");
      wrap.appendChild(cv);
      box.appendChild(wrap);
      a.canvas = cv;
      a.dirty = true;
      a.drawn = 0;

      var foot = document.createElement("p");
      foot.className = "armfoot";
      foot.id = "foot-" + a.label;
      box.appendChild(foot);

      var log = document.createElement("ul");
      log.className = "log";
      log.id = "log-" + a.label;
      box.appendChild(log);

      host.appendChild(box);
    });
  }

  function paintArmFooters() {
    arms.forEach(function (a) {
      var foot = document.getElementById("foot-" + a.label);
      if (foot) {
        var lastOps = a.ops.length ? a.ops[a.ops.length - 1] : 0;
        var lastMet = a.met.length ? a.met[a.met.length - 1] : 0;
        foot.textContent = "";
        foot.appendChild(document.createTextNode("rows drawn "));
        var b1 = document.createElement("b"); b1.textContent = String(a.rows.length);
        foot.appendChild(b1);
        foot.appendChild(document.createTextNode(
          "  ·  1 row = " + a.rowStep + " step" + (a.rowStep === 1 ? "" : "s") +
          " (an intervention or a branch also records one)" +
          "  ·  operations charged "));
        var b2 = document.createElement("b"); b2.textContent = String(lastOps);
        foot.appendChild(b2);
        foot.appendChild(document.createTextNode(
          "  ·  " + (cfg.system === "sorting" ? "inversions " : "live cells ")));
        var b3 = document.createElement("b"); b3.textContent = String(lastMet);
        foot.appendChild(b3);
      }
      var log = document.getElementById("log-" + a.label);
      if (log) {
        log.textContent = "";
        if (!a.log.length) {
          var li0 = document.createElement("li");
          li0.className = "empty";
          li0.textContent = "no interventions on this arm";
          log.appendChild(li0);
        } else {
          a.log.forEach(function (line) {
            var li = document.createElement("li");
            li.textContent = line;
            log.appendChild(li);
          });
        }
      }
    });
  }

  // ---- readouts -----------------------------------------------------------
  function setRO(id, value, note, good) {
    var v = $(id);
    v.textContent = value;
    v.className = "v" + (good ? " yes" : "");
    var n = $(id + "-n");
    if (n && note !== undefined) n.textContent = note;
  }

  function renderReadouts() {
    var inv = S.observe.inversions(lat);
    var dis = S.observe.localDisorder(lat);
    setRO("ro-ops", String(lat.ops));
    setRO("ro-steps", String(steps), cfg.system === "sorting"
      ? "one step is one interaction" : "one step is one synchronous sweep");
    setRO("ro-inv", String(inv));
    setRO("ro-dis", String(dis));
    if (cfg.system === "sorting") {
      var ok = inv === 0;
      setRO("ro-goal", ok ? "met" : "not met",
        "ascending order, left to right", ok);
    } else {
      var live = lat.occupants.reduce(function (s, v) { return s + (v ? 1 : 0); }, 0);
      setRO("ro-goal", "none declared",
        live + " of " + lat.size + " cells are 1; no target is declared for this system");
    }
  }

  function renderRunButtons() {
    $("status").textContent = halted ? haltNote
      : (running ? "running" : (steps === 0 ? "built, not yet run" : "paused"));
    $("btn-play").textContent = running ? "Pause" : "Play";
    $("btn-play").disabled = halted;
    $("btn-step").disabled = running || halted;
    $("btn-restore").disabled = !snap;
    $("btn-drop").disabled = arms.length < 2;
    $("btn-snap").disabled = !lat;
    var noSel = selected === null;
    ["btn-teleport", "btn-freeze", "btn-kill", "btn-degrade", "btn-clearsel"].forEach(function (id) {
      var el = $(id); if (el) el.disabled = noSel;
    });
    var f = $("btn-flip"); if (f) f.disabled = noSel;
    var sel = $("selbox");
    if (cfg.system === "sorting") {
      sel.innerHTML = noSel
        ? "No entity selected. Click an entity in the current-state row above to select it."
        : "Selected entity <b>" + selected + "</b>, currently at site <b>" +
          lat.occupants.indexOf(selected) + "</b>.";
    } else {
      sel.innerHTML = noSel
        ? "No cell selected. Click a cell in the current-state row above to select it."
        : "Selected site <b>" + selected + "</b>, currently holding <b>" +
          lat.occupants[selected] + "</b>.";
    }
    $("snapstate").textContent = snap
      ? ("Snapshot held from arm " + snap.from + " at step " + snap.steps +
         ". Restoring returns the occupants, the operation count and the random-number " +
         "generator to exactly that state.")
      : "No snapshot held.";
  }

  function renderAll() {
    if (!theme) theme = readTheme();
    paintCurrentRow();
    renderReadouts();
    renderRunButtons();
    arms.forEach(drawArm);
    paintArmFooters();
  }

  // ---- control wiring -----------------------------------------------------
  function syncControls() {
    document.querySelectorAll("[data-only]").forEach(function (el) {
      el.hidden = el.dataset.only !== cfg.system;
    });
    $("sys-" + (cfg.system === "sorting" ? "sorting" : "ca")).checked = true;
    $("n").value = String(cfg.n); $("n-out").value = String(cfg.n);
    $("seed").value = String(cfg.seed);
    $("controller").value = cfg.controller;
    $("ntb").max = String(cfg.n);
    $("ntb").value = String(cfg.nTypeB); $("ntb-out").value = String(cfg.nTypeB);
    $("carule").value = String(cfg.caRule); $("carule-out").value = String(cfg.caRule);
    $("carule-num").value = String(cfg.caRule);
    $("casize").value = String(cfg.caSize); $("casize-out").value = String(cfg.caSize);
    $("cainit").value = cfg.caInit;
    $("pfail").value = String(cfg.pFail); $("pfail-out").value = cfg.pFail.toFixed(2);
    if (cfg.system !== lastSystem) {
      lastSystem = cfg.system;
      $("speed").value = cfg.system === "sorting" ? "8" : "1";
    }
  }

  function onBuildControl() {
    cfg.system = $("sys-sorting").checked ? "sorting" : "ca";
    cfg.n = parseInt($("n").value, 10);
    cfg.seed = parseInt($("seed").value, 10) || 0;
    cfg.controller = $("controller").value;
    cfg.nTypeB = Math.min(parseInt($("ntb").value, 10), cfg.n);
    cfg.caRule = parseInt($("carule").value, 10);
    var size = parseInt($("casize").value, 10);
    cfg.caSize = size % 2 === 0 ? size + 1 : size;   // odd, so a single seed cell has a centre
    cfg.caInit = $("cainit").value;
    syncControls();
    build();
  }

  function applyPreset(p) {
    Object.keys(p).forEach(function (k) { cfg[k] = p[k]; });
    cfg.frozen = (p.frozen || []).slice();
    cfg.dead = (p.dead || []).slice();
    cfg.unreliable = Object.assign({}, p.unreliable || {});
    cfg.pFail = p.pFail || 0;
    syncControls();
    build();
  }

  var PRESETS = {
    "clean": { system: "sorting", n: 24, seed: 1, controller: "decentralized", nTypeB: 0, pFail: 0 },
    "noisy": { system: "sorting", n: 24, seed: 1, controller: "decentralized", nTypeB: 0, pFail: 0.3, frozen: [5] },
    "closed": { system: "sorting", n: 24, seed: 1, controller: "closed", nTypeB: 0, pFail: 0 },
    "watchdog": { system: "sorting", n: 24, seed: 1, controller: "watchdog", nTypeB: 0, pFail: 0.3 },
    "contrarian": { system: "sorting", n: 24, seed: 1, controller: "decentralized", nTypeB: 4, pFail: 0 },
    "big": { system: "sorting", n: 48, seed: 7, controller: "decentralized", nTypeB: 0, pFail: 0 },
    "ca110": { system: "ca", caRule: 110, caSize: 121, caInit: "seed", seed: 1 },
    "ca30": { system: "ca", caRule: 30, caSize: 121, caInit: "seed", seed: 1 },
    "ca90": { system: "ca", caRule: 90, caSize: 121, caInit: "seed", seed: 1 },
    "ca110r": { system: "ca", caRule: 110, caSize: 121, caInit: "random", seed: 3 }
  };

  function wire() {
    ["sys-sorting", "sys-ca", "n", "seed", "controller", "ntb", "casize", "cainit"]
      .forEach(function (id) { $(id).addEventListener("change", onBuildControl); });
    $("n").addEventListener("input", function () { $("n-out").value = this.value; $("ntb").max = this.value; });
    $("ntb").addEventListener("input", function () { $("ntb-out").value = this.value; });
    $("casize").addEventListener("input", function () { $("casize-out").value = this.value; });

    $("carule").addEventListener("input", function () {
      $("carule-out").value = this.value; $("carule-num").value = this.value;
    });
    $("carule").addEventListener("change", onBuildControl);
    $("carule-num").addEventListener("change", function () {
      var v = Math.min(255, Math.max(0, parseInt(this.value, 10) || 0));
      $("carule").value = String(v); onBuildControl();
    });

    // Faults are live: they belong to the lattice, not to the build.
    $("pfail").addEventListener("input", function () {
      cfg.pFail = parseFloat(this.value);
      $("pfail-out").value = cfg.pFail.toFixed(2);
      if (lat) lat.faults.pFail = cfg.pFail;
      renderAll();
    });

    $("btn-play").addEventListener("click", function () { running ? stop() : play(); });
    $("btn-step").addEventListener("click", function () { doStep(); renderAll(); });
    $("btn-reset").addEventListener("click", build);

    $("btn-swap").addEventListener("click", swapRandom);
    $("btn-teleport").addEventListener("click", teleport);
    $("btn-freeze").addEventListener("click", function () { setFault("frozen"); });
    $("btn-kill").addEventListener("click", function () { setFault("dead"); });
    $("btn-degrade").addEventListener("click", function () { setFault("unreliable"); });
    $("btn-clearsel").addEventListener("click", function () { setFault("clear"); });
    $("btn-clearfaults").addEventListener("click", clearAllFaults);
    $("btn-flip").addEventListener("click", flipCell);
    $("btn-scramble").addEventListener("click", scramble);

    $("btn-snap").addEventListener("click", capture);
    $("btn-restore").addEventListener("click", branch);
    $("btn-drop").addEventListener("click", dropBranches);

    document.querySelectorAll("[data-preset]").forEach(function (b) {
      b.addEventListener("click", function () { applyPreset(PRESETS[b.dataset.preset]); });
    });

    var resizeTimer = 0;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        arms.forEach(function (a) { a.dirty = true; });
        renderAll();
      }, 120);
    });

    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onTheme = function () {
      theme = readTheme();
      arms.forEach(function (a) { a.dirty = true; });
      renderAll();
    };
    if (mq.addEventListener) mq.addEventListener("change", onTheme);
    else if (mq.addListener) mq.addListener(onTheme);
  }

  // A deliberate hook for headless verification: it exposes what the page is
  // actually holding, so a test can assert on the substrate rather than on
  // scraped text. It reads state and never mutates it.
  globalThis.__bench = {
    state: function () {
      return {
        system: cfg.system,
        occupants: lat ? lat.occupants.slice() : null,
        ops: lat ? lat.ops : null,
        steps: steps, running: running, halted: halted,
        arms: arms.length, activeRows: active ? active.rows.length : 0,
        activeMarks: active ? active.marks.length : 0,
        rowStep: active ? active.rowStep : null,
        hasSnapshot: !!snap,
        inversions: lat ? S.observe.inversions(lat) : null,
        frozen: lat ? Array.from(lat.faults.frozen) : null,
        dead: lat ? Array.from(lat.faults.dead) : null,
        pFail: lat ? lat.faults.pFail : null
      };
    }
  };

  theme = readTheme();
  wire();
  syncControls();
  build();
})();
"""


def build_html(pyrandom_js: str, lattice_js: str, prov: dict) -> str:
    head = (
        # Without the charset declaration a browser opening this from disk
        # falls back to a legacy encoding and every UTF-8 character in the
        # page renders as mojibake. Found by reading the rendered page;
        # `TheGeneratedPagesDeclareTheirEncoding` now guards it.
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Substrate Bench</title>\n<style>" + CSS + "</style>\n"
    )

    prov_line = (
        f"generated {prov['generated']} &middot; revision <code>{prov['revision']}</code>"
        f"{' (working tree had uncommitted changes)' if prov['dirty'] else ''}"
        f" &middot; assembled by <code>scripts/render_bench.py</code>"
        f" &middot; substrate <code>scripts/bench/lattice.js</code> sha256:{prov['lattice']}"
        f" &middot; rng <code>scripts/bench/pyrandom.js</code> sha256:{prov['pyrandom']}"
    )

    lede = """
<section class="lede">
<p><strong>What you are looking at.</strong> A <em>lattice</em> is a line of sites. Each site
is empty or holds one <em>entity</em>. An entity carries an identity, a rule it follows, and
any defects it has; when it moves, all three move with it. Nothing in the lattice knows what
the system is for. There is no goal variable, no target, no fitness, no plan &mdash; only
entities, their local rules, and a schedule saying who acts next.</p>

<p><strong>Why that matters.</strong> Order can still appear. Run the sorting system and the
line arranges itself into ascending order, even though no entity can see the line and nothing
is coordinating them. Everything you might call the system's <em>purpose</em> is something
<em>you</em> impose from outside, by measuring. That is the whole point of this laboratory:
if a goal were stored inside the machine, discovering it would be reading a label rather than
doing science.</p>

<p><strong>What the bench is for.</strong> Configure a system, run it, damage it while it
runs, and watch what happens next. Then do the scientifically hard thing: take a snapshot,
run one way, restore, run a <em>different</em> way, and compare the two arms that started from
the identical state. Two runs from states that merely <em>look</em> similar differ by noise as
well as by what you did; two runs from the same snapshot differ only by what you did.</p>
</section>
"""

    legend = """
<section>
<h2>Legend &mdash; what everything on this page means</h2>
<dl class="legend">
  <div><dt>A row</dt><dd>One recorded sample of the whole lattice: the contents of every
    site at one moment. The current-state row at the top of the bench is the live one, drawn
    large; the space-time diagram below is a stack of past rows.</dd></div>
  <div><dt>A column</dt><dd>One <em>site</em> &mdash; a fixed position on the line. Site 0 is
    at the left. Entities move between sites; sites do not move.</dd></div>
  <div><dt>Downward</dt><dd>Time. The diagram grows downward as the run proceeds. When the
    recording outgrows the diagram, every other row is dropped and the number of steps each
    row represents doubles, so the whole run always stays in view. Each diagram prints its
    current steps-per-row underneath.</dd></div>
  <div><dt>Colour (sorting)</dt><dd>The entity's identity, which is also its sort value. Low
    values are blue, high values are magenta:
    <span class="swatches" id="ramp"></span>
    <span class="swatch-ends"><span>lowest value</span><span>highest value</span></span>
    A fully sorted line is one smooth left-to-right sweep. A jumbled one is speckle.</dd></div>
  <div><dt>Colour (cellular automaton)</dt><dd>Cell state only: dark is 1, pale is 0. Cells
    here never move, which is the special case a classic cellular automaton occupies inside
    this more general substrate.</dd></div>
  <div><dt>An operation</dt><dd>One rule evaluation, charged to the system that asked for it.
    <em>Looking costs the same as acting</em>: a coordinator that scans the line without
    changing anything still pays for every site it reads. This is the single currency that
    makes &ldquo;robustness is bought, not free&rdquo; a measurement rather than an opinion.</dd></div>
  <div><dt>Inversions</dt><dd>The number of pairs of entities anywhere on the line that are in
    the wrong order relative to each other. Zero means fully sorted.</dd></div>
  <div><dt>Local disorder</dt><dd>The number of <em>adjacent</em> pairs in the wrong order.
    This is what a purely local observer could count; it can reach zero only when inversions do.</dd></div>
  <div><dt>The narrow band beside each diagram</dt><dd>The tracked measurement over the same
    downward time axis, growing rightward: inversions for sorting, live-cell count for the
    cellular automaton. A wide band is a disordered line.</dd></div>
  <div><dt>Red horizontal line, red arrow</dt><dd>An intervention you injected, drawn at the
    row where it happened, so recovery afterwards is visible as a shape rather than a claim.</dd></div>
  <div><dt>Grey dashed line</dt><dd>The row a counterfactual arm branched from. Everything
    above it is shared history, copied from the parent arm; everything below it is this arm's
    own.</dd></div>
  <div><dt>Red bar across an entity</dt><dd>A <em>contrarian</em>: an entity running the
    opposite rule. Ordinary entities want the larger of a pair on the right; contrarians want
    it on the left.</dd></div>
  <div><dt>Hatching / &times; / dotted underline</dt><dd>Defects. Hatched is <em>frozen</em>
    (never acts on its own initiative, but can still be acted upon). Crossed out is
    <em>dead</em> (blocks any interaction touching it, including one it did not start).
    Dotted underline is <em>unreliable</em> (acts, but fails with a set probability).</dd></div>
</dl>
</section>
"""

    controls = """
<aside class="rack">

  <div class="card">
    <h2>Presets</h2>
    <p class="hint">Starting points, not special cases: every one of these is a setting the
    controls below can also reach by hand.</p>
    <div class="presets">
      <button type="button" data-preset="clean">Sorting, undamaged</button>
      <button type="button" data-preset="noisy">Sorting under noise and a frozen entity</button>
      <button type="button" data-preset="closed">Closed-loop coordinator</button>
      <button type="button" data-preset="watchdog">Watchdog under noise</button>
      <button type="button" data-preset="contrarian">Four contrarians</button>
      <button type="button" data-preset="big">48 entities</button>
      <button type="button" data-preset="ca110">Rule 110</button>
      <button type="button" data-preset="ca30">Rule 30</button>
      <button type="button" data-preset="ca90">Rule 90</button>
      <button type="button" data-preset="ca110r">Rule 110, random start</button>
    </div>
  </div>

  <div class="card">
    <h2>System</h2>
    <div class="radios">
      <label><input type="radio" name="system" id="sys-sorting" value="sorting" checked>
        <span><b>Sorting.</b> Entities carry a value and move. One neighbouring pair
        interacts at a time.</span></label>
      <label><input type="radio" name="system" id="sys-ca" value="ca">
        <span><b>Elementary cellular automaton.</b> Cells hold 0 or 1 and never move. The
        whole row updates at once.</span></label>
    </div>
    <div class="field">
      <label for="seed">Seed &mdash; fixes the starting arrangement and every random draw</label>
      <input type="number" id="seed" min="0" max="999999" step="1" value="1">
    </div>
    <p class="hint">Changing anything in this card or the next rebuilds the run from step 0.</p>
  </div>

  <div class="card" data-only="sorting">
    <h2>Sorting configuration</h2>
    <div class="field">
      <label for="n">Lattice size &mdash; how many entities are on the line</label>
      <input type="range" id="n" min="8" max="64" step="1" value="24">
      <output id="n-out">24</output>
    </div>
    <div class="field">
      <label for="controller">Controller &mdash; who decides which pair acts next</label>
      <select id="controller">
        <option value="decentralized">Decentralized &mdash; a random pair, nobody in charge</option>
        <option value="watchdog">Watchdog &mdash; sweeps the line forever, never stops</option>
        <option value="closed">Closed &mdash; sweeps, and stops when a pass finds nothing</option>
      </select>
      <p class="sub">The sweeping controllers pay an operation for every site they look at,
      whether or not they act on it.</p>
    </div>
    <div class="field">
      <label for="ntb">Contrarian entities &mdash; how many run the opposite rule</label>
      <input type="range" id="ntb" min="0" max="64" step="1" value="0">
      <output id="ntb-out">0</output>
    </div>
  </div>

  <div class="card" data-only="ca">
    <h2>Cellular automaton configuration</h2>
    <div class="field row2">
      <label for="carule">Rule number &mdash; the 8-entry lookup table, 0 to 255</label>
      <input type="range" id="carule" min="0" max="255" step="1" value="110">
      <output id="carule-out">110</output>
      <input type="number" id="carule-num" min="0" max="255" step="1" value="110">
    </div>
    <div class="field">
      <label for="casize">Row size &mdash; how many cells (forced odd, so a single seed cell has a centre)</label>
      <input type="range" id="casize" min="21" max="301" step="2" value="121">
      <output id="casize-out">121</output>
    </div>
    <div class="field">
      <label for="cainit">Initial row</label>
      <select id="cainit">
        <option value="seed">One live cell in the middle</option>
        <option value="random">Random cells, from the seed below</option>
      </select>
    </div>
  </div>

  <div class="card">
    <h2>Run</h2>
    <div class="btnrow">
      <button type="button" id="btn-play" class="primary">Play</button>
      <button type="button" id="btn-step">Single step</button>
      <button type="button" id="btn-reset">Reset</button>
    </div>
    <p class="hint">Reset rebuilds from the current configuration, including any defects you
    have inflicted. <b>Clear all defects</b> below is the way back to an undamaged run.</p>
    <div class="field" style="margin-top:11px">
      <label for="speed">Speed &mdash; substrate steps per animation frame</label>
      <select id="speed">
        <option value="1">1</option><option value="2">2</option><option value="4">4</option>
        <option value="8" selected>8</option><option value="16">16</option>
        <option value="32">32</option><option value="64">64</option><option value="128">128</option>
      </select>
    </div>
  </div>

  <div class="card" data-only="sorting">
    <h2>Faults &mdash; applied live</h2>
    <div class="field">
      <label for="pfail">p_fail &mdash; probability any action silently fails</label>
      <input type="range" id="pfail" min="0" max="1" step="0.01" value="0">
      <output id="pfail-out">0.00</output>
      <p class="sub">Population-wide. A per-entity value set below overrides it for that entity.</p>
    </div>
    <div class="selbox" id="selbox">No entity selected.</div>
    <div class="btngrid">
      <button type="button" id="btn-freeze">Freeze</button>
      <button type="button" id="btn-kill">Kill</button>
      <button type="button" id="btn-degrade">Degrade</button>
      <button type="button" id="btn-clearsel">Clear defects</button>
    </div>
    <div class="field" style="margin-top:9px">
      <label for="degp">Failure probability used by <b>Degrade</b></label>
      <input type="number" id="degp" min="0" max="1" step="0.05" value="0.5">
    </div>
    <div class="btnrow" style="margin-top:9px">
      <button type="button" id="btn-clearfaults">Clear all defects everywhere</button>
    </div>
  </div>

  <div class="card">
    <h2>Intervene</h2>
    <p class="hint">Damage you inject from outside, while it runs or while paused. Each one is
    logged and drawn on the diagram at the row where it happened. Interventions are analyst
    actions, so they are not charged as operations, and they draw their randomness from a
    stream separate from the substrate's &mdash; otherwise the counterfactual arms would
    differ by the draw as well as by what you did.</p>
    <div class="btngrid" data-only="sorting" style="margin-top:9px">
      <button type="button" id="btn-swap">Swap two random entities</button>
      <button type="button" id="btn-teleport">Teleport selected entity</button>
    </div>
    <div class="btngrid" data-only="ca" style="margin-top:9px">
      <button type="button" id="btn-flip">Flip selected cell</button>
      <button type="button" id="btn-scramble">Randomise a 9-cell block</button>
    </div>
  </div>

  <div class="card">
    <h2>Counterfactual branch</h2>
    <p class="hint"><b>Why this exists.</b> If you damage one run and compare it with another
    run that merely started out looking similar, the difference you measure is mostly noise.
    A snapshot captures the occupants, the operation count <em>and</em> the state of the
    random-number generator, so a restored run is the same run &mdash; and the only difference
    between two arms is what you did after the branch.</p>
    <div class="btnrow" style="margin-top:10px">
      <button type="button" id="btn-snap">Capture snapshot</button>
      <button type="button" id="btn-restore">Restore and branch</button>
    </div>
    <div class="selbox" id="snapstate" style="margin:9px 0 0">No snapshot held.</div>
    <div class="btnrow" style="margin-top:9px">
      <button type="button" id="btn-drop">Discard held arms</button>
    </div>
    <p class="hint"><b>One honest limit.</b> The snapshot is the lattice's state, and the
    sweeping controllers (<em>watchdog</em> and <em>closed</em>) keep their pass position
    outside it. Restoring puts those back at site 0 rather than mid-sweep. The
    <em>decentralized</em> controller holds no state at all, so its branches are exact.</p>
  </div>

</aside>
"""

    arena = """
<div class="arena">

  <div class="card">
    <p class="strip-label">Current state &mdash; every site right now, click to select</p>
    <div class="currentrow" id="currentrow"></div>
    <div class="axis"><span>site 0</span><span id="axis-right">site</span></div>
  </div>

  <div class="readouts">
    <div class="ro"><div class="k">Operations charged</div><div class="v" id="ro-ops">0</div>
      <div class="n">rule evaluations billed to the system, reads included</div></div>
    <div class="ro"><div class="k">Steps taken</div><div class="v" id="ro-steps">0</div>
      <div class="n" id="ro-steps-n">one step is one interaction</div></div>
    <div class="ro"><div class="k">Inversions</div><div class="v" id="ro-inv">0</div>
      <div class="n">pairs anywhere on the line in the wrong order</div></div>
    <div class="ro"><div class="k">Local disorder</div><div class="v" id="ro-dis">0</div>
      <div class="n">adjacent pairs in the wrong order</div></div>
    <div class="ro"><div class="k">Analyst's declared target</div><div class="v" id="ro-goal">&mdash;</div>
      <div class="n" id="ro-goal-n">imposed from outside; the system holds no goal</div></div>
    <div class="ro"><div class="k">Run status</div><div class="v mono" id="status" style="font-size:14px">idle</div>
      <div class="n">what the loop is doing right now</div></div>
  </div>

  <div id="arms" class="arms"></div>

</div>
"""

    footer = """
<footer>
<p>Self-contained and offline. The whole substrate &mdash; rules, schedules, fault model and
operation accounting &mdash; is inlined in this file from
<code>scripts/bench/lattice.js</code>, which is a line-for-line mirror of the laboratory's
Python in <code>goal-discovery/src/lattice/core.py</code>. Nothing here is precomputed:
<code>scripts/render_bench.py</code> only assembles the page, and every run you see executes
in your browser when you press Play. The two implementations are held to <em>identical</em>
trajectories, not merely similar ones, by <code>tests/test_bench_matches_python.py</code>,
which is possible because <code>scripts/bench/pyrandom.js</code> reproduces CPython's random
number stream exactly.</p>
<p>Convergence, prediction, low disorder and an attractive picture do not establish that a
system has a goal. This page lets you watch, measure and interfere; the interpretation is
still yours to argue for.</p>
</footer>
"""

    ramp_script = """
<script>
(function(){
  var RAMP=[[59,95,191],[47,143,168],[63,154,95],[176,144,48],[201,106,58],[182,69,107]];
  var host=document.getElementById("ramp");
  for(var i=0;i<24;i++){
    var pos=(i/23)*(RAMP.length-1), lo=Math.min(Math.floor(pos),RAMP.length-2), f=pos-lo;
    var c=[0,1,2].map(function(k){return Math.round(RAMP[lo][k]+(RAMP[lo+1][k]-RAMP[lo][k])*f);});
    var s=document.createElement("i");
    s.style.background="rgb("+c[0]+","+c[1]+","+c[2]+")";
    host.appendChild(s);
  }
})();
</script>
"""

    return (
        head
        + "<main>\n"
        + "<header><h1>Substrate bench</h1>\n"
        + f'<p class="prov">{prov_line}</p></header>\n'
        + lede
        + legend
        + ramp_script
        + '<div class="bench">\n'
        + controls
        + arena
        + "</div>\n"
        + footer
        + "</main>\n"
        + "<script>\n" + pyrandom_js + "\n</script>\n"
        + "<script>\n" + lattice_js + "\n</script>\n"
        + "<script>\n" + BENCH_JS + "\n</script>\n"
    )


def main() -> int:
    pyrandom_js = (BENCH / "pyrandom.js").read_text(encoding="utf-8")
    lattice_js = (BENCH / "lattice.js").read_text(encoding="utf-8")

    for name, text in (("pyrandom.js", pyrandom_js), ("lattice.js", lattice_js)):
        if "</script" in text.lower():
            raise SystemExit(
                f"{name} contains a literal </script>, which would end the inlined block "
                f"early and silently truncate the substrate. Refusing to assemble."
            )

    prov = {
        "revision": git("rev-parse", "--short", "HEAD"),
        "dirty": bool(git("status", "--porcelain")),
        "generated": datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"),
        "lattice": digest(lattice_js),
        "pyrandom": digest(pyrandom_js),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_html(pyrandom_js, lattice_js, prov), encoding="utf-8")

    size = OUTPUT.stat().st_size
    print(f"wrote {OUTPUT} ({size:,} bytes)")
    print(f"  revision      {prov['revision']}{' (dirty)' if prov['dirty'] else ''}")
    print(f"  generated     {prov['generated']}")
    print(f"  inlined       pyrandom.js sha256:{prov['pyrandom']} ({len(pyrandom_js):,} bytes)")
    print(f"  inlined       lattice.js  sha256:{prov['lattice']} ({len(lattice_js):,} bytes)")
    print("  precomputed   nothing; every trajectory is run in the browser")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
