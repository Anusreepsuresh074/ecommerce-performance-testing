# PT-01 smoke — PASS

- Run folder: `results/20260929T015410Z-shopper-journey-smoke`
- Plan version: 1.0
- Started: 2026-09-29 01:54:13 UTC, duration 36.4 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 95
- CDN cache split: DYNAMIC 10
- Injector CPU: max 43%, worst 15 s average 15.0% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 323.5 | 323.5 | 204 | 443 | 443 | 443 | 443 | 0.083 |
| T02_Get_Current_User | 2 | 0 | 90.5 | 90.5 | 90 | 91 | 91 | 91 | 91 | 0.083 |
| T03_Browse_Products | 2 | 0 | 98.5 | 98.5 | 98 | 99 | 99 | 99 | 99 | 0.087 |
| T04_Search_Products | 2 | 0 | 94.5 | 94.5 | 94 | 95 | 95 | 95 | 95 | 0.091 |
| T05_View_Product | 2 | 0 | 90.5 | 90.5 | 90 | 91 | 91 | 91 | 91 | 0.087 |
| **All** | 10 | 0 | 139.5 | 94.5 | 90 | 443 | 419.1 | 443 | 443 | 0.274 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | overall | 0 10 samples | == 0 | PASS |
