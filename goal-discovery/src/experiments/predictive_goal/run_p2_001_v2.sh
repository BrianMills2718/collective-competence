#!/usr/bin/env bash
set -euo pipefail

: "${NETLOGO_CONSOLE:?Set NETLOGO_CONSOLE to NetLogo 7 headless launcher}"
base_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
model="$base_dir/src/experiments/thermostat/thermostat.nlogox"
setup="$base_dir/src/experiments/predictive_goal/p2-001-v2-behaviorspace.xml"
raw_dir="$base_dir/results/p2-001-v2-predictive-goal/raw"
analysis_dir="$base_dir/results/p2-001-v2-predictive-goal/analysis"
mkdir -p "$raw_dir" "$analysis_dir"

declare -A outputs=(
  [p2v2-train-discovery-feedback]=p2-train-discovery-feedback.csv
  [p2v2-train-discovery-passive]=p2-train-discovery-passive.csv
  [p2v2-train-load-feedback]=p2-train-load-feedback.csv
  [p2v2-train-load-passive]=p2-train-load-passive.csv
  [p2v2-heldout-discovery]=p2-heldout-discovery.csv
  [p2v2-heldout-feedback]=p2-heldout-feedback.csv
)
for experiment in "${!outputs[@]}"; do
  "$NETLOGO_CONSOLE" --headless --model "$model" --setup-file "$setup" \
    --experiment "$experiment" --table "$raw_dir/${outputs[$experiment]}"
done
uv run python -m src.experiments.predictive_goal.analyze \
  --input-dir "$raw_dir" --output-dir "$analysis_dir"
