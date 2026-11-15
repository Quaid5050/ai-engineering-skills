---
name: shared-core
description: "Structure native mobile code as one functional core shared by Android and iOS — every rule and decision written once and tested once on both targets — plus thin imperative shells per platform: what may and may not go in the core, the 'is this a decision?' test, adapters that return failures instead of throwing, interop rules across the language boundary, threading kept in the shells, and lint checks for core purity, shells that decide nothing and file sizes, with no baseline. Use when native logic is (or should be) shared across platforms, or Android and iOS behave differently. Trigger on 'shared core', 'shared module', 'cross-platform core', 'functional core imperative shell', 'android and ios behave differently', 'where does this go in native code', 'is this kotlin/swift clean'."
argument-hint: "[a native change, a file to place, or a diff]"
license: MIT
metadata:
  version: "1.0.0"
---

# Shared core, thin shells

Apply this to `$ARGUMENTS` (a native change, a file to place, or a diff). If empty, apply it to the change in hand. Background-work workflow is `background-work`; app-layer rules are `mobile-conventions`; principles are `engineering-principles` (lifecycle plugin).

When both platforms must behave the same — and safety-critical background code must — **a rule lives once**. Duplicated rules in two languages drift: one platform retries, the other gives up; one clears a queue on sign-out, the other keeps it.

## 0. Read the project

1. Read `AGENTS.md`, `CLAUDE.md`, decision records, and the native folders' READMEs.
2. Find out whether the project already has a shared core and in which technology; open the reference: [references/kmp.md](references/kmp.md), or [references/other-cores.md](references/other-cores.md) for a shared native library or a core in the cross-platform framework's own language.
3. Find its commands: core tests on both targets, platform tests, native lint.

No shared core yet and the change adds a rule to native code on both platforms? Raise it as a design question (`design-review`, lifecycle plugin; `decision`, meta plugin) before writing the rule twice.

**Cross-platform framework apps.** When the app is written in a cross-platform framework, the framework's own language code can be the core: the same rules (pure, no UI or plugin imports, time and OS facts as parameters, failures as values) apply there, and the native side holds only the OS glue the framework's plugins need. A native shared core is needed only for rules that must run without the framework's engine. Which applies is a recorded decision; this skill's table holds for either.

## 1. Core and shell

| Part | Job | May | Must not |
|---|---|---|---|
| **Core** | Every rule and decision: what an answer from the server means, when to retry and how long to wait, what blocks, what is kept or dropped, what status to show, sampling/interval policy, OS-state rules, the problem codes and what each means, wire models and their encoding, and the interfaces it needs | depend on the interfaces it declares; take time and every OS fact (battery, charging, permission, connectivity) as parameters | import platform or I/O libraries; read the clock; start threads; log personal data; throw across an interface |
| **Platform bits of the core** | The few primitives the shared language lacks (a lock, an atomic) | use the platform's standard library | contain rules |
| **Adapters** | Implement the core's interfaces over the OS: HTTP transport, secure token store, local queue database, timers | call the OS; turn its failures into the interface's failure value | decide policy; return "empty" or "done" for a failure |
| **Shell** | Lifecycle and wiring: services/background tasks, OS callbacks, boot/update receivers, schedulers | read OS facts and pass them to the core; apply its answer (exhaustive match over a core enum); hop threads | decide — **no comparison of a problem code or a state** in shell code; ask the core |
| **Bridge boundary** | The app ↔ native contract (generated bindings) | translate bridge types ↔ core types | business logic; hand edits to generated files |

**What is a decision, and so goes in the core:** any `if`/`when` whose answer changes what the app does or shows — record, block, start, restart, clear, report, retry, which status. A rule only one platform needs still goes in the core. What stays in the shell is **a fact about one OS's API**: which system broadcasts mean "the device rebooted or the app was updated", how to read a permission, in which order an OS reports two facts. The test: *if the same question would be asked on the other platform, it is a core rule.*

**Where the OS forces two mechanisms**, the core holds both halves and says so in its doc comment (e.g. one platform takes an interval request, the other gives a stream the core filters — both from the same numbers).

