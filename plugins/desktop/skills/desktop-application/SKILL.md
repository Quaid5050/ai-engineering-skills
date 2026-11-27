---
name: desktop-application
description: "Build or change native or hybrid desktop applications. Use for desktop IPC, filesystem integration, packaging, signing, updates or OS-specific behavior."
license: MIT
metadata:
  version: "1.0.0"
---

# Desktop application

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Model platform authority

Identify supported OS versions/architectures, UI toolkit, distribution channel and required native capabilities. Separate untrusted renderer/content from privileged filesystem, process and device access. Define an allowlisted IPC schema with caller/origin checks; do not expose a general shell or unrestricted path bridge.

## 2. Implement native behavior

Respect platform permission prompts, keyboard/menu conventions, multi-window lifecycle and accessibility semantics. Normalize paths carefully and test case sensitivity, Unicode, symlinks, permissions and atomic persistence. Use capability-scoped file access; user selection of one file does not grant all-directory access.

## 3. Package and update

Build separately for supported targets, pin dependencies and verify signing/notarization or equivalent distribution requirements. Keep signing credentials outside untrusted builds. Updates verify trusted signatures, platform/architecture compatibility and rollback/recovery state; protect against downgrade and interrupted installation according to the product policy.

## 4. Verify real integration

Run packaged-app tests for first launch, permission denial/revocation, IPC abuse, multiple windows, suspend/resume, offline start, interrupted update, data migration and uninstall retention. Browser tests alone do not cover native authority or packaging.

## Verification and report

Test an unauthorized IPC/path request, symlink escape, keyboard-only/assistive navigation, standard-user install, signature failure, update interruption and data preservation. Record exact OS/architecture/toolchain and unrun targets.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never grant native authority to arbitrary web content.
- Do not treat unsigned debug builds as release evidence.
- Preserve user data during migration, rollback and uninstall according to explicit policy.

## Composition

| From | This skill | To |
|---|---|---|
| `spec`, `design-review`, `new-feature` (lifecycle) | Native behavior verified on each target OS; signed, updatable package | `threat-model` for IPC and file access; `supply-chain` for signing; `accessibility-audit`, `code-review` (quality); `release` (lifecycle) |
