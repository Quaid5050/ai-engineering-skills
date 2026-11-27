# quality 1.0.0

Testing doctrine, TDD, writing tests, code review with a separate design pass, security and privacy review, accessibility audit, performance checks and privacy-safe product analytics. Framework-agnostic, with stack references.

## Install

```text
/plugin marketplace add Quaid5050/ai-engineering-skills
/plugin install quality@ai-engineering-skills
```

## Skills

| Skill | What it does |
|---|---|
| [`accessibility-audit`](skills/accessibility-audit/SKILL.md) | WCAG 2.2 AA for web and mobile: automated checks, screen readers, text scaling, contrast |
| [`analytics-event`](skills/analytics-event/SKILL.md) | Add a privacy-safe product event, or answer a product question from events |
| [`code-review`](skills/code-review/SKILL.md) | Review a diff or PR: dimensions + the separate design pass + risk tier, posted on the PR |
| [`perf-check`](skills/perf-check/SKILL.md) | Measure against a budget, profile, change one thing, guard it (backend, web, mobile references) |
| [`static-catalogs`](skills/static-catalogs/SKILL.md) | One row per case instead of a switch per attribute; when a data file plus codegen is justified; pin, migrate, guard (Swift, TypeScript references) |
| [`security-privacy-review`](skills/security-privacy-review/SKILL.md) | Data flow, authorisation and isolation, consent, abuse cases, the logging rule, OWASP API pass, retention |
| [`tdd`](skills/tdd/SKILL.md) | Red-green-refactor, one behaviour at a time |
| [`testing-doctrine`](skills/testing-doctrine/SKILL.md) | The rules every test follows: exact, hard-coded, fakes only at real boundaries, failure paths first, prove it can fail |
| [`write-tests`](skills/write-tests/SKILL.md) | Write tests for code or a diff at the right level (stack references: .NET, Python, Node, JVM, Flutter, Swift) |

See the [catalogue](../../README.md#catalogue) and the [workflow map](../../docs/engineering-workflow.md). License: MIT.
