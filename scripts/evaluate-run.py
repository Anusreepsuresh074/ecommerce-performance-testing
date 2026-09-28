#!/usr/bin/env python3
"""Judges one run against the approved plan's NFRs: PASS, FAIL or INVALID.

Usage: scripts/evaluate-run.py <run dir> <scenario>
Reads <run dir>/results.jtl (and injector-cpu.csv if present) plus config/nfr.json.
Writes <run dir>/summary.json and <run dir>/summary.md.
Exit 0 = PASS (or VALID for a reference run with no NFR checks, e.g. the baseline), 1 = FAIL, 2 = INVALID.

Percentiles use Apache Commons Math's default (legacy) estimation, the one JMeter's
HTML dashboard uses, so both show the same numbers.
"""

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAT_HEADERS = ("Transaction", "Samples", "Errors %", "Avg ms", "Median", "Min", "Max", "p90", "p95", "p99", "Req/s")


def percentile(values, p):
    """Commons Math Percentile, EstimationType.LEGACY: pos = p * (n + 1) / 100."""
    data = sorted(values)
    n = len(data)
    if n == 0:
        return None
    if n == 1:
        return float(data[0])
    pos = p * (n + 1) / 100
    if pos < 1:
        return float(data[0])
    if pos >= n:
        return float(data[-1])
    lower = math.floor(pos)
    return data[lower - 1] + (pos - lower) * (data[lower] - data[lower - 1])


def stats(samples, window_s=None):
    times = [s["elapsed"] for s in samples]
    n = len(samples)
    errors = sum(not s["success"] for s in samples)
    if window_s is None and n:
        window_s = max((max(s["end"] for s in samples) - min(s["start"] for s in samples)) / 1000, 0.001)
    return {
        "samples": n,
        "errors": errors,
        "error_pct": round(100 * errors / n, 2) if n else None,
        "average": round(sum(times) / n, 1) if n else None,
        "median": round(percentile(times, 50), 1) if n else None,
        "min": min(times) if n else None,
        "max": max(times) if n else None,
        "p90": round(percentile(times, 90), 1) if n else None,
        "p95": round(percentile(times, 95), 1) if n else None,
        "p99": round(percentile(times, 99), 1) if n else None,
        "throughput_rps": round(n / window_s, 3) if n and window_s else None,
    }


def load_samples(jtl):
    samples = []
    with open(jtl, newline="") as f:
        for row in csv.DictReader(f):
            start = int(row["timeStamp"])
            elapsed = int(row["elapsed"])
            samples.append(
                {
                    "label": row["label"],
                    "start": start,
                    "end": start + elapsed,
                    "elapsed": elapsed,
                    "code": row["responseCode"],
                    "success": row["success"] == "true",
                    "cache": row.get("cacheStatus") or "NONE",
                    "remaining": row.get("rateLimitRemaining") or "NONE",
                    "threads": int(row.get("allThreads") or 0),
                }
            )
    return samples


def in_window(samples, t0, window):
    lo, hi = t0 + window[0] * 1000, t0 + window[1] * 1000
    return [s for s in samples if lo <= s["start"] < hi]


def compare(actual, op, value):
    if actual is None:
        return False
    if op == "==":
        return actual == value
    if op == "<":
        return actual < value
    if op == "<=":
        return actual <= value
    if op == "between":
        return value[0] <= actual <= value[1]
    raise ValueError(op)


def run_check(check, samples, t0, labels):
    window = check.get("window")
    subset = in_window(samples, t0, window) if window else samples
    length = (window[1] - window[0]) if window else None
    metric, op, value = check["metric"], check["op"], check["value"]
    results = []
    if metric == "p90-ratio":
        ref = stats(in_window(samples, t0, check["reference_window"]))["p90"]
        cur = stats(subset)["p90"]
        actual = round(cur / ref, 3) if cur is not None and ref else None
        results.append(("overall", actual, compare(actual, op, value), f"{cur} ms vs {ref} ms"))
    elif check["scope"] == "per-transaction":
        key = {"p90": "p90", "average": "average"}[metric]
        for label in labels:
            actual = stats([s for s in subset if s["label"] == label], length)[key]
            results.append((label, actual, compare(actual, op, value), ""))
    else:
        st = stats(subset, length)
        actual = {"error-rate": st["error_pct"], "throughput": st["throughput_rps"]}[metric]
        results.append(("overall", actual, compare(actual, op, value), f"{st['samples']} samples"))
    return {
        **check,
        "results": [{"scope": s, "actual": a, "pass": p, "note": n} for s, a, p, n in results],
        "pass": all(p for _, _, p, _ in results) and bool(results),
    }


