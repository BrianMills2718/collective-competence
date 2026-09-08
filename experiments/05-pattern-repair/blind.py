"""Package spatial repair behavior without revealing the authored criterion or rule."""
from __future__ import annotations
import gzip, hashlib, json, random
from pathlib import Path
from model import conflicts, lesion, random_state, settle, step

HERE = Path(__file__).resolve().parent


def symbols(colors: list[int]) -> list[str]:
    return [f"q{x}" for x in colors]


def formation_case(seed: int, n: int = 24) -> dict:
    rng=random.Random(seed); colors=random_state(n,rng); initial=symbols(colors)
    assert settle(colors,rng,budget=10_000) is not None
    return {"sample_id":f"f{seed:02d}","initial":initial,"terminal":symbols(colors)}


def repair_case(seed: int, width: int, n: int = 24) -> dict:
    rng=random.Random(seed); colors=random_state(n,rng); assert settle(colors,rng,budget=10_000) is not None
    baseline=colors.copy(); start=rng.randrange(n); lesion(colors,start,width); damaged=colors.copy()
    trajectory=[symbols(colors)]
    # Record coarse snapshots without exposing the hidden stopping statistic.
    for op in range(1,101):
        step(colors,rng,"aware")
        if op in {1,2,4,8,16,32,64,100}:
            trajectory.append(symbols(colors))
        if conflicts(colors)==0:
            break
    return {"sample_id":f"r{width}-{seed:02d}","operation":{"kind":"overwrite_contiguous_block","start":start,"width":width},
            "pre_operation":symbols(baseline),"post_operation":symbols(damaged),"observed_after":trajectory,"terminal":symbols(colors)}


def frozen_case(seed: int, pair: bool, n: int = 24) -> dict:
    rng=random.Random(seed); colors=random_state(n,rng); assert settle(colors,rng,budget=10_000) is not None
    baseline=colors.copy(); i=rng.randrange(n)
    if pair:
        colors[i]=0; colors[(i+1)%n]=0; frozen=frozenset({i,(i+1)%n})
    else:
        colors[i]=colors[(i-1)%n]; frozen=frozenset({i})
    changed=colors.copy()
    for _ in range(500): step(colors,rng,"aware",frozen)
    return {"sample_id":f"d{int(pair)}-{seed:02d}","operation":{"kind":"overwrite_and_freeze_sites","indices":sorted(frozen)},
            "pre_operation":symbols(baseline),"post_operation":symbols(changed),"after_500_updates":symbols(colors)}


def package() -> dict:
    return {"schema_version":1,"shape":"cyclic_sequence","categories":["q0","q1","q2"],
            "formation":[formation_case(s) for s in range(8)],
            "repair":[repair_case(s,w) for w in (4,8) for s in range(6)],
            "persistent_interventions":[frozen_case(s,False) for s in range(4)] + [frozen_case(s,True) for s in range(4)]}

if __name__ == "__main__":
    value=package(); raw=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode(); compressed=gzip.compress(raw,compresslevel=9,mtime=0)
    (HERE/'results/blind_case.json.gz').write_bytes(compressed)
    manifest={"sha256":hashlib.sha256(compressed).hexdigest(),"shape":"cyclic sequence with categorical site states",
              "withheld":["authored success criterion","update rule","meaning of categories","global score","whether one exact target exists"],
              "exposed":["cyclic adjacency structure","opaque categorical configurations","formation endpoints","contiguous overwrite/repair trajectories","site-freeze interventions"]}
    (HERE/'results/blind_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(manifest,indent=2,sort_keys=True))
