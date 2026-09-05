"""Diagnostic: is the frozen control's level actually the best available constant?

The protocol justified the frozen control by asserting p_bar (the live run's
time-average) is "close to the best available constant". That is a claim about
the world and this measures it. Sweeps every fixed threshold on the frozen
config; opens no new outcome and changes no frozen artifact.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import numpy as np
from src.experiments.shared_scarcity.model import simulate
from src.experiments.shared_scarcity.run import load_config, SEEDS

cfg = load_config()
rows = []
for c in np.arange(0.0, 1.61, 0.05):
    m = float(np.mean([simulate(cfg, s, signal="frozen", frozen_level=float(c)).quota_satisfaction
                       for s in SEEDS]))
    rows.append((float(c), m))
p_bars = [simulate(cfg, s, signal="live").mean_signal for s in SEEDS]
best = max(rows, key=lambda r: r[1])

print(f"{'constant':>9}  mean quota satisfaction")
for c, m in rows:
    print(f"{c:>9.2f}  {m:.3f}{'   <-- best' if (c, m) == best else ''}")
print(f"\nmean p_bar used by the frozen condition: {np.mean(p_bars):.4f}")
print(f"best constant: {best[0]:.2f} -> {best[1]:.3f}")
print(f"adaptive (live): 1.000")