**Product changes first:** a change to sampling, upload timing or what is reported changes how fresh the data users rely on is — it goes through `spec` (lifecycle plugin) before code, and says how a "running but degraded" state is reported.

**Gate:** every new `if` about policy is in the core with a test; the shells gained only OS facts and wiring.

## 2. Interop rules across the language boundary

The other platform sees the core through a generated binding. Write the core so the binding stays usable and safe:
- **No exceptions across an interface.** An exception crossing the boundary usually crashes the app. Interfaces the shell implements return their failure (`null` for "unreadable", `false` for "could not write"); entry points the shell calls catch everything and return an outcome value. A sequence both shells would otherwise write (a stop, a session switch) belongs in the core so it cannot drift.
- **Enum entries** follow the naming the binding maps cleanly (check the reference); matches over a core enum need a default branch on the other side.
- **No tuples and no default arguments the caller relies on** — the other side sees every parameter; use small named value types; constants a shell needs are exposed explicitly.
- **Numbers:** know how integer and nullable types map (boxing, widths). Prefer 64-bit integers for epoch times and floating point for measurements; keep conversions in one bridge file per platform.
- **Names** never collide with bridge-generated type names (core `Problem` vs bridge `BridgeProblem`).

## 3. Threading

- The core holds **no threads**; it is safe to call from the shell's one worker thread/queue, and anything shared across threads uses the core's own lock or atomics.
- Each shell keeps the threading model its files already use (one executor or one serial queue for uploads, OS callbacks on their thread, UI publishes on main). A new component may use structured concurrency with a scope it owns and cancels — never a global scope, never two models in one type, never blocking the main thread.
- Delays and retry intervals come from the core so tests control them.

## 4. Errors and safety

- A record is never dropped silently (`offline-queue`): failure to send keeps it and retries; an unreadable store ends the run with a retry, never "done".
- Every blocking condition is reported to the app and to the server, never swallowed.
- Catch the narrowest type; a broad catch only at a shell boundary that then reports; never an empty catch; no force unwraps or not-null assertions in new code.
- Personal data never in logs or in a type's string description (override it to leave fields out).

## 5. Tests and linting

- **Core logic is tested once**, in the core's common test set, with fakes of the core's own interfaces and time/OS state as parameters — and **runs on both targets** (the JVM-like host and the iOS simulator, or the equivalents). A test that passes on one and fails on the other is a platform difference inside the core: fix it there.
- **Adapter tests stay native:** the local queue database, secure stores, retry timer, bridge mapping. They test the adapter's contract with the core: unreadable store → failure value, never empty; rows written by an **older build** (real old bytes) still read.
- Lint, all **without a baseline**: *core purity* (core files import only the shared standard library; no platform, I/O, clock, threading or console APIs), *shells decide nothing* (no equality comparison on problem codes or states in shell code), *sizes* (production files ≤ ~320 lines and ≤ 3 top-level types of one concern; generated files skipped). Formatting and the platform linters run in CI.

**Gate:** core tests green on both targets, adapter tests green, native lint clean.

## Rules

- Rules change once, in the core; a shell-only change on one platform says in the change why the other is unaffected.
- No exceptions by precedent; no lint baseline.
- Native changes ship with a store release, not an over-the-air patch (`release`, lifecycle plugin).

## Composition

| From | This skill | To |
|---|---|---|
| `background-work`, `home-widget`, `implement` (lifecycle), `code-review` (quality) | Core/shell placement, interop, lint | `device-test` on both platforms (the core changed for both); `decision` (meta) to adopt a shared core |

## Checklist for review

- [ ] New rules in the core with tests run on both targets; no policy `if` and no state/problem comparison in shells.
- [ ] Core interfaces return failures, never throw; adapters never turn a failure into "empty" or "done".
- [ ] Interop rules respected (enums, no tuples/defaults, numbers, names).
- [ ] Threading follows the file's model; no I/O on the main thread; long-lived closures don't leak.
- [ ] Generated bridge files untouched; contract changed at its source and regenerated on both sides.
- [ ] No personal data in logs or string descriptions; files within size limits.
- [ ] Device checks planned on both platforms.
