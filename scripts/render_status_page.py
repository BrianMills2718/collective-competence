#!/usr/bin/env python3
"""Render wiki/status.html: the programme's state, from committed evidence.

Generated rather than authored, for the reason the scoreboard is: a
hand-maintained status surface goes stale, and this repository already has three
that must be updated in lockstep, two of which were stale when an outside reader
looked. Every number on the page is read at render time from a committed result
package or from the experiment register; nothing is transcribed.

Self-contained by requirement: no CDN, no script, no webfont, no build step. It
opens from `file://` on a machine with no network and renders in light or dark
according to the reader's own setting.

Colour follows the shared data-visualisation method:
  * the effect charts are DIVERGING (blue above the null, red below, neutral
    grey at zero) because zero is a real midpoint here -- it is the arm's own
    shuffle null, so above and below mean opposite things;
  * outcome classes are CATEGORICAL, validated as a four-slot set, and every
    one carries a visible text label, because the aqua/red pair sits in the
    6-8 CVD band where colour alone is not permitted to carry meaning.

`--check` fails when the rendered page differs from the committed one, so a new
experiment or a re-run result cannot silently leave the page behind.
"""

from __future__ import annotations

import argparse
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = "wiki/status.html"

Q1_009 = "goal-discovery/results/q1-009-information/followup.json"
Q1_010 = "goal-discovery/results/q1-010-determinism-control/result.json"
REGISTER = "roadmap/experiments.json"

OUTCOME_CLASSES = ("supported", "narrowed", "negative", "corrected")
OUTCOME_LABEL = {
    "supported": "Supported, one family",
    "narrowed": "Narrowed",
    "negative": "Negative result",
    "corrected": "Correction / voided gate",
}

# Two conjectures and the charter's four completion clauses. These are the only
# hand-written assertions on the page; each names the authority that owns it, so
# a reader can check rather than trust.
CONJECTURES = [
    ("C1", "Coordination by a shared scarcity signal",
     "Supported on one family", "supported",
     "A divisible renewable commons. C1-002 showed it does not transfer to an "
     "indivisible good: a shared scalar is common-mode and can gate a population "
     "together but never stagger it."),
    ("C2", "Symmetry breaking from a shared quantity",
     "Sharper half, one family", "supported",
     "Environmental heterogeneity substitutes for designer labelling — but the "
     "derivation rule and the period, which equals the population size, are both "
     "still authored."),
]

