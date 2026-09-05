#!/usr/bin/env bash
set -euo pipefail

: "${NETLOGO_CONSOLE:?Set NETLOGO_CONSOLE to NetLogo 7 headless launcher}"
base_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
model="$base_dir/src/experiments/thermostat/thermostat.nlogox"
setup="$base_dir/src/experiments/predictive_goal/p2-001-behaviorspace.xml"
raw_dir="$base_dir/results/p2-001-predictive-goal/raw"
analysis_dir="$base_dir/results/p2-001-predictive-goal/analysis"
mkdir -p "$raw_dir" "$analysis_dir"

experiments=(
  p2-train-discovery-feedback p2-train-discovery-passive
  p2-train-load-feedback p2-train-load-passive
  p2-heldout-discovery p2-heldout-feedback
)
for experiment in "${experiments[@]}"; do
  "$NETLOGO_CONSOLE" --headless --model "$model" --setup-file "$setup" \
    --experiment "$experiment" --table "$raw_dir/$experiment.csv"
done
uv run python -m src.experiments.predictive_goal.analyze \
  --input-dir "$raw_dir" --output-dir "$analysis_dir"
