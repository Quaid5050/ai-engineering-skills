---
name: safe-refactoring
description: "Refactor or modernize existing software while preserving explicit behavior and compatibility. Use for legacy seams, dependency upgrades or structural cleanup."
license: MIT
metadata:
  version: "1.0.0"
---

# Safe refactoring

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Characterize the current contract

Identify observable behavior, consumers, operational constraints and known defects. Add characterization tests where missing; they may start green. Do not preserve an unsafe defect silently—separate intended correction from behavior-preserving restructuring.

## 2. Choose a bounded migration

Prefer small reversible changes, adapters or a strangler boundary over a big-bang rewrite. Define compatibility, data migration and rollback. For dependency upgrades read release/migration notes for the actual version range and test deprecated/changed APIs.

## 3. Implement without scope drift

Keep unrelated formatting/renames separate when they obscure review. Tests may change to reflect a new seam or deliberate API contract, but cannot merely mirror implementation. Maintain an explicit old/new behavior comparison and update consumers together when authorized.

## 4. Verify and remove transitional code

Run characterization, contract/integration and performance checks relevant to the change. Exercise rollback before retiring the old path. Remove compatibility shims only when supported consumers/data no longer need them.

## Verification and report

Compare old/new outputs on representative and boundary inputs, verify consumers and migration rollback, and measure affected hot paths. State intentionally changed behavior separately.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never discard uncommitted user work to simplify a refactor.
- Do not claim behavior preservation from compilation alone.
- Avoid unrelated cleanup under a narrow bug-fix request.

## Composition

| From | This skill | To |
|---|---|---|
| `investigate-feature`, `design-review` (lifecycle); `code-review` (quality) findings | Characterized contract, bounded migration, transitional code removed | `implement` (lifecycle) per slice; `code-review` (quality); `deploy-check`, `release` (lifecycle) |
