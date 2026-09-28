# config/profiles/

One file per scenario of the approved plan ([`context/perf-test-plan.md`](../../context/perf-test-plan.md), section 7). `scripts/run-test.sh` passes the chosen file to JMeter with `-q`, and the script reads it with `${__P(name)}`.

| File | Scenario | Shape |
|---|---|---|
| `smoke.properties` | PT-01 Smoke | 1 user, 2 iterations |
| `baseline.properties` | PT-02 Baseline | 1 user, 10 iterations |
| `load.properties` | PT-03 Load | 6 users, 60 s ramp-up, 11 min total |
| `stress.properties` | PT-05 Stress | +3 users every 2 min, 3 → 15, 10 min |
| `spike.properties` | PT-06 Spike | 6 users, +9 in 10 s at 2 min, back to 6 at 4 min, 7 min total |

Keys: `tgN.threads`, `tgN.rampup`, `tgN.delay`, `tgN.duration` and `tgN.loops` for Thread Groups TG1–TG5 (unlisted groups keep 0 threads), plus `pacing.ms`, `think.min.ms` and `think.range.ms`.

Written by `jmeter-test-plan`, using only the numbers in the approved plan. `scripts/check-caps.py <profile>` refuses any profile over the plan's caps (15 users, 15 minutes) before a run starts. Don't add guessed values by hand; change the plan instead.
