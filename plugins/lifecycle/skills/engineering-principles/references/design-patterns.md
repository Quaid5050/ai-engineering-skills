# Design patterns

The point of every entry: **tomorrow's change touches one place, and a test proves it still works.** A pattern is used when its problem exists — never to look "enterprise". Each entry: **Use when** · **Not when** · **Example**.

## 1. How a change stays in one place (read this first)

| Tomorrow's change | Where it lands | Pattern | What proves it still works |
|---|---|---|---|
| A new business rule ("an order may hold 50 lines") | One domain constant + one check in the use case | Domain model, service layer | Domain unit test + API test of the refusal |
| A new email/SMS/payment vendor | A new adapter implementing the existing port + one registration line | Strategy + adapter (ports and adapters) | The adapter's test against recorded responses; use-case tests keep using the fake |
| A new expected failure | One error case, its code in the contract, one branch in the client's closed result type | Result object; exhaustive matching finds every `switch` | API test for the error; client test for the branch |
| A new screen state | One case of the closed state type | State (closed types) | One UI test per state |
| Fake backend → real backend for a screen | The repository binding | Repository + dependency injection | The same UI tests over a fake HTTP layer |
| A step on every request (auth header, timing, decompression) | One middleware / interceptor | Chain of responsibility / decorator | One test through the pipeline |
| A new consumer of "X changed" | Subscribe to the existing event; the sender does not change | Observer | Test that the new consumer is told |
| A field added on the wire | Contract + one mapper per side (rename/removal = breaking, new version) | Adapter at the boundary, single source of truth | Regenerated client compiles; mapping test; deploy check |

If a change needs edits in many unrelated places, a pattern is missing or misused — say so in the review.

## 2. Architectural patterns

| Pattern | Use when | Not when |
|---|---|---|
| **Layers with the dependency rule** (clean / onion) | For applications whose responsibilities benefit from these boundaries: edge → use case → domain; outer depends on inner | — |
| **Ports and adapters** (hexagonal) | The thing is outside the process and may be swapped or faked: vendors, the OS, other services, the clock | It is your own in-process code in the same layer |
| **Service layer** (application service) | A use case coordinates rules, data, a transaction and side effects | A pure rule (put it on the entity) or a single read (a projection is enough) |
| **Domain model** (rich entities) | Invariants must hold whoever changes the data | Plain read models |
| **Repository + unit of work** | Persistence behind a collection-like API, one commit per use case | A *generic* repository over an ORM that already is one — it hides the features you need (projections, bulk updates, locks) |
| **Read/write split** (light CQRS) | Reads need shapes the entities don't have: project straight into read models | Separate read databases or message pipelines before the scale needs them |
| **MVVM / presentation model** | Any screen with actions or several data sources | A static, read-only view |
| **Single source of truth + one-way data flow** | Data shown in more than one place | — |
| **Dependency injection** | Every dependency of a service, adapter, repository or view model | Value objects, pure functions |
| **Typed options, validated at start** | Any configuration value | Constants that are business rules (they belong on the domain type) |
| **Result object** | Expected failures the caller must handle | Bugs and broken infrastructure (exceptions) |
| **Idempotency key** | A client or job may retry a write (mobile networks, job retries) | Reads |
| **Transactional outbox** | A side effect must not be lost between the database commit and sending it | Best-effort notices the next refresh repairs |
| **Timeout, retry with backoff + jitter, circuit breaker** | Any call that leaves the process | Retrying non-idempotent writes without a key; two retry layers on one path |
| **Feature flag** | Code ships before it may be switched on; staged rollouts | Permanent configuration; flags without a removal condition |
| **Optimistic UI** | An action should feel instant and can be rolled back | Safety-critical actions — show the real result |

**Outbox shape that works:** insert the outbox row in the same transaction as the change; deliver right after commit; a background dispatcher retries: claim rows with a lease (`SELECT … FOR UPDATE SKIP LOCKED` or equivalent), send with **no transaction open**, record the result fenced on the lease; backoff; a give-up time tied to what the user sees; a metric for the backlog. Alert-type messages also carry an idempotency key so a lease overlap never sends twice.