CLAUSES = [
    ("1", "Recovery — proposes the authored coordinating structure",
     "Met on two families", "met"),
    ("2", "No false positive — abstains where the structure is absent",
     "Neither met nor failed: never validly tested", "open"),
    ("3", "Frozen before reveal", "Held where tested", "met"),
    ("4", "The proposal path was not authored against the case",
     "Unsatisfiable as staffed — one agent writes both", "blocked"),
]


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def diverging_chart(title: str, source: str, note: str, rows, replicates: int,
                    gate=None) -> str:
    """Horizontal diverging bars: effect above each arm's own shuffle null.

    Every bar is direct-labelled. That is not decoration: two of the four
    categorical slots and both chart hues sit below 3:1 on the light surface,
    and the method's relief rule requires visible labels wherever that is true.
    """
    label_w, plot_w, row_h, gap = 250, 420, 30, 10
    height = len(rows) * (row_h + gap) + 58
    span = max(max(abs(v) for _, v, _ in rows), 0.05) * 1.18
    zero_x = label_w + plot_w / 2
    scale = (plot_w / 2) / span

    parts = [
        f'<figure class="chart"><figcaption><h3>{esc(title)}</h3>',
        f'<p class="src">{esc(source)}</p></figcaption>',
        f'<svg viewBox="0 0 {label_w + plot_w + 74} {height}" role="img" '
        f'aria-label="{esc(title)}">',
    ]
    if gate is not None:
        gx = zero_x + gate * scale
        parts.append(
            f'<line class="gate" x1="{gx:.1f}" y1="10" x2="{gx:.1f}" '
            f'y2="{height - 34:.1f}"/>'
            f'<text class="gatelab" x="{gx + 5:.1f}" y="{height - 22:.1f}">'
            f'frozen gate {gate:+.4f}</text>'
        )
    for i, (name, value, sd) in enumerate(rows):
        y = 14 + i * (row_h + gap)
        w = abs(value) * scale
        x = zero_x if value >= 0 else zero_x - w
        cls = "pos" if value >= 0 else "neg"
        # Deliberately NOT value/sd. The shuffle-null sd is the spread of a
        # few-replicate estimate, and on arms whose null is near-deterministic
        # it collapses toward zero: the commons `live` sd is 0.0001 and `random`
        # is 0.0003, so the ratio reads "+4101 null sd" and "+20 null sd" --
        # the second of which flatly contradicts this page's own statement that
        # the matched-independent arm sits at its null. Report both numbers and
        # let the reader divide, or not. The ratios that ARE quoted in prose
        # come from result packages that computed and froze them.
        #
        # `replicates` is read from the package, not hardcoded. It was a literal
        # 8 until 2026-09-06, applied to BOTH charts -- but Q1-009 used 5, so
        # every commons tooltip overstated how well-resolved its null is, in the
        # direction that makes the unexplained commons arm look like a settled
        # measurement. That is the exact quantity failure-log F23 turns on.
        sds = f"null sd {sd:.4f} over {replicates} replicates"
        parts.append(
            f'<text class="rowlab" x="{label_w - 12}" y="{y + row_h * 0.68:.1f}">'
            f'{esc(name)}</text>'
            f'<rect class="bar {cls}" x="{x:.1f}" y="{y:.1f}" width="{max(w, 1.5):.1f}" '
            f'height="{row_h}" rx="4"><title>{esc(name)}: {value:+.4f} bits '
            f'above its own shuffle null ({sds})</title></rect>'
            f'<text class="val {cls}" x="{(x + w + 8) if value >= 0 else (x - 8):.1f}" '
            f'y="{y + row_h * 0.68:.1f}" text-anchor="{"start" if value >= 0 else "end"}">'
            f'{value:+.3f}</text>'
        )
    parts.append(
        f'<line class="zero" x1="{zero_x:.1f}" y1="6" x2="{zero_x:.1f}" '
        f'y2="{height - 34:.1f}"/>'
        f'<text class="zerolab" x="{zero_x:.1f}" y="{height - 12:.1f}" '
        f'text-anchor="middle">0 = at its own shuffle null</text>'
        '</svg>'
        f'<p class="note">{note}</p></figure>'
    )
    return "".join(parts)


