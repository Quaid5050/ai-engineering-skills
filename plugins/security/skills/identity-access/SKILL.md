---
name: identity-access
description: "Implement or review authentication, sessions and authorization. Use for sign-in, account recovery, service identity, tenant permissions or token lifecycle changes."
license: MIT
metadata:
  version: "1.0.0"
---

# Identity and access

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Separate identity from permission

Define human/service actors, tenants, resources and actions. Authentication establishes identity; each privileged action independently checks current authorization. Choose an established identity provider/protocol implementation rather than custom cryptography.

## 2. Implement the complete lifecycle

Verify token issuer, audience, signature/algorithm, expiry and intended usage; model key rotation. Use protocol-specific anti-replay/redirect/CSRF protections and secure browser session cookies where appropriate. Account recovery, device loss, refresh reuse, logout and permission revocation are first-class paths.

## 3. Enforce resource scope

Use deny-by-default resource/action/property authorization at trusted boundaries, including batch endpoints, background jobs, caches and replays. A client-supplied tenant or role is not authoritative. Versioned permission caching must meet the stated revocation window; do not assume a cached decision stays valid indefinitely.

## 4. Protect credentials and audit

Use vetted password/secret storage, platform key stores or managed keys. Keep service credentials narrowly scoped and short-lived where supported. Rate-limit abuse without enabling account-lockout denial of service. Record safe security events and recovery actions without tokens or passwords.

## Verification and report

Test role/tenant matrices, expired/wrong-audience tokens, key rotation, refresh reuse, session fixation, CSRF, recovery abuse, logout/revocation and stale-cache behavior. Include allowed cases so denial is not the only tested behavior.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never trust role/tenant claims without verifying their authority and intended use.
- Authentication success does not authorize every object or tool.
- Do not log secrets or use real credentials in fixtures.

## Composition

| From | This skill | To |
|---|---|---|
| `spec`, `design-review` (lifecycle); `threat-model` | Complete identity lifecycle with resource-scoped authorization tests | `security-privacy-review`, `code-review` (quality); `deploy-check`, `release` (lifecycle) |
