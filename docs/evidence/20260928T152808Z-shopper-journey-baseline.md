# PT-02 baseline — VALID

- Run folder: `results/20260928T152808Z-shopper-journey-baseline`
- Plan version: 1.0
- Started: 2026-09-28 15:28:10 UTC, duration 230.5 s, peak active threads 1
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 91
- CDN cache split: DYNAMIC 50
- Injector CPU: max 13%, worst 15 s average 6.3% (limit 80%)

_Reference run: recorded for comparison, no NFR gates this scenario._

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 10 | 0 | 483.8 | 367 | 302 | 1119 | 1092.9 | 1119 | 1119 | 0.046 |
| T02_Get_Current_User | 10 | 0 | 336.9 | 300.5 | 275 | 582 | 562.3 | 582 | 582 | 0.046 |
| T03_Browse_Products | 10 | 0 | 439.6 | 406 | 283 | 594 | 590.2 | 594 | 594 | 0.047 |
| T04_Search_Products | 10 | 0 | 405.7 | 371 | 286 | 691 | 667.8 | 691 | 691 | 0.046 |
| T05_View_Product | 10 | 0 | 383.6 | 355 | 297 | 480 | 479 | 480 | 480 | 0.046 |
| **All** | 50 | 0 | 409.9 | 360 | 275 | 1119 | 579.4 | 766.2 | 1119 | 0.217 |
