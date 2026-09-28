#!/usr/bin/env bash
# Runs one approved scenario end to end (plan section 12): caps check -> pre-run
# check -> the run (through run-test.sh) with injector CPU sampling -> verdict.
#
# Usage: scripts/run-scenario.sh <scenario> [env]
#   scenario  smoke | baseline | load | stress | spike  (a file in config/profiles/)
# Exit 0 = PASS (VALID for the baseline, which has no gates), 1 = FAIL, 2 = INVALID,
# 3 = not started (caps, run rules or pre-run check).
set -uo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <scenario> [env]" >&2
  exit 3
fi

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scenario="$1"
env="${2:-prod}"
plan="shopper-journey"

python3 "$root/scripts/check-caps.py" "$scenario" || exit 3
"$root/scripts/precheck.sh" "$env" || exit 3

# Injector (load generator) CPU, every 5 s: "<epoch>,<used %>", from /proc/stat.
cpu_file="$(mktemp)"
python3 -u -c '
import time
def read():
    v = [int(x) for x in open("/proc/stat").readline().split()[1:]]
    return v[3] + v[4], sum(v)          # idle + iowait, total
idle0, total0 = read()
while True:
    time.sleep(5)
    idle1, total1 = read()
    used = 100 * (1 - (idle1 - idle0) / max(total1 - total0, 1))
    print(f"{int(time.time())},{round(used)}", flush=True)
    idle0, total0 = idle1, total1
' > "$cpu_file" &
sampler=$!

"$root/scripts/run-test.sh" "$plan" "$scenario" "$env" | tee "$cpu_file.out"
run_status=${PIPESTATUS[0]}

kill "$sampler" 2>/dev/null
wait "$sampler" 2>/dev/null

run_rel="$(grep '^RUN_DIR=' "$cpu_file.out" | cut -d= -f2)"
rm -f "$cpu_file.out"
if [[ -z "$run_rel" ]]; then
  rm -f "$cpu_file"
  echo "The run did not start — see the messages above." >&2
  exit 3
fi
run_dir="$root/$run_rel"
mv "$cpu_file" "$run_dir/injector-cpu.csv"

if [[ $run_status -ne 0 ]]; then
  echo "JMeter exited with $run_status — see $run_dir/jmeter.log"
fi

python3 "$root/scripts/evaluate-run.py" "$run_dir" "$scenario"
