# Performance Test Plan — DummyJSON E-commerce API

## 1. Document control

| Version | Date | Author | Status | Approved by |
|---|---|---|---|---|
| 0.1 | 2026-09-28 | Anusree P (drafted with the perf-test-design skill) | Superseded by 0.2 (informal draft) | — |
| 0.2 | 2026-09-28 | Anusree P (drafted with the perf-test-design skill) | Superseded by 1.0 | — |
| 1.0 | 2026-09-28 | Anusree P (drafted with the perf-test-design skill) | **APPROVED** (clerical notes added after execution: section 16 locations, section 18 resolutions, the section 10 search-term result; no change to scope, numbers or rules) | Anusree P, 2026-09-28 (SLAs, workload model and durations accepted as proposed in section 18) |

Version 0.2 replaces 0.1, the same day. It restructures the plan into the standard Performance Test Plan format, adds a workload model with pacing and Little's Law, adds a Baseline scenario, moves SLAs to the 90th percentile, and adds entry/exit/suspension/resumption criteria.

## 2. Introduction and objectives

This plan covers performance testing of the DummyJSON e-commerce API (`https://dummyjson.com`) with Apache JMeter. It is the planning phase of the standard Performance Testing Life Cycle; scripting starts only after sign-off.

**Objectives:**
1. **Validate the script** under JMeter (smoke).
2. **Establish a single-user baseline** to compare every other result with (baseline).
3. **Measure response time, throughput and error rate at normal load**, and check them against the SLAs (load). Run it twice to show the results repeat.
4. **Find how response time degrades** as load rises step by step to 250% of normal (stress, within the safe budget).
5. **Check the API survives a sudden surge and recovers** (spike).

## 3. Scope

### 3.1 In scope
- The **Shopper journey**, five business transactions: login, current user, product list, product search, product detail (section 6.1).
- Client-side performance metrics measured from the load generator (section 11).

### 3.2 Out of scope

| Item | Reason |
|---|---|
| Breaking-point (capacity) testing | From one IP the rate limit (`LIMIT-rate-100-per-10s`) stops us far below server capacity; breaking a free public service isn't fair use. Stress is redefined as step-up within a safe budget (PT-05). |
| Endurance (soak) testing | A standard soak runs 2–8 hours; that would use hours of someone else's free service. Needs an environment the team owns. |
| Scalability and volume testing | No control over the server's infrastructure or data volume. |
| Server-side monitoring (CPU, memory, APM) | Third-party service; no access (NFR questionnaire). |
| Write transactions (`add`, `PUT`, `PATCH`, `DELETE`) | Simulated; nothing persists, so they don't model real shopper reads (`context/perf-context.md`, Not in scope). |
| `/auth/refresh` | The 60-minute token outlives every scenario (`LIMIT-auth-token-lifetime`). |
| Anonymous browse journey | Kept for a later version of the plan. |

## 4. Application overview

- **What it is:** a free public fake REST API for e-commerce test data. 194 products; JWT login; responses gzip-compressed (`context/perf-context.md`).
- **Architecture as known:** Node.js/Express, with data held in memory rather than in a database. It sits behind Cloudflare, which caches some URLs. The rate limiter runs before every route.
- **Environment:** only one, the public production service (NFR questionnaire).

## 5. Non-functional requirements (SLAs)

The NFR questionnaire (`context/perf-context.md`) found **no stakeholder SLA**, so every target below is an **`[Assumption]` proposed for sign-off**. Each is set relative to the single-user baseline: medians 618–839 ms per transaction, max 1403 ms, over the public internet with a new connection per request.

| ID | Metric | Scope | Target | Source |
|---|---|---|---|---|
| NFR-01 | `p90` response time | per transaction, at normal load (PT-03) | **≤ 1500 ms** | `[Assumption]` about 1.8× the slowest baseline median (839 ms), just above the baseline max (1403 ms), leaving room for internet variance |
| NFR-02 | `average` response time | per transaction, at normal load | **≤ 1000 ms** | `[Assumption]` about 1.2× the slowest baseline median |
| NFR-03 | `error-rate` | overall, at normal load | **< 1%** | `[Assumption]` common QA default for a stable service |
| NFR-04 | `throughput` achieved | overall, at normal load | **within ±10%** of the target 1.25 req/s | standard check that the workload model was actually delivered |
| NFR-05 | `p90` response time and `error-rate` | per transaction, at peak (200% of normal: the 12-user step of PT-05, and the peak of PT-06) | **p90 ≤ 2000 ms, errors < 2%** | `[Assumption]` some slowdown is acceptable at peak |
| NFR-06 | recovery after a spike | `p90` overall, recovery window vs pre-spike window (PT-06) | **≤ 1.2×** the pre-spike p90 | `[Assumption]` "recovered" means back within 20% |
| NFR-07 | `rate-limited` (`429`) | every scenario | **0** | test-validity rule (`LIMIT-rate-100-per-10s`). A `429` means *our load* was wrong, so the run is **invalid**, not failed. |

