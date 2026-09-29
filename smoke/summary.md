# PT-01 smoke — PASS

- Run folder: `results/20260929T092113Z-shopper-journey-smoke`
- Plan version: 1.0
- Started: 2026-09-29 09:21:16 UTC, duration 34.0 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 97
- CDN cache split: DYNAMIC 10
- Injector CPU: max 42%, worst 15 s average 14.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 399 | 399 | 45 | 753 | 753 | 753 | 753 | 0.083 |
| T02_Get_Current_User | 2 | 0 | 12.5 | 12.5 | 12 | 13 | 13 | 13 | 13 | 0.085 |
| T03_Browse_Products | 2 | 0 | 17.5 | 17.5 | 17 | 18 | 18 | 18 | 18 | 0.089 |
| T04_Search_Products | 2 | 0 | 16.5 | 16.5 | 15 | 18 | 18 | 18 | 18 | 0.09 |
| T05_View_Product | 2 | 0 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 0.095 |
| **All** | 10 | 0 | 92.1 | 16 | 12 | 753 | 682.2 | 753 | 753 | 0.294 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | overall | 0 10 samples | == 0 | PASS |
