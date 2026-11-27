---
name: memory-and-ffi
description: "Implement or review memory-sensitive and foreign-interface code. Use for ownership, unsafe operations, ABI boundaries, native parsers or resource lifetime defects."
license: MIT
metadata:
  version: "1.0.0"
---

# Memory And Ffi

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Define ownership and representation

Document who allocates/frees each resource, valid lifetime, mutability/aliasing, thread access, nullability, alignment, size and encoding. At an FFI boundary specify ABI, calling convention, allocator, versioning and error/cancellation representation. Never infer a buffer length from a terminator unless the protocol guarantees it.

## 2. Minimize unsafe surfaces

Prefer memory-safe abstractions and established parsers. Keep unavoidable unsafe code small with explicit preconditions/invariants. Validate lengths before arithmetic/copying; handle integer overflow, truncation, signedness, endianness and partial reads. Ensure every error path releases owned resources exactly once.

## 3. Handle failure across boundaries

Do not let exceptions/panics cross unsupported ABIs. Use typed error results and deliberate exception translation; aborting panics cannot be caught by an unwind handler. Callback lifetime, reentrancy, cancellation and unload behavior need explicit contracts.

## 4. Verify under hostile inputs

Use sanitizers, fuzzing, static analysis and architecture-specific tests where supported. Include zero/max lengths, malformed encodings, ownership transfer, allocation failure, double completion and callback after cancellation. Validate release builds, not only debug assertions.

## Verification and report

Compile/run supported sanitizer configurations and seeded fuzz regressions; test cross-language ownership, errors and cancellation. Report untested compiler/ABI targets explicitly.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- No unchecked ownership transfer or pointer lifetime assumptions.
- Never load or execute untrusted native artifacts during a static review.
- Keep numerical and memory correctness separate from performance claims.

## Composition

| From | This skill | To |
|---|---|---|
| An applicable engineering task | Scoped implementation and acceptance evidence | Relevant tests, security review and deployment readiness; external actions only when authorized |