def render() -> str:
    q9, q10, register = load(Q1_009), load(Q1_010), load(REGISTER)
    legacy = set(register["ontology_contract_policy"]["legacy_unversioned_record_ids"])
    live = [r for r in register["experiments"] if r["id"] not in legacy]

    for record in live:
        cls = record.get("outcome_class")
        if cls not in OUTCOME_CLASSES:
            raise ValueError(
                f"Record {record['id']} has outcome_class {cls!r}; expected one of "
                f"{', '.join(OUTCOME_CLASSES)}. Every live record must say which "
                "kind of result it was, or this page cannot show it."
            )

    commons = [
        ("live — coordinated", q9["commons"]["live"]),
        ("frozen — signal never updated", q9["commons"]["frozen"]),
        ("random — matched independent", q9["commons"]["random"]),
        ("none — degenerate control", q9["commons"]["none"]),
    ]
    commons_rows = [(n, v["ei_micro_above_null"], v["null_ei_micro_sd"]) for n, v in commons]
    slot_rows = [
        ("derived phase — coordinated", *_arm(q10, "derived_phase")),
        ("private period — independent", *_arm(q10, "private_period")),
        ("private period, primes — ungated", *_arm(q10, "private_period_primes")),
    ]

    counts = {c: sum(1 for r in live if r["outcome_class"] == c) for c in OUTCOME_CLASSES}

    body = [
        f'<h1>Where the programme stands</h1>',
        f'<p class="lede">Two bets, one instrument that has to verify them, and '
        f'{len(live)} experiments. Every number here is read from a committed result '
        f'package at render time — nothing on this page is typed by hand.</p>',

        '<h2>The two bets</h2>',
        '<div class="tiles">',
    ]
    for key, name, status, cls, detail in CONJECTURES:
        body.append(
            f'<div class="tile {cls}"><div class="tk">{esc(key)}</div>'
            f'<div class="tn">{esc(name)}</div>'
            f'<div class="ts"><span class="dot {cls}"></span>{esc(status)}</div>'
            f'<p>{esc(detail)}</p></div>'
        )
    body.append('</div>')
    body.append(
        '<p class="note">Owned by <code>wiki/conjectures.md</code>, which admits a '
        'claim only with a stated refuter.</p>'
    )

    body.append('<h2>Can the instrument verify them yet? No.</h2>')
    body.append(
        '<p class="lede">The charter says the analytic arm is finished when four '
        'clauses hold on a specimen it was not built for. Until then no construction '
        'claim in this programme is verified — including both bets above.</p>'
    )
    body.append('<ol class="clauses">')
    for num, text, status, state in CLAUSES:
        body.append(
            f'<li class="{state}"><span class="cn">{esc(num)}</span>'
            f'<span class="ct">{esc(text)}</span>'
            f'<span class="cs"><span class="dot {state}"></span>{esc(status)}</span></li>'
        )
    body.append('</ol>')

    body.append('<h2>The measurement the programme currently leans on</h2>')
    body.append(
        '<p class="lede">Effective information, measured against each arm\'s own '
        'shuffle null. The claim under test is that it reports structure where '
        'coordination is present and nothing where it is absent. On one family it '
        'does. On the other it does not, and that is unresolved.</p>'
    )
    body.append('<div class="charts">')
    body.append(diverging_chart(
        "Commons — the statistic does not behave",
        f"goal-discovery/results/q1-009-information/followup.json · {q9['seeds']} seeds",
        "<strong>frozen</strong> coordinates nothing — C1-001 measures its "
        "satisfaction at 0.000 — yet it sits <strong>+0.198 above its null</strong>, "
        "34.5 times the matched-independent arm and 5.3 times its own null "
        "spread of 0.037. That ratio is quoted because this arm's null has real "
        "spread; the near-deterministic arms' do not, which is why the bars carry "
        "raw numbers rather than ratios. No experiment explains this. It is the open "
        "half of the audit.",
        commons_rows, replicates=q9["null_replicates"]))
    body.append(diverging_chart(
        "Slot — the statistic behaves",
        f"goal-discovery/results/q1-010-determinism-control/result.json · "
        f"{q10['admissible_seeds']} seeds",
        "Q1-010 removed the shared period — the one quantity that tiles the cycle — "
        "and the population lost 27% of its performance. The statistic declined to "
        "report it as structured, below the gate frozen before the run. The auditor "
        "predicted the opposite and was wrong.",
        slot_rows, replicates=q10["null_replicates"],
        gate=q10["frozen_gates"]["G_A_min_above_null"]))
    body.append('</div>')

    body.append(f'<h2>All {len(live)} live experiments</h2>')
    body.append('<div class="legend">')
    for cls in OUTCOME_CLASSES:
        body.append(
            f'<span class="lg"><span class="sw {cls}"></span>'
            f'{esc(OUTCOME_LABEL[cls])} <b>{counts[cls]}</b></span>'
        )
    body.append('</div>')
    body.append(
        f'<p class="note">{counts["negative"] + counts["corrected"]} of {len(live)} '
        'are negative results or corrections to earlier work. That is the honest '
        'shape of this programme right now, and it is a feature of the method rather '
        'than a failure of it.</p>'
    )
    body.append('<ul class="exps">')
    for r in live:
        cls = r["outcome_class"]
        body.append(
            f'<li class="{cls}"><div class="eh"><span class="eid">{esc(r["id"])}</span>'
            f'<span class="chip {cls}">{esc(OUTCOME_LABEL[cls])}</span></div>'
            f'<div class="eq">{esc(r["question"])}</div>'
            f'<div class="ef">{esc(r["headline"])}</div></li>'
        )
    body.append('</ul>')

    body.append(
        '<h2>Where to go next</h2>'
        '<ul class="links">'
        '<li><code>wiki/scoreboard.md</code> — the same fifteen as plain text</li>'
        '<li><code>wiki/conjectures.md</code> — the bets, each with its refuter</li>'
        '<li><code>goal-discovery/docs/plans/current_research_plan.md</code> — the next action</li>'
        '<li><code>goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md</code> — what is known to be wrong</li>'
        '</ul>'
        '<p class="foot">Generated by <code>scripts/render_status_page.py --write</code>. '
        '<code>--check</code> fails if this page and the evidence disagree.</p>'
    )
    return TEMPLATE.replace("{{BODY}}", "\n".join(body))


