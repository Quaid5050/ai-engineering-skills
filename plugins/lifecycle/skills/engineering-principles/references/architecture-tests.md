# Architecture tests: intentional boundaries and owned baselines

These examples target layered business applications. Parsers, cryptographic libraries, active-record applications and systems projects need different allowed dependencies. Import checks do not prove runtime isolation. Line counts are optional review signals, not semantic checks.

## Why allowlists

The usual first architecture test is a **denylist**: "the domain does not reference the ORM". It passes every kind of code nobody listed — a hand-written image parser, a crypto helper, a JSON reader all pass "no ORM in domain". The tests looked green while the skills said what each layer *is*; nothing checked it.

The fix is an **allowlist**: "the domain may use only the standard library's core, collections, text and other domain code". Anything new and unexpected fails by default, and a human decides whether to widen the list — in review, with a reason.

## What to test

| Rule | Shape of the test |
|---|---|
| Domain allowlist | Every type in the domain module depends only on: core language types, collections, text/regex, date/time *types* (not clock reads), and the domain itself |
| Domain handles no raw bytes | No byte arrays, streams or buffers in domain signatures |
| Edges have no data access | Entry-point modules never reference the persistence module, the ORM or the DB driver (allowlist the health checks) |
| One home per technical kind | Crypto APIs only in the listed secret owners; storage SDKs only in the storage adapter folder; limiter types only in the limiter folder; field-error maps only in validation units; wire-name conversion only in its one mapping |
| Generated code stays in the data layer | Generated client/bridge types imported only by the data/adapter layer |
| Shared code never imports a feature | No import from `shared/` to `features/` (or the project's names) |
| Features meet only through their public handle | A feature imports another only via its domain or one re-export file; no cycles |
| No direct clock or config reads | Clock APIs and raw configuration only in the composition root |
| Size limits | Files ≤ N lines and ≤ M top-level types in the layers where it matters |
| Every allowlist entry is real | A stale entry naming a type that no longer exists fails |

## Baselines

- **Empty by default.** A new rule lands with the code already fixed.
- When that is not feasible in one change: a baseline file listing the current offenders, **one line of reason per entry**, a test that the baseline only shrinks (an entry that no longer offends must be deleted), and an issue to empty it.
- No exceptions by precedent: an existing offender is never a reason to add another.

## Tools by stack (examples)

| Stack | Tool |
|---|---|
| .NET | ArchUnitNET or NetArchTest over the built assemblies |
| JVM (Java, Kotlin) | ArchUnit; Konsist for Kotlin |
| Python | import-linter (contracts: layers, forbidden, independence); a pytest that walks `ast` imports |
| Node / TypeScript | dependency-cruiser (`forbidden` + `allowed` rules), eslint `no-restricted-imports`, `boundaries` plugin |
| Dart / Flutter | a plain test that reads `lib/` and checks `import` lines against an allowlist |
| Swift | a script over `import` lines per target; SwiftLint custom rules |
| Go | `go list -deps` checks, depguard in golangci-lint |
| Any | language-aware dependency analysis where available; text import checks miss dynamic and qualified access |

The test lives in the normal test suite and runs in CI on every change. Lint and formatting run in CI too, so review time goes to what a machine cannot see.
