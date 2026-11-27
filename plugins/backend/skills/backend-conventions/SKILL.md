---
name: backend-conventions
description: "How a backend service is structured and written on any stack — layered modules with feature folders (edge → application → domain, persistence, adapters, workers, a hot-path module), what each layer may do and call, thin edges, two kinds of validation, errors as results mapped to problem details, data access through the ORM's unit of work, transactions and locks owned by the use case, time and cancellation, logging without personal data, options validated at start, one secret per purpose, resilience with one retry owner, background work, performance, data integrity and allowlist architecture tests. Use when writing or reviewing server code. Trigger on 'backend conventions', 'where does this go in the backend', 'service layer', 'business logic in the controller', 'repository or ORM', 'request/response DTO', 'validator', 'how do I structure this endpoint', 'transaction', 'N+1'."
argument-hint: "[backend change, file to place, or diff]"
license: MIT
metadata:
  version: "2.0.0"
---

# Backend conventions

How server code is laid out and written. Apply it to `$ARGUMENTS` (a change, a file to place, or a diff). If empty, apply it to the change in hand. The **why** is `engineering-principles` (lifecycle plugin); this skill is the backend **how**. Stack idioms: [references/dotnet.md](references/dotnet.md), [references/django.md](references/django.md), [references/node.md](references/node.md), [references/spring.md](references/spring.md).

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

1. Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, the project's conventions doc and its placement table, and `docs/decisions/` (or `docs/adr/`).
2. Identify the stack from the manifest (build file, package manifest, lock file) and open the matching reference above; if none matches, map the generic rules below onto the stack's own community conventions and say so.
3. Find the existing modules, the architecture tests, the test host and the commands (build, test, lint, migrations). Use the project's names; this skill's names are placeholders.

**Gate:** you know which module and folder each part of the change lands in, by the project's own table or by §1–§2 below.

## 1. Modules and layers

**Pick the profile first.** If the project records an architecture profile (a placement table, a decision record, architecture tests), follow it: active-record applications, libraries and systems code have legitimate shapes of their own. **If the project has no profile, use the default profile** in [references/default-profile.md](references/default-profile.md) — open it whenever you place a file or review imports: the module table with the domain allowlist, the concept test, thin-edge limits and the architecture tests.

The default profile's shape:

```
  Edge (HTTP handlers, consumers, job entry points, realtime socket methods or channels)
                       │ calls one use case
                       ▼
  Application (use-case services, one per feature area)
        │                 │                     │
        ▼                 ▼                     ▼
     Domain          Persistence         Ports (interfaces) for outside systems
 (rules, no I/O)   (ORM context, mappings,   implemented by adapters
                    queries, locks, migrations)
```

Plus adapters (implement ports over vendors, never decide *whether* to act), workers (thin jobs calling application services) and an optional hot-path module reached only through its published types.

- **Domain** holds business concepts only, and imports only its allowlist. A type goes in Domain only if it passes the **concept test** (a product person would recognise it); pure technical code (codecs, encodings, HMACs) sits behind a port in the module that owns the technology — unless the project's profile is itself technical (a compiler, a codec library).
- **Ports** isolate dependencies outside the process or meaningful test boundaries; no interface that merely mirrors one in-process implementation.

**Gate:** each new file sits in one module of the selected profile and its imports are inside that module's allowlist.

## 2. Rules by topic

**Edges are thin.** Take inputs, validate shape, pass the caller's identity (a plain value, not a framework principal) to **one** service method, map the result; no queries, transactions, locks or rules. The edge authenticates; **the use case authorises**. The default profile sets the review limits (~15 lines, ~5 parameters).

**Two kinds of validation.** *Shape* (required, length, format, enum spelling) at the edge in one validation unit per area — the only place a field-error map is built, even for one field — using the **domain's constants**, never its own numbers. *Invariants* belong to the domain (factory methods guard them; this guard is also needed for non-web callers and state changes between checks); stateful checks (counts, uniqueness, membership) are the service's and return an error value.

