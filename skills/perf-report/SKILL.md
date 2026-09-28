---
name: perf-report
description: The result-analysis and reporting phase of the standard Performance Testing Life Cycle. Builds JMeter's HTML dashboard for each run (with Apdex set from the plan's SLA) and writes the committed Test Summary Report — executive summary with a go/no-go style verdict, the executed-runs log, SLA compliance per NFR, per-transaction results, baseline comparison, load repeatability, the stress degradation trend, spike recovery, observations with evidence, bottlenecks, recommendations, deviations from plan and limitations. Reads run-perf-test's results and summaries; never re-runs or re-judges them. Use after run-perf-test, or standalone on the runs already on disk.
---

# Perf Report

Turns raw runs into the documents stakeholders read: the **analysis and
reporting** phase of the PTLC. Two outputs:

- an **HTML dashboard per run** (JMeter's own report generator): the detailed
  graphs;
- the **Test Summary Report** (`docs/test-summary-report.md`, committed): the
  analysed result against the plan's SLAs.

## When to use

- After `run-perf-test` (step 7 in the agent sequence).
- Standalone, to re-report the runs already in `results/` (for example after
  adding a run).

## Guardrails

These are hard constraints, not style preferences. If a step below seems to
conflict with one of these, the guardrail wins.

- **Report what ran, as it ran.** Verdicts come from each run's
  `summary.json` (`run-perf-test`). Never re-judge a run, drop a failing or
  invalid run, or present a re-run instead of the original — list both.
- **Every claim has evidence:** a run folder, a number, a window. An
  observation without data is labelled as a hypothesis.
- **Standard metrics, the plan's percentile.** SLA tables use p90 (the plan's
  SLA metric), with average, p95, p99, min, max, error % and throughput
  alongside. Dashboard and summary numbers must agree (same percentile
  method); if they don't, say so rather than picking one.
- **Apdex from the plan.** The dashboard's satisfied threshold is the plan's
  normal-load p90 SLA; tolerated is 4× that (the Apdex standard).
- **Distinguish the three verdicts.** INVALID runs are listed with their
  reason and excluded from SLA conclusions.
- **Limitations are stated, not hidden:** no server-side monitoring, public
  internet latency, one load generator, shortened durations, assumed SLAs.
- **Write only:** `reports/<run>/` dashboards (not committed),
  `config/report.properties`, `scripts/build-dashboard.sh`,
  `scripts/build-report-data.py`, `scripts/build-charts.py`,
  `docs/test-summary-report.md`, `docs/images/` and `docs/evidence/`, plus the
  README's results section.
- **Evidence travels with the report.** Raw results and dashboards aren't
  committed, so copy each run's `summary.md` and the analysis tables into
  `docs/evidence/`, and link them from the report, so a reader can check
  every number without the raw files.
- **Charts follow data-visualisation rules:** one y-axis per panel (never a
  dual axis; two measures go in two panels), SLA lines drawn as dashed
  reference lines, a validated colour-blind-safe palette with light and dark
  variants, direct labels, and a table of the same numbers next to each
  chart.
- **No secrets.** Dashboards are built from `.jtl` files that hold no bodies;
  check that none are embedded before publishing.

## Steps

1. **Collect runs:** every `results/*/summary.json`, newest per scenario plus
   any earlier runs of the same day. Note INVALID and not-started runs.
2. **Build dashboards:** `scripts/build-dashboard.sh <run dir>` →
   `reports/<run>/index.html`, with `config/report.properties` (Apdex, title,
   granularity, the transactions filter that keeps only `T0n_` samples).
3. **Compute the analysis data** (`scripts/build-report-data.py`):
   - SLA compliance per NFR, taken from the summaries;
   - per-transaction tables per scenario;
   - load vs baseline degradation (p90 and average ratios);
   - repeatability of the two load runs (average and p90 per transaction
     within 10%);
   - the stress trend (p90 and throughput per step);
   - spike windows (pre-spike, spike, recovery);
   - the CDN cache split and the lowest rate-limit headroom.
4. **Draw the charts** (`scripts/build-charts.py`): load repeatability (p90
   over time, both runs), the stress trend (response time and throughput per
   step) and the spike timeline (p90 over time plus active users). Render
   them and look at them before using them.
5. **Copy the evidence** into `docs/evidence/`.
6. **Write `docs/test-summary-report.md`** with the template below. Write the
   observations and recommendations from the data; each one cites its
   evidence. Before publishing, re-check every number in the prose against
   the data.
7. **Update the README** results section: the headline verdict, the SLA table
   and a link to the report and dashboards.

## Output template (`docs/test-summary-report.md`)

```markdown
# Performance Test Summary Report — <application>

## 1. Document control
## 2. Executive summary
<overall verdict; 3–5 key findings; recommendation>
## 3. Test execution summary
| Run | Scenario | Date (UTC) | Duration | Peak users | Samples | Verdict |
## 4. Test environment and conditions
## 5. SLA compliance
| NFR | Requirement | Scenario | Target | Actual | Status |
## 6. Detailed results
### 6.1 Baseline (PT-02)
### 6.2 Load (PT-03) — including repeatability and degradation vs baseline
### 6.3 Stress (PT-05) — degradation trend
### 6.4 Spike (PT-06) — surge and recovery
## 7. Observations
## 8. Bottlenecks and risks
## 9. Recommendations
## 10. Deviations from the test plan
## 11. Limitations
## 12. Appendix: run folders, dashboards, how to reproduce
```

## Limitations

This skill must **not**:

- Run tests (`run-perf-test`), change the plan (`perf-test-design`), or tune
  the script (`jmeter-test-plan`).
- Claim a server-side cause without server-side evidence.

## Notes for reuse across projects

- The scripts read only the run folders and `config/nfr.json`; nothing in them
  is specific to this API.
- With server-side monitoring available, add a "Resource utilisation" section
  (CPU, memory, database, GC) and correlate it with the response-time graphs;
  that's where most real bottlenecks are found.
