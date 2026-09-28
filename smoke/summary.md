# PT-01 smoke — PASS

- Run folder: `results/20260928T180456Z-shopper-journey-smoke`
- Plan version: 1.0
- Started: 2026-09-28 18:04:58 UTC, duration 36.8 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 97
- CDN cache split: DYNAMIC 10
- Injector CPU: max 33%, worst 15 s average 11.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 544 | 544 | 180 | 908 | 908 | 908 | 908 | 0.083 |
| T02_Get_Current_User | 2 | 0 | 140 | 140 | 134 | 146 | 146 | 146 | 146 | 0.087 |
| T03_Browse_Products | 2 | 0 | 149.5 | 149.5 | 142 | 157 | 157 | 157 | 157 | 0.087 |
| T04_Search_Products | 2 | 0 | 147.5 | 147.5 | 145 | 150 | 150 | 150 | 150 | 0.086 |
| T05_View_Product | 2 | 0 | 132.5 | 132.5 | 131 | 134 | 134 | 134 | 134 | 0.084 |
| **All** | 10 | 0 | 222.7 | 145.5 | 131 | 908 | 835.2 | 908 | 908 | 0.272 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | overall | 0 10 samples | == 0 | PASS |
