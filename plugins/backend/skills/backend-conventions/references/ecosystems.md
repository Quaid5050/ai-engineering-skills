# Additional backend adapters

Select a profile from the actual runtime, persistence approach and workload. The layered business-app diagram is not a mandatory rewrite of idiomatic code.

| Stack | Implementation choices | Evidence |
|---|---|---|
| Go | Pass request contexts/deadlines, close resources, preserve error identity, bound goroutines and queues. Interfaces belong near consumers when substitution is meaningful; do not wrap every concrete type. | Unit/integration tests, race detector on representative paths, cancellation and leak checks. [Go diagnostics](https://go.dev/doc/diagnostics) |
| PHP / Laravel | Respect request versus long-lived worker lifetimes; authorize model actions/policies, validate mass assignment and use actual transaction semantics. After-commit dispatch is a wake-up, not durable intent. | Queue retry/restart, tenant isolation, policy tests, migration lock/rollback evidence. [Laravel queues](https://laravel.com/docs/queues) |
| Ruby / Rails | Active Record can be the chosen domain/persistence model; do not force duplicate entities purely to match a diagram. Strong parameters do not replace authorization. Database constraints handle uniqueness races; avoid callback-only external delivery. | Request authorization, job retries, N+1/query plans, constraints and old-client contracts. [Rails security](https://guides.rubyonrails.org/security.html) |
| Python | Pick synchronous/asynchronous boundaries from the actual server and libraries. Bound blocking work and process/model pools; do not share database sessions across concurrent tasks. | Integration against chosen engine, cancellation/timeouts and worker lifecycle. [Python asyncio](https://docs.python.org/3/library/asyncio.html) |
| JVM / .NET / Node | Existing adapters cover common frameworks. Match transaction/session lifetime, cancellation and connection pools to runtime semantics; language choice never determines SQL dialect. | Real database and concurrent connection tests, contract compatibility, outbound timeout/reconciliation. |

Relational indexes follow query evidence, not every filter mechanically. Document isolation, lock order and revocation latency. Keep a modular monolith unless independent deployment/ownership or scaling requirements justify services. Separate deployment boundaries add network, consistency, observability and recovery obligations.
