# Agent brief — <project>

Hand this file (not the conventions skills) to subagents and reviewers. Keep it ≤ 100 lines; `capture-lesson` adds the rules reviews keep finding.

## Commands
| Area | Build | Test (single / area) | Lint |
|---|---|---|---|
| <backend> | `<cmd>` | `<cmd>` / `<cmd>` | `<cmd>` |

## Where code goes (placement map)
| Kind | Home |
|---|---|
| Business rule | `<path>` |
| Endpoint / handler | `<path>` (thin: validate, call one use case, map the result) |
| Persistence | `<path>` |
| UI screen / view model | `<path>` |

## Naming and style
- <3–8 rules that differ from the stack's defaults>

## High-risk areas (Structural / High-risk tier)
- <the project's safety-critical and privacy-sensitive paths>

## Rules reviews keep finding
- <rule> — why, link to the lesson
