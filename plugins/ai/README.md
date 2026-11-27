# ai 1.0.0

Build and evaluate model integrations, retrieval applications and bounded tool agents with explicit trust, quality and cost contracts.

Install declared dependencies. Load only relevant skills/resources; required availability is not a recursive workflow.

| Skill | Purpose |
|---|---|
| [agent-workflow](skills/agent-workflow/SKILL.md) | Build bounded tool-using applications with authorization, durable state and recovery. Use for agent orchestration, approvals, delegation or interrupted workflows; not to mandate multiple agents for ordinary tasks. |
| [llm-integration](skills/llm-integration/SKILL.md) | Build or change a model-backed application feature. Use for provider integration, structured output, streaming, fallbacks or model migration; not for ordinary coding that merely uses an assistant. |
| [rag-pipeline](skills/rag-pipeline/SKILL.md) | Build or improve retrieval-grounded applications. Use for document ingestion, embeddings, vector or hybrid search, citations and retrieval evaluation; not for every model call. |