def steady_state(spec, samples, t0, labels):
    """Per-transaction stats inside the plan's steady-state window, if the scenario has one."""
    window = spec.get("steady_state")
    if not window:
        return None
    subset = in_window(samples, t0, window)
    length = window[1] - window[0]
    return {
        "window_s": window,
        "overall": stats(subset, length),
        "transactions": {label: stats([s for s in subset if s["label"] == label], length) for label in labels},
    }


def injector_cpu(path, limit):
    if not path.exists():
        return {"available": False}
    values = []
    for line in path.read_text().splitlines():
        parts = line.split(",")
        if len(parts) == 2 and parts[1].strip().isdigit():
            values.append(int(parts[1]))
    rolling = [sum(values[i : i + 3]) / 3 for i in range(max(len(values) - 2, 0))]
    worst = max(rolling) if rolling else (max(values) if values else None)
    return {
        "available": bool(values),
        "samples": len(values),
        "max_pct": max(values) if values else None,
        "worst_15s_avg_pct": round(worst, 1) if worst is not None else None,
        "over_limit": worst is not None and worst > limit,
        "limit_pct": limit,
    }


def suspension_windows(samples, t0, t_end, caps):
    """Any 60 s window (10 s steps) whose error rate is over the plan's suspension threshold."""
    hits = []
    size = caps["suspend_error_window_s"]
    for start in range(0, max(int((t_end - t0) / 1000) - size, 0) + 1, 10):
        sub = in_window(samples, t0, [start, start + size])
        if len(sub) >= 10:
            rate = 100 * sum(not s["success"] for s in sub) / len(sub)
            if rate > caps["suspend_error_rate_pct"]:
                hits.append({"window_s": [start, start + size], "error_pct": round(rate, 1)})
    return hits


def fmt(v):
    return "—" if v is None else (f"{v:g}" if isinstance(v, float) else str(v))


def row(*cells):
    return "| " + " | ".join(str(c) for c in cells) + " |"


def table(*headers):
    return [row(*headers), row(*["---"] * len(headers))]


def stat_row(label, st):
    keys = ("error_pct", "average", "median", "min", "max", "p90", "p95", "p99", "throughput_rps")
    return row(label, st["samples"], *(fmt(st[k]) for k in keys))


