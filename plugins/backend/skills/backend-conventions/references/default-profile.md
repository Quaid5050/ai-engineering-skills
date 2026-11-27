# Default profile: layered business application

Use this profile when the project has **no recorded architecture profile** (no placement table, no decision record, no architecture tests that say otherwise). It is opinionated on purpose: each rule below is enforceable by a test. A project that records a different profile (active record as the domain model, a library, systems code, a compiler or codec) follows its own record instead, and says so in its conventions doc.

## Modules

| Module | Job | May use (allowlist) | Must not |
|---|---|---|---|
| **Domain** | Business concepts only: entities, value objects, enums, invariants, limits as constants, pure rules | Core language, collections, text, date/time **types** (not the clock), the domain itself — nothing else | ORM annotations, the database, HTTP, logging, clock reads, randomness, crypto, raw bytes, file formats, encodings, wire spellings |
| **Persistence** | The ORM context (unit of work), mappings, reusable query extensions, explicit locks, migrations | Domain | Business decisions, HTTP |
| **Application** | One service per feature area; each public method is one use case: authorise the caller, load, call the domain, save in one transaction, notify after commit; returns a result | Domain, Persistence, ports | Request/response objects of the web framework, status codes, JSON, user principals as framework types |
| **Edge / API** | Bind input, validate shape, call **one** use-case method, map the result to the protocol; request/response records and mappers; the composition root | Everything (it wires the app) | Queries, transactions, locks, business rules — anywhere in the module |
| **Adapters** | Implement ports over vendors: email, SMS, push, payments, identity, object storage, file formats | The vendor SDK | Deciding *whether* to act (that is the use case) |
| **Workers** | Scheduled and queued jobs: thin, idempotent, call application services | Application | Rules inside the job |
| **Hot-path module** (optional) | A high-volume path with its own module and published types (e.g. bulk event ingest) | Domain, Persistence | Being reached by Application beyond its published types |

## The concept test

Before a type goes into Domain, ask: **would a product person recognise it?** An order, a booking, "at most 50 lines per order" — yes. A JPEG header reader, base64 helpers, an HMAC — no, even when pure: put them behind a port with an adapter in the module that owns the technology. Domain may *state* a rule (a constant: "an avatar is at most 2 MB"); the adapter *implements* the technical part (reading the bytes).

## Thin edges

- A handler is about **15 lines**: bind, validate shape, call one use-case method with the caller's identity as a plain value, map the result. More than that means work belongs in the service.
- A handler that needs more than about **5 parameters** is doing the service's job: move the work, don't bundle the parameters into an object to hide the count.
- These numbers are review triggers in this profile: exceeding them needs a reason in the PR, not a silent exception.

## Ports

Ports for things **outside the process** (email, payments, storage, identity, clocks if the stack has no clock abstraction) live in the application module (`application/ports/` or the project's name); their adapters live where the technology lives. An interface for in-process code you own, with one implementation and no test seam, is noise.

## Architecture tests: allowlists with empty baselines

Architecture tests run over the built code in CI. Each is an **allowlist** (what may depend on what), not a denylist, and starts with an **empty baseline**: there is no "existing violations" file, so a rule has no exception by precedent. An exception, when truly needed, is one named entry with a reason, an owner and a removal condition, reviewed like code.

The default set:

- Domain imports only its allowlist above.
- No raw bytes, streams, encodings or file formats in Domain.
- Edges never touch persistence types (health checks allowlisted by name).
- Field-error maps are built only in validation units.
- Crypto primitives only in the listed secret owners.
- Storage SDKs only in the storage adapter; each vendor SDK only in its adapter.
- Rate limiters only in their folder.
- No raw configuration reads outside the composition root.
- No direct clock reads (only the injected clock).
- The hot-path module reached only through its published types.
- Every allowlist entry names a type that exists (a stale entry fails the test).

A new structural rule lands with its test in the same change.