**Errors.** Expected outcomes are result values (or the stack's typed errors, used consistently) with a kind and a stable code. The edge maps kind → status (validation 400, unauthenticated 401, forbidden 403, not found 404, conflict 409, gone 410, too many requests 429, unavailable 503) and code → an RFC 9457 problem `type`. Clients key on the code, never the title. Exceptions are for bugs and broken infrastructure, turned into a 500 problem by one global handler. Catch only a specific type and recover visibly (log + metric + documented fallback) or rethrow. Best-effort side effects after commit may log a warning and continue; **safety-critical paths never** do.

**Authorisation and isolation.** The **use case authorises**, through one access unit per resource kind, every resource reachable through a tenant id: a caller who is not a member gets **not found** (existence is not leaked), a member without the role gets **forbidden** — or the project's stated rule. Queries filter by the tenant id; never trust an id from the URL alone. Define the revocation latency budget; revalidate sensitive actions; a permission cache needs tenant/principal/version scoping, invalidation and a bounded lifetime. Jobs re-check access when they run (`add-scheduled-job`).

**Data access.** One unit of work (session, context, transaction-bound connection) per request or job, never shared across concurrent tasks. Reads project only the needed columns (no change tracking). Writes load entities, call domain methods, save. Bulk changes: one set-based statement, row count checked. A query used by two services moves to the persistence query extensions. No lazy loading, no N+1. **No generic repository** over an ORM that already is one.

**Transactions and locks.** The use case owns the transaction: begin, take locks in the documented order, **re-read state and the caller's rights under the lock**, save, commit, **then** notify. A per-tenant limit takes the tenant lock; a new invariant gets its own documented lock namespace. One save is already atomic. Never call HTTP, caches or message brokers while a transaction or lock is held. A race test holds the request at the lock with a gate, never a sleep.

**Time, timeouts, concurrency.** Time only from an injected clock, passed to the domain as `now`; UTC everywhere. Every I/O call has a timeout. Asynchronous stacks stay async end to end with cancellation passed through, never blocking on a result; synchronous stacks keep request work short and push long work to a job.

**Logging.** Structured templates with named placeholders, never interpolation. Never log coordinates (or objects carrying them), addresses, phone numbers, emails, tokens, codes or names; opaque ids can still identify people: minimise them, restrict access and retention, no unbounded metric tags (`security-privacy-review`, quality plugin, owns the rule).

**Configuration and secrets.** Typed options per feature, **validated at start** so a bad deploy fails at once; no raw configuration reads outside the composition root. **One secret per purpose**, each with its own options and validation — never a fallback to another purpose's key. Each new setting is in the example env file; development-only behaviour is unreachable elsewhere.

**Feature flags.** A boolean in one flags section, read at the edge or in the service, never in the domain; each flag names its issue and its removal condition.

**Resilience for outbound calls.** One configured client per vendor (connection reuse, timeouts). Idempotent reads: total timeout + retry with backoff and jitter + circuit breaker, the total covering the retries. **Sends (email, SMS, push, payments) are never retried by the client**: timeout + breaker only; the job that sends is the **one retry owner**, with an idempotency key. Caches fail fast: skip the cache rather than stall.

**Wiring and lifetimes.** One composition root (a container, or explicit construction); each module wires its own types. Anything holding a unit of work lives per request/job; shared adapters, clients and the clock are thread-safe and hold no per-request state.

**Scheduled and background work.** A state that changes with time is a stored timestamp, not a job; a job is for something that must *happen*. Jobs are idempotent and never swallow failures; side effects that must not be lost are persisted as outbox intent in the business transaction. A continuous loop uses the injected clock, a fresh unit of work and **one application call per pass**, and a catch that logs and keeps it alive. Details: `add-scheduled-job`; uploads: `add-file-upload`.

## 3. Performance (write it fast, prove it with numbers)

- **No database or cache call inside a loop.** Load the set once (`IN (…)`, a join, a group) and match in memory; batch cache reads.
- Filter, sort, count and page **in the database**; `exists` instead of `count > 0`.
- Every growing list is bounded: limit + keyset (cursor) pagination, not offset.
- Several collection includes → split queries or projections; bulk inserts as one statement.
- **Indexes from representative plans and workload cost** (selectivity, composite order, write amplification); a scan may be optimal. An analyzing plan executes the query: use safe data and a timeout.
- Short transactions and locks; small responses; cache only with a measured need and a named invalidation owner (permission caches only as §2 allows).
- **Proof in the PR** for a query, hot path or list change: the plan, or a query count asserted in a test with one item and with several (so an N+1 fails); a benchmark against the budget for hot paths (`perf-check`, quality plugin).

## 4. Data model and integrity

- Normalised by default; denormalise only for a measured read path, naming the sync code.
- The database enforces what it can, behind the domain: `NOT NULL` unless absence means something, foreign keys with an **explicit delete behaviour** (cascade for owned rows, restrict where deletion loses meaning), unique indexes for uniqueness rules, `CHECK` constraints for ranges. A domain limit and its constraint use the same constant.
- Keys: UUIDs (time-ordered where available); timestamps with time zone in UTC; enums stored as short text, never as integers whose meaning shifts; units in column names (`weight_g`, `duration_s`).
- **A concurrency strategy for every invariant:** a lock for cross-row rules, an optimistic version for single-row edits two people may make, a unique index for uniqueness races (map the violation to a conflict error). Never check-then-insert without one.
- Personal data: one place per kind, a retention rule, and account deletion that removes or anonymises every identifying row (explicitly where no foreign key cascades). Caches hold only rebuildable state with an owner and an expiry.

## 5. Enforcement

- Architecture tests over the built code, written as **allowlists with empty baselines**: the default profile lists the set. A project with legacy violations keeps them as named, owned entries with a removal condition — never a baseline file that also hides new ones.
- Analyzers at the recommended level, warnings as errors. A suppression sits **at its location with a justification**, never a blanket switch-off that also silences new code.
- A new structural rule lands with its test in the same change.

## Review

When reviewing a diff, walk [references/review-checklist.md](references/review-checklist.md). For ecosystems without a stack reference above, read [references/ecosystems.md](references/ecosystems.md).

## Rules

- The project's conventions win on names and paths; these rules win over "the old file does it" — no exceptions by precedent.
- Never weaken a safety, privacy or testing rule to fit a convention.
- A convention that is wrong for the project is fixed in its doc and its test (`create-skill`, meta plugin), not ignored.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `design-review` (lifecycle), `code-review` (quality), `add-endpoint`, `add-migration`, `add-scheduled-job`, `add-file-upload` | Backend placement and rules | `engineering-principles` (lifecycle) for the why; `decision` (meta) for a new pattern or library |
