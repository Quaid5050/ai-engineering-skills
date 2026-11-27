# Placement table template

Adapt this business-application profile to the selected architecture, then copy relevant rows into the project's conventions (for example `docs/conventions.md`, linked from `AGENTS.md`) and fill in the **real** paths. One row per technical kind of code. Every row names the check that enforces it; a row without a check is a review question and says so.

```markdown
## Where each kind of code lives

| Kind of code | Home (path) | Rule | Enforced by |
|---|---|---|---|
| Entry points (HTTP, jobs, consumers, screens) | `src/<area>/api/` | Thin: validate shape, authenticate, pass the caller id to one use case, map the result | `ArchitectureTests.edges_have_no_data_access` |
| Use cases | `src/<area>/application/` | One method per use case; authorises through the access-check unit; owns the transaction | review |
| Business rules | `src/<area>/domain/` | Concept test; allowlist of imports | `ArchitectureTests.domain_allowlist` |
| Input shape validation | `src/<area>/api/<area>_validation.*` | Only place a field-error map is built | `ArchitectureTests.validation_home` |
| Secrets and crypto | `src/security/<purpose>/` | One owner + one config section per purpose, validated at start | `ArchitectureTests.crypto_owners` (list of owners) |
| Object storage | `src/storage/` (one port, one adapter per provider) | No per-feature storage class | `ArchitectureTests.storage_sdk_home` |
| File formats / parsing | next to its port in `src/storage/` or `src/<area>/adapters/` | Core when parsing is the product responsibility; otherwise isolate protocol details | `ArchitectureTests.domain_no_raw_bytes` |
| Rate limiters | `src/rate_limiting/` | Fail-open or fail-closed stated | `ArchitectureTests.limiter_home` |
| Background loops | `src/background/` | One use-case call per pass | `ArchitectureTests.loops_call_one_use_case` |
| Scheduled jobs | `src/jobs/` + one scheduler config | Coordinated triggers; idempotent; claim with lease; durable outbox with explicit completion state; re-check access at run time | `ArchitectureTests.jobs_call_one_use_case` + race test |
| Outbound notifications | `src/notifications/` (port + one adapter per channel, templates) | Preferences honoured; stable operation key with recoverable outbox state; access re-checked at send | `ArchitectureTests.notification_sdk_home` |
| File uploads | `src/uploads/` (one reader) + `src/storage/` | Type from bytes, size cap, metadata stripped, parent complete only when all files confirmed | `ArchitectureTests.raw_body_only_in_upload_reader` |
| Shared code | `src/shared/` | Purpose: …; may contain: …; never imports a feature | `ArchitectureTests.shared_imports_no_feature` |
| Wire contract | `contracts/api.yaml` → generated `src/<client>/api/` | Generated types stay in the data layer | `ArchitectureTests.generated_types_home` |
| Configuration | `src/<area>/<area>_options.*` | Validated at start; no raw lookups | `ArchitectureTests.no_raw_config` |
| Time | injected clock | No direct clock reads | `ArchitectureTests.no_clock_reads` |
```

## Filling it in

1. List what the code base already contains: `ls` the source tree, search for crypto, storage SDKs, HTTP clients, timers, loops, `utils`/`helpers`/`common` folders.
2. For each kind found in more than one place, pick **one** home and plan the move as its own refactor change (behaviour unchanged).
3. Write the check before the move (it fails), move the code (it passes). A check that cannot pass yet keeps a shrinking-only baseline with a reason per entry and an issue to empty it.
4. Link the table from `AGENTS.md` so every agent reads it before writing code.
