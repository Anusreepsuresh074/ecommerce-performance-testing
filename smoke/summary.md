# PT-01 smoke — PASS

- Run folder: `results/20260930T060551Z-shopper-journey-smoke`
- Plan version: 1.0
- Started: 2026-09-30 06:05:53 UTC, duration 37.7 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 97
- CDN cache split: DYNAMIC 10
- Injector CPU: max 42%, worst 15 s average 14.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 778 | 778 | 197 | 1359 | 1359 | 1359 | 1359 | 0.083 |
| T02_Get_Current_User | 2 | 0 | 150.5 | 150.5 | 150 | 151 | 151 | 151 | 151 | 0.083 |
| T03_Browse_Products | 2 | 0 | 157.5 | 157.5 | 156 | 159 | 159 | 159 | 159 | 0.081 |
| T04_Search_Products | 2 | 0 | 149 | 149 | 144 | 154 | 154 | 154 | 154 | 0.08 |
| T05_View_Product | 2 | 0 | 166 | 166 | 151 | 181 | 181 | 181 | 181 | 0.086 |
| **All** | 10 | 0 | 280.2 | 155 | 144 | 1359 | 1242.8 | 1359 | 1359 | 0.265 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | overall | 0 10 samples | == 0 | PASS |
