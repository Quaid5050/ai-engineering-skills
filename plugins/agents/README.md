# agents 1.0.0

Independent subagents: architect (design review of a plan before any code), reviewer (cold code review with a design pass), tester (fills test gaps, failure paths first).

## Install

```text
/plugin marketplace add Quaid5050/ai-engineering-skills
/plugin install agents@ai-engineering-skills
```

Installs with: `quality`.

## Agents

| Agent | Role |
|---|---|
| [`architect`](agents/architect.md) | Independent design review of a plan before code, posted on the issue |
| [`reviewer`](agents/reviewer.md) | Independent code review with the design pass, posted on the PR |
| [`tester`](agents/tester.md) | Fill test gaps in existing code, failure paths first |

See the [catalogue](../../README.md#catalogue) and the [workflow map](../../docs/engineering-workflow.md). License: MIT.
