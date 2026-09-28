#!/usr/bin/env bash
# Builds JMeter's HTML dashboard for one run: reports/<run name>/index.html
#
# Usage: scripts/build-dashboard.sh <run dir>
# The .jtl carries two extra columns (sample_variables), so the same
# jmeter-common.properties used for the run must be passed to read it.
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <run dir>" >&2
  exit 2
fi

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_dir="$(cd "$1" && pwd)"
name="$(basename "$run_dir")"
out="$root/reports/$name"

if [[ -e "$out" ]]; then
  echo "Dashboard already exists: reports/$name (delete it to rebuild)" >&2
  exit 1
fi

title="$name"
if [[ -f "$run_dir/summary.json" ]]; then
  title="$(python3 -c "import json,sys; s=json.load(open(sys.argv[1])); print(f\"{s['scenario_id']} {s['scenario']} - {s['verdict']} - {s['started_utc']} UTC\")" "$run_dir/summary.json")"
fi

mkdir -p "$root/reports"
jmeter -g "$run_dir/results.jtl" -o "$out" \
  -q "$root/config/jmeter-common.properties" \
  -q "$root/config/report.properties" \
  -Jjmeter.reportgenerator.report_title="DummyJSON Shopper Journey: $title" \
  -j "$out.log" >/dev/null
mv "$out.log" "$out/report-generation.log"
echo "Dashboard: reports/$name/index.html"
