# Concurrency and networking adapters

C/C++: mutex/condition-variable predicates, memory-order correctness, sanitizer-compatible tests. Rust: Send/Sync, cancellation-safe async ownership, synchronization/model checking where applicable. Go: goroutine ownership, context propagation, channel closure and race detector. JVM/.NET: structured task lifetime, thread-pool starvation, cancellation and blocking/async interaction.

Protocol fixtures should feed one byte at a time, truncated frames, oversized length fields, duplicate messages, disconnect after acceptance, slow readers and half-closed sockets. Synchronize race tests with barriers/events instead of relying on arbitrary sleeps.

For distributed coordination use leases plus fencing and receiver-side checks where required; a local mutex cannot enforce cross-process uniqueness.
