---
name: backend-conventions
description: "How a backend service is structured and written on any stack — layered modules with feature folders (edge → application → domain, persistence, adapters, workers, a hot-path module), what each layer may do and call, thin edges, two kinds of validation, errors as results mapped to problem details, data access through the ORM's unit of work, transactions and locks owned by the use case, time and cancellation, logging without personal data, options validated at start, one secret per purpose, resilience with one retry owner, background work, performance, data integrity and allowlist architecture tests. Use when writing or reviewing server code. Trigger on 'backend conventions', 'where does this go in the backend', 'service layer', 'business logic in the controller', 'repository or ORM', 'request/response DTO', 'validator', 'how do I structure this endpoint', 'transaction', 'N+1'."
argument-hint: "[backend change, file to place, or diff]"
license: MIT
metadata:
  version: "1.0.0"
---

# Backend conventions

How server code is laid out and written. Apply it to `$ARGUMENTS` (a change, a file to place, or a diff). If empty, apply it to the change in hand. The **why** is `engineering-principles` (lifecycle plugin); this skill is the backend **how**. Stack idioms: [references/dotnet.md](references/dotnet.md), [references/django.md](references/django.md), [references/node.md](references/node.md), [references/spring.md](references/spring.md).

## 0. Read the project

1. Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, the project's conventions doc and its placement table, and `docs/decisions/` (or `docs/adr/`).
2. Identify the stack from the manifest (build file, package manifest, lock file) and open the matching reference above; if none matches, map the generic rules below onto the stack's own community conventions and say so.
3. Find the existing modules, the architecture tests, the test host and the commands (build, test, lint, migrations). Use the project's names; this skill's names are placeholders.

**Gate:** you know which module and folder each part of the change lands in, by the project's own table or by §1–§2 below.

## 1. Modules and layers

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

| Module | Job | May use | Must not |
|---|---|---|---|
| **Domain** | Business concepts only: entities, value objects, enums, invariants, limits as constants, pure rules | an **allowlist**: core language, collections, text, date/time types, domain itself | ORM annotations, the database, HTTP, logging, clock reads, randomness, crypto, raw bytes, file formats, encodings, wire spellings |
| **Persistence** | The ORM context (unit of work), mappings, reusable query extensions, explicit locks, migrations | Domain | business decisions, HTTP |
| **Application** | One service per feature area; each public method is one use case: authorise the caller, load, call the domain, save in one transaction, notify after commit; returns a result | Domain, Persistence, ports | request/response objects of the web framework, status codes, JSON, user principals as framework types |
| **Edge / API** | Bind input, validate shape, call **one** use-case method, map the result to the protocol; request/response records and mappers; adapters for outside systems; the composition root | everything (it wires the app) | queries, transactions, locks, business rules — anywhere in the module |
| **Adapters** | Implement ports over vendors: email, SMS, push, payments, identity, object storage, file formats | the vendor SDK | deciding *whether* to act (that is the use case) |
| **Workers** | Scheduled and queued jobs: thin, idempotent, call application services | Application | rules inside the job |
| **Hot-path module** (optional) | A high-volume path with its own module and published types (e.g. bulk event ingest) | Domain, Persistence | being reached by Application beyond its published types |

**The concept test.** Before a type goes into Domain, ask: would a product person recognise it? An order, a booking, "at most 50 lines per order" — yes. A JPEG header reader, base64 helpers, an HMAC — no, even when pure: put them behind a port with an adapter in the module that owns the technology. Domain may *state* a rule (a constant); the adapter *implements* the technical part.

