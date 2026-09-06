#!/usr/bin/env python3
"""Render `wiki/lattice.html`: a self-contained page that shows the substrate running.

The owner asked for something he could open and see what the project is working
on. The stale Panel dashboard needs a server and a maintained environment; this
needs neither. It is one file, opened with a double click, with no network
access of any kind.

**There is exactly one simulator.** This script imports `src/lattice/` and runs
the real trajectories here, in Python, then embeds the resulting frames as data.
The JavaScript in the page only paints pre-computed frames -- it contains no
rule, no schedule, no fault model and no operation accounting. A second
implementation in the browser would be a correctness hazard: it could drift from
the substrate and show a picture of a system that does not exist. So the page is
generated, never authored, and the revision that generated it is printed on it.

Run it from the project directory so the project environment is active:

    cd goal-discovery && uv run --frozen --all-extras python ../scripts/render_lattice_page.py
"""

from __future__ import annotations

import json
import math
import statistics
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "goal-discovery"))

from src.lattice import observe
from src.lattice.core import Faults, step_synchronous
from src.lattice.specimens import elementary_ca, sorting

OUTPUT = REPO / "wiki" / "lattice.html"

# --- Experiment parameters. Every number the page prints comes from here. -----

N = 24                      # entities in a sorting run
SEED = 1                    # the trajectory that is animated
SORT_STEPS = 800            # interactions driven, per controller
SORT_STRIDE = 8             # interactions per drawn row
FAULT_STEPS = 1200          # the damaged runs need longer, so both get longer
FAULT_STRIDE = 12
FROZEN_IDENT = 5            # the entity that never acts on its own initiative
P_FAIL = 0.3
CA_SIZE = 121               # odd, so a single seed cell has a centre
CA_STEPS = 60               # (CA_SIZE - 1) // 2: the light cone just reaches the ends
CA_RULES = (90, 110, 30)
MEDIAN_SEEDS = range(25)    # seeds behind the cost-of-damage figure
MEDIAN_CAP = 20000          # interactions before a seed is abandoned as unsorted

# A hue sweep at roughly constant lightness, so it survives both a white and a
# near-black background, and so a sorted line reads as one smooth left-to-right
# sweep while a jumbled one reads as speckle. Ordinal data, ordinal ramp.
RAMP = ["#3b5fbf", "#2f8fa8", "#3f9a5f", "#b09030", "#c96a3a", "#b6456b"]


def palette(count: int) -> list[str]:
    """`count` colours interpolated along RAMP, one per entity value."""
    stops = [(int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)) for c in RAMP]
    out = []
    for i in range(count):
        pos = (i / (count - 1)) * (len(stops) - 1) if count > 1 else 0.0
        lo = min(int(pos), len(stops) - 2)
        frac = pos - lo
        rgb = [round(stops[lo][k] + (stops[lo + 1][k] - stops[lo][k]) * frac) for k in range(3)]
        out.append("#{:02x}{:02x}{:02x}".format(*rgb))
    return out


# --- Running the substrate ---------------------------------------------------


