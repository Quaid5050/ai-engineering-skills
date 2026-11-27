---
name: threat-model
description: "Produce or update an actionable threat model. Use for changed trust boundaries, sensitive data, privileged capabilities or explicit abuse/security review."
license: MIT
metadata:
  version: "1.0.0"
---

# Threat model

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Establish assets and boundaries

Draw the data/control flow with entry points, actors, tenants, secrets, stores and external services. Record assumptions and what the system must protect. Include malicious users, compromised dependencies/operators and coercive misuse where relevant; avoid inventing irrelevant threats.

## 2. Describe concrete attack paths

For each boundary ask how identity, authorization, integrity, confidentiality, availability and recovery could fail. Include injection, SSRF, path traversal, unsafe deserialization, resource exhaustion and business abuse. AI content/tool boundaries need prompt-injection and excessive-agency analysis.

## 3. Select controls with evidence

Prioritize by exposure, impact and feasibility. Assign prevention/detection/recovery controls to owners. Map applicable requirements to versioned standards; do not claim compliance from a checklist. Exceptions record scope, compensating controls, expiry and authorized acceptance.

## 4. Verify and maintain

Translate attack paths into negative tests and operational detections. Update the model when data flows, identities, tools or deployment boundaries change. Link findings to implementation and tests, not just prose.

## Verification and report

Demonstrate forbidden identity/resource/action denial, malformed-input handling, resource limits and recovery. Record controls not exercised and the reason.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Threats and control effectiveness require concrete scenarios.
- Sensitive evidence stays in authorized locations, not public reports.
- No security certification claim without the required independent process.

## Composition

| From | This skill | To |
|---|---|---|
| `spec`, `design-review` (lifecycle); `system-design`, `identity-access`, `agent-workflow` | Concrete attack paths with selected controls and verification evidence | `security-privacy-review` (quality) checks the controls in the diff; `feature-to-issues`, `file-bug` (lifecycle) for open controls; `decision` (meta) for accepted risk |
