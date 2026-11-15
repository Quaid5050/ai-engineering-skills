---
name: engineering-principles
description: "The principles every change follows on any stack — one job per layer, the concept test for domain code, dependencies pointing inwards with ports only at real boundaries, SOLID applied, small units, no rule-less dumping grounds, explicit errors, one source of truth, one home per technical kind of code (placement rows), rules enforced by allowlist architecture tests with empty baselines, performance by design, simple first. Use when deciding where code goes, reviewing a design, or judging whether code is clean. Trigger on 'where does this code go', 'which layer', 'is this clean', 'SOLID', 'separation of concerns', 'design patterns', 'is this over-engineered', 'utils folder', 'architecture test', 'placement'."
argument-hint: "[question, design or diff]"
license: MIT
metadata:
  version: "1.0.0"
---

# Engineering principles

The **why** behind every convention. The project's own conventions (and the stack skills: `backend-conventions`, `mobile-conventions`, `web-conventions`) hold the **how**. Apply this to `$ARGUMENTS` (a placement question, a design to check, or a diff). If empty, apply it to the change in hand.

## 0. Read the project

1. Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` and any conventions docs or decision records (`docs/decisions/`, `docs/adr/`).
2. Find the project's **placement table** (where each kind of code lives) and its **architecture tests** or import lints. If they exist, they are the concrete answer; this skill explains them.
3. If the project has no placement table, answer from §3 below and offer to add the table to the project's conventions (`bootstrap-project` does it for a new repo).

The project wins on facts (paths, names, commands). When a project rule conflicts with a principle here, say so to the user so one of them gets fixed — never quietly follow neither.

## 1. The principles

**1. One job per layer.** Each layer answers one question:

| Layer | Answers | Never does |
|---|---|---|
| Edge (HTTP handler, message consumer, job entry, screen/widget, CLI command) | What came in, what goes out? Parse, authenticate (who is calling), pass the caller's identity to **one** use case, translate the result | business rules, authorisation decisions, queries, transactions, retries |
| Use case (application service, view model, interactor) | What happens when someone does X? **Authorises the caller** through the one access-check unit, then orchestrates rules, data and side effects in order | status codes, wire formats, UI widgets, SQL |
| Domain (entities, value objects, pure rules) | Is this allowed? What is the new state? **Business concepts only** | I/O, clock reads (time is passed in), logging, randomness, and technical concerns even when pure: file formats, encodings, parsing, crypto, wire spellings |
| Data / adapters (repositories, API clients, platform services) | How is it stored, fetched or sent? | deciding what is allowed |

A rule that lives in two layers drifts; a rule in the wrong layer cannot be tested without the layer around it.

**The concept test.** Before code goes into the domain, ask: *would a product person or a support agent recognise this as one of the product's rules?* "An order holds at most 50 lines", "a booking older than its start time cannot be cancelled" — yes. "A JPEG starts with FF D8", "base64url without padding", "HMAC the code with a secret", "parse this CSV" — no: technical code belongs in an adapter **even when it is pure**. Purity decides testability, not placement.

**2. Dependencies point inwards; invert them only at real boundaries.** Edge → use case → domain. An interface (a *port*) earns its place when what is behind it is **outside the process and may be swapped or faked**: email/SMS/push providers, payment gateways, identity providers, the OS (location, camera, permissions), another service's API, the clock. Also when an inner layer needs something only an outer layer can provide. Do **not** add an interface for in-process code you own in the same layer — one implementation and no boundary is noise.

**3. SOLID, applied.** *Single responsibility:* one reason to change. *Open/closed:* add a case by adding a type or a table row, not by editing five `switch`es. *Liskov:* a fake honours the real contract (same errors, same ordering) or tests lie. *Interface segregation:* small interfaces shaped by the caller. *Dependency inversion:* principle 2.

**4. Small, cohesive units.** Make the limits tests where a machine can count them (lines per file, types per file, parameters per constructor); keep the rest as review questions: a function ≤ ~40 lines, ≤ ~5 injected dependencies (a sixth says the unit has two jobs — split it, don't bundle parameters to hide it).

**5. No rule-less dumping grounds.** A folder called `utils`, `helpers`, `common` or `shared` is **not** bad by name. A folder **with no rules** is: it collects unrelated code and becomes everyone's dependency. A shared folder is fine when it has (a) a stated purpose, (b) an allowlist of what may live there, and (c) a test that it never imports the features that use it. Otherwise a helper lives next to the type it serves, named for what it does.

**6. Explicit errors.** Expected outcomes (not found, not allowed, expired, conflict, full) are **values** — a result type or a closed set of cases the caller must handle. Exceptions are for bugs and broken infrastructure. Never catch and ignore: every catch either recovers in a way a user or a metric can see, or rethrows. On **safety-critical paths** — the project's list in `AGENTS.md` wins; by default anything where a silent failure can harm a person, lose money or lose or corrupt data — failures always surface. Unsure whether a path is safety-critical? Treat it as one and ask.

**7. Testable by construction.** Dependencies come in through the constructor or the DI container; time from an injected clock; randomness and ids injectable where tests need them. Seams exist only at real boundaries (`testing-doctrine`, quality plugin).

**8. One source of truth.** The API contract, design tokens, user-facing strings, limits and wire names each live in exactly one place; everything else is generated from it or reads it. A client may mirror a server limit for instant feedback, but the server is the authority and its refusal is handled.

**9. Names say what things are.** A reader can guess a file's contents from its path; role suffixes are consistent (`…Service`, `…Repository`, `…Request`, `…ViewModel`). Comments say **why** (a constraint, a race, a spec rule), not what the next line does.

**10. Rules are enforced by tests, not memory.** Every structural rule a machine can check is an architecture test or lint. Layer rules are **allowlists** (what a layer *may* use), not denylists (what it may not): a denylist passes every kind of code nobody thought of. Baselines are **empty**; a rule that cannot be met yet keeps a shrinking-only list with a one-line reason per entry. There are **no exceptions by precedent**: "the old file does it" is never a reason. See [references/architecture-tests.md](references/architecture-tests.md).

**11. Performance by design, proven by numbers.** No query or network call in a loop, bounded lists, work done once (not per item or per frame), heavy work off the UI thread; a hot-path change carries a measurement (`perf-check`, quality plugin).

**12. Simple first.** KISS; YAGNI (no flags, parameters, interfaces or config nobody asked for); DRY with care — duplicated *knowledge* (a rule, a limit, a wire name) is always a bug, duplicated *code shape* is fine until the third copy; composition over inheritance (inherit only from framework base types or within a closed set of cases).

**13. Small vertical slices.** One user-visible behaviour end to end (contract → server → client → tests) before the next. A refactor is its own change, behaviour unchanged, tests green before and after.

## 2. Design patterns

The catalogue — architectural patterns (layers, ports and adapters, service layer, domain model, repository and unit of work, read/write split, MVVM, result object, idempotency key, transactional outbox, resilience) and the classic object patterns we use or avoid, with *use when / not when* — is in [references/design-patterns.md](references/design-patterns.md). A pattern is justified by a problem in front of you, never by a future that may come. Prefer the language feature to the ceremony (closed types + exhaustive `switch` over Visitor; a function over a one-method interface).

## 3. One home per technical kind of code (placement rows)

Agents copy the code next to them. If a technical kind of code has no stated home, every feature invents one, and the wrong one becomes the pattern. So the project keeps **one row per kind**, each with a home, a rule and a check. The generic rows (adapt names to the stack; the template is in [references/placement-table.md](references/placement-table.md)):

| Kind of code | Home | Rule | Enforced by |
|---|---|---|---|
| Business rules and invariants | Domain | Concept test passes; no I/O, clock, logging | Allowlist test on domain imports |
| Use case orchestration | Application service / view model | One method per use case; owns the transaction; notifies after commit | Review; edges call one use case |
| Input shape validation | One validation unit per area at the edge | Uses the domain's constants, never its own numbers | Test: field-error maps built only there |
| Secrets and crypto (keyed hashes, signing, random tokens) | **One owner per purpose**, each with its own configuration, validated at start-up | Never reuse another purpose's key; no fallback to "some other secret" | Test: crypto APIs used only by the listed owners |
| File and object storage | **One generic storage port**, one adapter per provider | Features never get their own storage class; layout lives in the use case | Test: storage SDKs only inside the adapter folder |
| File formats, encodings, parsing (images, CSV, archives, metadata) | Adapter next to its port | Never in the domain, even when pure | Test: domain handles no raw bytes |
| Raw request bodies / uploads | One upload reader at the edge (type sniffed from bytes, size cap) | Handlers never read the raw body themselves | Test |
| Rate limits | One limiter folder, numbers in configuration | Each limiter states fail-open or fail-closed | Test: limiter types only there |
| Outbound calls (timeouts, retries, circuit breakers) | The adapter's client configuration | **One retry owner per path**; never retry a non-idempotent send without an idempotency key | Review |
| Long-lived loops (reconnect, reconcile, retry, outbox dispatch) | A coordinator / background worker | Makes **one use-case call per pass**; never holds rules | Test: repositories never import coordinators |
| Scheduled jobs (reminders, expiry, digests, clean-ups) | One scheduler + thin job entries calling one use case (`add-scheduled-job`, backend plugin) | **One scheduler instance**, also during deploys; jobs idempotent; claim rows with a lease or skip-locked; a **unique sent-ledger** key per effect; re-check access and state at run time; times computed from the stored zone | Test: jobs call one use case; race test of two runners; dedupe test |
| Outbound notifications (email, SMS, push, webhooks) | **One notification port**, one adapter per channel; templates in one place | User preferences and unsubscribe honoured; unique sent-ledger key; access re-checked at send time; one retry owner; no personal data in logs | Test: vendor SDKs only in the adapters; ledger dedupe test |
| File uploads and attachments | The one upload reader + the storage port (`add-file-upload`, backend plugin) | Presigned or multipart, size caps, type from bytes, metadata stripped; a parent record is complete only when every attachment is confirmed; client-generated ids make retries safe | Test: storage SDKs only in the adapter; incomplete-parent test |
| Code two or more features share | A shared module **with rules** (principle 5) | Never imports a feature | Test: no feature imports from shared code's dependents |
| Wire contract (requests, responses, events) | Contract file + mappers at the boundary | Generated types never leave the data/adapter layer | Test on imports |
| Enums on the wire | One wire-name mapping | Wire spelling only there | Test |
| Configuration | Typed options per feature, validated at start | No raw config lookups outside the composition root | Test |
| Time | Injected clock | No direct clock reads outside the composition root | Test |
| Local wall-clock times (schedules, quiet hours) | Store the IANA zone id + local time; compute instants in the domain | Never store a fixed UTC offset; test both DST transitions | Test |
| Expected failures | Result values per area → protocol errors at the edge | Clients key on a stable error code, never the message | Contract test |
| Authorisation | One access-check unit per resource kind, called by the **use case** (the edge only authenticates and passes the caller id) | Non-member → not found, member without the role → forbidden (or the project's stated rule); never cache a permission decision past a membership change | Integration tests with forbidden and removed callers |
| Retry-safe creates (idempotency) | The use case + a unique constraint | Records created offline carry a **client-generated id as a permanent unique key**; a repeat returns the original resource, never an error or a second row. A time-windowed idempotency-key store is only for online-only creates | Test: the same id twice → one row, same response |
| Transactions and concurrency | The use case | Lock or version every cross-row invariant; never check-then-insert without one | Race tests |

A kind of code that fits no row is a **design question**, not a place to improvise: add a row (with its check) before the code.

## 4. Review checklist

- [ ] Each changed unit does one job, in its layer; no business rule, query or transaction in an edge.
- [ ] Domain code passes the concept test: no I/O, clock, logging, file format, encoding, parsing or crypto.
- [ ] New interfaces sit at a real boundary; no single-implementation interface for in-process code.
- [ ] Every technical kind of code is in its §3 row; no new kind was improvised.
- [ ] Shared folders have a purpose, an allowlist and an import test; no rule-less dumping ground.
- [ ] Expected failures are values; every catch recovers visibly or rethrows; safety paths never swallow.
- [ ] One source of truth: no copied constant, token, string, contract or rule.
- [ ] Testable through injection and the boundary fakes in `testing-doctrine`.
- [ ] Patterns are used for the problem they solve; none of the anti-patterns in the catalogue.
- [ ] No call in a loop, lists bounded, hot-path change measured.
- [ ] Refactor and behaviour change are not mixed in one change.
- [ ] Architecture tests still pass with empty baselines; a new structural rule came with a new test.
- [ ] A problem that slipped through names the earliest rung that should have caught it (the rung ladder in `testing-doctrine`, quality plugin), and moves the guard there.

## 5. Design review before code

Every feature and every **non-trivial** fix gets a design review of its *plan* before the branch has production code: the `design-review` skill (this plugin), done by the `architect` agent (agents plugin) — spec-level on the epic, slice-level on each slice issue, fix-level on the bug issue. Non-trivial = anything but a one-file change that adds no type, file, dependency or rule. It is never skipped or shortened for speed: test reruns and review rounds may be trimmed, the design review may not.

## Rules

- These principles never weaken a project's safety, privacy or testing rules.
- Facts (paths, commands, APIs) come from the code; when the code and a convention disagree, fix whichever is wrong in the same change.
- No exceptions by precedent. A rule that turns out wrong is changed in the convention (and its test), not silently ignored.

## Composition

| From | This skill | To |
|---|---|---|
| `design-review`, `implement`, `code-review`, the stack conventions skills | Principles, placement rows, checklist | `decision` (meta plugin) for a costly-to-reverse choice; `bootstrap-project` to install the placement table and architecture tests |
