"""Package adaptation trajectories without policy or domain semantics."""
from __future__ import annotations
import gzip, hashlib, json
from pathlib import Path
from model import A_GOOD, B_GOOD, reversal, run, stationary

HERE=Path(__file__).resolve().parent
SEQUENCES={
    "c000": stationary(A_GOOD,6),
    "c001": stationary(B_GOOD,6),
    "c002": reversal(A_GOOD,B_GOOD),
    "c003": reversal(B_GOOD,A_GOOD),
}
ARMS=(("a000","adaptive","none"),("a001","frozen","hold_component_000_fixed"),("a002","reset","restore_component_000_before_each_block"))


def package() -> dict:
    arms=[]
    for aid, policy, operation in ARMS:
        conditions=[]
        for cid, envs in SEQUENCES.items():
            rows=[]
            for r in run(policy,envs):
                rows.append({
                    "block": r["episode"],
                    "u000": r["quality_a"],
                    "u001": r["quality_b"],
                    "f000": r["delivered"],
                    "f001": r["allocated_a"],
                    "f002": r["allocated_b"],
                })
            conditions.append({"condition_id":cid,"rows":rows})
        arms.append({"arm_id":aid,"operation":operation,"conditions":conditions})
    return {"schema_version":1,"arms":arms,"notes":{"u_fields":"known exogenous inputs","f_fields":"anonymous observed outputs"}}

if __name__ == "__main__":
    value=package(); raw=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    comp=gzip.compress(raw,compresslevel=9,mtime=0)
    (HERE/'results/blind_case.json.gz').write_bytes(comp)
    manifest={
      "sha256":hashlib.sha256(comp).hexdigest(),
      "withheld":["policy meanings","field semantics","route/foraging semantics","objective","learning rule","implementation"],
      "exposed":["three anonymous arms","two known exogenous inputs per block","three anonymous outputs","generic hold/restore interventions"],
    }
    (HERE/'results/blind_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(manifest,indent=2,sort_keys=True))
