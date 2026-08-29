#!/usr/bin/env bash
set -euo pipefail

: "${NETLOGO_CONSOLE:?Set NETLOGO_CONSOLE to the NetLogo 7 headless launcher}"

repo_root="$(git rev-parse --show-toplevel)"
model="$repo_root/goal-discovery/src/experiments/thermostat/thermostat.nlogox"
setup_file="$repo_root/goal-discovery/src/experiments/thermostat/003b-behaviorspace.xml"
result_root="${1:-$repo_root/goal-discovery/results/003b-blind-target}"
raw_dir="$result_root/raw"
analysis_dir="$result_root/analysis"
mkdir -p "$raw_dir" "$analysis_dir"

experiments=(
  003b-discovery-passive
  003b-discovery-feedback
  003b-validation-passive
  003b-validation-feedback
  003b-validation-sensor-blocked
  003b-validation-actuator-disabled
)

for experiment in "${experiments[@]}"; do
  "$NETLOGO_CONSOLE" \
    --headless \
    --model "$model" \
    --setup-file "$setup_file" \
    --experiment "$experiment" \
    --threads 1 \
    --table "$raw_dir/$experiment.csv"
done

cd "$repo_root/goal-discovery"
uv run python -m src.experiments.thermostat.goal_inference \
  --input-dir "$raw_dir" \
  --output-dir "$analysis_dir" \
  --unlock-target 20
