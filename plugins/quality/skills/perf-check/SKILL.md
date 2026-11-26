---
name: perf-check
description: "Measure a screen, page, endpoint, query, background task or PR against the project's performance budgets and fix what is over — pick or write the budget first, measure a baseline in release/profile mode on the reference device or environment (3+ runs, median), find the cause with a profiler, change one thing, measure again the same way, guard it with a test or CI threshold, report before and after. Covers app startup, jank, memory, size, battery, web vitals, API latency, slow queries and N+1. Use when a change touches a hot path or something feels slow. Trigger on /perf-check, 'is this fast enough', 'performance', 'slow endpoint', 'slow query', 'jank', 'battery drain', 'app size', 'load test', 'N+1'."
argument-hint: "[screen, page, endpoint, query, task or PR]"
license: MIT
metadata:
  version: "1.1.0"
---

# Perf check

Measure `$ARGUMENTS` (a screen, page, endpoint, query, background task or PR) against the project's performance budgets, and fix what is over. If empty, check the hot paths the current branch's diff touches.

Writing-time rules (no call in a loop, bounded lists, rebuild scope, work off the UI thread) live in the conventions skills: `engineering-principles` principle 11 (lifecycle plugin), `backend-conventions`, `mobile-conventions`, `web-conventions`. This skill **measures and fixes**.

## 0. Read the project

1. Find the budgets file (for example `docs/performance-budgets.md`) and the reference devices/environments it names.
2. Find existing guards: query-count assertions, load-test scripts, bundle-size checks, benchmark projects.
3. Open the reference for the area: [references/backend.md](references/backend.md) · [references/web.md](references/web.md) · [references/mobile.md](references/mobile.md).

No budgets file → propose one (startup, frame time, memory, size, battery, API p95 per route class, query time at 10× today's data) and get the user's OK before measuring against it.

## 1. The loop (always)

1. **Pick the budget** the question is about. No budget fits → write a proposed one into the budgets file first.
2. **Measure the baseline** on the reference device or environment, in **release/profile mode**, 3+ runs, take the median. Debug builds, simulators and a laptop's localhost do not count for app or web performance.
3. **Find the cause** with a profiler, a query plan or a trace — not a guess.
4. **Change one thing.** Measure again exactly the same way.
5. **Guard it** where possible: a query-count test, a plan test, a load-test threshold, a bundle-size limit, a benchmark in CI.
6. **Report** before → after numbers, device/environment, mode, runs, and the change.

**Gate:** a before number exists before any optimisation; an after number exists before the change is called faster.

## 2. Client apps

| Question | Approach |
|---|---|
| Startup | Trace time to first frame / first useful paint; look for work before the first frame, eager initialisation, large asset decoding. |
| Jank in scrolling, maps, animations | Frame timeline in profile mode; rebuild/re-render tracking; narrow what re-renders, cache expensive children, move parsing and geometry off the UI thread, cap item counts (cluster, virtualise). |
| Repeatable numbers | A scripted interaction in an integration test that records frame percentiles (p90/p99) and janky-frame share. |
| Memory | Snapshot after 10 minutes of use; look for growing caches, undisposed controllers/subscriptions, retained images. |
| Size | The platform's size analysis on the release build; remove unused assets and fonts, compress images, split per architecture, check new dependencies' native size. |
| Animations | Stop when off screen and with reduced motion; no controller left running in the background. |

## 3. Battery and background work

Battery is a budget. For background changes: count work per hour (wake-ups, network calls, sensor time) in both active and idle scenarios and compare with the budget; measure on real devices with the platform's battery tooling (reference: mobile). A low-end device is part of the reference set.

## 4. Backend

| Question | Approach |
|---|---|
| Endpoint latency under load | A load-test script with ramping virtual users and think time; thresholds from the budget (p95, error rate). Run against **local or a dedicated test environment**; staging only with the user's OK; **never production**. |
| Hot code path | A micro-benchmark of the function, before and after. |
| Slow query | Read the plan with real execution statistics on 10× realistic synthetic data; look for sequential scans on large tables, missing indexes, missing time predicates on time-partitioned tables, N+1 from the ORM. |
| Slow or frequent queries | The database's statement statistics; a slow-query log threshold in the app (no parameter values logged). |
| Query count of a request | An API test that resets a command counter, calls the endpoint, and asserts the exact count — once with one item and once with several, so an N+1 fails. |
| Fan-out / realtime | Trace from event to delivery; group sizes, backplane load. |

## Rules

- No optimisation without a before number. No "should be faster".
- One change per measurement.
- Never load-test production; never use real users' data for performance fixtures.
- A performance fix must not weaken a safety guarantee (fewer background runs must not delay a critical notification) — check with the safety tests.

## Composition

| From | This skill | To |
|---|---|---|
| `code-review` (dimension 9), `implement` (lifecycle plugin), `background-work` (mobile plugin) | Budget → baseline → cause → one change → guard → report | `observe` (lifecycle) for production signals; `data-check` (backend plugin) for read-only query plans; `device-test` (mobile) for battery rows |
