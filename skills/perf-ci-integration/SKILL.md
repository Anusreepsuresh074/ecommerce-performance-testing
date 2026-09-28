---
name: perf-ci-integration
description: The continuous-performance-testing phase of the standard Performance Testing Life Cycle. Wires the approved scenarios into CI (GitHub Actions by default) within the plan's CI rules — which scenarios run on push or pull request, which only by hand, which never in CI — with the same pinned JMeter version (checksum-verified), secrets from the CI secret store, one run at a time, the same caps, pre-run check and verdict as local runs, the dashboard and summary as artifacts, and the dashboard published to GitHub Pages. Never adds a scenario the plan keeps out of CI. Use once the scenarios pass locally; re-run when the plan's CI rules change.
---

# Perf CI Integration

Makes performance testing continuous: every change to the script is
smoke-tested against the real target, and the heavier approved scenarios can
be started from CI on demand, with results published. This is the **CI**
phase of the PTLC.

## When to use

- After `run-perf-test` has passed smoke locally and `perf-report` works (step
  8 in the agent sequence).
- When the plan's CI rules, the JMeter version or the secrets change.

## Guardrails

These are hard constraints, not style preferences. If a step below seems to
conflict with one of these, the guardrail wins.

- **The plan decides what runs in CI.** Follow the plan's CI rules exactly:
  triggers per scenario, and scenarios that are *local only* (for example
  because CI runners share IPs and a rate limit). Never add a scenario, a
  schedule or a matrix that multiplies load beyond the plan.
- **One run at a time.** A workflow-level concurrency group, never
  cancelling a run already in progress (a half-run is invalid and wasted
  load).
- **Same run path as local.** CI calls `scripts/run-scenario.sh`, so caps,
  pre-run check, CPU sampling and the verdict are identical. No CI-only
  JMeter command lines and no `-J` overrides of load.
- **Pinned, verified tool.** The exact JMeter version from the plan, from
  Apache's permanent archive, checked against its SHA-512 before use, and
  cached.
- **Secrets from the secret store only**, named as in `context/perf-auth.md`.
  If they're missing (forks, Dependabot pull requests), skip with a clear
  notice instead of failing a login against the real target.
- **Verdict gates the job:** PASS → green; FAIL or INVALID → red, with the
  summary on the run page. Artifacts upload whatever the verdict.
- **Publish only from trusted events** (push to the main branch, manual
  runs), never from pull requests.
- **Honour the pre-run check.** If it says no-go, retry a few times a minute
  apart; if still no-go, fail with that reason. Never skip the check.
- **Write only:** `.github/workflows/perf.yml`, `.github/dependabot.yml`
  (action updates), and the README's CI section.

## Steps

1. **Read the plan's CI rules** (scenarios, triggers, local-only list) and the
   JMeter version.
2. **Write `.github/workflows/perf.yml`:**
   - triggers per the plan, with a manual scenario picker limited to the
     CI-allowed scenarios;
   - a concurrency group;
   - the job: checkout → Java (the runner's preinstalled version when
     available) → cached, checksum-verified JMeter → secrets check →
     `scripts/run-scenario.sh` with pre-run retries → dashboard → run-page
     summary → artifacts;
   - a publish job for trusted events that puts the dashboard on GitHub Pages
     under the scenario's name, with an index page.
3. **Dependabot for actions**, so action versions stay current.
4. **Update the README CI section:** badge, triggers, what's local only and
   why, the required secrets, and the Pages setup.
5. **Summarise** the one-time repository setup the user must do: secrets and
   the Pages source.

## Limitations

This skill must **not**:

- Change scenarios, caps or thresholds (`perf-test-design`), or the script
  (`jmeter-test-plan`).
- Push commits or change repository settings. It lists them for the user.

## Notes for reuse across projects

- For a system the team owns, a scheduled nightly load run against a
  dedicated environment is the usual next step, with results compared to the
  previous night's to catch regressions.
- A self-hosted runner gives a fixed IP and hardware, making CI results
  comparable run to run; shared hosted runners don't.
