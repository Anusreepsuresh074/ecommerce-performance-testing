## Runs executed

| # | Run folder | Scenario | Started (UTC) | Duration s | Peak threads | Samples | Error % | 429s | Min rate-limit remaining | Injector CPU worst 15 s | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `20260928T152513Z-shopper-journey-smoke` | PT-01 smoke | 2026-09-28 15:25:15 | 39.1 | 1 | 10 | 0 | 0 | 96 | 7.7% | **PASS** |
| 2 | `20260928T152808Z-shopper-journey-baseline` | PT-02 baseline | 2026-09-28 15:28:10 | 230.5 | 1 | 50 | 0 | 0 | 91 | 6.3% | **VALID** |
| 3 | `20260928T153403Z-shopper-journey-load` | PT-03 load | 2026-09-28 15:34:04 | 659.6 | 6 | 801 | 0 | 0 | 71 | 4.7% | **PASS** |
| 4 | `20260928T154706Z-shopper-journey-load` | PT-03 load | 2026-09-28 15:47:08 | 660.1 | 6 | 795 | 0.13 | 0 | 85 | 4.3% | **PASS** |
| 5 | `20260928T160010Z-shopper-journey-stress` | PT-05 stress | 2026-09-28 16:00:12 | 599 | 15 | 1125 | 0 | 0 | 76 | 4.3% | **PASS** |
| 6 | `20260928T161214Z-shopper-journey-spike` | PT-06 spike | 2026-09-28 16:12:15 | 420 | 15 | 742 | 0 | 0 | 82 | 5.3% | **PASS** |

## SLA compliance (every check, every valid run)

| NFR | Requirement | Run | Scope | Actual | Target | Result |
| --- | --- | --- | --- | --- | --- | --- |
| PT-01 | every transaction and assertion passes | PT-01 `20260928T152513Z-shopper-journey-smoke` | overall | 0 10 samples | == 0 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T01_Login | 685.7 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T02_Get_Current_User | 593.6 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T03_Browse_Products | 632.4 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T04_Search_Products | 497.8 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T05_View_Product | 713.6 | <= 1500 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T01_Login | 477.1 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T02_Get_Current_User | 406.2 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T03_Browse_Products | 411 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T04_Search_Products | 399.6 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | T05_View_Product | 434.6 | <= 1000 | PASS |
| NFR-03 | error rate at normal load | PT-03 `20260928T153403Z-shopper-journey-load` | overall | 0 751 samples | < 1 | PASS |
| NFR-04 | achieved throughput within 10% of 1.25 req/s | PT-03 `20260928T153403Z-shopper-journey-load` | overall | 1.252 751 samples | between [1.125, 1.375] | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T01_Login | 757 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T02_Get_Current_User | 732 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T03_Browse_Products | 664.6 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T04_Search_Products | 695 | <= 1500 | PASS |
| NFR-01 | p90 per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T05_View_Product | 723 | <= 1500 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T01_Login | 514.4 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T02_Get_Current_User | 456.7 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T03_Browse_Products | 446.1 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T04_Search_Products | 430.7 | <= 1000 | PASS |
| NFR-02 | average per transaction at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | T05_View_Product | 446.1 | <= 1000 | PASS |
| NFR-03 | error rate at normal load | PT-03 `20260928T154706Z-shopper-journey-load` | overall | 0 746 samples | < 1 | PASS |
| NFR-04 | achieved throughput within 10% of 1.25 req/s | PT-03 `20260928T154706Z-shopper-journey-load` | overall | 1.243 746 samples | between [1.125, 1.375] | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | PT-05 `20260928T160010Z-shopper-journey-stress` | T01_Login | 796.2 | <= 2000 | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | PT-05 `20260928T160010Z-shopper-journey-stress` | T02_Get_Current_User | 728.2 | <= 2000 | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | PT-05 `20260928T160010Z-shopper-journey-stress` | T03_Browse_Products | 531.7 | <= 2000 | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | PT-05 `20260928T160010Z-shopper-journey-stress` | T04_Search_Products | 504.7 | <= 2000 | PASS |
| NFR-05 | p90 per transaction at peak (12-user step) | PT-05 `20260928T160010Z-shopper-journey-stress` | T05_View_Product | 693.5 | <= 2000 | PASS |
| NFR-05 | error rate at peak (12-user step) | PT-05 `20260928T160010Z-shopper-journey-stress` | overall | 0 301 samples | < 2 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | PT-06 `20260928T161214Z-shopper-journey-spike` | T01_Login | 729 | <= 2000 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | PT-06 `20260928T161214Z-shopper-journey-spike` | T02_Get_Current_User | 689.4 | <= 2000 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | PT-06 `20260928T161214Z-shopper-journey-spike` | T03_Browse_Products | 509.4 | <= 2000 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | PT-06 `20260928T161214Z-shopper-journey-spike` | T04_Search_Products | 517.8 | <= 2000 | PASS |
| NFR-05 | p90 per transaction during the spike (15 users) | PT-06 `20260928T161214Z-shopper-journey-spike` | T05_View_Product | 476.6 | <= 2000 | PASS |
| NFR-05 | error rate during the spike | PT-06 `20260928T161214Z-shopper-journey-spike` | overall | 0 375 samples | < 2 | PASS |
| NFR-06 | recovery: last 60 s p90 vs pre-spike p90 | PT-06 `20260928T161214Z-shopper-journey-spike` | overall | 0.878 495.3 ms vs 564.4 ms | <= 1.2 | PASS |

