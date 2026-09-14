#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/wiki/reference/metamodel/scientific-role-schema-v1.json"

python "$ROOT/scripts/bootstrap_role_schema_hypergraph.py" -o "$OUT"
python "$ROOT/scripts/generate_role_contracts_from_schema_graph.py" \
  "$OUT" \
  -o "$ROOT/artifacts/scientific-role-contracts.from-schema.json"
python - <<'PY' "$ROOT/wiki/reference/metamodel/scientific-role-contracts.json" "$ROOT/artifacts/scientific-role-contracts.from-schema.json"
import json, pathlib, sys
expected=json.loads(pathlib.Path(sys.argv[1]).read_text())
actual=json.loads(pathlib.Path(sys.argv[2]).read_text())
if expected != actual:
    raise SystemExit('materialized schema graph does not regenerate current contract index')
print('PASS materialized schema graph regenerates the current role contract index exactly')
PY

echo "Wrote $OUT"
echo "Review and commit the generated graph; after that, flip validator/migrator authority to graph -> contracts."
