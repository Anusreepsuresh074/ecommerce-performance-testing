#!/usr/bin/env python3
"""Refuses a run that would break the approved plan's safety caps or run rules (plan section 13).

Usage: scripts/check-caps.py <profile>
Checks config/profiles/<profile>.properties against the caps in config/nfr.json (total users, latest end time), and
the run history in results/ against the run rules: the minimum gap since the last run ended, and the maximum runs of
this scenario per UTC day.
Exit 0 = OK to start, 1 = refused (the run must not start).
"""

import json
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_properties(path):
    props = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            key, _, value = line.partition("=")
            props[key.strip()] = value.strip()
    return props


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: scripts/check-caps.py <profile>")
    profile = sys.argv[1]
    props = read_properties(ROOT / "config" / "profiles" / f"{profile}.properties")
    caps = json.loads((ROOT / "config" / "nfr.json").read_text())["caps"]

    groups = sorted({m.group(1) for k in props if (m := re.fullmatch(r"(tg\d+)\.threads", k))})
    users = sum(int(props[f"{g}.threads"]) for g in groups)
    end = max(
        (
            int(props.get(f"{g}.delay", 0)) + int(props[f"{g}.duration"])
            for g in groups
            if int(props[f"{g}.threads"]) > 0
        ),
        default=0,
    )

    problems = []
    if users > caps["max_users"]:
        problems.append(f"{users} users > cap {caps['max_users']}")
    if end > caps["max_duration_s"]:
        problems.append(f"ends at {end} s > cap {caps['max_duration_s']} s")

    results = ROOT / "results"
    runs = sorted(results.glob("*/results.jtl")) if results.is_dir() else []
    if runs:
        since = time.time() - max(p.stat().st_mtime for p in runs)
        if since < caps["min_gap_between_runs_s"]:
            problems.append(f"last run ended {since:.0f} s ago < {caps['min_gap_between_runs_s']} s gap")
    per_day = caps.get("max_runs_per_day", {}).get(profile)
    if per_day is not None:
        today = datetime.now(UTC).strftime("%Y%m%d")
        done = [p for p in runs if p.parent.name.startswith(today) and p.parent.name.endswith(f"-{profile}")]
        if len(done) >= per_day:
            problems.append(f"{len(done)} '{profile}' runs today (UTC) >= {per_day} per day")

    if problems:
        print(f"REFUSED '{profile}': " + "; ".join(problems))
        sys.exit(1)
    print(
        f"Caps OK for '{profile}': {users} users, ends by {end} s "
        f"(caps: {caps['max_users']} users, {caps['max_duration_s']} s); run rules OK"
    )


if __name__ == "__main__":
    main()
