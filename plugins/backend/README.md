# backend 1.0.0

Backend conventions (layers, ports and adapters, one home per technical kind of code, allowlist architecture tests), contract-first endpoints, safe schema migrations and read-only data checks. References for .NET, Django, Node and Spring.

## Install

```text
/plugin marketplace add Quaid5050/ai-engineering-skills
/plugin install backend@ai-engineering-skills
```

Installs with: `lifecycle`.

## Skills

| Skill | What it does |
|---|---|
| [`add-endpoint`](skills/add-endpoint/SKILL.md) | Contract-first endpoint with forbidden-caller tests and regenerated clients |
| [`add-file-upload`](skills/add-file-upload/SKILL.md) | File uploads and attachments: one upload reader + storage port, presigned or multipart, type from bytes, metadata stripped, parent complete only when all files are confirmed |
| [`add-migration`](skills/add-migration/SKILL.md) | Schema change: expand → migrate → contract, read the SQL for locks and rewrites |
| [`add-scheduled-job`](skills/add-scheduled-job/SKILL.md) | Scheduled jobs and outbound notifications: one scheduler, claimed rows, unique sent-ledger, access re-checked at run time, DST-safe schedules |
| [`backend-conventions`](skills/backend-conventions/SKILL.md) | Structure server code: layers, thin edges, validation, errors, transactions, resilience, data integrity, architecture tests (.NET, Django, Node, Spring references) |
| [`data-check`](skills/data-check/SKILL.md) | Read-only, privacy-safe database questions and migration verification |

See the [catalogue](../../README.md#catalogue) and the [workflow map](../../docs/engineering-workflow.md). License: MIT.
