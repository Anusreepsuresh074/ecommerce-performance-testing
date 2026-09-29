# PT-01 smoke — PASS

- Run folder: `results/20260929T052823Z-shopper-journey-smoke`
- Plan version: 1.0
- Started: 2026-09-29 05:28:25 UTC, duration 37.8 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 97
- CDN cache split: DYNAMIC 10
- Injector CPU: max 45%, worst 15 s average 15.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 839 | 839 | 217 | 1461 | 1461 | 1461 | 1461 | 0.083 |
| T02_Get_Current_User | 2 | 0 | 186.5 | 186.5 | 186 | 187 | 187 | 187 | 187 | 0.085 |
| T03_Browse_Products | 2 | 0 | 190 | 190 | 187 | 193 | 193 | 193 | 193 | 0.089 |
| T04_Search_Products | 2 | 0 | 191 | 191 | 189 | 193 | 193 | 193 | 193 | 0.086 |
| T05_View_Product | 2 | 0 | 193 | 193 | 187 | 199 | 199 | 199 | 199 | 0.08 |
| **All** | 10 | 0 | 319.9 | 191 | 186 | 1461 | 1336.6 | 1461 | 1461 | 0.264 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | overall | 0 10 samples | == 0 | PASS |
