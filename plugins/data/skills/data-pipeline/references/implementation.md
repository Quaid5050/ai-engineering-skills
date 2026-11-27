# Data pipeline adapters

- SQL/dbt-style batch: declare unique/not-null/reference/business constraints, incremental keys and full-refresh cost; a row-count check alone cannot prove correctness.
- Spark/warehouse processing: inspect shuffle/partition skew, serialization, spill and schema evolution; measure on representative synthetic distributions.
- Kafka/Flink-style streams: verify broker/processor transactional boundaries, consumer offsets, retention and late-event semantics. Broker guarantees do not automatically cover external sinks.
- Python orchestration: separate orchestration retries from idempotent transform tasks; pin environments and preserve safe failure evidence.

Use actual engine documentation for the selected versions. These adapters are documented guidance until a project-specific integration fixture runs.
