# Protocol and compatibility adapters

The core table is an HTTP/JSON example, not a universal protocol mandate.

- REST/HTTP: define safety/idempotence, cache controls, conditional updates (`ETag` / `If-Match`), pagination stability and bounded filters. A successful repeated DELETE need not return the same status; idempotence concerns intended server state. Nullable, absent and empty may have different meanings.
- GraphQL: field/resolver authorization and tenant scoping, bounded depth/complexity and batched loaders; never cache loaders across users. Schema additions such as enum variants can break exhaustive clients. Preserve error/path semantics. [GraphQL security](https://graphql.org/learn/security/).
- gRPC/protobuf: keep field numbers stable, reserve removed fields/names, define deadlines, cancellation and stream flow control. Do not infer retries are safe for non-idempotent RPCs. [Protobuf evolution](https://protobuf.dev/programming-guides/proto3/#updating).
- WebSockets/SSE: authenticate the session and authorize each subscription/action, handle revocation/reconnect, bounded buffering and missed-event replay. Avoid bearer tokens in logged URLs; if a platform forces query credentials, scope/expire them and redact all intermediaries.
- Events: version payloads, define ordering key, dedupe identity, retention/replay window and dead-letter recovery. Consumer contracts and persisted outbox state supplement schema validation.

Compatibility means testing representative old clients, not simply labeling a change additive. Test optimistic-concurrency conflicts, pagination under concurrent writes, tenant replay, changed idempotency payload and revoked access to cached responses. See [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110).
