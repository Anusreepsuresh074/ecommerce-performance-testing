# PT-01 smoke — PASS

- Run folder: `results/20260929T063558Z-shopper-journey-smoke`
- Plan version: 1.0
- Started: 2026-09-29 06:36:00 UTC, duration 36.1 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 97
- CDN cache split: DYNAMIC 10
- Injector CPU: max 39%, worst 15 s average 13.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 567 | 567 | 168 | 966 | 966 | 966 | 966 | 0.083 |
| T02_Get_Current_User | 2 | 0 | 128 | 128 | 128 | 128 | 128 | 128 | 128 | 0.089 |
| T03_Browse_Products | 2 | 0 | 132 | 132 | 131 | 133 | 133 | 133 | 133 | 0.088 |
| T04_Search_Products | 2 | 0 | 249.5 | 249.5 | 132 | 367 | 367 | 367 | 367 | 0.092 |
| T05_View_Product | 2 | 0 | 127 | 127 | 126 | 128 | 128 | 128 | 128 | 0.096 |
| **All** | 10 | 0 | 240.7 | 131.5 | 126 | 966 | 906.1 | 966 | 966 | 0.277 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | overall | 0 10 samples | == 0 | PASS |