def write_markdown(path, s):
    cpu = s["injector_cpu"]
    cpu_text = (
        f"max {cpu['max_pct']}%, worst 15 s average {cpu['worst_15s_avg_pct']}% (limit {cpu['limit_pct']}%)"
        if cpu.get("available")
        else "not recorded"
    )
    lines = [
        f"# {s['scenario_id']} {s['scenario']} — {s['verdict']}",
        "",
        f"- Run folder: `{s['run_dir']}`",
        f"- Plan version: {s['plan_version']}",
        f"- Started: {s['started_utc']} UTC, duration {s['duration_s']} s, peak active threads {s['peak_threads']}",
        f"- Rate-limit (429) responses: {s['rate_limited']}",
        f"- Lowest x-ratelimit-remaining seen: {fmt(s['min_rate_limit_remaining'])}",
        f"- CDN cache split: {', '.join(f'{k} {v}' for k, v in s['cache_split'].items())}",
        f"- Injector CPU: {cpu_text}",
        "",
    ]
    if s["invalid_reasons"]:
        lines += ["**INVALID:** " + "; ".join(s["invalid_reasons"]), ""]
    if s["verdict"] == "VALID":
        lines += ["_Reference run: recorded for comparison, no NFR gates this scenario._", ""]
    lines += ["## Whole run, per transaction", ""]
    lines += table(*STAT_HEADERS)
    lines += [stat_row(label, st) for label, st in s["transactions"].items()]
    lines.append(stat_row("**All**", s["overall"]))
    ss = s.get("steady_state")
    if ss:
        lines += ["", f"## Steady state ({ss['window_s'][0]}–{ss['window_s'][1]} s), per transaction", ""]
        lines += table(*STAT_HEADERS)
        lines += [stat_row(label, st) for label, st in ss["transactions"].items()]
        lines.append(stat_row("**All**", ss["overall"]))
    if s["trend"]:
        lines += ["", "## Trend by window", ""]
        lines += table("Window", "Seconds", "Samples", "Avg ms", "Median", "p90", "Errors %", "Req/s")
        for name, t in s["trend"].items():
            w = t["window_s"]
            cells = (fmt(t[k]) for k in ("average", "median", "p90", "error_pct", "throughput_rps"))
            lines.append(row(name, f"{w[0]}–{w[1]}", t["samples"], *cells))
    if s["checks"]:
        lines += ["", "## NFR checks", ""]
        lines += table("NFR", "Requirement", "Scope", "Actual", "Target", "Result")
        for c in s["checks"]:
            for r in c["results"]:
                actual = f"{fmt(r['actual'])} {r['note']}".strip()
                result = "PASS" if r["pass"] else "**FAIL**"
                lines.append(row(c["nfr"], c["desc"], r["scope"], actual, f"{c['op']} {c['value']}", result))
    path.write_text("\n".join(lines) + "\n")


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: scripts/evaluate-run.py <run dir> <scenario>")
    run_dir = Path(sys.argv[1]).resolve()
    scenario = sys.argv[2]
    nfr = json.loads((ROOT / "config" / "nfr.json").read_text())
    caps, spec = nfr["caps"], nfr["scenarios"][scenario]

    samples = load_samples(run_dir / "results.jtl")
    if not samples:
        print("No samples in results.jtl — INVALID")
        sys.exit(2)
    t0 = min(s["start"] for s in samples)
    t_end = max(s["end"] for s in samples)
    labels = sorted({s["label"] for s in samples})

    remaining = [int(s["remaining"]) for s in samples if s["remaining"].isdigit()]
    cache_split = {}
    for s in samples:
        cache_split[s["cache"]] = cache_split.get(s["cache"], 0) + 1

    summary = {
        "scenario": scenario,
        "scenario_id": spec["id"],
        "plan_version": nfr["plan_version"],
        "run_dir": str(run_dir.relative_to(ROOT)) if run_dir.is_relative_to(ROOT) else str(run_dir),
        "started_utc": datetime.fromtimestamp(t0 / 1000, UTC).strftime("%Y-%m-%d %H:%M:%S"),
        "duration_s": round((t_end - t0) / 1000, 1),
        "peak_threads": max(s["threads"] for s in samples),
        "rate_limited": sum(s["code"] == "429" for s in samples),
        "min_rate_limit_remaining": min(remaining) if remaining else None,
        "cache_split": dict(sorted(cache_split.items())),
        "injector_cpu": injector_cpu(run_dir / "injector-cpu.csv", caps["injector_cpu_max_pct"]),
        "overall": stats(samples),
        "transactions": {label: stats([s for s in samples if s["label"] == label]) for label in labels},
        "steady_state": steady_state(spec, samples, t0, labels),
        "trend": {
            name: {"window_s": w, **stats(in_window(samples, t0, w), w[1] - w[0])}
            for name, w in spec.get("trend_windows", {}).items()
        },
        "suspension_windows": suspension_windows(samples, t0, t_end, caps),
        "checks": [run_check(c, samples, t0, labels) for c in spec["checks"]],
    }

    invalid = []
    if summary["rate_limited"]:
        invalid.append(f"{summary['rate_limited']} rate-limit (429) responses (NFR-07)")
    if summary["injector_cpu"].get("over_limit"):
        invalid.append(
            f"injector CPU {summary['injector_cpu']['worst_15s_avg_pct']}% > {caps['injector_cpu_max_pct']}%"
        )
    if summary["suspension_windows"]:
        invalid.append(
            f"error rate over {caps['suspend_error_rate_pct']}% for {caps['suspend_error_window_s']} s "
            f"(first at {summary['suspension_windows'][0]['window_s']} s)"
        )
    overall_rps = summary["overall"]["throughput_rps"] or 0
    if overall_rps > caps["max_throughput_rps"]:
        invalid.append(f"throughput {overall_rps} req/s over the {caps['max_throughput_rps']} req/s ceiling")
    summary["invalid_reasons"] = invalid
    if invalid:
        summary["verdict"] = "INVALID"
    elif not summary["checks"]:
        summary["verdict"] = "VALID"  # a reference run (baseline): recorded, not gated
    else:
        summary["verdict"] = "PASS" if all(c["pass"] for c in summary["checks"]) else "FAIL"

    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_markdown(run_dir / "summary.md", summary)
    print((run_dir / "summary.md").read_text())
    sys.exit({"PASS": 0, "VALID": 0, "FAIL": 1, "INVALID": 2}[summary["verdict"]])


if __name__ == "__main__":
    main()