**Ports** for things outside the process go in the application module (`application/ports/` or the project's name); their adapters go where the technology lives. An interface for in-process code you own is noise.

**Gate:** each new file sits in one row above (or the project's row) and its imports are inside that row's allowlist.

## 2. Rules by topic

**Edges are thin (~15 lines).** Take inputs, validate shape, pass the caller's identity (a plain value, not a framework principal) to one service method, map the result. The edge authenticates; **the use case authorises** (§2, authorisation). A handler that needs more than ~5 parameters is doing the service's job: move the work, don't bundle the parameters.

**Two kinds of validation.** *Shape* (required, length, format, enum spelling) at the edge in one validation unit per area — the only place a field-error map is built, even for one field — using the **domain's constants**, never its own numbers. *Invariants* belong to the domain (factory methods guard them; reaching that guard is a bug because the edge checked first); stateful checks (counts, uniqueness, membership) are the service's and return an error value.

**Errors.** Expected outcomes are a result value with an error `kind` + stable `code` + title. The edge maps kind → status (validation 400, unauthenticated 401, forbidden 403, not found 404, conflict 409, gone 410, too many requests 429, unavailable 503) and code → an RFC 9457 problem `type`. Clients key on the code, never the title. Exceptions are for bugs and broken infrastructure; one global handler turns them into a 500 problem. `catch` only a specific type and recover visibly (log + metric + documented fallback) or rethrow. Best-effort side effects after commit may log a warning and continue; **safety-critical paths never** do.

**Authorisation and isolation.** The edge only authenticates and passes the caller's identity; the **use case authorises**, through one access unit per resource kind, for every resource reachable through a tenant/workspace/team id: a caller who is not a member gets **not found** (existence is not leaked), a member without the role gets **forbidden** — or the project's stated rule. Queries filter by the tenant id; never trust an id from the URL alone. **Never cache a permission decision**: a removed member loses access on the next request, and jobs re-check access when they run (`add-scheduled-job`).

**Data access.** One unit of work per request or job (whatever the stack calls it: a session, a context, a transaction-bound connection); never shared across threads or concurrent tasks. Reads: project into the read model with only the needed columns (no change tracking where the ORM has it). Writes: load the entities, call domain methods, save. Bulk changes: the ORM's bulk update/delete (check the row count) or one set-based statement. A query used by two services moves to the persistence query extensions. No lazy loading, no N+1. **No generic repository** over an ORM that already is one.

**Transactions and locks.** The use case owns the transaction: begin, take locks in the documented order, **re-read state and the caller's rights under the lock**, save, commit, **then** notify. A per-tenant limit (members, items) takes the tenant lock; a new invariant gets its own lock namespace, documented with its place in the order. One save is already atomic — no explicit transaction for one write. Never call HTTP, caches or message brokers while a transaction or lock is held. A race test holds the request at the lock with a gate, never a sleep.

**Time, timeouts, concurrency.** Time only from an injected clock, passed into domain methods as `now`; UTC everywhere. Every I/O call has a timeout; where the stack is asynchronous, stay asynchronous end to end and pass cancellation through, never block on an async result; where it is synchronous, keep request work short and push long work to a job.

**Logging.** Structured templates with named placeholders, never string interpolation. Never log coordinates or objects carrying them, addresses, phone numbers, emails, tokens, codes or people's names; ids are fine in logs, never as metric tags (`security-privacy-review`, quality plugin, owns the rule).

**Configuration and secrets.** Typed options per feature, bound from configuration, **validated at start** so a bad deploy fails at once. No class reads raw configuration keys outside the composition root. **One secret per purpose**, each with its own options and validation — never a fallback to another purpose's key. Every new setting gets a line in the example env file. Development-only behaviour is gated on the environment and unreachable elsewhere.

**Feature flags.** A boolean in one flags section, read at the edge or in the service, never in the domain; each flag names its issue and its removal condition.

**Resilience for outbound calls.** Outbound clients are created once and configured in one place per vendor (connection reuse, timeouts). Idempotent reads get a total timeout + retry with backoff and jitter + a circuit breaker, configured so the overall timeout does not cut the retries off. **Sends (email, SMS, push, payments) are never retried by the client**: timeout + breaker only; the job that sends is the **one retry owner**, with an idempotency key. Caches fail fast with short timeouts: degrade (skip the cache) rather than stall the request path.

**Wiring and lifetimes.** Dependencies are wired in one composition root (a DI container, or explicit construction where the stack has none). Anything holding a unit of work lives per request/job; stateless adapters, clients and the clock are shared and thread-safe and never hold per-request state. Each module wires its own types; the composition root only calls those.

**Scheduled and background work.** First ask whether a stored time is enough ("suspended until 17:30" is a column that reads as resumed once it passes — no job). Use a job only when something must *happen* at a time. Jobs are idempotent (they may run twice), record what they sent, never swallow failures. A continuous loop is a background worker: a timer on the injected clock, a fresh unit of work per pass, **one application call per pass** (never data access directly), a catch that logs and keeps the loop alive. Side effects that must not be lost go through a transactional outbox (`engineering-principles` references). Schedulers, claiming rows, sent-ledgers and notifications: `add-scheduled-job`. Uploads: `add-file-upload`.

## 3. Performance (write it fast, prove it with numbers)

- **No database or cache call inside a loop.** Load the set once (`IN (…)`, a join, a group) and match in memory; batch cache reads.
- Filter, sort, count and page **in the database**; `exists` instead of `count > 0`.
- Every growing list is bounded: limit + keyset (cursor) pagination, not offset.
- Several collection includes → split queries or projections (no cartesian explosion).
- Bulk inserts as one statement, not one save per row.
- **Every `WHERE`, `JOIN` and `ORDER BY` on a large table has an index** the migration adds; read the plan (`EXPLAIN ANALYZE` or equivalent) for any new query on a large table.
- Keep transactions and locks short; responses small; cache only with a measured need and a named owner of invalidation; never cache permission decisions.
- **Proof in the PR** for a change to a query, hot path or list endpoint: the plan or a query count (assert the exact count in a test, once with one item and once with several, so an N+1 fails), and a load or benchmark number against the budget for hot paths (`perf-check`, quality plugin).

## 4. Data model and integrity

- Normalised by default; denormalise only for a measured read path, naming the code that keeps it in sync.
- The database enforces what it can, behind the domain: `NOT NULL` unless absence means something, foreign keys with an **explicit delete behaviour** (cascade for owned rows, restrict where deletion loses meaning), unique indexes for uniqueness rules, `CHECK` constraints for ranges. A domain limit and its constraint use the same constant.
- Keys: UUIDs (time-ordered where available); timestamps with time zone in UTC; enums stored as short text, never as integers whose meaning shifts; units in column names (`weight_g`, `duration_s`).
- **A concurrency strategy for every invariant:** a lock for cross-row rules, an optimistic version for single-row edits two people may make, a unique index for uniqueness races (map the violation to a conflict error). Never check-then-insert without one.
- Personal data: one place per kind, a retention rule, and account deletion that removes or anonymises every row identifying the person (explicitly where no foreign key cascades). The database is the source of truth; caches hold only rebuildable state with an owner and an expiry.

## 5. Enforcement

- Architecture tests over the built code, **allowlists with empty baselines** (`engineering-principles` references): domain allowlist, no raw bytes in domain, edges never touch persistence (health checks allowlisted), field-error maps only in validation units, crypto only in the listed secret owners, storage SDKs only in the storage adapter, limiters only in their folder, no raw config reads, no direct clock reads, hot-path module reached only through its published types, every allowlist entry names a real type.
- Analyzers at the recommended level, warnings as errors. A suppression sits **at its location with a justification**, never a blanket switch-off that also silences new code.
- A new structural rule lands with its test in the same change.

## Checklist for review

- [ ] Files in the right module and folder with the right suffix; one public type per file (DTO groups excepted).
- [ ] Each technical kind of code in its placement row (secrets, storage, parsing, limiters, loops).
- [ ] Edges thin: no data access, transaction, lock or rule; one use-case call.
- [ ] Services take plain ids/values, return results/read models, own the transaction, notify after commit, re-read rights under the lock.
- [ ] Non-member → not found, missing role → forbidden (or the project's rule), through the access unit.
- [ ] Domain: no I/O, ORM annotations, logging, clock reads; new types pass the concept test.
- [ ] Shape validation in the validation unit using domain constants.
- [ ] No call in a loop; projections for reads; paging in SQL; indexes for new filters; plan or query count in the PR.
- [ ] Expected errors are values with stable codes; catches typed and visible; safety paths never swallow.
- [ ] Injected clock; timeouts on I/O; no blocking on async results where the stack is async.
- [ ] Logs pass the personal-data rule; no ids as metric tags.
- [ ] New tables: constraints, FKs with explicit delete, enums as text, UTC, a concurrency strategy per invariant, retention/deletion.
- [ ] Options validated at start; one secret per purpose; lifetimes right (nothing per-request held by a shared object); one retry owner per send.
- [ ] The use case authorises; no cached permission decisions; jobs re-check access at run time.
- [ ] Architecture tests and analyzers green with empty baselines.

## Rules

- The project's own conventions win on names and paths; these rules win over "the old file does it" — no exceptions by precedent.
- Never weaken a safety, privacy or testing rule to fit a convention.
- A convention that is wrong for the project is fixed in its doc and its test (`create-skill`, meta plugin), not ignored.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `design-review` (lifecycle), `code-review` (quality), `add-endpoint`, `add-migration`, `add-scheduled-job`, `add-file-upload` | Backend placement and rules | `engineering-principles` (lifecycle) for the why; `decision` (meta) for a new pattern or library |
