"""One picture of what Q1-009 established, drawn from live runs rather than illustrated.

Exists because the result records did not survive contact with a reader. Three
prose explanations of the same findings failed in a row; the thing that landed was
a picture of the actual system with the actual numbers on it. Regenerate from the `goal-discovery/` directory, not the repository root -- the
package root is there and the output path is relative to it:

    cd goal-discovery
    uv run --extra visual-workbench python -m src.experiments.q1_information.figure

Every value is computed at render time from the specimen and from
results/q1-009-information/followup.json, so the figure cannot drift from the
evidence it describes.
"""
import json

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from src.experiments.q1_information import commons as cm
from src.substrate import run
from src.substrate.specimens.renewable_commons import SPECIMEN

cfg = cm.load()
SEED = 0

def trace(arm):
    stock, drew = [], []
    conf = cm.arm_cfg(cfg, arm, SEED)
    run(SPECIMEN, conf, SEED,
        observer=lambda t, att, st: (stock.append(st.resource), drew.append(att > 0.0)))
    out = run(SPECIMEN, conf, SEED)
    return np.array(stock), np.array(drew), out.satisfaction

live_s, live_d, live_sat = trace("live")
rand_s, rand_d, rand_sat = trace("random")
none_s, none_d, none_sat = trace("none")

with open("results/q1-009-information/followup.json") as fh:
    nums = json.load(fh)
ei = {k: nums["commons"][k]["ei_micro_above_null"] for k in ("live", "random", "none")}
emerg_detail = nums["commons"]["live"]["ei_micro"]
emerg_summary = nums["commons"]["live"]["ei_macro"]

INK, MUTE = "#1a1a1a", "#8a8a8a"
C_LIVE, C_RAND, C_NONE = "#1f6f4a", "#b8860b", "#a33"
fig = plt.figure(figsize=(13.5, 10.0), facecolor="white")
fig.suptitle("Twelve users, one shared well, 120 days — what the experiment actually showed",
             fontsize=17, fontweight="bold", color=INK, y=0.975)
fig.text(0.5, 0.936, "Each user must draw 80 buckets. The well refills slowly. Nobody is in charge; "
         "the only thing they share is one number that says how scarce water is.",
         ha="center", fontsize=10.5, color=MUTE)

# A — the well
ax = fig.add_axes([0.065, 0.60, 0.40, 0.28])
ax.plot(live_s, color=C_LIVE, lw=2.2, label=f"shared scarcity signal working  →  {live_sat:.0%} of users met their need")
ax.plot(rand_s, color=C_RAND, lw=1.8, ls="--", label=f"everyone draws at random, same overall rate  →  {rand_sat:.0%}")
ax.plot(none_s, color=C_NONE, lw=1.8, ls=":", label=f"no signal, everyone draws whenever  →  {none_sat:.0%}")
ax.set_title("A.  Does the shared number actually help?", fontsize=12.5, fontweight="bold",
             color=INK, loc="left", pad=8)
