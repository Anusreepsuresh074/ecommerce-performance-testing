# test-plans/

JMeter test plans: `<journey-name>.jmx`, one per user journey. Built by `jmeter-test-plan` from the approved [`context/perf-test-plan.md`](../context/perf-test-plan.md).

## `shopper-journey.jmx`

```
DummyJSON Shopper Journey (Test Plan)
├── User Defined Variables      username / password  ← ${__groovy(System.getenv('AUTH_USERNAME'))} …
├── HTTP Request Defaults       protocol + host from config/env/*.properties, HttpClient4, 10 s connect / 30 s response timeout
├── HTTP Header Manager         Accept: application/json, Accept-Encoding: gzip, an honest User-Agent
├── CSV Data Set Config         ../data/search-terms.csv → ${term} (all threads, recycle)
├── Test Fragment "Shopper Journey"          ← the journey, defined once
│   ├── Flow Control Action "Pacing"          + JSR223 Timer: next iteration starts pacing.ms after the last one
│   └── Simple Controller "Journey T01-T05"
│       ├── Constant Throughput Timer          safety ceiling 300 samples/min, shared by all threads
│       ├── Regex Extractors (headers)         cf-cache-status → cacheStatus, x-ratelimit-remaining → rateLimitRemaining
│       ├── JSR223 PostProcessor               stop the whole test on the first 429
│       ├── T01_Login                          POST /auth/login → JSON Extractor accessToken · assert 200 + $.accessToken
│       ├── T02_Get_Current_User               GET /auth/me + Header Manager "Bearer ${accessToken}" · assert 200 + $.username
│       ├── T03_Browse_Products                GET /products?limit=30&skip=<random 0–180> · assert 200 + a product
│       ├── T04_Search_Products                GET /products/search?q=${term} → random productId · assert 200 + total > 0
│       └── T05_View_Product                   GET /products/${productId} · assert 200 + $.id = productId
│       (T02–T05 each carry a Uniform Random Timer: think time from think.min.ms + think.range.ms)
└── Thread Groups TG1 … TG5     each: tgN.threads / rampup / delay / duration / loops from the profile,
                                on sample error → start next loop, Module Controller → the fragment
```

## Transaction mix and timing

From the plan, sections 6.1–6.3. Every virtual user runs the whole journey once per iteration, so the mix is equal.

| Transaction | Share of requests | Think time before it | Notes |
|---|---|---|---|
| `T01_Login` | 20% | none (first step) | logs in every iteration |
| `T02_Get_Current_User` | 20% | 2–4 s, uniform random | Bearer token from T01 |
| `T03_Browse_Products` | 20% | 2–4 s, uniform random | random `skip` to avoid CDN cache hits |
| `T04_Search_Products` | 20% | 2–4 s, uniform random | term from `data/search-terms.csv` |
| `T05_View_Product` | 20% | 2–4 s, uniform random | `productId` correlated from T04 |

| Setting | Value | Property |
|---|---|---|
| Think time | 2–4 s per gap (average 3 s), 4 gaps, so about 12 s per iteration | `think.min.ms=2000`, `think.range.ms=2000` |
| Pacing | one iteration starts every 24 s per user, whatever the response times | `pacing.ms=24000` |
| Rate per user | 5 requests / 24 s = 0.208 req/s | derived |
| Users (Little's Law, `N = X × 24 s`) | normal 6 (1.25 req/s), peak 12 (200%), stress top and spike peak 15 (250%) | `tgN.threads` in each profile |
| Safety ceiling | 300 samples/min (5 req/s), shared by all threads | Constant Throughput Timer |

Why it's built this way:

- **One script, every scenario.** The load shape lives only in `config/profiles/<scenario>.properties`. Five property-driven Thread Groups are enough for step-up (stress) and surge (spike) shapes in core JMeter, with no plugins, so CI needs nothing extra.
- **Correlation, not hard-coding:** the token and the product id are extracted at run time, each with a `NOT_FOUND` default that an assertion catches.
- **No Cookie Manager, on purpose.** DummyJSON accepts the login cookie as auth, so a cookie would hide a broken Bearer header ([`context/perf-auth.md`](../context/perf-auth.md)).
- **No listeners.** Results go to `results.jtl` only, and response bodies (which hold tokens) are never saved.

Open the plan in the JMeter GUI (`jmeter -t test-plans/shopper-journey.jmx`) to read or edit it. Run it only through `scripts/run-scenario.sh` (non-GUI).