def run_sorting(controller: str, steps: int, stride: int,
                faults: Faults | None = None, seed: int = SEED, n: int = N) -> dict:
    """Drive one controller for `steps` interactions, sampling a row every `stride`.

    A controller is a generator, so one `next()` is one interaction. `closed`
    stops on its own; when it does, the recording continues with the frozen
    configuration and the frozen operation count, so every panel in a group
    shares one time axis and can be read across.
    """
    lat, rule = sorting.make(n, seed=seed, faults=faults)
    drive = sorting.CONTROLLERS[controller](lat, rule, MEDIAN_CAP * 10)

    rows = [list(lat.occupants)]
    ops = [lat.ops]
    inv = [observe.inversions(lat)]
    halted_step = None
    sorted_step = None
    sorted_ops = None

    for step in range(1, steps + 1):
        if halted_step is None:
            try:
                next(drive)
            except StopIteration:
                halted_step = step - 1
        if halted_step is None and sorted_step is None and observe.is_sorted(lat):
            sorted_step, sorted_ops = step, lat.ops
        if step % stride == 0:
            rows.append(list(lat.occupants))
            ops.append(lat.ops)
            inv.append(observe.inversions(lat))

    return {
        "rows": rows,
        "ops": ops,
        "inv": inv,
        "haltedStep": halted_step,
        # The FIRST sampled row at or after the event, not the one before it.
        # Floor division put the "fully in order" marker on a row where the
        # line was still out of order -- by up to stride-1 interactions -- and
        # the picture disagreed with the caption drawn across it.
        "haltedRow": None if halted_step is None else math.ceil(halted_step / stride),
        "sortedStep": sorted_step,
        "sortedOps": sorted_ops,
        "sortedRow": None if sorted_step is None else math.ceil(sorted_step / stride),
        "finalOps": lat.ops,
        "stride": stride,
        "steps": steps,
        "cols": lat.size,
    }


def ops_to_sorted(controller: str, seed: int, faults: Faults | None) -> int | None:
    """Operations charged before the line is first fully in order, or None."""
    lat, rule = sorting.make(N, seed=seed, faults=faults)
    drive = sorting.CONTROLLERS[controller](lat, rule, MEDIAN_CAP * 10)
    for _ in range(MEDIAN_CAP):
        try:
            next(drive)
        except StopIteration:
            break
        if observe.is_sorted(lat):
            return lat.ops
    return None


def median_ops(controller: str, faults: Faults | None) -> dict:
    """Median operations-to-sorted over MEDIAN_SEEDS.

    One seed is not evidence about the cost of damage: the fault draws and the
    schedule draws come from the same random stream, so a single damaged trial
    can finish sooner than a single clean one purely by luck. It does, for
    seed 1. The animated run is one trajectory; this is the claim.
    """
    got = [ops_to_sorted(controller, s, faults) for s in MEDIAN_SEEDS]
    finished = [v for v in got if v is not None]
    return {
        "median": None if not finished else int(statistics.median(finished)),
        "finished": len(finished),
        "trials": len(got),
    }