## PT-01 smoke — `20260928T152513Z-shopper-journey-smoke` — PASS

| Transaction | Samples | Error % | Avg | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 2 | 0 | 749 | 749 | 446 | 1052 | 1052 | 1052 | 1052 | 0.082 |
| T02_Get_Current_User | 2 | 0 | 373.5 | 373.5 | 273 | 474 | 474 | 474 | 474 | 0.081 |
| T03_Browse_Products | 2 | 0 | 364 | 364 | 281 | 447 | 447 | 447 | 447 | 0.08 |
| T04_Search_Products | 2 | 0 | 318 | 318 | 297 | 339 | 339 | 339 | 339 | 0.075 |
| T05_View_Product | 2 | 0 | 314 | 314 | 284 | 344 | 344 | 344 | 344 | 0.071 |
| **All** | 10 | 0 | 423.7 | 341.5 | 273 | 1052 | 994.2 | 1052 | 1052 | 0.256 |

CDN cache split: DYNAMIC 10.

## PT-02 baseline — `20260928T152808Z-shopper-journey-baseline` — VALID

| Transaction | Samples | Error % | Avg | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 10 | 0 | 483.8 | 367 | 302 | 1119 | 1092.9 | 1119 | 1119 | 0.046 |
| T02_Get_Current_User | 10 | 0 | 336.9 | 300.5 | 275 | 582 | 562.3 | 582 | 582 | 0.046 |
| T03_Browse_Products | 10 | 0 | 439.6 | 406 | 283 | 594 | 590.2 | 594 | 594 | 0.047 |
| T04_Search_Products | 10 | 0 | 405.7 | 371 | 286 | 691 | 667.8 | 691 | 691 | 0.046 |
| T05_View_Product | 10 | 0 | 383.6 | 355 | 297 | 480 | 479 | 480 | 480 | 0.046 |
| **All** | 50 | 0 | 409.9 | 360 | 275 | 1119 | 579.4 | 766.2 | 1119 | 0.217 |

CDN cache split: DYNAMIC 50.

## PT-03 load — `20260928T153403Z-shopper-journey-load` — PASS

| Transaction | Samples | Error % | Avg | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 162 | 0 | 486.1 | 400 | 304 | 2617 | 724.5 | 841.8 | 2153.3 | 0.246 |
| T02_Get_Current_User | 161 | 0 | 401.7 | 326 | 259 | 2395 | 593.2 | 723 | 2359.7 | 0.246 |
| T03_Browse_Products | 160 | 0 | 417.4 | 340.5 | 270 | 1942 | 632.4 | 848.3 | 1878.6 | 0.246 |
| T04_Search_Products | 160 | 0 | 399.4 | 336 | 254 | 2498 | 504.8 | 697.7 | 2096 | 0.246 |
| T05_View_Product | 158 | 0 | 438.2 | 336.5 | 255 | 2464 | 716 | 1022.7 | 2230.4 | 0.245 |
| **All** | 801 | 0 | 428.7 | 352 | 254 | 2617 | 621.8 | 808.8 | 1880.5 | 1.214 |

CDN cache split: DYNAMIC 801.

## PT-03 load — `20260928T154706Z-shopper-journey-load` — PASS

| Transaction | Samples | Error % | Avg | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 161 | 0 | 528.4 | 427 | 307 | 2536 | 772.8 | 1005.6 | 2535.4 | 0.245 |
| T02_Get_Current_User | 160 | 0.62 | 683.6 | 342.5 | 256 | 37102 | 729.3 | 1224.8 | 15747.1 | 0.245 |
| T03_Browse_Products | 159 | 0 | 442.9 | 348 | 263 | 2559 | 661 | 816 | 2268.6 | 0.244 |
| T04_Search_Products | 158 | 0 | 428.6 | 344.5 | 258 | 1798 | 689.6 | 932.5 | 1741.9 | 0.244 |
| T05_View_Product | 157 | 0 | 446.5 | 342 | 250 | 1706 | 742.8 | 996.2 | 1678.7 | 0.243 |
| **All** | 795 | 0.13 | 506.5 | 364 | 250 | 37102 | 720 | 977.6 | 1829.2 | 1.204 |

CDN cache split: DYNAMIC 794, NONE 1.

## PT-05 stress — `20260928T160010Z-shopper-journey-stress` — PASS

