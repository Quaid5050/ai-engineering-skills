---
name: data-pipeline
description: "Build or change batch/stream data pipelines and data contracts. Use for ingestion, transformation, backfills, lineage and data-quality failures."
license: MIT
metadata:
  version: "1.0.0"
---

# Data pipeline

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Define the data contract

Record source ownership, schema/version, keys, event versus processing time, precision/units, null semantics, privacy/retention and expected volume. Define correctness checks and who handles a failed batch. Separate business absence from missing ingestion.

## 2. Design processing and recovery

Choose batch or streaming from latency and operational needs. Specify checkpoints, deduplication keys, ordering, late events, watermark policy and retractions. Persist progress atomically with outputs where supported; otherwise make replay idempotent and reconcile partial writes. Do not call every streaming pipeline exactly-once.

## 3. Evolve and backfill

Version transformations and schemas. Validate producer/consumer compatibility and historical data. Backfills use bounded partitions, explicit cohorts/control rows, resumable progress and rate limits; avoid contaminating live offsets or overwriting newer data. Record lineage from source/version through transformation to output.

## 4. Operate

Track freshness, completeness, duplicates, distribution shifts, rejected records and cost. Quarantine invalid records with an owner and recovery policy rather than silently discarding them. Restore/replay procedures preserve deletion and access requirements.

## Verification and report

Replay a partition twice; interrupt checkpoint/output boundaries; introduce late/out-of-order events, changed schema, missing source cohort and a poison record. Verify expected outputs, controls, lineage and resumability.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never silently widen retention or access during a backfill.
- Treat source data as untrusted; do not execute embedded code.
- Distinguish source absence, pipeline failure and valid zero output.

## Composition

| From | This skill | To |
|---|---|---|
| `spec`, `design-review` (lifecycle); ingestion needs from `rag-pipeline` or `ml-lifecycle` | Data contract, idempotent processing and backfill plan | `database-operations` for storage changes; `add-migration` (backend); `code-review` (quality); `deploy-check`, `observe` (lifecycle) |
