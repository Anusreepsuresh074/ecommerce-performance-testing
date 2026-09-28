# PT-06 spike — PASS

- Run folder: `results/20260928T161214Z-shopper-journey-spike`
- Plan version: 1.0
- Started: 2026-09-28 16:12:15 UTC, duration 420.0 s, peak active threads 15
- Rate-limit (429) responses: 0
- Lowest x-ratelimit-remaining seen: 82
- CDN cache split: DYNAMIC 742
- Injector CPU: max 12%, worst 15 s average 5.3% (limit 80%)

## Whole run, per transaction

| Transaction | Samples | Errors % | Avg ms | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 150 | 0 | 490.4 | 399.5 | 304 | 1932 | 796.9 | 930.2 | 1883 | 0.359 |
| T02_Get_Current_User | 149 | 0 | 398.4 | 334 | 260 | 2348 | 640 | 710 | 1951.5 | 0.361 |
| T03_Browse_Products | 149 | 0 | 394.9 | 337 | 266 | 2269 | 532 | 731.5 | 1794.5 | 0.362 |
| T04_Search_Products | 148 | 0 | 374.3 | 324.5 | 258 | 1894 | 506.5 | 650.5 | 1441.7 | 0.362 |
| T05_View_Product | 146 | 0 | 392.7 | 327.5 | 256 | 2388 | 527.5 | 618.3 | 2261.6 | 0.361 |
| **All** | 742 | 0 | 410.4 | 346.5 | 256 | 2388 | 576.8 | 737 | 1796 | 1.767 |

## Trend by window

| Window | Seconds | Samples | Avg ms | Median | p90 | Errors % | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pre-spike | 60–120 | 73 | 407.9 | 372 | 564.4 | 0 | 1.217 |
| spike | 120–240 | 375 | 404.9 | 328 | 559.8 | 0 | 3.125 |
| recovery | 360–420 | 78 | 368.1 | 339.5 | 495.3 | 0 | 1.3 |

## NFR checks

| NFR | Requirement | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- |
| NFR-05 | p90 per transaction during the spike (15 users) | T01_Login | 729 | <= 2000 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | T02_Get_Current_User | 689.4 | <= 2000 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | T03_Browse_Products | 509.4 | <= 2000 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | T04_Search_Products | 517.8 | <= 2000 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | T05_View_Product | 476.6 | <= 2000 | PASS |
| NFR-05 | error rate during the spike | overall | 0 375 samples | < 2 | PASS |
| NFR-06 | recovery: last 60 s p90 vs pre-spike p90 | overall | 0.878 495.3 ms vs 564.4 ms | <= 1.2 | PASS |
