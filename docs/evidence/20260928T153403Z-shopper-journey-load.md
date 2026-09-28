# PT-03 load — PASS

- Run folder: `results/20260928T153403Z-shopper-journey-load`
- Plan version: 1.0
- Started: 2026-09-28 15:34:04 UTC, duration 659.6 s, peak active threads 6
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 71
- CDN cache split: DYNAMIC 801
- Injector CPU: max 11%, worst 15 s average 4.7% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 162 | 0 | 486.1 | 400 | 304 | 2617 | 724.5 | 841.8 | 2153.3 | 0.246 |
| T02_Get_Current_User | 161 | 0 | 401.7 | 326 | 259 | 2395 | 593.2 | 723 | 2359.7 | 0.246 |
| T03_Browse_Products | 160 | 0 | 417.4 | 340.5 | 270 | 1942 | 632.4 | 848.3 | 1878.6 | 0.246 |
| T04_Search_Products | 160 | 0 | 399.4 | 336 | 254 | 2498 | 504.8 | 697.7 | 2096 | 0.246 |
| T05_View_Product | 158 | 0 | 438.2 | 336.5 | 255 | 2464 | 716 | 1022.7 | 2230.4 | 0.245 |
| **All** | 801 | 0 | 428.7 | 352 | 254 | 2617 | 621.8 | 808.8 | 1880.5 | 1.214 |

## Steady state (60–660 s), per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 150 | 0 | 477.1 | 391.5 | 304 | 2617 | 685.7 | 797 | 2241.6 | 0.25 |
| T02_Get_Current_User | 150 | 0 | 406.2 | 329 | 259 | 2395 | 593.6 | 735.8 | 2365.9 | 0.25 |
| T03_Browse_Products | 150 | 0 | 411 | 340.5 | 270 | 1942 | 632.4 | 821.3 | 1652.3 | 0.25 |
| T04_Search_Products | 151 | 0 | 399.6 | 334 | 254 | 2498 | 497.8 | 744.6 | 2155.3 | 0.252 |
| T05_View_Product | 150 | 0 | 434.6 | 337 | 255 | 2464 | 713.6 | 1013.7 | 2262 | 0.25 |
| **All** | 751 | 0 | 425.7 | 353 | 254 | 2617 | 614.6 | 791 | 1910.3 | 1.252 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| NFR-01 | p90 per transaction at normal load | T01_Login | 685.7 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T02_Get_Current_User | 593.6 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T03_Browse_Products | 632.4 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T04_Search_Products | 497.8 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T05_View_Product | 713.6 | <= 1500 | PASS |
| NFR-02 | average per transaction at normal load | T01_Login | 477.1 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T02_Get_Current_User | 406.2 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T03_Browse_Products | 411 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T04_Search_Products | 399.6 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T05_View_Product | 434.6 | <= 1000 | PASS |
| NFR-03 | error rate at normal load | overall | 0 751 samples | < 1 | PASS |
| NFR-04 | achieved throughput within 10% of 1.25 req/s | overall | 1.252 751 samples | between [1.125, 1.375] | PASS |
