# PT-03 load — PASS

- Run folder: `results/20260928T154706Z-shopper-journey-load`
- Plan version: 1.0
- Started: 2026-09-28 15:47:08 UTC, duration 660.1 s, peak active threads 6
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 85
- CDN cache split: DYNAMIC 794, NONE 1
- Injector CPU: max 11%, worst 15 s average 4.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 161 | 0 | 528.4 | 427 | 307 | 2536 | 772.8 | 1005.6 | 2535.4 | 0.245 |
| T02_Get_Current_User | 160 | 0.62 | 683.6 | 342.5 | 256 | 37102 | 729.3 | 1224.8 | 15747.1 | 0.245 |
| T03_Browse_Products | 159 | 0 | 442.9 | 348 | 263 | 2559 | 661 | 816 | 2268.6 | 0.244 |
| T04_Search_Products | 158 | 0 | 428.6 | 344.5 | 258 | 1798 | 689.6 | 932.5 | 1741.9 | 0.244 |
| T05_View_Product | 157 | 0 | 446.5 | 342 | 250 | 1706 | 742.8 | 996.2 | 1678.7 | 0.243 |
| **All** | 795 | 0.13 | 506.5 | 364 | 250 | 37102 | 720 | 977.6 | 1829.2 | 1.204 |

## Steady state (60–660 s), per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 149 | 0 | 514.4 | 418 | 307 | 2536 | 757 | 909.5 | 2154.5 | 0.248 |
| T02_Get_Current_User | 149 | 0 | 456.7 | 338 | 256 | 2094 | 732 | 1205.5 | 1956.5 | 0.248 |
| T03_Browse_Products | 150 | 0 | 446.1 | 346.5 | 263 | 2559 | 664.6 | 906.4 | 2312.2 | 0.25 |
| T04_Search_Products | 149 | 0 | 430.7 | 344 | 258 | 1798 | 695 | 946 | 1750.5 | 0.248 |
| T05_View_Product | 149 | 0 | 446.1 | 342 | 250 | 1706 | 723 | 997 | 1682.5 | 0.248 |
| **All** | 746 | 0 | 458.8 | 362.5 | 250 | 2559 | 717.2 | 970.9 | 1786.2 | 1.243 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| NFR-01 | p90 per transaction at normal load | T01_Login | 757 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T02_Get_Current_User | 732 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T03_Browse_Products | 664.6 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T04_Search_Products | 695 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | T05_View_Product | 723 | <= 1500 | PASS |
| NFR-02 | average per transaction at normal load | T01_Login | 514.4 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T02_Get_Current_User | 456.7 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T03_Browse_Products | 446.1 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T04_Search_Products | 430.7 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | T05_View_Product | 446.1 | <= 1000 | PASS |
| NFR-03 | error rate at normal load | overall | 0 746 samples | < 1 | PASS |
| NFR-04 | achieved throughput within 10% of 1.25 req/s | overall | 1.243 746 samples | between [1.125, 1.375] | PASS |