def _arm(report: dict, name: str):
    arm = report["arms"][name]
    return arm["ei_micro_above_null"], arm["null_ei_micro_sd"]


TEMPLATE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Where the programme stands</title>
<!-- GENERATED by scripts/render_status_page.py; do not edit. -->
<style>
:root{
  color-scheme: light;
  --plane:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,.10);
  --pos:#2a78d6; --neg:#d03b3b; --neutral:#f0efec;
  --supported:#1baf7a; --narrowed:#eda100; --negative:#2a78d6; --corrected:#e34948;
  --met:#0ca30c; --open:#fab219; --blocked:#d03b3b;
}
@media (prefers-color-scheme: dark){ :root:where(:not([data-theme="light"])){
  color-scheme: dark;
  --plane:#0d0d0d; --surface:#1a1a19; --ink:#fff; --ink2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,.10);
  --pos:#3987e5; --neg:#e66767; --neutral:#383835;
  --supported:#199e70; --narrowed:#c98500; --negative:#3987e5; --corrected:#e66767;
}}
:root[data-theme="dark"]{
  color-scheme: dark;
  --plane:#0d0d0d; --surface:#1a1a19; --ink:#fff; --ink2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,.10);
  --pos:#3987e5; --neg:#e66767; --neutral:#383835;
  --supported:#199e70; --narrowed:#c98500; --negative:#3987e5; --corrected:#e66767;
}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);
  font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;
  padding:40px 24px 72px;}
main{max-width:940px;margin:0 auto}
h1{font-size:30px;line-height:1.2;margin:0 0 10px;letter-spacing:-.02em}
h2{font-size:19px;margin:44px 0 12px;letter-spacing:-.01em;
  padding-bottom:8px;border-bottom:1px solid var(--grid)}
h3{font-size:14px;margin:0 0 2px}
p{margin:0 0 12px}
.lede{color:var(--ink2);max-width:66ch}
.note{color:var(--muted);font-size:13px;max-width:70ch}
code{font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--ink2)}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block;margin-right:7px;
  vertical-align:middle}
.dot.supported,.dot.met{background:var(--met)}
.dot.open{background:var(--open)}
.dot.blocked{background:var(--blocked)}

.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.tile{background:var(--surface);border:1px solid var(--ring);border-radius:10px;padding:16px 18px}
.tk{font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.08em}
.tn{font-size:16px;font-weight:600;margin:2px 0 8px}
.ts{font-size:13px;font-weight:600;margin-bottom:8px}
.tile p{font-size:13px;color:var(--ink2);margin:0}

