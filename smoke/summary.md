# PT-01 smoke — PASS

- Run folder: `results/20260928T182413Z-shopper-journey-smoke`
- Plan version: 1.0
- Started: 2026-09-28 18:24:15 UTC, duration 36.9 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 90
- CDN cache split: DYNAMIC 10
- Injector CPU: max 41%, worst 15 s average 14.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 559 | 559 | 224 | 894 | 894 | 894 | 894 | 0.083 |
| T02_Get_Current_User | 2 | 0 | 150.5 | 150.5 | 148 | 153 | 153 | 153 | 153 | 0.088 |
| T03_Browse_Products | 2 | 0 | 154.5 | 154.5 | 152 | 157 | 157 | 157 | 157 | 0.09 |
| T04_Search_Products | 2 | 0 | 151 | 151 | 150 | 152 | 152 | 152 | 152 | 0.091 |
| T05_View_Product | 2 | 0 | 146 | 146 | 145 | 147 | 147 | 147 | 147 | 0.09 |
| **All** | 10 | 0 | 232.2 | 152 | 145 | 894 | 827 | 894 | 894 | 0.271 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | overall | 0 10 samples | == 0 | PASS |
