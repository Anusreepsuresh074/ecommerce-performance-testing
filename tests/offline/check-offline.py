#!/usr/bin/env python3
"""Checks one offline run of the JMeter script against what the plan and context/perf-auth.md require.

Usage: tests/offline/check-offline.py <case> <out dir>
  case: journey | notoken | ratelimit | shape-load | shape-stress | shape-spike
Reads <out dir>/results.jtl, requests.log (from stub_server.py) and jmeter.log. Exit 0 = all checks pass.
"""

import csv
import json
import sys
from pathlib import Path

LABELS = ["T01_Login", "T02_Get_Current_User", "T03_Browse_Products", "T04_Search_Products", "T05_View_Product"]
SECRETS = ["stub-user-Q7", "stub-pass-Z93k", "stub.jwt.token"]


def main():
    case, out = sys.argv[1], Path(sys.argv[2])
    with open(out / "results.jtl", newline="") as f:
        rows = list(csv.DictReader(f))
    reqs = [json.loads(line) for line in (out / "requests.log").read_text().splitlines()]
    checks = []

    def check(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    if case in ("journey", "shape-load", "shape-stress", "shape-spike"):
        check(
            "every sample passed",
            rows and all(r["success"] == "true" for r in rows),
            f"{sum(r['success'] != 'true' for r in rows)} failed of {len(rows)}",
        )
        check("only T01–T05 samples", {r["label"] for r in rows} <= set(LABELS))
        check(
            "extra columns recorded",
            all(r.get("cacheStatus") == "DYNAMIC" and r.get("rateLimitRemaining") == "97" for r in rows),
        )
        check(
            "Authorization sent only to /auth/me",
            all((q["auth"] == "bearer-ok") == (q["path"] == "/auth/me") for q in reqs),
        )
        check("no Cookie header ever sent", not any(q["cookie"] for q in reqs))
    if case == "journey":
        check("exactly 2 iterations (10 samples in T01…T05 order)", [r["label"] for r in rows] == LABELS * 2)
        terms = [q["query"]["q"][0] for q in reqs if q["path"] == "/products/search"]
        check("CSV terms rotate", len(set(terms)) == 2, str(terms))
        opened = [q["path"] for q in reqs if q["path"].startswith("/products/") and q["path"] != "/products/search"]
        check(
            "product id correlated from search",
            all(p in ("/products/3", "/products/7", "/products/11") for p in opened),
            str(opened),
        )
        logins = [int(r["timeStamp"]) for r in rows if r["label"] == "T01_Login"]
        gap = logins[1] - logins[0] if len(logins) == 2 else 0
        check("pacing holds (second iteration ~2000 ms after the first)", 1800 <= gap <= 2600, f"{gap} ms")
    if case == "notoken":
        check(
            "login fails its assertion",
            rows and all(r["label"] == "T01_Login" and r["success"] == "false" for r in rows),
        )
        check("/auth/me never called without a token", not any(q["path"] == "/auth/me" for q in reqs))
    if case == "ratelimit":
        check(
            "test stops at the first 429", len(reqs) == 8 and rows[-1]["responseCode"] == "429", f"{len(reqs)} requests"
        )
        check("stop is logged as INVALID", "This run is INVALID" in (out / "jmeter.log").read_text())
    if case.startswith("shape-"):
        expected = {"shape-load": 6, "shape-stress": 15, "shape-spike": 15}[case]
        peak = max(int(r["allThreads"]) for r in rows)
        check(f"peak active threads = {expected}", peak == expected, f"peak {peak}")

    texts = [(out / f).read_text() for f in ("jmeter.log", "results.jtl", "console.txt") if (out / f).exists()]
    check("no credentials or token in log, results or console", not any(s in t for s in SECRETS for t in texts))

    for name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
    sys.exit(0 if all(ok for _, ok, _ in checks) else 1)


if __name__ == "__main__":
    main()
