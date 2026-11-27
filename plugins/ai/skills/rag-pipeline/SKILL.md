---
name: rag-pipeline
description: "Build or improve retrieval-grounded applications. Use for document ingestion, embeddings, vector or hybrid search, citations and retrieval evaluation; not for every model call."
license: MIT
metadata:
  version: "1.0.0"
---

# Rag Pipeline

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Define corpus and access semantics

Identify authoritative sources, ownership, tenant/record ACLs, update/deletion requirements and expected queries. Establish lexical retrieval as a baseline before adding embedding/hybrid complexity. Define whether retrieval is permitted at all for each caller and document.

## 2. Build versioned ingestion

Parse untrusted documents with limits and isolation. Preserve source identity, version, offsets, permissions and deletion state. Choose chunk boundaries from document structure and evaluation, not one universal token count. Version parsing/chunking/embedding models and index schema together; a changed embedding space requires a planned rebuild or dual-index migration.

## 3. Retrieve and ground answers

Apply authoritative access control before exposing candidates, including caches and reranking. Recheck revocation before returning content. Filter-only postprocessing after unauthorized text reaches a model is too late. Bound query expansion and ranking cost; compare lexical, vector and hybrid candidates on labeled queries.

Citations reference actual accessible source spans. When evidence is absent or conflicting, answer with uncertainty or abstain. Treat retrieved instructions as data; they cannot grant tools or override policy.

## 4. Operate and delete

Propagate edits, ACL changes and deletion through raw stores, chunks, embeddings, caches and backups according to the retention contract. Track ingestion lag, index freshness, retrieval failures and answer quality. Define migration rollback without serving revoked content.

## Verification and report

Verify tenant isolation before model invocation, access revocation, deleted documents/caches, stale embeddings, citation spans, poisoned content and empty retrieval. Compare held-out query results against the lexical baseline.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Similarity is not authority or truth.
- Do not expose unauthorized chunks to rerankers, traces or prompts.
- Do not claim retrieval quality from a few hand-picked examples.

## Composition

| From | This skill | To |
|---|---|---|
| An applicable engineering task | Scoped implementation and acceptance evidence | Relevant tests, security review and deployment readiness; external actions only when authorized |
