---
name: supply-chain
description: "Secure dependency, build and artifact delivery paths. Use for package updates, CI permissions, release provenance, secrets or dependency compromise review."
license: MIT
metadata:
  version: "1.0.0"
---

# Supply chain

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Inventory trust

Record source repositories, dependency registries, lockfiles, build images/actions, generators and artifact consumers. Separate untrusted PR builds from signing/publishing. Identify who can alter dependencies, workflows, caches and release inputs.

## 2. Constrain and reproduce builds

Pin dependencies and actions to reviewed immutable identities where supported, with an owned update mechanism. Verify integrity and license requirements. Installation/build scripts execute code; run untrusted inputs without privileged credentials or host mounts. Cache keys include relevant lock/toolchain inputs and cannot promote untrusted artifacts into a release.

## 3. Verify artifacts and secrets

Generate an SBOM when useful to consumers and retain build provenance tying source, inputs and artifact digest. Signing verifies identity/integrity, not freedom from vulnerabilities. Scan for secrets with redacted output; rotate/revoke actual exposures according to scope. Keep release credentials in protected environments with minimal lifetime and authority.

## 4. Respond and maintain

Triage dependency findings by reachability, exploitability and exposure, not severity labels alone. Track exceptions with owner/expiry. Rebuild/revoke affected artifacts after compromise; test the recovery and downstream notification process.

## Verification and report

Test a malicious PR/build input without secrets, changed dependency/artifact digest, poisoned cache, expired credential and scanner-output redaction. Exercise provenance verification and rejected unsigned/untrusted update paths.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never use privileged PR-target execution on untrusted checked-out code.
- No secret values in findings.
- Artifact promotion reuses a verified artifact rather than silently rebuilding different inputs.

## Composition

| From | This skill | To |
|---|---|---|
| `ci`, `pre-commit`, `release` (lifecycle); dependency update PRs | Inventoried trust, constrained builds and verified artifacts | `security-privacy-review`, `code-review` (quality); `release` (lifecycle); `incident` (lifecycle) on a compromise |
