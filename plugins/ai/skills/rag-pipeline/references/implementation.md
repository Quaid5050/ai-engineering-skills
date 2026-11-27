# Retrieval implementation reference

For each chosen database/search engine, verify filter semantics, transaction/isolation behavior, vector dimensions, distance metric and index rebuild requirements against its official versioned docs. Do not assume every vector store enforces authorization.

Maintain separate metrics: retrieval recall/precision at a cutoff; ranking quality; citation correctness; answer grounding; abstention; end-to-end latency/cost. Include absent-answer queries, near duplicates, conflicting versions, deleted documents and revoked tenants.

Reference security model: [OWASP prompt injection](https://genai.owasp.org/llm2026/llm012026-prompt-injection/). The local ACL fixture in this repository is policy/integration evidence only; it is not an evaluation of a real embedding model or vector engine.
