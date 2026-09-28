#!/usr/bin/env python3
"""Collects every run's summary.json into the analysis tables the Test Summary Report is written from.

Usage: scripts/build-report-data.py [--evidence] [results dir]      (default: results/)
Writes reports/analysis.json and reports/analysis.md, and prints the Markdown.
--evidence also refreshes the committed docs/evidence/: each run's summary.md plus analysis.md.
Load comparisons (degradation, repeatability) use the plan's steady-state window, the same window the SLAs use.
Reads only run folders; judges nothing itself (verdicts come from run-perf-test's evaluate-run.py).
"""

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["smoke", "baseline", "load", "stress", "spike"]
REPEATABILITY_PCT = 10  # plan section 7: two load runs are consistent when within 10%


def fmt(v, digits=1):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.{digits}f}".rstrip("0").rstrip(".")
    return str(v)


def row(*cells):
    return "| " + " | ".join(str(c) for c in cells) + " |"


def table(*headers):
    return [row(*headers), row(*["---"] * len(headers))]


def ratio(a, b):
    return round(a / b, 2) if a is not None and b else None


def delta_pct(a, b):
    return round(100 * abs(b - a) / a, 1) if a and b is not None else None


def runs_table(runs):
    md = ["## Runs executed", ""]
    md += table(
        "#",
        "Run folder",
        "Scenario",
        "Started (UTC)",
        "Duration s",
        "Peak threads",
        "Samples",
        "Error %",
        "429s",
        "Min rate-limit remaining",
        "Injector CPU worst 15 s",
        "Verdict",
    )
    for n, r in enumerate(runs, 1):
        o = r["overall"]
        md.append(
            row(
                n,
                f"`{r['run_name']}`",
                f"{r['scenario_id']} {r['scenario']}",
                r["started_utc"],
                fmt(r["duration_s"]),
                r["peak_threads"],
                o["samples"],
                fmt(o["error_pct"], 2),
                r["rate_limited"],
                fmt(r["min_rate_limit_remaining"]),
                f"{fmt(r['injector_cpu'].get('worst_15s_avg_pct'))}%",
                f"**{r['verdict']}**",
            )
        )
    return md


def sla_table(runs):
    md = ["", "## SLA compliance (every check, every valid run)", ""]
    md += table("NFR", "Requirement", "Run", "Scope", "Actual", "Target", "Result")
    for r in runs:
        if r["verdict"] == "INVALID":
            continue
        for c in r["checks"]:
            for res in c["results"]:
                md.append(
                    row(
                        c["nfr"],
                        c["desc"],
                        f"{r['scenario_id']} `{r['run_name']}`",
                        res["scope"],
                        f"{fmt(res['actual'], 3)} {res['note']}".strip(),
                        f"{c['op']} {c['value']}",
                        "PASS" if res["pass"] else "**FAIL**",
                    )
                )
    return md


def run_detail(r):
    md = ["", f"## {r['scenario_id']} {r['scenario']} — `{r['run_name']}` — {r['verdict']}", ""]
    md += table("Transaction", "Samples", "Error %", "Avg", "Median", "Min", "Max", "p90", "p95", "p99", "Req/s")
    for label, t in [*r["transactions"].items(), ("**All**", r["overall"])]:
        md.append(
            row(
                label,
                t["samples"],
                fmt(t["error_pct"], 2),
                fmt(t["average"]),
                fmt(t.get("median")),
                t["min"],
                t["max"],
                fmt(t["p90"]),
                fmt(t["p95"]),
                fmt(t["p99"]),
                fmt(t["throughput_rps"], 3),
            )
        )
    if r["trend"]:
        md += ["", *table("Window", "Seconds", "Samples", "Avg", "Median", "p90", "Error %", "Req/s")]
        for name, t in r["trend"].items():
            md.append(
                row(
                    name,
                    f"{t['window_s'][0]}–{t['window_s'][1]}",
                    t["samples"],
                    fmt(t["average"]),
                    fmt(t.get("median")),
                    fmt(t["p90"]),
                    fmt(t["error_pct"], 2),
                    fmt(t["throughput_rps"], 3),
                )
            )
    md += ["", f"CDN cache split: {', '.join(f'{k} {v}' for k, v in r['cache_split'].items())}."]
    return md


