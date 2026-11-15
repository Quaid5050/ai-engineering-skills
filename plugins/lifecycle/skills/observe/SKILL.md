---
name: observe
description: "Answer health questions from production signals, or add the signals a change needs so someone finds out about a failure before a user does — pin the window, read errors, metrics, traces and logs, compare with a baseline, keep facts apart from theories; when adding signals, errors reach the error tracker, metrics use low-cardinality tags with no personal data, traces wrap hot paths and outbound calls, logs follow the privacy logging rule, every safety signal gets an alert rule and an owner, and a test proves the signal fires on the failure path. Use after a release, when something looks slow or broken, or while building a new failure mode. Trigger on /observe, 'is the release healthy', 'why is it slow', 'error rate', 'add metrics', 'add monitoring', 'add an alert', 'instrument this'."
argument-hint: "[question | add <change>]"
license: MIT
metadata:
  version: "1.0.0"
---

# Observe

`$ARGUMENTS` is either a **question** ("is the 2.3.0 release healthy?", "why are notifications slow since 14:00?") or `add <change>` to instrument new behaviour. Default environment: the one named, else local.

## 0. Read the project

From `AGENTS.md` and the repo: which error tracker, metrics, tracing and log backends exist, how instruments are named and registered, where alert rules live (as code if possible), health endpoints, dashboards, and the targets for each signal. **What is not wired yet** is said as such: until it is, "observe" means local logs and the test suite, and the first instrument sets it up as its own issue.

## 1. The signals that matter

Adapt to the product; keep the safety ones first.

| Signal | Why | Typical target |
|---|---|---|
| Crash-free sessions / users per release and platform | Client stability | ≥ 99.5% |
| Delivery success and lag of critical notifications or messages | Safety and trust | 100% delivered or a fallback sent; p95 lag within the spec |
| Freshness of background data (share of users whose last sync is recent) | Background work silently killed | Per OS version and device maker |
| Server 5xx rate and p95/p99 latency per route | Backend health | 5xx < 0.5%; latency per budget |
| Queue/backlog lag, failed jobs, outbox age | Pipeline health | No growing backlog |
| Client-side offline queue: depth and **age of the oldest unsent record**, reported on reconnect | Data stuck on devices (killed background work, a poison record, storage full) | Oldest unsent record younger than the spec allows |
| Scheduled jobs: runs, duplicates prevented by the sent-ledger, lag behind schedule | Missed or doubled scheduled effects | Zero missed runs; lag within the spec |
| Third-party provider errors (payments, email, SMS, push) | Delivery channels | Alert when the error rate rises |

## 2. Answer a question

1. Pin the **time window** and the **environment**.
2. Read the signals that answer it: error tracker (release, platform, issue list, breadcrumbs), metrics and dashboards, traces, logs filtered by trace id.
3. **Compare** with the previous release or the same window last week.
4. Report facts with links and numbers, separate from theories.

**Gate:** every statement in the answer cites a signal or is labelled a theory. A user-visible problem → `incident`; a bug → `investigate-bug`.

## 3. Add signals for a change (`add`)

For every new failure mode the change introduces, someone must find out **without a user telling us**:

- **Errors:** unexpected exceptions reach the global handler or the error tracker with context; caught errors on safety paths are reported through one helper. Never an empty catch.
- **Metrics:** counters and histograms named `<app>.<area>.<thing>` (e.g. `shop.orders.payment_result`, `shop.notifications.lag_seconds`), tags with **low cardinality only** (`platform`, `result`, `channel`). Never user ids, emails, free text or locations as tags.
- **Traces:** a span around each hot-path operation, each batch, and each outbound call (payments, messaging, other services).
- **Logs:** structured, with named placeholders; follow the privacy logging rule in `security-privacy-review` (quality plugin): no personal data, tokens or precise locations in anything shipped off the device or server. Pseudonymous ids are fine in logs, never as metric tags.
- **Alerts:** each safety signal gets a rule with a threshold, a window and an **owner**, written as code where the project supports it, and named in the PR.
- **Product analytics** (did people use it?) are separate: `analytics-event` (quality plugin).

**Test the signal:** a unit or integration test asserts the metric or error is recorded on the failure path (an in-memory metric listener, a fake error transport).

**Gate:** each new failure mode maps to a signal, an alert (if safety-relevant) and a test.

## Rules

- Read-only in production: observing never changes data or configuration.
- No personal data in telemetry; scrub before sending (a tested scrubber hook in the error reporter).
- Every new safety-critical path ships with its metric and alert — **no observability = not done**.
- Small samples are not trends; say how many events a number is based on.

## Composition

| From | This skill | To |
|---|---|---|
| `release` (watch windows), `implement` (new failure modes) | Answers or new signals | `incident`, `investigate-bug`, `perf-check` (quality) |