Reported with every run but **not gated**: average, 95th and 99th percentile, min, max, throughput per transaction, and the degradation of each scenario compared with the baseline (PT-02).

## 6. Workload model

### 6.1 Business transactions

| ID | Transaction name (JMeter) | Request | Mix per iteration |
|---|---|---|---|
| T01 | `T01_Login` | `POST /auth/login`: credentials from `AUTH_USERNAME` / `AUTH_PASSWORD`; extract `accessToken` | 1 (20%) |
| T02 | `T02_Get_Current_User` | `GET /auth/me` with `Authorization: Bearer ${accessToken}` | 1 (20%) |
| T03 | `T03_Browse_Products` | `GET /products?limit=30&skip=${skip}` | 1 (20%) |
| T04 | `T04_Search_Products` | `GET /products/search?q=${term}`; extract a random `productId` | 1 (20%) |
| T05 | `T05_View_Product` | `GET /products/${productId}` | 1 (20%) |

- **One iteration = one shopper session = T01 → T05**, so the mix is equal. A real shop would browse more than it logs in; with no production traffic data to model a weighted mix (NFR questionnaire: volumes not stated), an equal mix keeps every transaction's sample count the same for analysis. `[Assumption]`
- **Login every iteration** (`context/perf-auth.md`, Login frequency).
- **Success checks** (JMeter assertions):
  - T01: `200` and `$.accessToken` exists.
  - T02: `200` and `$.username` exists.
  - T03: `200` and one or more products.
  - T04: `200` and `$.total` > 0.
  - T05: `200` and `$.id` = `productId`.

### 6.2 Think time and pacing

- **Think time (Z):** Uniform Random Timer, 2–4 s (average 3 s), between transactions (4 gaps per iteration, so 12 s). `[Assumption]` Time a shopper spends reading each screen.
- **Pacing:** each virtual user starts a new iteration **every 24 s**, whatever the response times. It's standard practice: it fixes the arrival rate, so the load doesn't drop when the API slows (or rise when it speeds up).
  - Check: baseline R (3.8 s) + Z (12 s) = 15.8 s, which leaves 8.2 s of slack.
  - Pacing holds as long as the average response per transaction stays ≤ 2.4 s. Beyond that, iterations run late, throughput falls short and NFR-04 flags it.

### 6.3 Target load and user sizing (Little's Law)

**Little's Law:** `N = X × (R + Z)`. With pacing, (R + Z) is replaced by the pacing interval, so `N = X × 24 s`.

| Load level | Journeys per hour (X) | X per second | Users N = X × 24 s | Requests/s (N × 5 ÷ 24) | Per 10 s | % of rate limit |
|---|---|---|---|---|---|---|
| Normal (100%) | 900 | 0.25 | **6** | 1.25 | 12.5 | 12.5% |
| Peak (200%) | 1,800 | 0.50 | **12** | 2.50 | 25 | 25% |
| Stress top (250%) | 2,250 | 0.625 | **15** | 3.13 | 31 | 31% |

- **Normal load = 900 journeys/hour** is `[Assumption]`: no volume is stated (NFR questionnaire). It's chosen to use only one-eighth of the rate limit.
- Peak at 200% and stress to 250% of normal are standard multiples.
- The largest level uses **31%** of the limit, keeping the required margin of at least 50%.

## 7. Test scenarios

| ID | Type | Objective | Users | Ramp-up | Steady state | Total | Target throughput | NFRs | Runs |
|---|---|---|---|---|---|---|---|---|---|
| PT-01 | `smoke` | Script validation: every transaction and assertion works | 1 | — | 2 iterations | ~50 s | — | all assertions pass, 0 errors, NFR-07 | 1 per script change, and at the start of each test day |
| PT-02 | `baseline` | Single-user reference times | 1 | — | 10 iterations | ~4 min | 0.21 req/s | reported, not gated; NFR-07 | 1 per test day |
| PT-03 | `load` | SLA check at normal load | 6 | 60 s | 10 min | 11 min | 1.25 req/s | NFR-01 to 04, NFR-07 | **2** (repeatability) |
| PT-04 | — | *(reserved for endurance: out of scope, section 3.2)* | — | — | — | — | — | — | — |
| PT-05 | `stress` (step-up) | Degradation trend from 50% to 250% of normal | 3 → 6 → 9 → 12 → 15 (+3 every 2 min) | 10 s per step | 2 min per step | 10 min | 0.6 → 3.1 req/s | NFR-05 at the 12-user step; NFR-07; p90 per step reported as a trend | 1 |
| PT-06 | `spike` | Surge from normal to 250% and recovery | 6 → 15 → 6 | 10 s to the spike | 2 min normal, 2 min spike, 3 min recovery | 7 min | 1.25 → 3.1 → 1.25 req/s | NFR-05 during the spike, NFR-06, NFR-07 | 1 |

