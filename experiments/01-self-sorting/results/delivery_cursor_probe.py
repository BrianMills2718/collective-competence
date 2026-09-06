#!/usr/bin/env python3
"""Isolate WHY repeated disturbance costs central_watchdog and not decentralized.

Supporting diagnostic for the D2 delivery run. `exp_delivery` measures that the
watchdog's per-episode recovery cost RISES across eight episodes (+10.5% swap2,
+21.1% teleport, episode 0 -> 7) while the decentralized rule is flat. The
proposed mechanism is the watchdog's scan cursor: it sweeps i = 0..n-2 forever,
so its phase at the moment damage arrives is history-dependent state that
survives a disturbance, and repair cost depends on the cursor's distance from
the damage. The decentralized rule picks pairs at random and has no phase.

The test: a watchdog identical in every respect except that each sweep starts at
a random offset, destroying the phase carry-over while changing nothing else.
If the cursor is the mechanism, the per-episode rise disappears. If the rise
survives, the mechanism is something else and the claim must be withdrawn.

    python3 delivery_cursor_probe.py
"""
from __future__ import annotations

import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import selfsort as s  # noqa: E402


def watchdog_random_phase(w, budget):
    """central_watchdog with the cursor's starting offset randomised per sweep.

    Identical work per sweep -- the same n-1 positions are scanned -- so this
    changes the ORDER, not the amount. Any difference is attributable to phase.
    """
    n = len(w.a)
    while w.ops < budget:
        offset = w.rng.randrange(n - 1)
        for k in range(n - 1):
            if w.ops >= budget:
                return
            i = (offset + k) % (n - 1)
            if w.scan(i):
                w.attempt(i, charge=False)
            yield


s.CONTROLLERS["watchdog_random_phase"] = watchdog_random_phase
s.STYLE["watchdog_random_phase"] = dict(color="C4", ls="-.", marker="x", lw=1.6)


def profile(name: str, pert: str, trials: int = 400) -> list[float]:
    ts = [
        s.run_trial(name, n=10, seed=1000 * k + 71, faults=s.Faults(p_fail=0.0),
                    budget=20_000, perturbation=pert, perturb_on_sorted=True,
                    perturb_delay=20, perturb_repeats=8, perturb_magnitude=1,
                    stop_on_goal=False)
        for k in range(trials)
    ]
    full = [t for t in ts if len(t.episodes) == 8 and all(e.recovered for e in t.episodes)]
    if len(full) < trials * 0.9:
        raise SystemExit(
            f"{name}/{pert}: only {len(full)}/{trials} trials recovered from all "
            "eight episodes; the per-episode means below would be survivorship, "
            "not cost. Refusing to report them."
        )
    return [st.mean(t.episodes[i].ops_to_recover for t in full) for i in range(8)]


def main() -> int:
    print("per-episode mean ops to recover, 8 episodes, 400 trials, p_fail=0\n")
    verdicts = []
    for pert in ("swap2", "teleport"):
        for name in ("decentralized", "central_watchdog", "watchdog_random_phase"):
            per = profile(name, pert)
            rise = 100 * (per[7] - per[0]) / per[0]
            verdicts.append((pert, name, rise))
            print(f"  {pert:<9} {name:<22} " + " ".join(f"{v:5.1f}" for v in per)
                  + f"   episode 0->7 {rise:+6.1f}%")
    print()
    for pert in ("swap2", "teleport"):
        plain = next(r for p, n, r in verdicts if p == pert and n == "central_watchdog")
        fixed = next(r for p, n, r in verdicts if p == pert and n == "watchdog_random_phase")
        print(f"  {pert}: watchdog rise {plain:+.1f}% -> with the cursor phase "
              f"randomised {fixed:+.1f}%")
    print("\nThe cursor is the mechanism only if the second number is close to "
          "zero while the first is not.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
