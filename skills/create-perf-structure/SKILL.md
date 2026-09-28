---
name: create-perf-structure
description: Designs and builds a brand-new JMeter performance testing project from scratch, one layer at a time — confirms the tool version, environments and CI platform, presents the full target folder structure with the reason for each folder, then creates each layer (environment config, load-profile and test-plan shelves, test data, the single run script, output folders, docs) only after explaining what it is, why it exists, and how it connects to the rest. Never writes a test plan (.jmx), load numbers, pass/fail thresholds, or API-specific logic — those belong to perf-test-design, jmeter-test-plan, and get-perf-auth. Use once, at the start of a new performance testing project, when there is no existing structure to extend.
---

# Create Perf Structure

Builds the empty skeleton of a JMeter performance testing project from a
blank repo. This skill's whole job is folders, config plumbing and the one
run script — the shelves that `get-perf-context`, `get-perf-auth`,
`perf-test-design`, `jmeter-test-plan`, `run-perf-test`, `perf-report` and
`perf-ci-integration` fill later. It never writes a `.jmx` test plan, a load
number, a threshold, or anything specific to one API's business logic.

The point is deliberate, explained construction, not a bulk file dump: plan
the whole structure and get it confirmed, then create one layer at a time,
saying what is being created, why it's needed, where it lives and how it
connects to the rest — *before* creating it.

## When to use

- Once, at the very start of a new performance testing project — before any
  other skill in this suite has anything to read.
- Never mid-project "to add a folder" — if the structure already exists,
  extend it by hand; this skill is for a blank repo only.

## Guardrails

These are hard constraints, not style preferences. If a step below seems to
conflict with one of these, the guardrail wins.

- **Plan before you build.** Present the full target tree (see "Target
  structure") with a one-line purpose per folder and get the user's
  confirmation before creating anything.
- **One layer at a time, explained as you go.** After the plan is confirmed,
  create the layers in the order under "Build phases". For each one, say
  what/why/where/how in plain, beginner-friendly English *before* writing
  files, and wait for the user's go-ahead before the next phase.
- **Create only what the current phase needs.** `test-plans/`,
  `config/profiles/` and `data/` start as empty, documented folders (a short
  `README.md` each). Don't pre-create sample `.jmx` files, sample CSVs or
  guessed load profiles.
- **No load numbers, no thresholds.** User counts, ramp-up, duration, think
  time, p95/error-rate limits and safety caps are decided by
  `perf-test-design` and approved by a human. Never put a guessed value in a
  config file here.
- **No business-specific content.** Don't invent endpoints, request bodies or
  user journeys. The only API-specific value this skill writes is the
  confirmed host/protocol per environment (Step 0).
- **No credentials.** Never write a real username, password or token into any
  file. `.env.example` lists variable *names* with empty values; the real
  `.env` stays gitignored.
- **Centralize configuration.** Host, protocol and environment selection live
  in `config/env/<env>.properties` only. Downstream `.jmx` files read them
  through JMeter properties (`${__P(host)}`), never as literals typed into a
  sampler.
- **One way to run.** Every run — local or CI — goes through
  `scripts/run-test.sh`, which calls JMeter in non-GUI mode (`jmeter -n`).
  The GUI is for building and viewing plans only, never for real load runs.
  Downstream skills call this script instead of writing their own `jmeter`
  command lines.
- **Generated output is never committed.** `results/` (raw `.jtl` files,
  `jmeter.log`) and `reports/` (HTML dashboards) are gitignored. Published
  reports reach GitHub Pages through `perf-ci-integration`, not the repo.
- **Meaningful names only.** No `test1.jmx`, `new-folder/`, `misc/`. Every
  folder and file name says what it holds.

## Step 0 — Confirm scope

Before designing anything, confirm (ask if not already stated in the
conversation or in an existing `.claude/agents/perf-automation-agent.md`):

1. **Tool and version.** Default Apache JMeter, the version installed
   locally (`jmeter --version`). Record the exact version — CI must download
   the same one so local and CI results are comparable. If JMeter or Java
   (8+; 17/21 recommended) is missing, say so and ask before installing
   anything.
2. **Environments.** Which environments need entries and their host +
   protocol (e.g. one public `prod`-style host for a demo API). If the target
   is a shared or public service, note it — `perf-test-design` must then set
   strict safety caps.
3. **CI platform.** Default to the one matching the repo's remote (GitHub →
   `.github/workflows/`). This skill does **not** create the workflow —
   `perf-ci-integration` does — it only records the choice in the README.

Don't proceed past this step on assumptions where the answer changes the
structure.

## Target structure

Present this tree, with the purpose column, before creating anything:

