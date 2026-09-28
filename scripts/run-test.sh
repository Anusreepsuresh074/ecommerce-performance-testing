#!/usr/bin/env bash
# Runs one JMeter test plan in non-GUI mode. This is the only way tests are run,
# locally and in CI, so every run uses the same settings.
#
# Usage: scripts/run-test.sh <plan> <profile> [env]
#   plan     test-plans/<plan>.jmx
#   profile  config/profiles/<profile>.properties   (users, ramp-up, duration)
#   env      config/env/<env>.properties            (server address, default: prod)
# config/jmeter-common.properties (result-file columns, safety ceiling) is always
# passed first.
#
# Each run gets its own folder, results/<UTC timestamp>-<plan>-<profile>/, holding
# results.jtl (one row per request) and jmeter.log. Earlier runs are never
# overwritten. Building the HTML report and judging pass/fail happen after this
# script, in their own steps.
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "Usage: $0 <plan> <profile> [env]" >&2
  exit 2
fi

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
plan="$1"
profile="$2"
env="${3:-prod}"

plan_file="$root/test-plans/$plan.jmx"
profile_file="$root/config/profiles/$profile.properties"
env_file="$root/config/env/$env.properties"
common_file="$root/config/jmeter-common.properties"

if ! command -v jmeter >/dev/null 2>&1; then
  echo "jmeter not found on PATH. Install Apache JMeter and add its bin/ folder to PATH." >&2
  exit 1
fi

for file in "$common_file" "$plan_file" "$profile_file" "$env_file"; do
  if [[ ! -f "$file" ]]; then
    echo "Not found: ${file#"$root"/}" >&2
    exit 1
  fi
done

# Secrets come from .env as environment variables. They are exported, never
# passed on the command line (which would show them in jmeter.log and ps).
if [[ -f "$root/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$root/.env"
  set +a
fi

run_dir="$root/results/$(date -u +%Y%m%dT%H%M%SZ)-$plan-$profile"
if [[ -e "$run_dir" ]]; then
  echo "Run folder already exists: ${run_dir#"$root"/}" >&2
  exit 1
fi
mkdir -p "$run_dir"

echo "Plan: $plan | Profile: $profile | Env: $env"
echo "Output: ${run_dir#"$root"/}"

status=0
jmeter -n \
  -t "$plan_file" \
  -q "$common_file" \
  -q "$env_file" \
  -q "$profile_file" \
  -l "$run_dir/results.jtl" \
  -j "$run_dir/jmeter.log" || status=$?

echo "RUN_DIR=${run_dir#"$root"/}"
exit "$status"