| Transaction | Samples | Error % | Avg | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 225 | 0 | 502.5 | 409 | 292 | 2124 | 795.8 | 930.2 | 1806.5 | 0.386 |
| T02_Get_Current_User | 225 | 0 | 459.2 | 338 | 256 | 3466 | 698.4 | 1140.4 | 2974.5 | 0.386 |
| T03_Browse_Products | 225 | 0 | 447.6 | 344 | 261 | 2623 | 646.2 | 1007.4 | 2473.5 | 0.386 |
| T04_Search_Products | 225 | 0 | 398.8 | 338 | 253 | 1337 | 605.6 | 802.8 | 1276.2 | 0.385 |
| T05_View_Product | 225 | 0 | 448 | 353 | 245 | 2861 | 729.8 | 913.5 | 2466.7 | 0.385 |
| **All** | 1125 | 0 | 451.2 | 352 | 245 | 3466 | 701.4 | 903 | 2167.7 | 1.878 |

| Window | Seconds | Samples | Avg | Median | p90 | Error % | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 users | 0–120 | 77 | 516.8 | 413 | 848.6 | 0 | 0.642 |
| 6 users | 120–240 | 151 | 426 | 367 | 645.6 | 0 | 1.258 |
| 9 users | 240–360 | 226 | 480.1 | 353.5 | 711.4 | 0 | 1.883 |
| 12 users | 360–480 | 301 | 409.6 | 342 | 655.4 | 0 | 2.508 |
| 15 users | 480–600 | 370 | 464.1 | 340 | 755.6 | 0 | 3.083 |

CDN cache split: DYNAMIC 1125.

## PT-06 spike — `20260928T161214Z-shopper-journey-spike` — PASS

| Transaction | Samples | Error % | Avg | Median | Min | Max | p90 | p95 | p99 | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 150 | 0 | 490.4 | 399.5 | 304 | 1932 | 796.9 | 930.2 | 1883 | 0.359 |
| T02_Get_Current_User | 149 | 0 | 398.4 | 334 | 260 | 2348 | 640 | 710 | 1951.5 | 0.361 |
| T03_Browse_Products | 149 | 0 | 394.9 | 337 | 266 | 2269 | 532 | 731.5 | 1794.5 | 0.362 |
| T04_Search_Products | 148 | 0 | 374.3 | 324.5 | 258 | 1894 | 506.5 | 650.5 | 1441.7 | 0.362 |
| T05_View_Product | 146 | 0 | 392.7 | 327.5 | 256 | 2388 | 527.5 | 618.3 | 2261.6 | 0.361 |
| **All** | 742 | 0 | 410.4 | 346.5 | 256 | 2388 | 576.8 | 737 | 1796 | 1.767 |

| Window | Seconds | Samples | Avg | Median | p90 | Error % | Req/s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pre-spike | 60–120 | 73 | 407.9 | 372 | 564.4 | 0 | 1.217 |
| spike | 120–240 | 375 | 404.9 | 328 | 559.8 | 0 | 3.125 |
| recovery | 360–420 | 78 | 368.1 | 339.5 | 495.3 | 0 | 1.3 |

CDN cache split: DYNAMIC 742.

## Load (steady state) vs baseline (whole run) — `20260928T154706Z-shopper-journey-load` vs `20260928T152808Z-shopper-journey-baseline`

| Transaction | Baseline median | Load median | × | Baseline p90 | Load p90 | × |
| --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 367 | 418 | 1.14 | 1092.9 | 757 | 0.69 |
| T02_Get_Current_User | 300.5 | 338 | 1.12 | 562.3 | 732 | 1.3 |
| T03_Browse_Products | 406 | 346.5 | 0.85 | 590.2 | 664.6 | 1.13 |
| T04_Search_Products | 371 | 344 | 0.93 | 667.8 | 695 | 1.04 |
| T05_View_Product | 355 | 342 | 0.96 | 479 | 723 | 1.51 |

## Load repeatability (consistent when average and p90 are within 10%)

Runs: `20260928T153403Z-shopper-journey-load` vs `20260928T154706Z-shopper-journey-load`, steady state (the SLA window).

| Transaction | Run 1 avg | Run 2 avg | Δ avg % | Run 1 p90 | Run 2 p90 | Δ p90 % | Run 1 median | Run 2 median | Δ median % | Consistent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01_Login | 477.1 | 514.4 | 7.8 | 685.7 | 757 | 10.4 | 391.5 | 418 | 6.8 | **no** |
| T02_Get_Current_User | 406.2 | 456.7 | 12.4 | 593.6 | 732 | 23.3 | 329 | 338 | 2.7 | **no** |
| T03_Browse_Products | 411 | 446.1 | 8.5 | 632.4 | 664.6 | 5.1 | 340.5 | 346.5 | 1.8 | yes |
| T04_Search_Products | 399.6 | 430.7 | 7.8 | 497.8 | 695 | 39.6 | 334 | 344 | 3 | **no** |
| T05_View_Product | 434.6 | 446.1 | 2.6 | 713.6 | 723 | 1.3 | 337 | 342 | 1.5 | yes |
