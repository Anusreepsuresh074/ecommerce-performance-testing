---
name: run-perf-test
description: The test-execution phase of the standard Performance Testing Life Cycle. Runs the approved scenarios against the real target in the plan's order (smoke → baseline → load ×2 → stress → spike), enforcing entry criteria (plan approved, smoke passed, caps respected, pre-run rate-limit check), monitoring the load generator's CPU, and judging each run against the plan's NFRs — PASS, FAIL or INVALID — from its results.jtl, using the same percentile method as JMeter's dashboard. Writes config/nfr.json from the approved plan, the execution scripts, and a summary per run. Never changes the plan, the script or the profiles. Use after jmeter-test-plan has built and validated the script.
---

# Run Perf Test

Carries out the **test execution** phase of the PTLC: it enforces the plan's
entry criteria, runs each scenario exactly as approved, watches for the
suspension criteria, and records a verdict per run for `perf-report` to
analyse.

## When to use

- After `jmeter-test-plan` (step 6 in the agent sequence).
- Whenever a scenario needs re-running: a new day, a changed script, a
  suspended or invalid run.

## Guardrails

These are hard constraints, not style preferences. If a step below seems to
conflict with one of these, the guardrail wins.

- **Approved plan, built script.** Stop if `context/perf-test-plan.md` isn't
  APPROVED, or if the script or profiles are missing (`jmeter-test-plan`).
- **Execution order is the plan's.** Smoke (PT-01) first: on each new day and
  after any script change. Nothing else runs until smoke passes. Then the rest
  in the plan's schedule. Never two runs at once; keep the plan's minimum gap
  between runs.
- **Caps are checked before every run, not trusted.** Refuse a profile whose
  total users or end time exceed the plan's caps, or a `-J` override that
  would raise load. Overrides that change the load shape are never used on the
  real target.
- **Pre-run check before every run:** one request that reaches the server (not
  a CDN-cached URL). Go only if it returns `200` and the plan's minimum
  `x-ratelimit-remaining`. Otherwise wait, then check again, up to the plan's
  resumption rule.
- **Verdicts are evidence-based and three-way:**
  - **INVALID:** any rate-limit response, injector CPU over the plan's limit,
    or a suspension criterion met. The result says nothing about the API and
    must not be reported as a pass or a fail.
  - **FAIL:** a valid run that breaks one or more NFRs.
  - **PASS:** a valid run that meets every NFR that applies.
  - **VALID:** a valid reference run with no NFR gates (the baseline). It
    is recorded for comparison and never reported as a pass.
  JMeter's exit code is not a verdict: it exits `0` even after a *stop test
  now*.
- **Percentiles match JMeter's dashboard.** Use Apache Commons Math's default
  (legacy) estimation, `pos = p × (n + 1) / 100`, so the numbers here and in
  `perf-report`'s HTML dashboard agree.
- **Steady state for SLA checks.** Use only the time window the plan names
  (for example, after ramp-up). Report whole-run numbers too, labelled.
- **Thresholds come from the plan, through one file.** Write
  `config/nfr.json` from the approved plan's NFR table, scenario windows and
  caps. The execution scripts read it and hold no numbers of their own.
- **Write only what this skill owns:** `config/nfr.json`,
  `scripts/precheck.sh`, `scripts/check-caps.py`, `scripts/evaluate-run.py`,
  `scripts/run-scenario.sh`, and files inside each run's `results/` folder.
- **Never change the plan, the script, the profiles or the data.** A problem
  goes back to the skill that owns it.
- **No secrets in any output.** The same rules as `context/perf-auth.md`:
  never print `.env`, and never save response bodies.
- **Report honestly.** Say which runs were done, which were skipped and why,
  and give each run's verdict with its numbers, including failures.

## Steps

1. **Check entry criteria:** plan APPROVED, script and profiles present,
   `.env` present (check the variable names only), `jmeter` on `PATH`.
2. **Write `config/nfr.json`** from the approved plan: plan version; caps
   (max users, max duration, max throughput, injector CPU limit, minimum
   rate-limit remaining, gap between runs); and per scenario: its ID, the
   analysis windows (seconds from the first sample) and each check (NFR ID,
   metric, scope, window, operator, value).
3. **Write the execution scripts:**
   - `scripts/check-caps.py <profile>`: total users and latest end time
     against the caps, plus the run rules (the minimum gap since the last
     run, and the maximum runs per scenario per UTC day).
   - `scripts/precheck.sh`: one server-reaching request; checks the status and
     `x-ratelimit-remaining`.
   - `scripts/evaluate-run.py <run dir> <scenario>`: per-transaction samples,
     average, min, max, p90/p95/p99, error %, throughput (whole run and
     windows); `429` count; CDN-cache split; injector CPU; each NFR check →
     `summary.json` + `summary.md` in the run folder; exit code 0 PASS,
     1 FAIL, 2 INVALID.
   - `scripts/run-scenario.sh <scenario>`: check-caps → precheck →
     `run-test.sh` with CPU sampling (from `/proc/stat`, every 5 s) in the background → evaluate.
4. **Run the scenarios in the plan's order**, respecting the gaps. After each
   run, read its summary before starting the next. If smoke fails, stop and
   report.
5. **Summarise:** a table of run → verdict → key numbers, anything invalid or
   skipped with the reason, and that `perf-report` is next.

## Limitations

This skill must **not**:

- Build HTML dashboards or the Test Summary Report (`perf-report`).
- Tune the script or change load to make a test pass.
- Retry a failed run until it passes. A re-run is reported alongside the
  original, never instead of it.

## Notes for reuse across projects

- The scripts are generic: the plan-specific numbers live in
  `config/nfr.json` and the profiles.
- Against a system the team owns, add server-side monitoring (APM, CPU,
  memory, database) to the run folder alongside the injector CPU.
