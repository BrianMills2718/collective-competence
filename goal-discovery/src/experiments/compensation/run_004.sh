#!/usr/bin/env bash
set -euo pipefail

: "${NETLOGO_CONSOLE:?Set NETLOGO_CONSOLE to NetLogo 7 headless launcher}"
base_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
model="$base_dir/src/experiments/compensation/compensation.nlogox"
setup="$base_dir/src/experiments/compensation/004-behaviorspace.xml"
raw_dir="$base_dir/results/004-compensation/raw"
analysis_dir="$base_dir/results/004-compensation/analysis"
mkdir -p "$raw_dir" "$analysis_dir"

experiments=(
  004-passive 004-intact 004-route-a-disabled 004-route-b-disabled
  004-route-a-fixed 004-route-b-fixed 004-dual-disabled
)
for experiment in "${experiments[@]}"; do
  "$NETLOGO_CONSOLE" --headless --model "$model" --setup-file "$setup" \
    --experiment "$experiment" --table "$raw_dir/$experiment.csv"
done
uv run python -m src.experiments.compensation.analyze \
  --input-dir "$raw_dir" --output-dir "$analysis_dir"
