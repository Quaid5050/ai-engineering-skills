---
name: llm-integration
description: "Build or change a model-backed application feature. Use for provider integration, structured output, streaming, fallbacks or model migration; not for ordinary coding that merely uses an assistant."
license: MIT
metadata:
  version: "1.0.0"
---

# LLM integration

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Define the application contract

Specify the task, allowed inputs, data handling, output schema, refusal/uncertainty behavior, latency/cost budget and acceptable error rate. Establish a simple non-model baseline when one can solve the problem. Separate developer policy, user input and retrieved content; do not turn model text into executable commands.

## 2. Integrate at a narrow boundary

Keep credentials server-side, choose an explicit provider/model version policy and validate request/response shapes. Use bounded input/output sizes, deadlines, cancellation and per-tenant quotas. Treat transport success as distinct from a valid application result. Validate structured outputs against the domain contract and reauthorize any resulting action.

For streaming, define partial-output visibility, interrupted output, cancellation and final validation. Do not commit a payment or irreversible tool effect from an unvalidated partial response. Retry only known retryable failures with a capped budget and jitter; avoid retrying an ambiguous external side effect.

## 3. Evaluate and release

Use a versioned dataset with ordinary, boundary, adversarial and out-of-domain cases. Hold out evaluation data from prompt tuning. Compare baseline/candidate on task quality, schema adherence, refusal behavior, latency and cost; stratify by important cohorts. Human review handles ambiguous labels. Keep model, prompt, retrieval and tool versions in evidence.

Roll out behind an existing feature control where useful, with a measured rollback threshold. Fallbacks must satisfy the same privacy and output contract; cheaper or alternate models are not automatically safe substitutes.

## Verification and report

Test timeout/rate-limit/cancellation, malformed or semantically invalid output, refusal, prompt injection, cross-tenant quotas and fallback privacy. Run the held-out evaluation only with authorized data/service access; otherwise record it pending.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never evaluate quality solely by a model grading its own output.
- Do not log prompts/responses by default; define redaction, retention and sampling.
- Treat nondeterminism and confidence as uncertainty, not authorization.

## Composition

| From | This skill | To |
|---|---|---|
| `spec`, `investigate-feature`, `design-review` (lifecycle) | Provider boundary, output contract and held-out evaluation | `rag-pipeline` or `agent-workflow` when retrieval or tools are added; `security-privacy-review`, `code-review` (quality); `deploy-check`, `observe` (lifecycle) |
