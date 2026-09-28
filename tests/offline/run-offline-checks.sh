#!/usr/bin/env bash
# Offline script validation: runs test-plans/shopper-journey.jmx against a local
# stub of the DummyJSON endpoints (no request leaves this machine) and checks
# the script behaves as the plan and context/perf-auth.md require.
#
# Usage: tests/offline/run-offline-checks.sh
# Cases: the smoke journey; a login without a token; a 429 stop; and the load,
# stress and spike profiles' thread shapes with pacing, think time and
# durations shortened (for example pacing 24 s -> 2 s, stress steps 120 s -> 6 s).
# Exit 0 = every case passes.
set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

if ! command -v jmeter >/dev/null 2>&1; then
  echo "jmeter not found on PATH" >&2
  exit 2
fi

# Fake credentials only: these must never appear in any log or result.
export STUB_USER="stub-user-Q7" STUB_PASS="stub-pass-Z93k" STUB_PORT=18089
export AUTH_USERNAME="$STUB_USER" AUTH_PASSWORD="$STUB_PASS"
fast=(-Jpacing.ms=2000 -Jthink.min.ms=50 -Jthink.range.ms=100)
failed=0

# run_case <name> <stub mode> <profile> [extra -J overrides...]
run_case() {
  local name="$1" mode="$2" profile="$3"
  shift 3
  local out="$work/$name"
  mkdir -p "$out"
  STUB_MODE="$mode" STUB_LOG="$out/requests.log" python3 "$here/stub_server.py" &
  local stub=$!
  sleep 1
  printf 'protocol=http\nhost=127.0.0.1\nport=%s\n' "$STUB_PORT" > "$out/local.properties"
  timeout 180 jmeter -n -t "$root/test-plans/shopper-journey.jmx" \
    -q "$root/config/jmeter-common.properties" -q "$out/local.properties" \
    -q "$root/config/profiles/$profile.properties" "$@" \
    -l "$out/results.jtl" -j "$out/jmeter.log" > "$out/console.txt" 2>&1
  kill "$stub" 2>/dev/null
  wait "$stub" 2>/dev/null
  echo "== $name ($profile profile, stub mode: $mode)"
  python3 "$here/check-offline.py" "$name" "$out" || failed=1
}

run_case journey ok smoke "${fast[@]}"
run_case notoken notoken smoke "${fast[@]}"
run_case ratelimit ratelimit baseline "${fast[@]}"
run_case shape-load ok load "${fast[@]}" -Jtg1.rampup=3 -Jtg1.duration=20
run_case shape-stress ok stress "${fast[@]}" \
  -Jtg1.rampup=1 -Jtg1.duration=30 -Jtg2.rampup=1 -Jtg2.delay=6 -Jtg2.duration=24 \
  -Jtg3.rampup=1 -Jtg3.delay=12 -Jtg3.duration=18 -Jtg4.rampup=1 -Jtg4.delay=18 -Jtg4.duration=12 \
  -Jtg5.rampup=1 -Jtg5.delay=24 -Jtg5.duration=6
run_case shape-spike ok spike "${fast[@]}" -Jtg1.rampup=2 -Jtg1.duration=21 -Jtg2.rampup=1 -Jtg2.delay=6 -Jtg2.duration=6

if [[ $failed -eq 0 ]]; then
  echo "OFFLINE CHECKS: ALL PASS"
else
  echo "OFFLINE CHECKS: FAILURES ABOVE"
fi
exit "$failed"