```
.
├── config/
│   ├── env/
│   │   └── <env>.properties     # host + protocol per environment — the only place they live
│   └── profiles/                # <test-type>.properties (users, ramp-up, duration) — empty until jmeter-test-plan fills it from the approved plan
├── test-plans/                  # .jmx JMeter test plans — empty until jmeter-test-plan builds them
├── data/                        # CSV test data (search terms, non-secret inputs) — empty until jmeter-test-plan adds it
├── scripts/
│   └── run-test.sh              # the single entry point: jmeter -n with env + profile, timestamped output
├── context/                     # written by get-perf-context / get-perf-auth / perf-test-design, not this skill
├── results/                     # raw .jtl results + jmeter.log per run — gitignored
├── reports/                     # HTML dashboards per run — gitignored
├── skills/                      # this suite's reusable skills (committed)
├── agents/                      # the agent template that runs them in order (committed)
├── .env.example                 # names of secret variables, empty values
├── .gitignore
└── README.md
```

Note in the presentation: `config/profiles/`, `test-plans/` and `data/` are
intentionally empty — they're the shelves `jmeter-test-plan` stocks once a
human has approved `context/perf-test-plan.md`. `context/` is created by
`get-perf-context` when it first writes there.

## Build phases

Create these in order. For each phase, explain what/why/where/how *before*
writing, create only that phase's files, then pause for the user.

1. **Environment configuration** — `config/env/<env>.properties` (one per
   confirmed environment: `protocol`, `host`, optional `port`) and
   `.env.example`.
   *Why:* every test plan needs to know which server to hit without that
   being typed into the plan. *How it connects:* `run-test.sh` passes the
   chosen file to JMeter with `-q`, and `.jmx` samplers read `${__P(host)}`.

2. **Empty shelves** — `config/profiles/README.md`, `test-plans/README.md`,
   `data/README.md`, each stating what belongs there, the naming rule
   (`<test-type>.properties`, `<journey-name>.jmx`, `<purpose>.csv`) and that
   `jmeter-test-plan` fills it.
   *Why:* sets the shape without inventing content. *How it connects:* these
   are exactly the paths `jmeter-test-plan` writes into and `run-test.sh`
   reads from.

3. **Run script** — `scripts/run-test.sh` (executable). Arguments: test plan
   name, profile name, environment (default the first confirmed one).
   Behaviour:
   - fail with a clear message if `jmeter` isn't on `PATH`, or if the named
     `.jmx`, profile or env file doesn't exist;
   - load `.env` if present, without echoing its values;
   - write each run to its own folder,
     `results/<UTC timestamp>-<plan>-<profile>/` (for example
     `20260928T152513Z-…`, matching the UTC times in every report), holding
     `results.jtl` and `jmeter.log` — never overwrite an earlier run;
   - run `jmeter -n -t … -q <env file> -q <profile file> -l … -j …` and exit
     with JMeter's exit code. (`jmeter-test-plan` later adds
     `config/jmeter-common.properties` as the first `-q` file.)
   It does **not** build the HTML dashboard (`perf-report`) or judge
   pass/fail (`run-perf-test`).
   *Why:* one known, repeatable way to run, identical locally and in CI.

4. **Output folders and ignore rules** — make sure `.gitignore` covers
   `results/`, `reports/`, `*.jtl`, `jmeter.log`, `.env` and `.claude/`
   (edit the existing file, don't replace it). No `.gitkeep` is needed —
   `run-test.sh` creates the folders on first run.
   *Why:* raw results are large and change on every run.

5. **Documentation** — `README.md`: what the project is, the folder table
   above, prerequisites (Java, the exact JMeter version), how to run one
   test through `scripts/run-test.sh`, and the skill order. Mark sections that
   later skills will complete (test types, thresholds, report link) as
   `To be added by <skill>` instead of guessing them.
   *Why:* anyone opening the repo — an interviewer included — understands it
   without asking.

## Limitations

This skill must **not**:

- Collect API facts (that's `get-perf-context`) or work out login
  (`get-perf-auth`).
- Decide load numbers, test types or thresholds (`perf-test-design`).
- Build `.jmx` files, profile values or CSV data (`jmeter-test-plan`).
- Run tests or judge results (`run-perf-test`), build reports
  (`perf-report`), or write the CI workflow (`perf-ci-integration`).

If asked to do any of these mid-conversation, name the skill that owns it
instead of doing it here.

## Notes for reuse across projects

- Never hardcode a project's host, API name or domain in this skill file —
  Step 0 supplies those per project.
- The same structure works for any HTTP API tested with JMeter; only the
  environment files change.
- Re-running this skill on a project that already has this structure is out
  of scope.
