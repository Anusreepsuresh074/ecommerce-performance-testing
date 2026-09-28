# PT-05 stress — PASS

- Run folder: `results/20260928T160010Z-shopper-journey-stress`
- Plan version: 1.0
- Started: 2026-09-28 16:00:12 UTC, duration 599.0 s, peak active threads 15
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 76
- CDN cache split: DYNAMIC 1125
- Injector CPU: max 11%, worst 15 s average 4.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 225 | 0 | 502.5 | 409 | 292 | 2124 | 795.8 | 930.2 | 1806.5 | 0.386 |
| T02_Get_Current_User | 225 | 0 | 459.2 | 338 | 256 | 3466 | 698.4 | 1140.4 | 2974.5 | 0.386 |
| T03_Browse_Products | 225 | 0 | 447.6 | 344 | 261 | 2623 | 646.2 | 1007.4 | 2473.5 | 0.386 |
| T04_Search_Products | 225 | 0 | 398.8 | 338 | 253 | 1337 | 605.6 | 802.8 | 1276.2 | 0.385 |
| T05_View_Product | 225 | 0 | 448 | 353 | 245 | 2861 | 729.8 | 913.5 | 2466.7 | 0.385 |
| **All** | 1125 | 0 | 451.2 | 352 | 245 | 3466 | 701.4 | 903 | 2167.7 | 1.878 |

## Trend by window

| Window | Seconds | Samples | Avg ms | Median | p90 | Errors % | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 users | 0–120 | 77 | 516.8 | 413 | 848.6 | 0 | 0.642 |
| 6 users | 120–240 | 151 | 426 | 367 | 645.6 | 0 | 1.258 |
| 9 users | 240–360 | 226 | 480.1 | 353.5 | 711.4 | 0 | 1.883 |
| 12 users | 360–480 | 301 | 409.6 | 342 | 655.4 | 0 | 2.508 |
| 15 users | 480–600 | 370 | 464.1 | 340 | 755.6 | 0 | 3.083 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| NFR-05 | p90 per transaction at peak (12-user step) | T01_Login | 796.2 | <= 2000 | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | T02_Get_Current_User | 728.2 | <= 2000 | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | T03_Browse_Products | 531.7 | <= 2000 | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | T04_Search_Products | 504.7 | <= 2000 | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | T05_View_Product | 693.5 | <= 2000 | PASS |
| NFR-05 | error rate at peak (12-user step) | overall | 0 301 samples | < 2 | PASS |
