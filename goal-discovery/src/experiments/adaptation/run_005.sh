#!/usr/bin/env bash
set -euo pipefail

: "${NETLOGO_CONSOLE:?Set NETLOGO_CONSOLE to NetLogo 7 headless launcher}"
base_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
model="$base_dir/src/experiments/adaptation/adaptation.nlogox"
setup="$base_dir/src/experiments/adaptation/005-behaviorspace.xml"
result_dir="$base_dir/results/005-adaptation"
mkdir -p "$result_dir/raw-a" "$result_dir/raw-b" "$result_dir/analysis"

for batch in raw-a raw-b; do
  for arm in adaptive frozen reset-between; do
    "$NETLOGO_CONSOLE" --headless --model "$model" --setup-file "$setup" \
      --experiment "005-$arm" --table "$result_dir/$batch/005-$arm.csv"
  done
done
uv run python -m src.experiments.adaptation.analyze \
  --first "$result_dir/raw-a" --second "$result_dir/raw-b" \
  --output-dir "$result_dir/analysis"
