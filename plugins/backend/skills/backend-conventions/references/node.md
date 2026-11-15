# Node.js / TypeScript (Express, Fastify, NestJS)

How the generic rows map onto a TypeScript backend. Use TypeScript with `strict: true`.

## Modules (feature folders)

```
src/
├── <area>/
│   ├── domain/          # entities, value objects, pure rules — imports only other domain files
│   ├── application/     # <area>.service.ts: one method per use case; ports as interfaces
│   ├── persistence/     # repository over the ORM / query builder, mappings, queries
│   ├── http/            # routes/controllers, request/response schemas (zod/TypeBox), validation, mappers
│   └── adapters/        # vendor implementations of ports
├── shared/              # with a stated purpose and an import rule
├── workers/             # BullMQ / pg-boss job handlers, thin
└── main.ts              # composition root
```

NestJS: modules per area map to the same folders; keep providers in `application/` free of `@nestjs/common` HTTP types (`HttpException`), and map results to exceptions/problems only in controllers or a filter.

## Idioms

- Handlers: parse with a schema (`zod`, TypeBox with Fastify's schema validation), call one service with `req.user.id`, map the `Result` to a problem response (`application/problem+json`). One error middleware / `setErrorHandler` for the 500 path.
- Results: a discriminated union `{ ok: true, value } | { ok: false, error }` with `kind` + `code`; exhaustive `switch` with a `never` check.
- ORM: Prisma, Drizzle, Kysely or TypeORM. Reads `select` only needed fields; `include` carefully (N+1 through loops of `findUnique`); bulk `updateMany`/`createMany`.
- Transactions: `prisma.$transaction(async (tx) => …)` / Kysely `transaction().execute`; advisory locks via raw SQL; notify after the transaction resolves.
- Time: inject a `Clock` (`{ now(): Date }`); tests use a fixed clock; avoid `Date.now()` in rules.
- Config: one typed config object validated with zod at start (`process.exit(1)` on failure); no `process.env` reads elsewhere.
- Async: every promise awaited or explicitly handled (`@typescript-eslint/no-floating-promises`); `AbortSignal` passed to fetch/DB calls where supported.
- Logging: pino with `redact` paths for tokens/emails/phones; structured fields, no template strings with personal data.
- Resilience: `undici`/`fetch` with `AbortSignal.timeout`; `cockatiel` or `opossum` for retry/breaker on idempotent reads; sends retried only by the job queue with an idempotency key.
- DI: constructor injection via a small container (tsyringe, awilix) or NestJS providers; request-scoped only for things holding a transaction.

## Tests and tools

- Vitest or Jest; HTTP tests with `supertest` or Fastify `inject`; real database via testcontainers or the compose file.
- Query count guard: Prisma `$on('query')` / a Kysely log hook counting statements per request.
- Architecture tests: dependency-cruiser `forbidden` + `allowed` rules (domain allowlist, `http` never imports `persistence`), eslint `no-restricted-imports`, `eslint-plugin-boundaries`.
- Migrations: Prisma Migrate (`prisma migrate dev --create-only`, read `migration.sql`), Drizzle Kit, Knex or node-pg-migrate; `CREATE INDEX CONCURRENTLY` needs a non-transactional migration.
- Commands: `npm run lint && npm run typecheck && npm test`.

## Quick greps

```bash
grep -rn 'prisma\.\|db\.' src/*/http
grep -rn 'Date.now()\|new Date()' src/*/domain src/*/application
grep -rn 'process.env' src | grep -v config
grep -rn 'catch *(\w*) *{ *}' src
```