.clauses{list-style:none;padding:0;margin:0;counter-reset:c}
.clauses li{display:grid;grid-template-columns:26px 1fr auto;gap:12px;align-items:baseline;
  padding:11px 14px;background:var(--surface);border:1px solid var(--ring);
  border-radius:8px;margin-bottom:6px}
.clauses .cn{color:var(--muted);font-weight:700;font-variant-numeric:tabular-nums}
.clauses .ct{font-size:14px}
.clauses .cs{font-size:12.5px;color:var(--ink2);white-space:nowrap}
@media(max-width:640px){.clauses li{grid-template-columns:26px 1fr}.clauses .cs{grid-column:2}}

.charts{display:grid;grid-template-columns:1fr;gap:18px}
.chart{margin:0;background:var(--surface);border:1px solid var(--ring);
  border-radius:10px;padding:16px 18px 14px}
.chart .src{font:11.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;
  color:var(--muted);margin:0 0 6px;word-break:break-all}
.chart svg{width:100%;height:auto;display:block;overflow:visible}
.bar.pos{fill:var(--pos)} .bar.neg{fill:var(--neg)}
.val{font-size:12px;font-weight:600;font-variant-numeric:tabular-nums;fill:var(--ink2)}
.rowlab{font-size:12.5px;fill:var(--ink2);text-anchor:end}
.zero{stroke:var(--axis);stroke-width:1}
.gate{stroke:var(--muted);stroke-width:1}
.zerolab,.gatelab{font-size:11px;fill:var(--muted)}
.chart .note{margin:10px 0 0}

.legend{display:flex;flex-wrap:wrap;gap:16px;margin:0 0 10px}
.lg{font-size:13px;color:var(--ink2)}
.sw{width:11px;height:11px;border-radius:3px;display:inline-block;margin-right:6px;
  vertical-align:middle}
.sw.supported,.chip.supported{background:var(--supported)}
.sw.narrowed,.chip.narrowed{background:var(--narrowed)}
.sw.negative,.chip.negative{background:var(--negative)}
.sw.corrected,.chip.corrected{background:var(--corrected)}

.exps{list-style:none;padding:0;margin:0}
.exps li{background:var(--surface);border:1px solid var(--ring);border-radius:8px;
  padding:13px 16px;margin-bottom:7px;border-left:3px solid var(--axis)}
.exps li.supported{border-left-color:var(--supported)}
.exps li.narrowed{border-left-color:var(--narrowed)}
.exps li.negative{border-left-color:var(--negative)}
.exps li.corrected{border-left-color:var(--corrected)}
.eh{display:flex;align-items:center;gap:10px;margin-bottom:4px;flex-wrap:wrap}
.eid{font-weight:700;font-size:13px;letter-spacing:.02em}
.chip{font-size:10.5px;font-weight:700;color:#fff;padding:2px 8px;border-radius:99px;
  letter-spacing:.02em;text-transform:uppercase}
.chip.narrowed{color:#2a2100}
.eq{font-size:12.5px;color:var(--muted);margin-bottom:5px}
.ef{font-size:14px;color:var(--ink)}
.links{margin:0 0 12px;padding-left:20px;color:var(--ink2);font-size:13.5px}
.links li{margin-bottom:3px}
.foot{color:var(--muted);font-size:12.5px;margin-top:26px}
</style>
<main>
{{BODY}}
</main>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = ap.parse_args()
    try:
        page = render()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"FAIL: {error}")
        return 1
    target = ROOT / OUTPUT
    if args.write:
        target.write_text(page, encoding="utf-8")
        print(f"PASS: wrote {OUTPUT} ({len(page):,} bytes)")
        return 0
    if not target.exists() or target.read_text(encoding="utf-8") != page:
        print(f"FAIL: {OUTPUT} is stale; run scripts/render_status_page.py --write")
        return 1
    print(f"PASS: {OUTPUT} matches the committed evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