- **Repeatability (PT-03):** two runs count as consistent when average and p90 per transaction are within 10% of each other. If they aren't, investigate (network, time of day) before reporting.
- **Steady-state length:** on an environment the team owns, a load test normally holds steady state for 30–60 minutes. Here it's cut to 10 minutes out of fairness to a free public service; that's still enough for stable percentiles at these sample counts (about 750 samples). `[Assumption]`
- **Approximate requests per run:** smoke 10, baseline 50, load about 790, stress about 1,130, spike about 750.

## 8. Test environment

| Item | Detail |
|---|---|
| Target | `https://dummyjson.com`, public production (the only environment), behind Cloudflare (`config/env/prod.properties`) |
| Differences from a normal perf environment | Shared with every other DummyJSON user; not dedicated, not isolated, not monitored by us |
| Load generator | The local machine (Linux, Java 21), one IP address, over the public internet. CI runs only PT-01 (and PT-03 when started by hand) on GitHub Actions runners, which have different, shared IPs. |
| Effect on results | Response times include internet latency from the load generator's network. Only runs from the same place are comparable. |

## 9. Tools

| Tool | Version | Use |
|---|---|---|
| Apache JMeter | 5.6.3 | Scripting, execution (non-GUI), HTML dashboard |
| Java (OpenJDK) | 21 | JMeter runtime |
| `scripts/run-test.sh` | project | The single way to run a scenario |
| GitHub Actions | — | CI (`perf-ci-integration`) |

## 10. Test data

| Data | Source | Volume | Sharing / selection |
|---|---|---|---|
| Credentials | `.env`: `AUTH_USERNAME`, `AUTH_PASSWORD` (`context/perf-auth.md`) | 1 public test user | Shared by all users (`context/perf-context.md`, Test-data facts) |
| Search terms | `data/search-terms.csv`, column `term` | about 10 | CSV Data Set Config, all threads, recycle at end of file. `phone` is known to return 23 products (functional context). The others (`laptop`, `perfume`, `watch`, `shirt`, `chair`, `lipstick`, `sunglasses`, `bag`, `apple`) are **`[To verify]`** with one request each by `jmeter-test-plan` before the file is committed. *(Verified 2026-09-28: `perfume` returned 0 products and was dropped; the other 9 are in the CSV.)* |
| `skip` (T03) | random multiple of 30 from 0 to 180 | 7 values | Random per iteration, so requests reach the server rather than Cloudflare's cache (`context/perf-context.md`, Environment traits) |
| `productId` (T05) | correlated: a random id from T04's result (`$.products[*].id`, match no. 0) | — | Spreads detail views across the catalog and avoids the cached `/products/1` |

## 11. Metrics and monitoring

- **Client-side, per transaction** (JMeter): samples, average, min, max, p90, p95, p99, error %, throughput, received KB/s, latency, connect time, active threads over time.
- **Extra per-sample fields** in `results.jtl` via `sample_variables`:
  - `cacheStatus` (the `cf-cache-status` header) shows how much was served by the CDN rather than the server;
  - `rateLimitRemaining` (the `x-ratelimit-remaining` header) shows how close the run came to the limit.
- **Server-side:** not available (third-party service). Stated as a limitation in every report.
- **Load-generator health:** CPU and memory of the JMeter machine are sampled during each run by `run-perf-test`. **If the injector's CPU goes over 80%, the run is invalid**, because JMeter itself becomes the bottleneck.
- **No response bodies saved** (`context/perf-auth.md`, Results and log hygiene).

## 12. Entry and exit criteria

### 12.1 Entry criteria (all must hold before PT-02 onwards)
- This plan is signed off (section 1).
- Scripts are built and PT-01 smoke has passed on the current script version.
- Test data is verified (all search terms return results).
- `.env` holds valid credentials.
- Pre-run check passes: one request to the target returns `200` with `x-ratelimit-remaining` ≥ 80.

