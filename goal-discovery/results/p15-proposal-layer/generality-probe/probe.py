"""Diagnostic: apply every P15 proposer to every frozen P15 package.

Reads only frozen artifacts. Opens no new outcome. The diagonal reproduces what
P15 ran; the off-diagonal measures whether the four proposers constitute one
grammar or four case-specific programs.
"""
import gzip, json, sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from src.experiments.proposal_layer.contract import load_config
from src.experiments.proposal_layer import model

FROZEN = Path("results/p15-proposal-layer/frozen")
PROPOSERS = {
    "endpoint(P10)":   model._propose_endpoint,
    "scalar(P12)":     model._propose_scalar_branches,
    "entity_dyn(P13)": model._propose_entity_dynamics,
    "directional(P14)":model._propose_directional,
}
NATIVE = {c["case_id"]: c for c in json.loads((FROZEN/"input-manifest.json").read_text())["cases"]}
MAP = {m["case_id"]: m["native_case"] for m in
       json.loads(Path("results/p15-proposal-layer/evaluator/revealed-mapping.json").read_text())["cases"]}

config = load_config()
rows = []
for case_id, entry in NATIVE.items():
    pkg = json.loads(gzip.decompress((FROZEN/entry["package_path"]).read_bytes()))
    for name, fn in PROPOSERS.items():
        try:
            out = fn(pkg, config)
            status = out.get("status")
            fam = out.get("family") or out.get("claim_type")
            result = f"{status}:{fam}"
        except Exception as exc:
            result = f"ERROR:{type(exc).__name__}"
        rows.append((MAP[case_id], pkg["shape"], name, result))

print(f"{'native':<6} {'package shape':<28} {'proposer':<18} result")
print("-"*95)
for native, shape, name, result in sorted(rows):
    own = "  <-- own" if name.endswith(f"({native})") else ""
    print(f"{native:<6} {shape:<28} {name:<18} {result}{own}")

off = [r for r in rows if not r[2].endswith(f"({r[0]})")]
errs = [r for r in off if r[3].startswith("ERROR")]
print(f"\noff-diagonal applications: {len(off)}")
print(f"  raised before producing anything: {len(errs)}")
print(f"  produced a candidate or abstention: {len(off)-len(errs)}")
