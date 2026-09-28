# PT-01 smoke — PASS

- Run folder: `results/20260928T152513Z-shopper-journey-smoke`
- Plan version: 1.0
- Started: 2026-09-28 15:25:15 UTC, duration 39.1 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 96
- CDN cache split: DYNAMIC 10
- Injector CPU: max 13%, worst 15 s average 7.7% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 749 | 749 | 446 | 1052 | 1052 | 1052 | 1052 | 0.082 |
| T02_Get_Current_User | 2 | 0 | 373.5 | 373.5 | 273 | 474 | 474 | 474 | 474 | 0.081 |
| T03_Browse_Products | 2 | 0 | 364 | 364 | 281 | 447 | 447 | 447 | 447 | 0.08 |
| T04_Search_Products | 2 | 0 | 318 | 318 | 297 | 339 | 339 | 339 | 339 | 0.075 |
| T05_View_Product | 2 | 0 | 314 | 314 | 284 | 344 | 344 | 344 | 344 | 0.071 |
| **All** | 10 | 0 | 423.7 | 341.5 | 273 | 1052 | 994.2 | 1052 | 1052 | 0.256 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | overall | 0 10 samples | == 0 | PASS |