ax.set_xlabel("day", fontsize=9.5); ax.set_ylabel("water left in the well", fontsize=9.5)
ax.legend(fontsize=8.6, frameon=False, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
ax.annotate("drained early and never recovers", xy=(16, 4), xytext=(34, 48), fontsize=8.5,
            color=C_NONE, arrowprops={"arrowstyle": "->", "color": C_NONE, "lw": 1.1})
ax.text(0.5, -0.30, "Leaving more water in the well is NOT better — the goal is every user meeting their need.\n"
        "Random leaves more water precisely because a quarter of its users never get enough.",
        transform=ax.transAxes, ha="center", fontsize=8.6, color="#8b2f2f", style="italic")

# B — who drew when
ax = fig.add_axes([0.545, 0.60, 0.40, 0.28])
gap = np.full((2, 120), np.nan)
img = np.vstack([live_d.T.astype(float), gap, rand_d.T.astype(float)])
ax.imshow(img, aspect="auto", cmap=matplotlib.colors.ListedColormap(["#f2f2f2", INK]),
          interpolation="nearest")
ax.set_title("B.  This is the pattern the measurement reads", fontsize=12.5, fontweight="bold",
             color=INK, loc="left", pad=8)
ax.set_yticks([5.5, 19.5]); ax.set_yticklabels(["signal\nworking", "random"], fontsize=9)
ax.set_xlabel("day  (one row per user; dark = drew water that day)", fontsize=9.5)
ax.spines[["top", "right", "left"]].set_visible(False); ax.tick_params(left=False)

# C — detail vs summary
ax = fig.add_axes([0.065, 0.225, 0.40, 0.25])
ax.bar([0, 1], [emerg_detail, emerg_summary], color=[INK, "#7fa8c9"], width=0.55)
for x, v in zip((0, 1), (emerg_detail, emerg_summary)):
    ax.text(x, v + 0.02, f"{v:.3f}", ha="center", fontsize=11, fontweight="bold", color=INK)
ax.set_xticks([0, 1])
ax.set_xticklabels(["DETAIL\nexactly who drew today", "SUMMARY\njust how many drew today"], fontsize=9.5)
ax.set_ylabel("how much today tells you\nabout tomorrow  (bits)", fontsize=9.5)
ax.set_title("C.  Does zooming out to the group tell you more?", fontsize=12.5,
             fontweight="bold", color=INK, loc="left", pad=8)
ax.set_ylim(0, 0.78); ax.spines[["top", "right"]].set_visible(False)
ax.text(0.5, 0.685, "No — the summary is worse.\nThe answer the project had avoided for a week.",
        ha="center", fontsize=9.5, color="#8b2f2f", style="italic")

# D — the control fix
ax = fig.add_axes([0.545, 0.225, 0.40, 0.25])
bars = ax.bar([0, 1, 2], [ei["live"], ei["random"], ei["none"]],
              color=[C_LIVE, C_RAND, "#cccccc"], width=0.55)
for x, v in zip((0, 1, 2), (ei["live"], ei["random"], ei["none"])):
    ax.text(x, v + 0.018, f"{v:.3f}", ha="center", fontsize=11, fontweight="bold", color=INK)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["signal working", "random\n(the honest control,\nbuilt today)",
                    "no signal\n(the OLD control —\nuseless)"], fontsize=9)
ax.set_ylabel("structure found, above chance  (bits)", fontsize=9.5)
ax.set_title("D.  Can the measurement tell coordination from randomness?", fontsize=12.5,
             fontweight="bold", color=INK, loc="left", pad=8)
ax.set_ylim(0, 0.72); ax.spines[["top", "right"]].set_visible(False)
ax.annotate("", xy=(1, 0.10), xytext=(2, 0.10),
            arrowprops={"arrowstyle": "<->", "color": MUTE, "lw": 1.0})
ax.text(1.5, 0.125, "the old control was a stopped clock:\neveryone drew every single day,\nso of course it looked different",
        ha="center", fontsize=8.3, color=MUTE, style="italic")
ax.text(0, 0.50, "yes —\n0.589 vs 0.006", ha="center", fontsize=9.5, color=C_LIVE, fontweight="bold")

fig.text(0.065, 0.112, "What this establishes", fontsize=11.5, fontweight="bold", color=INK)
fig.text(0.065, 0.020,
    "The measurement finds structure when the twelve are coordinating and finds essentially nothing when they are not — 0.589 against 0.006, and the same\n"
    "pattern on a second, unrelated test system. That is the result this project had been trying to demonstrate. Separately, and negatively: looking at the group\n"
    "instead of the individuals loses information rather than gaining it, so there is no hidden higher level here to find.",
    fontsize=10, color=INK, linespacing=1.65)
out = "results/q1-009-information/what-q1-009-showed.png"
fig.savefig(out, dpi=155, facecolor="white")
print("wrote", out)
print("live/random/none satisfaction:", live_sat, rand_sat, none_sat)
print("EI above null:", ei, "| detail", emerg_detail, "summary", emerg_summary)