## 3. Classic object patterns

### Creational
| Pattern | Use when | Not when |
|---|---|---|
| **Factory method** (static creation) | Creating an object must enforce invariants or assign an id/time | A record with no rules |
| **Builder** | Many optional parts assembled step by step (mostly frameworks) | Your own code with few parameters — named parameters instead |
| **Abstract factory** | Families of related objects that vary together | Almost when the actual responsibility warrants it |
| **Singleton** | One shared instance — **through the DI container only** | Never as static mutable state: tests cannot replace it |

### Structural
| Pattern | Use when | Not when |
|---|---|---|
| **Adapter** | A vendor's shape differs from your port | Your own types — rename instead |
| **Facade** | Callers need one simple entry to a subsystem (an application service is one) | It starts collecting unrelated methods |
| **Decorator** | Add timing, metrics or caching to a port without changing implementations | A second retry layer — each path has one retry owner |
| **Composite** | Trees treated uniformly (UI trees) | — |
| **Proxy** | Control access with the same interface | It hides failures the caller must see |

### Behavioural
| Pattern | Use when | Not when |
|---|---|---|
| **Strategy** | Interchangeable algorithms or vendors chosen by config | 2–3 fixed cases that never vary — a `switch` expression |
| **Observer** | Many parties react to one change without the source knowing them | One fixed reaction — call it |
| **Command** | Work must be queued, retried or undone as an object (a job) | A plain synchronous call |
| **Chain of responsibility** | Ordered steps that may stop or pass on (middleware) | Business rules — keep those readable top to bottom in the use case |
| **State** | Behaviour depends on a finite set of states — closed types + exhaustive matching | — |
| **Template method** | — | Avoid: inheritance for reuse; inject the varying step |
| **Visitor** | — | Pattern matching over closed types does the job |

## 4. Anti-patterns to reject in review

| Anti-pattern | Why it hurts | Do instead |
|---|---|---|
| God class, "Manager", rule-less "Utils" | Every change touches it; nobody owns it | One job per unit; shared code with rules and a test |
| Logic in the edge | Rules can't be reused or unit-tested; edges drift apart | Use case / view model |
| Anaemic domain, rules scattered in services | The same check copied five times | Rules on the entity |
| Generic repository over an ORM | Hides projections, bulk updates, locks | The ORM's unit of work + query extensions |
| An interface for every class | Twice the files, no boundary | Interfaces at real boundaries only |
| Service locator in business code | Hidden dependencies | Constructor injection |
| Static mutable state | Tests interfere; no override | DI singleton |
| Inheritance for reuse | Fragile base class | Composition |
| Primitive obsession | Ids and phone numbers as any string — mix-ups compile | Value objects / typed ids where mix-ups are likely |
| Boolean flag parameters | Unreadable call sites, doubled paths | Two named methods or an options object |
| Catch-all-and-continue | Failures vanish; on safety paths, alerts are lost | Typed catch that recovers visibly, or rethrow |
| Speculative generality | Abstractions for needs that never come | Build for today; the layering makes the second case cheap |
| Per-feature copy of a generic piece | The next feature copies it again | Design the generic port now |

## Sources

- Gamma, Helm, Johnson, Vlissides, *Design Patterns* (1994); summaries: https://refactoring.guru/design-patterns/catalog
- Martin Fowler, *Patterns of Enterprise Application Architecture*: https://martinfowler.com/eaaCatalog/
- Alistair Cockburn, *Hexagonal architecture*: https://alistair.cockburn.us/hexagonal-architecture/
- Robert C. Martin, *The Clean Architecture*: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- Chris Richardson, *Transactional outbox*: https://microservices.io/patterns/data/transactional-outbox.html
- Microsoft Azure Architecture Center, *Cloud design patterns*: https://learn.microsoft.com/en-us/azure/architecture/patterns/
- Pete Hodgson, *Feature Toggles*: https://martinfowler.com/articles/feature-toggles.html
