#!/usr/bin/env bash
# Pre-run check (plan 12.1): one request that reaches the server, not the CDN
# cache. Passes only on 200 with enough of the rate-limit budget free.
#
# Usage: scripts/precheck.sh [env]     (default env: prod)
# Exit 0 = go, 1 = don't start the run now.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
env_file="$root/config/env/${1:-prod}.properties"

prop() { grep -E "^$1=" "$env_file" | head -1 | cut -d= -f2-; }
protocol="$(prop protocol)"
host="$(prop host)"
min_remaining="$(python3 -c "import json; print(json.load(open('$root/config/nfr.json'))['caps']['min_rate_limit_remaining'])")"

# A search with a query string is served by the origin (cf-cache-status: DYNAMIC),
# so its rate-limit header is live, not a cached copy.
headers="$(curl -s -o /dev/null -D - --max-time 30 "$protocol://$host/products/search?q=phone&limit=1&select=id" | tr -d '\r')"
status="$(printf '%s\n' "$headers" | awk 'NR==1 {print $2}')"
remaining="$(printf '%s\n' "$headers" | awk -F': ' 'tolower($1)=="x-ratelimit-remaining" {print $2}')"
cache="$(printf '%s\n' "$headers" | awk -F': ' 'tolower($1)=="cf-cache-status" {print $2}')"

echo "Pre-run check: status=${status:-none} x-ratelimit-remaining=${remaining:-none} cf-cache-status=${cache:-none} (need 200 and >= $min_remaining)"
if [[ "$status" == "200" && -n "$remaining" && "$remaining" -ge "$min_remaining" ]]; then
  echo "Pre-run check: GO"
else
  echo "Pre-run check: NO GO — not enough rate-limit budget free; wait a minute and check again"
  exit 1
fi