### 12.2 Exit criteria
- PT-01, PT-02, PT-03 (×2), PT-05 and PT-06 have all run to completion, with valid results (no `429`, injector CPU ≤ 80%).
- Results are analysed against NFR-01 to NFR-07 and the Test Summary Report is produced (`perf-report`).
- Every SLA breach is recorded as an observation, with its evidence.

### 12.3 Suspension criteria (stop the run at once)
- Any `429` response (NFR-07). This is automatic, built into the script.
- Error rate above 10% for more than 1 minute, meaning the target is probably down.
- Injector CPU above 80%.
- The pre-run check fails.

### 12.4 Resumption criteria
- Wait **at least 10 minutes**, then the pre-run check must pass again.
- The cause of the suspension is understood, and fixed if it was on our side (a script or load error).
- Re-run the suspended scenario from its start. A partial run is never reported as a result.

## 13. Safety caps

| Cap | Value |
|---|---|
| Max virtual users | **15** |
| Max duration of one run | **15 minutes** |
| Max throughput | **5 req/s** (50% of the limit), enforced by a Constant Throughput Timer as a safety net above pacing |
| Automatic stop | on the first `429` |
| Between runs | at least **2 minutes**; never two runs in parallel |
| Per day | at most **3** runs each of PT-03, PT-05 and PT-06 |
| CI | PT-01 on every push; PT-03 only when started by hand; PT-05 and PT-06 **local only** |

`run-perf-test` refuses any profile above these caps.

## 14. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Rate limit shared with other traffic on the same IP | `429`, invalid run | 31% max use of the limit, pre-run check, automatic stop |
| Cloudflare cache answers some requests | Times measure the CDN, not the API | Randomized `skip` and `productId`; `cacheStatus` recorded and reported |
| Internet latency varies | Noisy, non-repeatable results | PT-03 run twice; compare only runs from the same place; baseline each day |
| No server-side monitoring | Bottlenecks can't be located on the server | State it in the report; analyse client-side trends only |
| Public service changes or goes down | Tests fail for reasons outside our control | Suspension criteria; re-check `context/perf-context.md` facts if behaviour changes |
| Injector overload | JMeter becomes the bottleneck | Non-GUI only, no heavy listeners, CPU monitored |

## 15. Assumptions and dependencies

- All SLAs, the normal load of 900 journeys/hour, the equal transaction mix, and the think time and pacing are **assumptions** (sections 5 and 6), accepted at sign-off on 2026-09-28.
- DummyJSON stays available and keeps the behaviour recorded in `context/perf-context.md` (2026-09-28).
- One shared public test user is acceptable for all virtual users.

## 16. Deliverables

| Deliverable | Produced by | Location |
|---|---|---|
| Performance Test Plan (this document) | `perf-test-design` | `context/perf-test-plan.md` |
| JMeter scripts, load profiles, test data | `jmeter-test-plan` | `test-plans/`, `config/profiles/`, `data/` |
| Raw results and logs per run | `run-perf-test` | `results/` (not committed) |
| HTML dashboard per run | `perf-report` | `reports/` (not committed), published by CI |
| Test Summary Report: SLA compliance table, graphs, observations, recommendations | `perf-report` | `docs/test-summary-report.md` (committed, linked from the README), with charts in `docs/images/` and per-run evidence in `docs/evidence/` |
| CI workflow | `perf-ci-integration` | `.github/workflows/` |

## 17. Execution schedule

In this order, following section 13's gaps and caps:

1. PT-01 Smoke. If it fails, fix the script and repeat.
2. PT-02 Baseline.
3. PT-03 Load, run 1.
4. PT-03 Load, run 2, then the repeatability check.
5. PT-05 Stress.
6. PT-06 Spike.
7. Analysis and Test Summary Report.

## 18. Open questions for sign-off

**Resolved at sign-off (2026-09-28):** questions 1–3 were accepted as proposed. For question 4, the pre-run check ran before every scenario and passed each time (readings 96–99 of 100 at the start of each run).

1. **Approve the assumed SLAs** in section 5: p90 ≤ 1500 ms at normal load, ≤ 2000 ms at peak, errors < 1% (normal) and < 2% (peak). Alternatively, sign off after the baseline (PT-02) and adjust.
2. **Approve the workload model:** normal load of 900 journeys/hour (6 users), peak 200% (12 users), stress up to 250% (15 users), pacing 24 s.
3. **Approve the durations:** load has a 10-minute steady state, cut from the usual 30–60 minutes out of fairness to a public service.
4. **Network:** one request showed `x-ratelimit-remaining: 50`. If your network is shared (an office, for example), the pre-run check will catch it, but runs from home give cleaner results.

---
**Signed off 2026-09-28 (version 1.0). `jmeter-test-plan` may build from this version.**
