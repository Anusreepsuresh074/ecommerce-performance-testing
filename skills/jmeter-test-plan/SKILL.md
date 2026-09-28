---
name: jmeter-test-plan
description: The script-development phase of the standard Performance Testing Life Cycle. Builds the JMeter script (.jmx), one load profile per approved scenario, and the test data from an APPROVED context/perf-test-plan.md, following standard JMeter scripting practice — named business transactions, HTTP Request Defaults, correlation with extractors, parameterisation with CSV and properties, assertions per transaction, think time, pacing, a throughput safety ceiling, stop-on-rate-limit, no heavy listeners — then validates the script offline against a local stub before any real run. Never sends load to the real target; the first real run is run-perf-test's smoke. Use after perf-test-design has been signed off.
---

# JMeter Test Plan

Turns the signed-off Performance Test Plan into files JMeter runs. It's the
**script development** phase of the PTLC: scripting, correlation,
parameterisation, assertions, think time, pacing, and script validation.

## When to use

- After `context/perf-test-plan.md` has status **APPROVED** (step 5 in the
  agent sequence).
- When the approved plan's version changes: rebuild, then re-validate.

## Guardrails

These are hard constraints, not style preferences. If a step below seems to
conflict with one of these, the guardrail wins.

- **Approved plan only.** If `context/perf-test-plan.md` isn't marked
  APPROVED, say `The test plan needs sign-off first (perf-test-design).` and
  stop. Build exactly what the approved version says; a change of transaction,
  number or rule goes back to `perf-test-design`, never improvised here.
- **Write only what this skill owns:** `test-plans/*.jmx`,
  `config/profiles/*.properties`, `data/*.csv`,
  `config/jmeter-common.properties`, and the offline validation suite in
  `tests/offline/`. It may extend `scripts/run-test.sh` only to
  pass `config/jmeter-common.properties`; say so if it does.
- **One script, many profiles.** Every scenario runs the same `.jmx`; load shape
  comes only from the profile file (`${__P(name,default)}`). No scenario-specific
  copies of the script.
- **No hardcoded environment, load or secrets in the `.jmx`.** Host and protocol
  from `config/env/`, load numbers from profiles, credentials from environment
  variables through `${__groovy(System.getenv('NAME'))}` in User Defined
  Variables (`context/perf-auth.md`).
- **Standard scripting conventions:**
  - samplers or Transaction Controllers named by the plan's transaction IDs
    (`T01_Login` …), so reports read in business terms;
  - **HTTP Request Defaults** for protocol, host, timeouts and implementation
    (HttpClient4);
  - **correlation** of dynamic values (tokens, ids) with JSON extractors, each
    with a detectable default (`NOT_FOUND`);
  - **parameterisation** of inputs with CSV Data Set Config or functions;
  - **an assertion on every transaction** (status code plus one content
    check), so a fast wrong answer never counts as a pass;
  - **think time** with timers and **pacing** at the start of each iteration,
    both from properties;
  - **modular structure:** the journey lives once in a Test Fragment, and
    Thread Groups call it with Module Controllers.
- **Safety is built into the script:** a shared Constant Throughput Timer at
  the plan's hard ceiling, and an automatic *stop test now* on the first
  rate-limit response. Thread Group sample-error action: *Start Next Thread
  Loop*.
- **No heavy or leaky elements:** no View Results Tree, Summary Report or other
  GUI listeners, no Debug Sampler or PostProcessor, no saved response data. Load
  runs are non-GUI and results go to `.jtl` only (`context/perf-auth.md`,
  Results and log hygiene).
- **Correct XML.** Build Thread Groups and Loop Controllers in the exact form
  JMeter saves them (copy the structure from JMeter's own
  `bin/templates/*.jmx`), including `LoopController.continue_forever=false`. An
  element missing a property JMeter expects can behave very differently (for
  example, looping forever).
- **No load against the real target.** Verifying CSV values is allowed: one
  request per value, sequential, at least 1 second apart. Script validation
  runs **offline against a local stub** (`tests/offline/`, committed so
  anyone, and CI, can re-run it). The first real run is
  `run-perf-test`'s PT-01 smoke.
- **Profiles must fit the plan's safety caps.** Total users and the longest
  thread-group end time must stay within the approved caps. Check this before
  writing the profile.

## Steps

1. **Read the approved plan** plus `context/perf-auth.md` and
   `context/perf-context.md`.
2. **Test data:** build each CSV from the plan's Test data section. Verify each
   `[To verify]` value with one real request (sequential, at least 1 s apart);
   drop values that fail and say which.
3. **Common properties** (`config/jmeter-common.properties`): the per-sample
   variables to save (`sample_variables`), the results-file settings (CSV, no
   response or sampler data, thread counts, latency, connect time), the
   summariser interval, and the safety ceiling. Make `scripts/run-test.sh` pass
   this file first, before the env and profile files.
4. **Script** (`test-plans/<journey>.jmx`):
   Test Plan (User Defined Variables for credentials) → HTTP Request Defaults →
   a plan-wide HTTP Header Manager (`Accept`, `Accept-Encoding`, an honest
   `User-Agent`) → CSV Data Set Config → Test Fragment (pacing Flow Control
   Action with its timer; a Simple Controller holding the safety timer, the
   header extractors, the rate-limit stop and the transactions in order) →
   Thread Groups `TG1`…`TGn`, each driven by `tgN.*` properties and calling the
   fragment through a Module Controller.
5. **Profiles** (`config/profiles/<scenario>.properties`), one per approved
   scenario: `tgN.threads`, `tgN.rampup`, `tgN.delay`, `tgN.duration`,
   `tgN.loops`, `pacing.ms`, `think.min.ms`, `think.range.ms`, and a comment
   giving the plan's scenario ID. Check each one against the caps.
6. **Validate offline:**
   - Write `tests/offline/stub_server.py`, a local stub that imitates each
     endpoint's success response and the headers the script extracts, and
     records what the script sent (header *presence*, never values);
     `tests/offline/check-offline.py`, the checks; and
     `tests/offline/run-offline-checks.sh`, the runner.
   - Run each profile's structure against it with pacing and think time
     shortened by `-J` overrides: every sampler must run, every assertion must
     pass, extracted values must flow to the next step, and the Authorization
     header must go only to the step that needs it.
   - Check that a stub `429` stops the test.
   - Check that a missing token is caught by an assertion.
   - Confirm the credentials appear nowhere in `jmeter.log` or the `.jtl`.
   - Keep the stub's output in a temporary folder, and delete it afterwards.
7. **Update the README:** the test types, NFRs and how to run each scenario.
8. **Summarise:** the files written, the validation results, and that the next
   step is `run-perf-test` PT-01 smoke against the real target.

## Limitations

This skill must **not**:

- Change the plan's transactions, numbers or rules (`perf-test-design`).
- Run scenarios against the real target, judge results against NFRs
  (`run-perf-test`), or build reports (`perf-report`).
- Add a JMeter plugin without the plan saying so; core JMeter only by default,
  so CI needs nothing extra.

## Notes for reuse across projects

- The structure (fragment + Module Controllers + property-driven Thread Groups)
  fits any closed-workload plan. Add more `TGn` groups if a plan needs more
  steps than the script has.
- If a plan uses an open workload model (arrivals per second instead of users),
  JMeter's core Open Model Thread Group (5.5+) replaces the Thread Groups; the
  fragment stays the same.
- Record the JMeter version in the `.jmx` header and the README; CI must use the
  same version.
