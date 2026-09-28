# PT-03 load — PASS

- Run folder: `results/20260928T180910Z-shopper-journey-load`
- Plan version: 1.0
- Started: 2026-09-28 18:09:11 UTC, duration 658.9 s, peak active threads 6
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 42
- CDN cache split: DYNAMIC 796, NONE 1
- Injector CPU: max 29%, worst 15 s average 10.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 162 | 0.62 | 222.4 | 166.5 | 63 | 2280 | 308.4 | 500 | 1451.6 | 0.246 |
| T02_Get_Current_User | 160 | 0 | 122.8 | 105 | 80 | 859 | 220 | 273.9 | 507.6 | 0.246 |
| T03_Browse_Products | 159 | 0 | 121 | 106 | 83 | 815 | 131 | 279 | 670.4 | 0.245 |
| T04_Search_Products | 159 | 0 | 112.5 | 104 | 81 | 672 | 123 | 273 | 518.4 | 0.245 |
| T05_View_Product | 157 | 0 | 130.6 | 109 | 81 | 665 | 240.2 | 284.3 | 565.2 | 0.244 |
| **All** | 797 | 0.13 | 142.2 | 112 | 63 | 2280 | 240.2 | 283 | 801.3 | 1.21 |

## Steady state (60–660 s), per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 150 | 0.67 | 205.4 | 161.5 | 63 | 965 | 302.8 | 420.4 | 956.3 | 0.25 |
| T02_Get_Current_User | 149 | 0 | 121.4 | 105 | 80 | 859 | 220 | 267 | 571 | 0.248 |
| T03_Browse_Products | 149 | 0 | 120.6 | 106 | 83 | 815 | 131 | 279 | 694.5 | 0.248 |
| T04_Search_Products | 149 | 0 | 111.9 | 104 | 81 | 672 | 122 | 200 | 544 | 0.248 |
| T05_View_Product | 149 | 0 | 127.8 | 109 | 81 | 665 | 237 | 280 | 527 | 0.248 |
| **All** | 746 | 0.13 | 137.5 | 112 | 63 | 965 | 228 | 279 | 740.4 | 1.243 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| NFR-01 | p90 per transaction at normal load | T01_Login | 302.8 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T02_Get_Current_User | 220 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T03_Browse_Products | 131 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T04_Search_Products | 122 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T05_View_Product | 237 | <= 1500 | PASS |
| NFR-02 | average per transaction at normal load | T01_Login | 205.4 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T02_Get_Current_User | 121.4 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T03_Browse_Products | 120.6 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T04_Search_Products | 111.9 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T05_View_Product | 127.8 | <= 1000 | PASS |
| NFR-03 | error rate at normal load | overall | 0.13 746 samples | < 1 | PASS |
| NFR-04 | achieved throughput within 10% of 1.25 req/s | overall | 1.243 746 samples | between [1.125, 1.375] | PASS |