def steady(run):
    """The run's steady-state stats when the scenario has a window, else its whole-run stats."""
    return run.get("steady_state") or {"transactions": run["transactions"], "overall": run["overall"]}


def degradation(base, load):
    md = ["", f"## Load (steady state) vs baseline (whole run) — `{load['run_name']}` vs `{base['run_name']}`", ""]
    md += table("Transaction", "Baseline median", "Load median", "×", "Baseline p90", "Load p90", "×")
    data = {}
    for label, b in base["transactions"].items():
        cur = steady(load)["transactions"].get(label)
        if cur:
            data[label] = {"median_x": ratio(cur.get("median"), b.get("median")), "p90_x": ratio(cur["p90"], b["p90"])}
            md.append(
                row(
                    label,
                    fmt(b.get("median")),
                    fmt(cur.get("median")),
                    fmt(data[label]["median_x"], 2),
                    fmt(b["p90"]),
                    fmt(cur["p90"]),
                    fmt(data[label]["p90_x"], 2),
                )
            )
    return md, data


def repeatability(a, b):
    md = [
        "",
        f"## Load repeatability (consistent when average and p90 are within {REPEATABILITY_PCT}%)",
        "",
        f"Runs: `{a['run_name']}` vs `{b['run_name']}`, steady state (the SLA window).",
        "",
    ]
    md += table(
        "Transaction",
        "Run 1 avg",
        "Run 2 avg",
        "Δ avg %",
        "Run 1 p90",
        "Run 2 p90",
        "Δ p90 %",
        "Run 1 median",
        "Run 2 median",
        "Δ median %",
        "Consistent",
    )
    data = {}
    for label, x in steady(a)["transactions"].items():
        y = steady(b)["transactions"].get(label)
        if not y:
            continue
        d_avg, d_p90 = delta_pct(x["average"], y["average"]), delta_pct(x["p90"], y["p90"])
        d_med = delta_pct(x.get("median"), y.get("median"))
        ok = d_avg <= REPEATABILITY_PCT and d_p90 <= REPEATABILITY_PCT
        data[label] = {"avg_delta_pct": d_avg, "p90_delta_pct": d_p90, "median_delta_pct": d_med, "consistent": ok}
        md.append(
            row(
                label,
                fmt(x["average"]),
                fmt(y["average"]),
                d_avg,
                fmt(x["p90"]),
                fmt(y["p90"]),
                d_p90,
                fmt(x.get("median")),
                fmt(y.get("median")),
                fmt(d_med),
                "yes" if ok else "**no**",
            )
        )
    return md, data


def main():
    args = [a for a in sys.argv[1:] if a != "--evidence"]
    results = Path(args[0]) if args else ROOT / "results"
    runs = []
    for path in sorted(results.glob("*/summary.json")):
        s = json.loads(path.read_text())
        s["run_name"] = path.parent.name
        runs.append(s)
    runs.sort(key=lambda s: s["started_utc"])
    valid = {k: [r for r in runs if r["scenario"] == k and r["verdict"] != "INVALID"] for k in ORDER}

    md = runs_table(runs) + sla_table(runs)
    for r in runs:
        md += run_detail(r)

    analysis = {"runs": [r["run_name"] for r in runs]}
    base = valid["baseline"][-1] if valid["baseline"] else None
    loads = valid["load"]
    if base and loads:
        part, analysis["degradation_vs_baseline"] = degradation(base, loads[-1])
        md += part
    if len(loads) >= 2:
        part, analysis["repeatability"] = repeatability(loads[-2], loads[-1])
        md += part

    out_dir = ROOT / "reports"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "analysis.json").write_text(json.dumps(analysis, indent=2) + "\n")
    text = "\n".join(md) + "\n"
    (out_dir / "analysis.md").write_text(text)
    if "--evidence" in sys.argv:
        evidence = ROOT / "docs" / "evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        for r in runs:
            shutil.copyfile(results / r["run_name"] / "summary.md", evidence / f"{r['run_name']}.md")
        (evidence / "analysis.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