def run_ca(number: int, size: int, steps: int) -> dict:
    """One elementary rule, synchronously, on the same Lattice as sorting."""
    lat, rule = elementary_ca.make(number, size=size)
    rows = ["".join(str(c) for c in lat.occupants)]
    ops = [lat.ops]
    for _ in range(steps):
        step_synchronous(lat, rule)
        rows.append("".join(str(c) for c in lat.occupants))
        ops.append(lat.ops)
    return {"rows": rows, "ops": ops, "cols": lat.size, "opsPerStep": lat.ops // steps}


# --- Provenance --------------------------------------------------------------


def provenance() -> dict:
    def git(*args: str) -> str:
        try:
            return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                                  text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return "unknown"

    revision = git("rev-parse", "--short", "HEAD")
    dirty = bool(git("status", "--porcelain"))
    return {
        "revision": revision,
        "dirty": dirty,
        "generated": datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"),
        "script": "scripts/render_lattice_page.py",
    }


# --- Page text ---------------------------------------------------------------

CONTROLLERS = [
    ("decentralized", "Decentralized",
     ("Nobody is in charge. A neighbouring pair is picked at random, and one of "
      "the two items in it decides whether that pair should swap. It never stops "
      "and never announces that it is finished.")),
    ("watchdog", "Watchdog",
     ("A supervisor walks the line left to right, over and over, checking every "
      "pair before it acts. It is charged for each check, including the ones "
      "that find nothing wrong, so its meter keeps climbing.")),
    ("closed", "Closed loop",
     ("The same supervisor, except it stops once a complete pass finds nothing "
      "to do. Cheapest of the three, and blind afterwards: whatever goes wrong "
      "later happens with nobody watching.")),
]

CA_BLURB = {
    90: "Draws the Sierpinski triangle. Its rows are binomial coefficients "
        "modulo 2 — a result worked out on paper long before this code existed, "
        "which is what makes it usable as a check.",
    110: "Capable, in principle, of running any computation at all, given the "
         "right starting line. From a single filled cell it produces this "
         "drifting, repeatedly interrupted texture.",
    30: "The standard chaotic one. Its left half settles into a repeating "
        "pattern and its right half does not, and a small change to the "
        "starting line changes all of it.",
}


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


HEAD = """<title>Lattice Substrate Viewer</title>
<style>
:root {
  color-scheme: light dark;
  --bg: #fbfaf8;
  --surface: #ffffff;
  --line: #d8d4cc;
  --line-soft: #e8e5de;
  --text: #1c1b19;
  --muted: #5d594f;
  --ink: #15150f;
  --paper: #ffffff;
  --unrun: #e9e6e0;
  --accent: #7a3b1f;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #131417;
    --surface: #191b1f;
    --line: #33363c;
    --line-soft: #26282d;
    --text: #e6e3dd;
    --muted: #a09b91;
    --ink: #eae7e0;
    --paper: #0e0f12;
    --unrun: #2a2d33;
    --accent: #d99a6c;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 15px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}
main { max-width: 1120px; margin: 0 auto; padding: 40px 24px 72px; }
h1 { font-size: 27px; line-height: 1.25; margin: 0 0 6px; font-weight: 620; letter-spacing: -0.01em; }
h2 {
  font-size: 13px; text-transform: uppercase; letter-spacing: 0.09em;
  font-weight: 700; color: var(--muted); margin: 0 0 14px;
  padding-bottom: 8px; border-bottom: 1px solid var(--line);
}
h3 { font-size: 16px; margin: 0 0 4px; font-weight: 620; }
p { margin: 0 0 12px; }
a { color: inherit; }
.prov {
  font: 12px/1.5 var(--mono); color: var(--muted);
  margin: 0 0 34px; padding-bottom: 18px; border-bottom: 1px solid var(--line);
}
section { margin: 0 0 42px; }
.lede { max-width: 68ch; }
.lede p + p { margin-top: 12px; }
.lede strong { font-weight: 640; }
.q {
  border-left: 2px solid var(--accent);
  padding: 2px 0 2px 16px; margin: 18px 0 0; max-width: 68ch;
}
dl.legend { margin: 0; max-width: 78ch; }
dl.legend > div { display: grid; grid-template-columns: 150px 1fr; gap: 4px 20px; padding: 9px 0; border-bottom: 1px solid var(--line-soft); }
dl.legend > div:last-child { border-bottom: 0; }
dt { font-weight: 640; }
dd { margin: 0; color: var(--muted); }
.swatches { display: flex; align-items: center; gap: 0; margin: 6px 0 4px; max-width: 320px; }
.swatches i { display: block; height: 14px; flex: 1 1 0; }
.swatch-ends { display: flex; justify-content: space-between; max-width: 320px; font: 11px var(--mono); color: var(--muted); }
.controls {
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
  margin: 0 0 16px; padding: 10px 12px;
  background: var(--surface); border: 1px solid var(--line); border-radius: 4px;
}
button {
  font: inherit; font-size: 13px; font-weight: 600;
  padding: 5px 14px; min-width: 74px; cursor: pointer;
  background: var(--bg); color: var(--text);
  border: 1px solid var(--line); border-radius: 3px;
}
button:hover { border-color: var(--muted); }
input[type=range] { flex: 1 1 180px; min-width: 140px; accent-color: var(--accent); }
.tstamp { font: 12px var(--mono); color: var(--muted); white-space: nowrap; }
.panels { display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(255px, 1fr)); }
.panels.pair { grid-template-columns: repeat(auto-fit, minmax(255px, 370px)); justify-content: start; }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: 4px; padding: 14px; }
.panel .blurb { font-size: 13px; color: var(--muted); margin: 0 0 12px; min-height: var(--blurb-min, 0); }
.canvas-wrap { background: var(--unrun); border: 1px solid var(--line-soft); width: fit-content; max-width: 100%; }
canvas { display: block; max-width: 100%; height: auto; }
.readout { margin: 11px 0 0; font: 12px/1.7 var(--mono); color: var(--muted); }
.readout b { color: var(--text); font-weight: 600; }
.note { font-size: 12.5px; color: var(--muted); margin: 10px 0 0; max-width: 78ch; }
.note code { font: 12px var(--mono); }
p.caption { font-size: 13px; color: var(--muted); margin: 0 0 16px; max-width: 78ch; }
footer { margin-top: 8px; padding-top: 18px; border-top: 1px solid var(--line); font-size: 12.5px; color: var(--muted); }
footer code { font: 12px var(--mono); }
</style>
"""


def panel_html(pid: str, title: str, blurb: str, readout: str) -> str:
    return (
        f'<div class="panel">'
        f'<h3>{esc(title)}</h3>'
        f'<p class="blurb">{esc(blurb)}</p>'
        f'<div class="canvas-wrap"><canvas id="cv-{pid}"></canvas></div>'
        f'<p class="readout" id="ro-{pid}">{readout}</p>'
        f"</div>"
    )


def controls_html(gid: str, label: str) -> str:
    return (
        f'<div class="controls">'
        f'<button id="pp-{gid}" type="button">Play</button>'
        f'<input type="range" id="sc-{gid}" min="0" value="0" '
        f'aria-label="{esc(label)}">'
        f'<span class="tstamp" id="ts-{gid}"></span>'
        f"</div>"
    )


def build_html(data: dict) -> str:
    prov = data["provenance"]
    ramp = data["sorting"]["palette"]
    swatches = "".join(f'<i style="background:{c}"></i>' for c in ramp)

    sort_panels = "".join(
        panel_html(f"sort-{key}", title, blurb, "&nbsp;")
        for key, title, blurb in CONTROLLERS
    )
    ca_panels = "".join(
        panel_html(f"ca-{n}", f"Rule {n}", CA_BLURB[n], "&nbsp;") for n in CA_RULES
    )
    fault_panels = (
        panel_html("flt-clean", "Undamaged",
                   "Nothing is broken. Every item acts when it is asked to, and "
                   "every attempted action succeeds.",
                   "&nbsp;")
        + panel_html("flt-damaged", "Damaged",
                     f"Three in ten attempted actions fail outright, and item "
                     f"{FROZEN_IDENT} (outlined) never acts on its own initiative.",
                     "&nbsp;")
    )

    clean = data["faults"]["cleanMedian"]
    dmg = data["faults"]["damagedMedian"]
    if clean["median"] and dmg["median"]:
        ratio = dmg["median"] / clean["median"]
        cost_line = (
            f"Across {clean['trials']} different starting shuffles, the undamaged runs "
            f"needed a median of <b>{clean['median']:,} operations</b> to first put the "
            f"line fully in order, and the damaged runs <b>{dmg['median']:,}</b> "
            f"— about {ratio:.1f} times as many for the same result. "
            f"The two pictures below are one of those {clean['trials']} shuffles, "
            f"animated; a single pair of runs is not the measurement, because the "
            f"failures and the schedule are drawn from the same random stream and "
            f"one damaged run can finish sooner than one clean run by luck."
        )
    else:
        cost_line = "Not every trial finished within the cap, so no median is reported."

    sd = data["sorting"]
    fd = data["faults"]
    cd = data["ca"]

    dirty_note = (
        " &middot; working tree had uncommitted changes when this was generated"
        if prov["dirty"] else ""
    )

    return f"""{HEAD}
<main>

<h1>Watching the substrate run</h1>
<p class="prov">Generated {prov['generated']} from revision {prov['revision']} by
{prov['script']}{dirty_note}. Self-contained: no server, no network, no fonts or
scripts from anywhere else. Re-run the script to rebuild it.</p>

<section class="lede">
<h2>What we are working on</h2>
<p>This project is trying to work out, from the outside, what a system is
<strong>for</strong> — what would count as its goal, and how much of what it does
deserves to be called competence rather than coincidence. That is the current
phase: goal and competence discovery.</p>
<p>Everything in the phase now runs on one piece of shared machinery, and this
page is that machinery running. It is a line of positions, each holding at most
one item. Items follow rules that can only ever look at their immediate
neighbours. Nothing anywhere in it knows what the line is supposed to end up
looking like.</p>
<div class="q">
<p>The sorting runs are asking one question. A jumbled line of numbers puts
itself in order. There are two very different stories about that, and they look
identical if you only check the ending. Either the system is in some real sense
<strong>pursuing</strong> order — in which case damaging it should show it
recovering, and it should get there by more than one route — or it is only
rolling downhill into the nearest resting place, the way water finds a drain,
with nothing goal-like about it at all.</p>
<p style="margin-bottom:0">Telling those two apart is the work. The runs below
are the beginning of it: the same task under three different control
arrangements, the same task again with parts of the system broken, and the same
machinery doing something that is not sorting at all.</p>
</div>
</section>

<section>
<h2>How to read these pictures</h2>
<dl class="legend">
<div><dt>One column</dt><dd>One position on the line. The leftmost position is
drawn on the left. There are {sd['cols']} of them in the sorting runs and
{cd['cols']} in the cellular-automaton runs.</dd></div>
<div><dt>One row</dt><dd>The whole line at one moment. The top row is the
starting arrangement.</dd></div>
<div><dt>Downwards</dt><dd>Time. Reading a picture from top to bottom is
watching the line change. The pictures fill in as they play.</dd></div>
<div><dt>Colour</dt><dd>Which item is sitting in that position. Colour follows
the item's number, low to high, along this ramp:
<div class="swatches">{swatches}</div>
<div class="swatch-ends"><span>item 0</span><span>item {sd['cols'] - 1}</span></div>
So a fully sorted line is one smooth left-to-right sweep of colour, and a
jumbled line is speckled. In the cellular-automaton runs there are only two
possible states, drawn filled and empty.</dd></div>
<div><dt>The horizontal line</dt><dd>Drawn across a sorting picture at the first
moment the line was completely in order. Runs continue past it, because most of
these controllers have no way of knowing they have arrived.</dd></div>
<div><dt>An operation</dt><dd>One evaluation of a rule: one moment where the
machinery looks at a small neighbourhood and decides something. Looking costs
the same as acting, so a supervisor that patrols and finds nothing still runs
the meter up. That is deliberate — it is what makes the operation count a
price tag on an arrangement rather than a measure of how fast it is.</dd></div>
<div><dt>Pairs out of order</dt><dd>Also called inversions: how many pairs of
items are the wrong way round anywhere in the line, counting distant pairs too.
It is zero exactly when the line is sorted. No single item could work this
number out from its own neighbourhood; only an outside observer can.</dd></div>
</dl>
</section>

<section>
<h2>Sorting, under three different control arrangements</h2>
<p class="caption">The same {sd['cols']} items, the same starting shuffle, and the same
local rule — swap us if we are the wrong way round. Only the arrangement that
decides who acts next differs. Each row is the line after every
{sd['stride']} interactions; {sd['steps']:,} interactions are shown.</p>
{controls_html('sort', 'Time step for the three sorting runs')}
<div class="panels" style="--blurb-min:8em">{sort_panels}</div>
<p class="note">Watch the operation counters rather than the pictures. All three
arrangements reach the same sorted line. They do not pay the same price for it,
and two of them go on paying after they have arrived.</p>
</section>

<section>
<h2>The same substrate, differently configured</h2>
<p class="caption">These are elementary cellular automata, and they are not a separate
program. They run on the same lattice, the same fault model, the same operation
currency and the same observation rules as the sorting runs above. Three
settings differ: items are no longer conserved (a cell's state is rewritten
rather than moved), the neighbourhood is the three cells centred on a position
rather than an adjacent pair, and every position updates at once instead of one
at a time. That is the whole difference. Each starts from a single filled cell
in the middle of a ring of {cd['cols']} cells; each row is one synchronous
update of the whole ring, costing {cd['opsPerStep']} operations — one for
every cell.</p>
{controls_html('ca', 'Time step for the three cellular-automaton runs')}
<div class="panels" style="--blurb-min:8em">{ca_panels}</div>
<p class="note">The point of this section is negative, and it is the reason the
substrate is worth having: it is not a sorting program with extra options. The
sorting behaviour above is one configuration of a general machine, so a claim
about what the sorting runs are doing has to survive the machine also being
able to do this.</p>
</section>

<section>
<h2>What damage costs</h2>
<p class="caption">{cost_line} Both runs below use the decentralized arrangement — the
one with nobody in charge — with the same starting shuffle. A frozen item
still gets moved when a neighbour is the one that acts, so it is a drag on the
line rather than a wall across it; the outline on it lets you follow where it
ends up. Each row is the line after every {fd['stride']} interactions;
{fd['steps']:,} interactions are shown.</p>
{controls_html('flt', 'Time step for the undamaged and damaged runs')}
<div class="panels pair" style="--blurb-min:4.8em">{fault_panels}</div>
<p class="note">The damaged line still gets there. That is the finding that
makes the opening question sharp rather than rhetorical: recovering from damage
is exactly what you would expect from something pursuing a goal, and it is also
exactly what you would expect from a ball rolling to the bottom of a bowl you
keep nudging. Distinguishing the two needs damage the bowl cannot absorb, and
that is what the phase is building towards.</p>
</section>

<footer>
<p>Every trajectory on this page was computed in Python by
<code>{prov['script']}</code>, which imports <code>goal-discovery/src/lattice/</code>
and runs the real substrate. The JavaScript here only paints frames that were
already computed; it contains no rule, no schedule and no operation accounting,
so there is no second implementation that could disagree with the first.</p>
<p style="margin-bottom:0">Rebuild with
<code>cd goal-discovery &amp;&amp; uv run --frozen --all-extras python ../scripts/render_lattice_page.py</code>.</p>
</footer>

</main>
<script>
const DATA = {json.dumps(data, separators=(",", ":"))};
{PAGE_JS}
</script>
"""


PAGE_JS = r"""
"use strict";

const THEMES = {
  light: { paper: "#ffffff", ink: "#15150f", unrun: "#e9e6e0", mark: "#111111" },
  dark:  { paper: "#0e0f12", ink: "#eae7e0", unrun: "#2a2d33", mark: "#ffffff" }
};
const mq = window.matchMedia("(prefers-color-scheme: dark)");
function theme() { return mq.matches ? THEMES.dark : THEMES.light; }

const N = (v) => v.toLocaleString("en-US");

/* A panel paints pre-computed rows. It decides nothing about the simulation. */
function makePanel(id, spec) {
  const canvas = document.getElementById("cv-" + id);
  const readout = document.getElementById("ro-" + id);
  const cols = spec.cols, rowCount = spec.rows.length;
  const cw = spec.cw, rh = spec.rh, dpr = 2;
  canvas.width = cols * cw * dpr;
  canvas.height = rowCount * rh * dpr;
  canvas.style.width = (cols * cw) + "px";
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
  let painted = -1;

  function cellColour(v) {
    if (spec.kind === "sorting") return spec.palette[v];
    return v === 1 ? theme().ink : theme().paper;
  }

  function paintRow(r) {
    const row = spec.rows[r];
    const y = r * rh;
    for (let c = 0; c < cols; c++) {
      const v = spec.kind === "sorting" ? row[c] : (row.charCodeAt(c) - 48);
      ctx.fillStyle = cellColour(v);
      ctx.fillRect(c * cw, y, cw, rh);
      if (spec.markIdent !== null && spec.kind === "sorting" && v === spec.markIdent) {
        ctx.strokeStyle = theme().mark;
        ctx.lineWidth = 1;
        ctx.strokeRect(c * cw + 0.5, y + 0.5, cw - 1, rh - 1);
      }
    }
    if (r === spec.sortedRow) {
      ctx.fillStyle = theme().mark;
      ctx.fillRect(0, y + rh - 1, cols * cw, 1);
    }
  }

  function draw(t) {
    if (t < painted) {
      ctx.fillStyle = theme().unrun;
      ctx.fillRect(0, 0, cols * cw, rowCount * rh);
      painted = -1;
    }
    for (let r = painted + 1; r <= t; r++) paintRow(r);
    painted = t;
    readout.innerHTML = spec.readout(t);
  }

  function repaint(t) { painted = -1; draw(t); }
  ctx.fillStyle = theme().unrun;
  ctx.fillRect(0, 0, cols * cw, rowCount * rh);
  return { draw, repaint, rowCount };
}

function makeGroup(gid, panels, stepsPerRow, unitLabel) {
  const btn = document.getElementById("pp-" + gid);
  const slider = document.getElementById("sc-" + gid);
  const stamp = document.getElementById("ts-" + gid);
  const last = panels[0].rowCount - 1;
  slider.max = String(last);
  let t = 0, playing = false, timer = null;

  function show(next) {
    t = Math.max(0, Math.min(last, next));
    slider.value = String(t);
    stamp.textContent = unitLabel(t);
    for (const p of panels) p.draw(t);
  }
  function stop() {
    playing = false; btn.textContent = "Play";
    if (timer) { clearInterval(timer); timer = null; }
  }
  function start() {
    if (t >= last) show(0);
    playing = true; btn.textContent = "Pause";
    timer = setInterval(() => {
      if (t >= last) { stop(); return; }
      show(t + 1);
    }, 45);
  }
  btn.addEventListener("click", () => playing ? stop() : start());
  slider.addEventListener("input", () => { stop(); show(Number(slider.value)); });
  mq.addEventListener("change", () => { for (const p of panels) p.repaint(t); });
  show(0);
}

/* --- wire the three groups ------------------------------------------------ */

const sd = DATA.sorting, cd = DATA.ca, fd = DATA.faults;

function sortReadout(run, stride) {
  return (t) => {
    const step = t * stride;
    let extra = "";
    if (run.sortedRow !== null && t >= run.sortedRow) {
      extra += "<br>first fully in order at interaction " + N(run.sortedStep) +
               ", having spent " + N(run.sortedOps) + " operations";
    }
    if (run.haltedRow !== null && t >= run.haltedRow) {
      extra += "<br>stopped itself after " + N(run.haltedStep) +
               " interactions — a full pass found nothing to do";
    }
    return "interactions elapsed: <b>" + N(step) + "</b><br>" +
           "operations charged: <b>" + N(run.ops[t]) + "</b><br>" +
           "pairs out of order: <b>" + N(run.inv[t]) + "</b>" + extra;
  };
}

const sortPanels = sd.panels.map((run) => makePanel("sort-" + run.key, {
  kind: "sorting", rows: run.rows, cols: sd.cols, cw: 13, rh: 5,
  palette: sd.palette, markIdent: null, sortedRow: run.sortedRow,
  readout: sortReadout(run, sd.stride)
}));
makeGroup("sort", sortPanels, sd.stride,
  (t) => "row " + t + " of " + (sd.rowCount - 1) + " — interaction " + N(t * sd.stride));

const caPanels = cd.panels.map((run) => makePanel("ca-" + run.rule, {
  kind: "ca", rows: run.rows, cols: cd.cols, cw: 3, rh: 5,
  palette: null, markIdent: null, sortedRow: null,
  readout: (t) => "synchronous updates: <b>" + N(t) + "</b><br>" +
                  "operations charged: <b>" + N(run.ops[t]) + "</b><br>" +
                  "filled cells now: <b>" +
                  N(run.rows[t].split("1").length - 1) + "</b>"
}));
makeGroup("ca", caPanels, 1,
  (t) => "row " + t + " of " + (cd.rowCount - 1) + " — update " + t);

const faultPanels = fd.panels.map((run) => makePanel("flt-" + run.key, {
  kind: "sorting", rows: run.rows, cols: fd.cols, cw: 13, rh: 5,
  palette: sd.palette, markIdent: run.markIdent, sortedRow: run.sortedRow,
  readout: sortReadout(run, fd.stride)
}));
makeGroup("flt", faultPanels, fd.stride,
  (t) => "row " + t + " of " + (fd.rowCount - 1) + " — interaction " + N(t * fd.stride));
"""


def main() -> int:
    ramp = palette(N)

    sort_runs = []
    for key, _title, _blurb in CONTROLLERS:
        run = run_sorting(key, SORT_STEPS, SORT_STRIDE)
        run["key"] = key
        sort_runs.append(run)

    ca_runs = []
    for number in CA_RULES:
        run = run_ca(number, CA_SIZE, CA_STEPS)
        run["rule"] = number
        ca_runs.append(run)

    damaged = Faults(p_fail=P_FAIL, frozen={FROZEN_IDENT})
    clean_run = run_sorting("decentralized", FAULT_STEPS, FAULT_STRIDE)
    clean_run["key"] = "clean"
    clean_run["markIdent"] = None
    damaged_run = run_sorting("decentralized", FAULT_STEPS, FAULT_STRIDE, faults=damaged)
    damaged_run["key"] = "damaged"
    damaged_run["markIdent"] = FROZEN_IDENT

    data = {
        "provenance": provenance(),
        "sorting": {
            "cols": N,
            "seed": SEED,
            "steps": SORT_STEPS,
            "stride": SORT_STRIDE,
            "rowCount": len(sort_runs[0]["rows"]),
            "palette": ramp,
            "panels": sort_runs,
        },
        "ca": {
            "cols": CA_SIZE,
            "steps": CA_STEPS,
            "rowCount": len(ca_runs[0]["rows"]),
            "opsPerStep": ca_runs[0]["opsPerStep"],
            "panels": ca_runs,
        },
        "faults": {
            "cols": N,
            "steps": FAULT_STEPS,
            "stride": FAULT_STRIDE,
            "rowCount": len(clean_run["rows"]),
            "cleanMedian": median_ops("decentralized", None),
            "damagedMedian": median_ops("decentralized", damaged),
            "panels": [clean_run, damaged_run],
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_html(data), encoding="utf-8")

    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")
    for run in sort_runs:
        print(f"  sorting/{run['key']:<14} rows={len(run['rows']):>4} "
              f"final_ops={run['finalOps']:>6} sorted_at_step={run['sortedStep']} "
              f"halted_at_step={run['haltedStep']}")
    for run in ca_runs:
        print(f"  ca/rule-{run['rule']:<11} rows={len(run['rows']):>4} "
              f"final_ops={run['ops'][-1]:>6} cols={run['cols']}")
    for run in (clean_run, damaged_run):
        print(f"  faults/{run['key']:<15} rows={len(run['rows']):>4} "
              f"final_ops={run['finalOps']:>6} sorted_at_step={run['sortedStep']}")
    print(f"  median ops to sorted: clean={data['faults']['cleanMedian']} "
          f"damaged={data['faults']['damagedMedian']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
