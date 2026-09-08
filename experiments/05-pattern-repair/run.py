"""Characterize formation, repair, non-unique endpoints, and defect boundaries."""
from __future__ import annotations
import json, random, statistics
from pathlib import Path
from model import conflicts, hamming, lesion, random_state, settle

HERE = Path(__file__).resolve().parent
SEEDS = range(200)
BUDGET = 10_000


def formation(n: int, rule: str) -> dict:
    ops=[]
    for seed in SEEDS:
        rng=random.Random(seed); colors=random_state(n,rng)
        value=settle(colors,rng,rule=rule,budget=BUDGET)
        if value is not None: ops.append(value)
    return {"n":n,"rule":rule,"trials":200,"successes":len(ops),"success_rate":len(ops)/200,
            "mean_ops":statistics.mean(ops) if ops else None,"max_ops":max(ops) if ops else None}


def repair(width: int, n: int = 24) -> dict:
    ops=[]; exact=0; distances=[]; initial_conf=[]
    for seed in SEEDS:
        rng=random.Random(seed); colors=random_state(n,rng); assert settle(colors,rng,budget=BUDGET) is not None
        baseline=colors.copy(); start=rng.randrange(n); lesion(colors,start,width); initial_conf.append(conflicts(colors))
        value=settle(colors,rng,budget=BUDGET); assert value is not None
        ops.append(value); d=hamming(colors,baseline); distances.append(d); exact += d == 0
    return {"width":width,"trials":200,"successes":200,"mean_ops":statistics.mean(ops),"max_ops":max(ops),
            "min_initial_conflicts":min(initial_conf),"mean_initial_conflicts":statistics.mean(initial_conf),
            "exact_original_restorations":exact,"different_valid_endpoints":200-exact,"mean_hamming_from_original":statistics.mean(distances)}


def defect_boundary(n: int = 24) -> dict:
    one=0; pair=0
    for seed in SEEDS:
        rng=random.Random(seed); colors=random_state(n,rng); assert settle(colors,rng,budget=BUDGET) is not None
        i=rng.randrange(n); colors[i]=colors[(i-1)%n]
        one += settle(colors,rng,budget=BUDGET,frozen=frozenset({i})) is not None
        rng=random.Random(seed); colors=random_state(n,rng); assert settle(colors,rng,budget=BUDGET) is not None
        i=rng.randrange(n); colors[i]=0; colors[(i+1)%n]=0
        pair += settle(colors,rng,budget=BUDGET,frozen=frozenset({i,(i+1)%n})) is not None
    return {"trials":200,"single_frozen_conflict_repairs":one,"adjacent_same_colour_frozen_pair_repairs":pair}


def characterize() -> dict:
    return {"criterion":"no adjacent equal colours on a ring",
            "valid_patterns_n24":2**24+2,
            "formation":[formation(n,r) for n in (12,24,48) for r in ("aware","random")],
            "repair":[repair(w) for w in (1,2,4,8,12)],
            "permanent_defects":defect_boundary()}

if __name__ == "__main__":
    value=characterize(); out=HERE/'results/characterization.json'; out.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n'); print(json.dumps(value,indent=2,sort_keys=True))
